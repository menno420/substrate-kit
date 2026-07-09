"""Status-freshness checker — the ``control/`` heartbeat must exist and beat.

Why + provenance: the fleet coordination protocol (canonical spec: superbot
``docs/planning/fleet-coordination-protocol-2026-07-09.md``; kit band KL-8,
inbox ORDER 002) makes ``control/status.md`` each Project's heartbeat — the
manager treats a stale status as a **dark** Project. The protocol's whole
value collapses if a Project silently stops writing it, so the discipline is
enforced, not exhorted (PL-007), exactly like the session-card gate.

Two postures, deliberately split (the spec's "warns → graduates to the
born-red post-adopt gate" wording, resolved so a *required CI check* never
reds on wall-clock time alone):

- **Gate findings** (ride the ordinary strict finding loop — RED under
  ``check --strict``): *static, deterministic* protocol states —
  ``status-missing`` (the control bus exists but ``status.md`` doesn't) and
  ``status-no-heartbeat`` (``status.md`` is still the adopt-time seed, or
  carries no parseable ``updated:`` ISO-8601 line). These are the born-red
  graduation: an adopted host stays red until its first real heartbeat, the
  same shape as ``session-loop-idle``.
- **Advisory findings** (warn-only — emitted + telemetry-recorded, **never**
  exit-affecting): ``status-stale`` — the heartbeat parses but is older than
  ``max_age_hours`` (default 72h). Time-based red in a required check would
  be a bomb: an untouched-for-a-week repo's next unrelated PR would arrive
  pre-reddened. The warning still surfaces in every ``check`` run and the
  Stop hook separately nags when ``status.md`` wasn't overwritten this
  session (``hooks/stop_check.py``).

Input-gated like every checker: engages only when the protocol is present
(any ``control/{README,inbox,status}.md`` exists) — a host that never adopted
the bus adds nothing here. Stdlib only; unreadable files fail open.
"""

from __future__ import annotations

import re
from datetime import datetime, timedelta, timezone
from pathlib import Path

from engine.checks.check_docs import Finding

CONTROL_DIR = "control"
STATUS_RELPATH = "control/status.md"
INBOX_RELPATH = "control/inbox.md"
CONTROL_README_RELPATH = "control/README.md"

# The manager's stale-= -dark horizon. Wider than the self-poll cadence the
# spec suggests (2-4h) on purpose: the checker warns about *abandonment*, not
# about a quiet afternoon — revise with data (KF-8 posture).
DEFAULT_MAX_AGE_HOURS = 72

_UPDATED_RE = re.compile(r"^updated:\s*(\S+)", re.MULTILINE)


def parse_heartbeat(text: str) -> datetime | None:
    """Return the ``updated:`` line's timestamp as an aware UTC datetime.

    Accepts the contract's ISO-8601 shapes (``2026-07-09T12:07Z``,
    ``...T12:07:00+00:00``, minutes or seconds precision). A trailing ``Z``
    is normalized for ``fromisoformat`` (Python 3.10 floor). A naive
    timestamp is taken as UTC — the contract says ISO8601, sessions write
    UTC, and treating it otherwise would fabricate staleness. None when the
    line is absent or unparseable (the adopt seed's prose sentinel lands
    here by design).
    """
    match = _UPDATED_RE.search(text)
    if not match:
        return None
    raw = match.group(1)
    if raw.endswith(("Z", "z")):
        raw = raw[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(raw)
    except ValueError:
        return None
    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _control_present(target: Path) -> bool:
    """True when the control bus exists (any of the three protocol files)."""
    return any(
        (target / rel).is_file()
        for rel in (STATUS_RELPATH, INBOX_RELPATH, CONTROL_README_RELPATH)
    )


def check_status_current(
    target: Path,
    *,
    now: datetime | None = None,
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
) -> tuple[list[Finding], list[Finding]]:
    """Return ``(gate_findings, advisory_findings)`` for ``target``'s heartbeat.

    Gate findings ride the strict finding loop (exit-affecting under
    ``--strict``); advisory findings are surfaced + telemetry-recorded but
    must never touch the exit code (see module docstring). Both lists are
    empty when the ``control/`` protocol is absent.
    """
    if not _control_present(target):
        return [], []
    status_path = target / STATUS_RELPATH
    if not status_path.is_file():
        return (
            [
                Finding(
                    STATUS_RELPATH,
                    "status-missing",
                    "the control/ bus exists but status.md doesn't — the "
                    "manager reads this file as your heartbeat; write it "
                    "(format: control/README.md).",
                ),
            ],
            [],
        )
    try:
        text = status_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [], []  # fail open — an unreadable file is not a verdict
    heartbeat = parse_heartbeat(text)
    if heartbeat is None:
        return (
            [
                Finding(
                    STATUS_RELPATH,
                    "status-no-heartbeat",
                    "no parseable `updated:` ISO-8601 heartbeat — still the "
                    "adopt seed? Overwrite the whole file with your real "
                    "status as the session's LAST step (control/README.md).",
                ),
            ],
            [],
        )
    current = now or datetime.now(timezone.utc)
    age = current - heartbeat
    if age > timedelta(hours=max_age_hours):
        hours = int(age.total_seconds() // 3600)
        return (
            [],
            [
                Finding(
                    STATUS_RELPATH,
                    "status-stale",
                    f"heartbeat is ~{hours}h old (> {max_age_hours}h) — the "
                    "manager treats a stale status as a DARK Project; "
                    "overwrite control/status.md this session.",
                ),
            ],
        )
    return [], []
