"""check_staged_regen — staged-artifact regeneration-lag advisory.

Why + provenance: staged ``.substrate/`` artifacts (the staged CLAUDE.md,
skills, agents) can carry unfilled ``${...}`` slots even though ``state.json``
``slot_values`` are ALL filled — they were staged pre-slot-fill and nothing
re-renders them outside an ``upgrade``. The engagement gate never sees it:
``_unrendered_findings`` scans **planted docs** (``scan_relpaths``), not the
staged tree. A "looks staged, isn't rendered" class — proven live on websites
at main ``992c045`` (``.substrate/agents/architect.md``, ``reviewer.md``,
``claude/CLAUDE.md``, two skills templated while every slot was answered),
and re-proven on the kit's own staged tree at build time. Design authority:
``docs/ideas/staged-artifact-regen-lag-checker-2026-07-12.md`` (origin:
consumer friction issue #39). Added 2026-07-13 (ORDER 019 item 6).
Reliability (PL-008): UNVERIFIED — confirm its findings against ground truth
a few times across sessions before trusting it; **delete this if it proves
unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** (idea file: "advisory-first
per the adopt-freely posture") — the same nudge-never-door contract as
``check_claims`` / ``check_skill_grounds``: a lagging staged artifact costs
the host one regen command, and a required-check red here would bomb every
currently-green adopter whose staged tree predates its answers the moment it
upgrades. Graduation to strict is a later, deliberate step.

What fires: for each staged artifact under the staged subtrees of
``<state_dir>/`` (:data:`STAGED_SUBDIRS` — exactly the directories
``adopt``'s staging pass writes; never ``backup/`` or the state files at the
state-dir root), a live ``${slot}`` placeholder **outside code spans**
(:func:`engine.render.find_placeholders_outside_code` — the code-span-aware
scan the engagement gate already uses, so backticked mentions never
false-positive) whose slot name **is filled** in ``state.json``
``slot_values`` yields one finding. The filled-slot intersection is the
regen-lag definition — the answer exists, the staged copy predates it — and
is also the false-positive firewall: shell ``${VAR}`` in staged hook/CI
material and GitHub's ``${{ ... }}`` syntax are not filled slot names and
can never fire. A genuinely-unfilled slot is not lag (there is nothing to
render yet) and stays the interview's business.

The message names the recovering commands: ``upgrade`` regenerates the whole
staged tree; ``skills --build`` / ``agents --build`` regenerate one pack.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from engine.checks.check_docs import Finding
from engine.render import find_placeholders_outside_code

# The staged subtrees adopt's staging pass writes under <state_dir>/ — the
# scan surface. Deliberately NOT a recursive walk of the whole state dir:
# files at the state-dir root (state.json, guard-fires.jsonl, upgrade
# reports, reflection/episodic indexes) are kit state, not staged artifacts
# — free-text state (a reflection *about* a slot) must never fire — and
# backup/ holds banked previous dists that are legitimately old.
STAGED_SUBDIRS = ("agents", "claude", "ci", "hooks", "skills")


def _filled_slots(target: Path, config: Any) -> set[str]:
    """Return the slot names with a non-empty recorded value in state.json."""
    path = target / config.state_dir / "state.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return set()
    values = data.get("slot_values") if isinstance(data, dict) else None
    if not isinstance(values, dict):
        return set()
    return {
        slot
        for slot, entry in values.items()
        if isinstance(entry, dict) and str(entry.get("value", "")).strip()
    }


def check_staged_regen(target: Path, config: Any) -> list[Finding]:
    """Return regen-lag findings for ``target``'s staged tree (empty = current).

    Self-gating like every input-gated checker: no filled slots (bare tree,
    pre-interview install) or no staged tree means nothing can lag — the
    scan adds nothing before onboarding.
    """
    filled = _filled_slots(target, config)
    if not filled:
        return []
    state_base = target / config.state_dir
    findings: list[Finding] = []
    for subdir in STAGED_SUBDIRS:
        base = state_base / subdir
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*")):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except (OSError, UnicodeDecodeError):
                continue
            lagging = sorted(
                find_placeholders_outside_code(text) & filled,
            )
            if not lagging:
                continue
            rel = f"{config.state_dir}/{path.relative_to(state_base).as_posix()}"
            listed = ", ".join(lagging[:5]) + (" …" if len(lagging) > 5 else "")
            findings.append(
                Finding(
                    rel,
                    "staged-regen-lag",
                    f"{len(lagging)} filled slot(s) still unrendered in this "
                    f"staged artifact: {listed} — the answers already exist "
                    "in state; regenerate the staged tree "
                    "(`python3 bootstrap.py upgrade`, or the pack verb: "
                    "`bootstrap.py skills --build` / `agents --build`).",
                ),
            )
    return findings
