"""SessionStart orientation composer (plan section 5.B, Lane B7).

The nervous system's *injection* point: when Claude Code starts a session, the
``bootstrap hook sessionstart`` entry point prints the text this module
composes, so the agent boots already knowing the project's mode, stance,
learned lessons, fired triggers, and pending questions. The composition is
**mode-aware** — ``orientation_depth`` (observe → minimal, guided → standard,
active → full) decides which sections render and how hard they cap.

Section order (the plan's fixed sequence, plus the handoff push at slot 2 and
the git-freshness check at slot 3): status header → **handoff push** (newest
session card + unresolved slots + the previous session's resolved handoff
pointer — the B1 run-4/run-5 continuity-null fix: cold sessions never PULL
the card, so the kit pushes it) → **git-freshness check** (fetches the
tracked remote and reports ahead/behind — a laptop-side investigation on
2026-09-01 read a resident clone that was hours stale against origin and
produced findings that missed nine already-merged PRs; nothing downstream of
this section can be trusted more than the clone it read from) → stance
briefing → user-style block → learned lessons (AFTER user-style) → trigger
block → guided-practices line → economy-gauges advisory (over-cap only) →
pending questions (quota view) → observe-mode workflow proposal.

Every section is defensive: a failure inside one section drops that section,
never the whole composition — orientation must never crash a session. This is
the one place broad ``except Exception`` is correct by design (fail open, like
the stance guard). The git-freshness section additionally bounds every
subprocess call with a short timeout, so an unreachable remote degrades to a
silently-dropped section rather than a slow session start.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any

from engine.economy.engine import economy_gauges
from engine.interview.interview import pending_questions, session_questions
from engine.lib.config import Config
from engine.lib.modes import (
    active_practices,
    orientation_depth,
    triggers_mandate,
    workflow_proposal_due,
)
from engine.loop.handoff_pointer import handoff_lines
from engine.loop.reflections import (
    REFLECTIONS_FILENAME,
    active_lessons,
    lessons_block,
    load_reflections,
)
from engine.loop.triggers import check_triggers, mandatory_questions, trigger_block
from engine.stances.stances import stance_briefing

# Depth "standard" caps the learned-lessons section at this many entries.
_ORI_STANDARD_LESSON_CAP = 3
# Depth "minimal" (observe) renders only these section numbers: the status
# header (1), the handoff push (2 — a pointer informs, it imposes nothing;
# continuity is the kit's core promise at every depth), the git-freshness
# check (3 — whether the clone is even current is not optional information
# at any depth), the trigger block as an advisory (7), and the workflow
# proposal (11) — observe imposes nothing else.
_ORI_MINIMAL_SECTIONS = frozenset({1, 2, 3, 7, 11})

# Bounds every git subprocess call in the freshness section — an unreachable
# or slow remote must degrade to a silently-dropped section, never a slow
# session start (fetch gets longer, everything else is a local git-metadata
# read and stays fast).
_GIT_FETCH_TIMEOUT_S = 8
_GIT_LOCAL_TIMEOUT_S = 3


def _ori_status_header(state: dict[str, Any], config: Config) -> str:
    """Render section 1 — the compact status header line block."""
    project = str(state.get("project_id") or config.project_id)
    return (
        f"# Session orientation — {project}\n"
        f"mode: {state.get('mode', '?')} · stage: {state.get('stage', '?')} · "
        f"stance: {state.get('stance', '?')} · "
        f"session: {int(state.get('session_count', 0))}"
    )


def _ori_handoff(root: Path, config: Config) -> str:
    """Render section 2 — the handoff push ('' when no session card exists).

    The B1 run-4/run-5 continuity-null fix: both hook-live bench runs showed
    cold sessions re-deriving history via ``git show`` while the newest
    session card sat unopened — the continuity surface was PULL-only. This
    section PUSHES it: the newest card's path, its completion state, its
    unresolved auto-draft slot count, and the previous session's resolved
    "Next session should know" pointer, capped terse (the M1 budget).

    The bullet lines are the shared ``engine.loop.handoff_pointer`` composer
    — the same content the repo-root ``HANDOFF.md`` pointer file carries (the
    B1 run-6 delivery-gap fix: this push stops at the orchestrator, so the
    file delivers the identical trail through the working-tree surfaces
    delegated workers actually touch). One composer, two surfaces — the
    pushed and pulled text can never drift apart.
    """
    lines = handoff_lines(root, config)
    if not lines:
        return ""
    return "\n".join(
        [
            "## Handoff — the previous session's trail (pushed; read before re-deriving)",
            "",
            *lines,
        ],
    )


def _ori_git_freshness(root: Path) -> str:
    """Render section 3 — clone-vs-remote drift ('' when current or inapplicable).

    Fetches the tracked remote for the current branch and compares HEAD
    against it. Returns '' — never raises, never blocks — when: there is no
    ``.git`` directory (not a repo), no remote is configured, the fetch fails
    (offline, no auth, host unreachable), HEAD is detached, or the branch has
    no upstream counterpart. All of those are legitimate states, not errors;
    a bad state document elsewhere gets the same silent-drop treatment via
    ``_ori_safe``, and this section earns no different behavior for a bad
    network instead of a bad file.

    Only fetches — never pulls, merges, or rebases. A stale-but-clean clone
    should be reported, not silently rewritten out from under uncommitted
    work the agent has not seen yet.
    """
    if not (root / ".git").exists():
        return ""
    try:
        remotes = subprocess.run(
            ["git", "remote"],
            cwd=root, capture_output=True, text=True,
            timeout=_GIT_LOCAL_TIMEOUT_S, check=False,
        )
        if remotes.returncode != 0 or not remotes.stdout.strip():
            return ""
        remote = remotes.stdout.splitlines()[0].strip()

        branch = subprocess.run(
            ["git", "symbolic-ref", "--short", "HEAD"],
            cwd=root, capture_output=True, text=True,
            timeout=_GIT_LOCAL_TIMEOUT_S, check=False,
        )
        if branch.returncode != 0 or not branch.stdout.strip():
            return ""  # detached HEAD — skip rather than guess a branch
        branch_name = branch.stdout.strip()

        fetch = subprocess.run(
            ["git", "fetch", "--quiet", remote, branch_name],
            cwd=root, capture_output=True, text=True,
            timeout=_GIT_FETCH_TIMEOUT_S, check=False,
        )
        if fetch.returncode != 0:
            return ""  # offline / unreachable / no auth — fail open

        upstream = f"{remote}/{branch_name}"
        counts = subprocess.run(
            ["git", "rev-list", "--left-right", "--count", f"HEAD...{upstream}"],
            cwd=root, capture_output=True, text=True,
            timeout=_GIT_LOCAL_TIMEOUT_S, check=False,
        )
        if counts.returncode != 0:
            return ""  # no such upstream ref — nothing to compare against
        parts = counts.stdout.split()
        if len(parts) != 2:
            return ""
        ahead, behind = int(parts[0]), int(parts[1])
        if ahead == 0 and behind == 0:
            return ""

        pieces = []
        if behind:
            plural = "s" if behind != 1 else ""
            pieces.append(f"**{behind} commit{plural} behind** `{upstream}`")
        if ahead:
            plural = "s" if ahead != 1 else ""
            pieces.append(f"**{ahead} commit{plural} ahead**, not yet pushed")
        return (
            "## Clone freshness — " + " · ".join(pieces) + "\n\n"
            "This was just fetched; it was not current before this line ran. "
            "Anything read from this working tree before now may be stale — "
            "`git pull` (or re-clone, if local changes make a pull awkward) "
            "before treating file contents as the repo's current state."
        )
    except (OSError, subprocess.SubprocessError, ValueError):
        return ""  # fail open — a freshness check must never block a session


def _ori_stance(state: dict[str, Any]) -> str:
    """Render section 4 — the active stance briefing ('' when no stance set)."""
    stance = state.get("stance")
    if not stance:
        return ""
    return stance_briefing(str(stance))


def _ori_user_style(state: dict[str, Any]) -> str:
    """Render section 5 — the owner_profile user-style block ('' when unfilled)."""
    entry = state.get("slot_values", {}).get("owner_profile")
    value = entry.get("value") if isinstance(entry, dict) else entry
    text = str(value).strip() if value else ""
    if not text:
        return ""
    return f"## How the owner works:\n\n> {text}"


def _ori_lessons(root: Path, config: Config, depth: str) -> str:
    """Render section 6 — learned lessons (standard caps at 3, full uncapped)."""
    entries = load_reflections(root / config.state_dir / REFLECTIONS_FILENAME)
    cap = _ORI_STANDARD_LESSON_CAP if depth == "standard" else len(entries)
    return lessons_block(active_lessons(entries, cap))


def _ori_triggers(root: Path, config: Config, state: dict[str, Any]) -> str:
    """Render section 7 — the trigger block (mandate flag per the mode policy)."""
    triggers = check_triggers(root, config, state)
    questions = mandatory_questions(triggers)
    return trigger_block(triggers, questions, mandate=triggers_mandate(state))


def _ori_practices(state: dict[str, Any], config: Config) -> str:
    """Render section 8 — the one-line guided-practices block ('' when empty)."""
    practices = active_practices(state, dict(config.cadence or {}))
    if not practices:
        return ""
    return "Active practices: " + ", ".join(practices)


def _ori_gauges(root: Path, config: Config) -> str:
    """Render section 9 — economy advisory listing ONLY over-cap gauges."""
    over = [g for g in economy_gauges(root, config) if g.get("over")]
    if not over:
        return ""
    lines = ["## Economy advisory — over-cap gauges", ""]
    lines += [
        f"- {g['name']} ({g['kind']}): {g['value']} words/items over cap {g['cap']}"
        for g in over
    ]
    return "\n".join(lines)


def _ori_questions(state: dict[str, Any]) -> str:
    """Render section 10 — the quota-capped ask list with a '+N more' suffix."""
    asks = session_questions(state)
    if not asks:
        return ""
    lines = ["## Questions this session", ""]
    lines += [
        f"- {q['id']} ({q.get('priority', 'normal')}): {q['prompt']}" for q in asks
    ]
    extra = len(pending_questions(state)) - len(asks)
    if extra > 0:
        lines += ["", f"(+{extra} more later)"]
    return "\n".join(lines)


def _ori_proposal(state: dict[str, Any]) -> str:
    """Render section 11 — observe mode's workflow proposal when it is due."""
    if state.get("mode") != "observe" or not workflow_proposal_due(state):
        return ""
    return (
        "## Proposed workflow\n\n"
        "Observe mode has watched enough sessions to propose a tailored "
        "workflow. If the pacing looks right, switch mode to adopt it: "
        "`bootstrap mode guided` (one practice at a time) or "
        "`bootstrap mode active` (the full workflow now). Observe imposes "
        "nothing until you do."
    )


