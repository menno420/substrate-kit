"""Stop-hook session-close advisor (plan section 5.B, Lane B7).

Runs when a Claude Code session stops: the CLI's ``hook stopcheck`` entry
point prints the advisory lines ``evaluate_stop`` returns, reminding the agent
what the session ritual still owes —

- the session log is missing, or exists but lacks required markers
  (``latest_session_log`` + ``check_log`` with ``config.session_markers``);
- escalated blocking questions are still open (``state["open_questions"]``);
- the compaction cadence window has elapsed (``compaction_due``);
- the reflection buffer has not been mined today
  (``reflection_buffer.last_mined`` vs today's ISO date);
- no configured control heartbeat (``config.heartbeat_files``, default
  ``control/status.md``) was overwritten this session (KL-8: the
  coordination protocol's deliberate LAST step) — every existing heartbeat
  file's mtime predates the KL-5 session-start anchor's epoch. Skipped,
  fail-open, when the protocol or the anchor is absent; in a multi-lane
  repo (ORDER 004) ANY lane's fresh heartbeat clears the advisory (a
  session cannot know which lane it belongs to, so it never nags a lane
  that isn't its own);
- the current branch's head is already merged to ``origin/main``
  (``_stop_push_guard``, ORDER 022) — the session's final push would only
  re-create the branch GitHub just deleted, so the advisory says SKIP it,
  loudly and honestly. Fail-open by design: unprovable ancestry (shallow
  clone / failed fetch) lets the push proceed with a NOTE — a wrongly
  skipped push loses work, a wrongly executed one only re-creates a branch.

Returns ``[]`` when all clean. Advisory only, and it **fails open**: every
check runs inside its own guard, so a bad state document or an unreadable log
drops that one advisory rather than crashing the stop hook.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Any

from engine.checks.check_session_log import check_log, latest_session_log
from engine.checks.check_status_current import heartbeat_relpaths
from engine.lib.config import Config
from engine.lib.git_truth import NO, YES, GitCommand, make_runner, provable_ancestry
from engine.loop.handoff import SESSION_ANCHOR_KEY
from engine.loop.maintenance import compaction_due

_STOP_UNMINED_MSG = "reflections unmined this session — run bootstrap reflect --mine"


def _stop_safe(check: Any) -> list[str]:
    """Run one advisory check, returning [] on any failure (fail open).

    Each check is guarded on its own so one bad input never suppresses the
    other advisories — the stop hook is advisory by contract.
    """
    try:
        return list(check())
    except Exception:  # fail open — one bad check drops only itself
        return []


def _stop_state(backend: Any) -> dict[str, Any]:
    """Return the state document ({} when the backend is unusable — fail open)."""
    try:
        return dict(backend.data)
    except Exception:  # fail open — a broken backend yields no state advisories
        return {}


def _stop_log(root: Path, config: Config) -> list[str]:
    """Advise when the session log is missing or lacks required markers."""
    log = latest_session_log(root / config.sessions_dir)
    if log is None:
        return [
            f"no session log found under {config.sessions_dir}/ — "
            "write one before ending the session",
        ]
    missing = check_log(log, config.session_markers)
    if missing:
        return [f"session log {log.name} is missing: {', '.join(missing)}"]
    return []


def _stop_questions(state: dict[str, Any]) -> list[str]:
    """Advise when escalated blocking questions are still open."""
    open_questions = [str(q) for q in state.get("open_questions", [])]
    if not open_questions:
        return []
    listed = ", ".join(open_questions)
    return [f"{len(open_questions)} blocking question(s) open: {listed}"]


def _stop_compaction(state: dict[str, Any], config: Config) -> list[str]:
    """Advise when the compaction cadence window has elapsed."""
    if compaction_due(state, dict(config.cadence or {})):
        return ["compaction due — write the State Delta snapshot (bootstrap maintain)"]
    return []


def _stop_reflections(state: dict[str, Any]) -> list[str]:
    """Advise when the reflection buffer has not been mined today."""
    buffer = state.get("reflection_buffer")
    last_mined = buffer.get("last_mined") if isinstance(buffer, dict) else None
    if last_mined == date.today().isoformat():
        return []
    return [_STOP_UNMINED_MSG]


def _stop_status(root: Path, state: dict[str, Any], config: Config) -> list[str]:
    """Advise when no control heartbeat was overwritten this session.

    The coordination protocol's LAST step (KL-8) is overwriting the status
    heartbeat; a session that ends without it leaves the manager reading a
    stale (eventually dark) Project. Evidence = file mtime vs the KL-5
    session-start anchor's epoch — no anchor (or no protocol) means no basis
    for the claim, so the advisory is skipped rather than guessed. The
    checked set is ``config.heartbeat_files`` (ORDER 004 — one file per lane
    in a shared multi-Project repo); a fresh mtime on ANY existing lane file
    clears the advisory, because the hook cannot know which lane this
    session belongs to and must not nag another lane's duty.
    """
    statuses = [
        root / rel
        for rel in heartbeat_relpaths(config.heartbeat_files)
        if (root / rel).is_file()
    ]
    if not statuses:
        return []
    anchor = state.get(SESSION_ANCHOR_KEY)
    epoch = anchor.get("epoch") if isinstance(anchor, dict) else None
    if not isinstance(epoch, (int, float)) or isinstance(epoch, bool):
        return []
    if any(status.stat().st_mtime >= float(epoch) for status in statuses):
        return []
    named = ", ".join(
        status.relative_to(root).as_posix() for status in statuses
    )
    return [
        f"{named} not overwritten this session — the protocol's "
        "deliberate LAST step (see control/README.md)",
    ]


# Branches whose final push is normal flow, never the deleted-branch
# re-creation class the ORDER 022 guard exists for: the default branch
# (pushing main is ordinary work) and a detached HEAD (no branch ref for a
# bare `git push` to re-create).
_PUSH_GUARD_EXEMPT_BRANCHES = frozenset({"", "HEAD", "main", "master"})


def _stop_push_guard(root: Path, run: GitCommand | None = None) -> list[str]:
    """Advise SKIPPING the final push when the branch head is already merged.

    ORDER 022 (curious-research PROPOSAL 003 + same-day ADDENDUM): when a
    session's PR merges, GitHub deletes the head branch — but the finished
    session's clone still has it checked out, and one last nudged ``git
    push`` silently re-creates the ref at the same commit (fleet census
    2026-07-14: 460/491 surviving ``claude/*`` branches sit at exactly their
    merged PR's head SHA). The ADDENDUM's revised best-fit makes the primary
    cause GitHub-side (auto-delete not firing for bot-merged PRs); this
    guard is retained as defensive hygiene closing the proven secondary
    re-creation path.

    Decision, after ``git fetch origin main`` (ancestry via the shared
    ``provable_ancestry`` primitive — shallow-clone semantics included):

    - head provably merged (ancestor of ``origin/main``) → one loud, honest
      SKIP advisory (defensive hygiene, NOT an error);
    - provably unmerged on a fresh fetch → silent, push proceeds unchanged;
    - unprovable (shallow clone / failed fetch / git error) → push proceeds
      with a NOTE — fail-open, because a wrongly-skipped push loses work
      while a wrongly-executed one only re-creates a branch.

    Not a git repo / no git / detached HEAD / on the default branch →
    silent (nothing this guard protects).
    """
    if run is None:
        run = make_runner(root)
    rc, out, _err = run(["rev-parse", "--abbrev-ref", "HEAD"])
    if rc != 0:
        return []  # not a git repo, or no git — nothing to guard (fail open)
    branch = out.strip()
    if branch in _PUSH_GUARD_EXEMPT_BRANCHES:
        return []
    fetch_rc, _out, fetch_err = run(["fetch", "origin", "main", "--quiet"])
    answer = provable_ancestry(run, "HEAD", "origin/main")
    if answer.verdict == YES:
        # A positive ancestry answer is a proof even against a stale
        # origin/main (a stale ref only ever lags — containment can only
        # grow), so the fetch outcome does not gate the SKIP.
        return [
            f"branch '{branch}' head already merged to origin/main "
            "(PR merged); SKIP the final push — do not re-create the "
            "branch GitHub just deleted (defensive hygiene, not an error; "
            "divert genuinely new work to a rescue ref instead)",
        ]
    if answer.verdict == NO and fetch_rc == 0:
        return []  # provably unmerged against a fresh origin/main — normal flow
    if fetch_rc != 0:
        reason = "fetch of origin/main failed: " + (
            fetch_err.strip().splitlines()[0] if fetch_err.strip() else f"rc {fetch_rc}"
        )
    else:
        reason = answer.detail or f"git merge-base rc {answer.returncode}"
    return [
        f"NOTE: merged-head push guard could not prove ancestry ({reason}) "
        "— final push proceeds (fail-open: a wrongly-skipped push loses "
        "work; a wrong push only re-creates a branch)",
    ]


def evaluate_stop(root: Path, config: Config, backend: Any) -> list[str]:
    """Return the session-close advisory lines ([] when all clean).

    Six checks in fixed order: session log, open blocking questions,
    compaction cadence, reflection mining, the control-status heartbeat
    (KL-8), the merged-head final-push guard (ORDER 022). Each runs inside
    its own guard so
    one failing check never suppresses the others — the stop hook is advisory
    and fails open by contract.
    """
    state = _stop_state(backend)
    checks = (
        lambda: _stop_log(root, config),
        lambda: _stop_questions(state),
        lambda: _stop_compaction(state, config),
        lambda: _stop_reflections(state),
        lambda: _stop_status(root, state, config),
        lambda: _stop_push_guard(root),
    )
    advisories: list[str] = []
    for check in checks:
        advisories.extend(_stop_safe(check))
    return advisories
