"""Status-freshness checker — the ``control/`` heartbeat(s) must exist and beat.

Why + provenance: the fleet coordination protocol (canonical spec: superbot
``docs/planning/fleet-coordination-protocol-2026-07-09.md``; kit band KL-8,
inbox ORDER 002) makes ``control/status.md`` each Project's heartbeat — the
manager treats a stale status as a **dark** Project. The protocol's whole
value collapses if a Project silently stops writing it, so the discipline is
enforced, not exhorted (PL-007), exactly like the session-card gate.

Multi-Project repos (inbox ORDER 004): a SHARED repo hosting several
Projects keeps one heartbeat file *per lane* (the superbot-games pattern —
``control/status-mining.md`` + ``control/status-exploration.md``), preserving
one-writer-per-file per lane. The validated path set is therefore
**configurable**: ``substrate.config.json`` → ``heartbeat_files`` (default
``["control/status.md"]``); every listed heartbeat is checked independently
and each finding names its own file. Callers pass the configured list via
``status_files``; unset/empty falls back to the single-file default (a
misconfiguration must not silently disable the gate).

Two postures, deliberately split (the spec's "warns → graduates to the
born-red post-adopt gate" wording, resolved so a *required CI check* never
reds on wall-clock time alone):

- **Gate findings** (ride the ordinary strict finding loop — RED under
  ``check --strict``): *static, deterministic* protocol states —
  ``status-missing`` (the control bus exists but a configured heartbeat file
  doesn't) and ``status-no-heartbeat`` (the file is still the adopt-time
  seed, or carries no parseable ``updated:`` ISO-8601 line). These are the
  born-red graduation: an adopted host stays red until its first real
  heartbeat, the same shape as ``session-loop-idle``.
- **Advisory findings** (warn-only — emitted + telemetry-recorded, **never**
  exit-affecting): ``status-stale`` — the heartbeat parses but is older than
  ``max_age_hours`` (default 72h). Time-based red in a required check would
  be a bomb: an untouched-for-a-week repo's next unrelated PR would arrive
  pre-reddened. The warning still surfaces in every ``check`` run and the
  Stop hook separately nags when no heartbeat file was overwritten this
  session (``hooks/stop_check.py``).

Input-gated like every checker: engages only when the protocol is present
(any ``control/{README,inbox}.md`` or configured heartbeat file exists) — a
host that never adopted the bus adds nothing here. Stdlib only; unreadable
files fail open.
"""

from __future__ import annotations

from collections.abc import Sequence
from datetime import datetime, timedelta, timezone
from pathlib import Path

from engine.checks.check_docs import Finding

# The `updated:` heartbeat-line grammar is kit-owned with ONE home —
# engine.grammar (EAP §6.8): the writer templates and this enforcer consume
# the same constant, so they cannot drift apart.
from engine.grammar import UPDATED_LINE_RE

CONTROL_DIR = "control"
STATUS_RELPATH = "control/status.md"
INBOX_RELPATH = "control/inbox.md"
CONTROL_README_RELPATH = "control/README.md"

# The manager's stale-= -dark horizon. Wider than the self-poll cadence the
# spec suggests (2-4h) on purpose: the checker warns about *abandonment*, not
# about a quiet afternoon — revise with data (KF-8 posture).
DEFAULT_MAX_AGE_HOURS = 72


def parse_heartbeat(text: str) -> datetime | None:
    """Return the ``updated:`` line's timestamp as an aware UTC datetime.

    Accepts the contract's ISO-8601 shapes (``2026-07-09T12:07Z``,
    ``...T12:07:00+00:00``, minutes or seconds precision) behind a
    case-insensitive ``updated:`` prefix (``Updated:`` is a writer spelling
    variant, not a dead heartbeat — kit #326). A trailing ``Z``
    is normalized for ``fromisoformat`` (Python 3.10 floor). A naive
    timestamp is taken as UTC — the contract says ISO8601, sessions write
    UTC, and treating it otherwise would fabricate staleness. None when the
    line is absent or unparseable (the adopt seed's prose sentinel lands
    here by design).
    """
    match = UPDATED_LINE_RE.search(text)
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


def heartbeat_relpaths(status_files: Sequence[str] | None) -> list[str]:
    """Normalize the configured heartbeat list (unset/empty → the default).

    The fallback-on-empty is deliberate: a stray ``"heartbeat_files": []``
    must degrade to the protocol's single-file default, never silently
    disable the gate (same fail-safe instinct as the fast lane's
    empty-diff-runs-the-full-suite rule).
    """
    files = [str(rel) for rel in (status_files or []) if str(rel).strip()]
    return files or [STATUS_RELPATH]


def _control_present(target: Path, status_relpaths: Sequence[str]) -> bool:
    """True when the control bus exists (any protocol/heartbeat file)."""
    candidates = [INBOX_RELPATH, CONTROL_README_RELPATH, *status_relpaths]
    return any((target / rel).is_file() for rel in candidates)


def _check_one_status(
    target: Path,
    rel: str,
    *,
    now: datetime,
    max_age_hours: int,
) -> tuple[list[Finding], list[Finding]]:
    """Return ``(gate, advisory)`` findings for one heartbeat file ``rel``."""
    status_path = target / rel
    if not status_path.is_file():
        return (
            [
                Finding(
                    rel,
                    "status-missing",
                    f"the control/ bus exists but {rel} doesn't — the "
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
                    rel,
                    "status-no-heartbeat",
                    "no parseable `updated:` ISO-8601 heartbeat — still the "
                    "adopt seed? Overwrite the whole file with your real "
                    "status as the session's LAST step (control/README.md); "
                    "mechanical writer: `python3 bootstrap.py heartbeat "
                    '--full --phase "…"`.',
                ),
            ],
            [],
        )
    age = now - heartbeat
    if age > timedelta(hours=max_age_hours):
        hours = int(age.total_seconds() // 3600)
        return (
            [],
            [
                Finding(
                    rel,
                    "status-stale",
                    f"heartbeat is ~{hours}h old (> {max_age_hours}h) — the "
                    "manager treats a stale status as a DARK Project; "
                    f"overwrite {rel} this session (mechanical restamp: "
                    "`python3 bootstrap.py heartbeat`).",
                ),
            ],
        )
    return [], []


def check_status_current(
    target: Path,
    *,
    now: datetime | None = None,
    max_age_hours: int = DEFAULT_MAX_AGE_HOURS,
    status_files: Sequence[str] | None = None,
) -> tuple[list[Finding], list[Finding]]:
    """Return ``(gate_findings, advisory_findings)`` for ``target``'s heartbeat(s).

    Gate findings ride the strict finding loop (exit-affecting under
    ``--strict``); advisory findings are surfaced + telemetry-recorded but
    must never touch the exit code (see module docstring). Both lists are
    empty when the ``control/`` protocol is absent. ``status_files`` is the
    host's configured heartbeat list (``Config.heartbeat_files``); each
    listed file is validated independently so a multi-Project repo gates
    every lane's heartbeat — unset/empty falls back to
    ``["control/status.md"]``.
    """
    relpaths = heartbeat_relpaths(status_files)
    if not _control_present(target, relpaths):
        return [], []
    current = now or datetime.now(timezone.utc)
    gate: list[Finding] = []
    advisory: list[Finding] = []
    for rel in relpaths:
        one_gate, one_advisory = _check_one_status(
            target,
            rel,
            now=current,
            max_age_hours=max_age_hours,
        )
        gate += one_gate
        advisory += one_advisory
    return gate, advisory