def _ori_safe(build: Any) -> str:
    """Run one section builder, returning '' on any failure (fail open).

    The one place broad ``except Exception`` is correct by design: a bad state
    document or an unreadable file drops that single section — orientation
    must never crash a session.
    """
    try:
        return str(build()).strip()
    except Exception:  # fail open — one bad section never breaks the whole
        return ""


def compose_orientation(root: Path, config: Config, backend: Any) -> str:
    """Compose the mode-aware SessionStart orientation injection.

    Assembles the eleven sections (the nine plan sections plus the handoff
    push and the git-freshness check) in fixed order, gated by
    ``orientation_depth``: ``minimal`` renders only the status header, the
    handoff push, the git-freshness check, the trigger advisory, and the
    observe-mode proposal; ``standard`` renders all sections but caps lessons
    at 3; ``full`` renders everything uncapped. Every section builder runs
    inside its own guard — a bad state document, an unreadable file, or an
    unreachable git remote drops that one section, never the whole
    composition (orientation must never crash a session).
    """
    try:
        state = dict(backend.data)
    except Exception:  # fail open — orientation never crashes a session
        state = {}
    try:
        depth = orientation_depth(state)
    except Exception:  # fail open — fall back to the default depth
        depth = "standard"
    builders = (
        (1, lambda: _ori_status_header(state, config)),
        (2, lambda: _ori_handoff(root, config)),
        (3, lambda: _ori_git_freshness(root)),
        (4, lambda: _ori_stance(state)),
        (5, lambda: _ori_user_style(state)),
        (6, lambda: _ori_lessons(root, config, depth)),
        (7, lambda: _ori_triggers(root, config, state)),
        (8, lambda: _ori_practices(state, config)),
        (9, lambda: _ori_gauges(root, config)),
        (10, lambda: _ori_questions(state)),
        (11, lambda: _ori_proposal(state)),
    )
    sections: list[str] = []
    for number, build in builders:
        if depth == "minimal" and number not in _ORI_MINIMAL_SECTIONS:
            continue
        text = _ori_safe(build)
        if text:
            sections.append(text)
    if not sections:
        return ""
    return "\n\n".join(sections) + "\n"
