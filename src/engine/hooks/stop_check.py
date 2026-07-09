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
  that isn't its own).

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


def evaluate_stop(root: Path, config: Config, backend: Any) -> list[str]:
    """Return the session-close advisory lines ([] when all clean).

    Five checks in fixed order: session log, open blocking questions,
    compaction cadence, reflection mining, the control-status heartbeat
    (KL-8). Each runs inside its own guard so
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
    )
    advisories: list[str] = []
    for check in checks:
        advisories.extend(_stop_safe(check))
    return advisories
