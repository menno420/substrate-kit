"""Telemetry substrate — guard-fire records + the model-usage harvest (KL-3).

Two feeds, both mechanized (the Phase-2.5 lesson: mechanize, don't exhort)
and both **fail-open by contract** — telemetry must never crash a check, a
hook, or session-close (founding plan §5.3/§5.2):

- **Guard fires** (B3): one JSONL record per finding a guard surfaces,
  appended to ``<state_dir>/guard-fires.jsonl`` by the two local choke points
  (``cmd_check``'s finding loop, ``cmd_hook``'s dispatch). The ``ci`` surface
  is **derived, not written** — a JSONL appended inside an Actions runner
  dies with the job, so the lab sweep reads the GitHub Checks API instead,
  and ``did_not_run`` rows are computed the same way (never written here).
- **Model usage** (B2 / PL-004): sessions self-report one machine-parsed
  run-report line — ``- **📊 Model:** <model> · <effort> · <task-class>`` —
  and ``session-close`` harvests it into ``telemetry/model-usage.jsonl``.
  ``tokens_out`` is null-tolerated (KF-9: no meter exists; an optional 4th
  ``·`` segment fills it when one does). ``outcome`` ships as the PL-004
  object with null fields — the lab loop's sweep backfills them (CI result,
  merged PR, the 14-day revert window).

Appends use a single ``write`` in append mode (atomic enough for one-line
records on POSIX); full-file rewrites are never performed on either feed —
JSONL because atomic appends beat rewriting a JSON array (plan D-10).
"""

from __future__ import annotations

import json
import re
from datetime import date, datetime, timezone
from pathlib import Path

from engine.checks.check_session_log import DRAFT_FILL_TOKEN

GUARD_FIRES_FILENAME = "guard-fires.jsonl"
MODEL_USAGE_RELPATH = "telemetry/model-usage.jsonl"

# The run-report needle. \N escape keeps the engine source ASCII-safe.
MODEL_LINE_NEEDLE = "\N{BAR CHART} Model:"  # 📊 Model:

# The 9 PL-004 task classes, verbatim (docs/program/rulings.md): the 8
# founding Q-0248 classes + `feature build` (the PL-010 amendment).
TASK_CLASSES = (
    "docs-only",
    "mechanical refactor",
    "test writing",
    "runtime bugfix",
    "kernel/architecture design",
    "review/verify",
    "research",
    "idea/planning",
    "feature build",
)

_DATE_PREFIX_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})")


def guard_fires_path(root: Path, state_dir: str) -> Path:
    """Return the guard-fire JSONL path for one install."""
    return root / state_dir / GUARD_FIRES_FILENAME


def _append_jsonl(path: Path, record: dict) -> None:
    """Append one compact JSON line to ``path`` (parents created)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    line = json.dumps(record, ensure_ascii=False, sort_keys=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(line + "\n")


def record_guard_fires(
    root: Path,
    state_dir: str,
    *,
    cmd: str,
    surface: str,
    posture: str,
    findings: list,
    verdict: str | None = None,
    reason: str | None = None,
) -> int:
    """Append one §5.3 record per finding; return how many were written.

    ``findings`` is any iterable of objects with ``path``/``kind``/``message``
    attributes (the kit's uniform ``Finding`` tuple is already the payload).
    ``guard`` is the finding's ``kind`` — per-kind granularity is exactly the
    per-guard unit B3 computes fire/FP rates over. ``verdict``/``reason`` are
    pre-filled only when an allowlist entry suppressed the finding (creating
    the entry IS the false_positive/accepted_risk verdict event); ``judge``
    and ``outcome`` always start null — a later, *different* party fills them
    (the grading-separation rule).

    Fail-open by contract: any failure (unwritable path, weird finding
    object) writes nothing and raises nothing — telemetry never blocks an
    agent-facing path. Writes only into an **existing** install
    (``state_dir`` present): ``check`` runs on un-adopted trees and must stay
    read-only there.
    """
    try:
        if not (root / state_dir).is_dir():
            return 0
        path = guard_fires_path(root, state_dir)
        ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
        written = 0
        for finding in findings:
            record = {
                "ts": ts,
                "guard": str(finding.kind),
                "cmd": cmd,
                "surface": surface,
                "posture": posture,
                "finding": {
                    "path": str(finding.path),
                    "kind": str(finding.kind),
                    "message": str(finding.message),
                },
                "verdict": verdict,
                "reason": reason,
                "judge": None,
                "outcome": None,
            }
            _append_jsonl(path, record)
            written += 1
        return written
    except Exception:  # noqa: BLE001 — telemetry fails open by contract
        return 0


def parse_model_line(text: str) -> dict | None:
    """Parse the last ``📊 Model:`` line out of a session log's text.

    Returns ``{"model", "effort", "task_class", "tokens_out"}`` or None when
    the needle is absent or the line has fewer than three ``·`` segments.
    Bold markers and the list dash are cosmetic and stripped; an optional 4th
    integer segment fills ``tokens_out`` (KF-9 — null until a meter exists).
    """
    payload = None
    for line in text.splitlines():
        if MODEL_LINE_NEEDLE in line and DRAFT_FILL_TOKEN not in line:
            # An auto-drafted stand-in (`[[fill: model]] · …`, KL-5) is not a
            # report — harvesting it would feed placeholder junk into the
            # PL-004 dataset. Skip it; the advisory keeps asking for the line.
            payload = line.split(MODEL_LINE_NEEDLE, 1)[1]
    if payload is None:
        return None
    parts = [p.strip(" *`") for p in payload.split("\N{MIDDLE DOT}")]
    parts = [p for p in parts if p]
    if len(parts) < 3:
        return None
    tokens_out: int | None = None
    if len(parts) >= 4:
        try:
            tokens_out = int(parts[3].replace(",", "").replace("_", ""))
        except ValueError:
            tokens_out = None
    return {
        "model": parts[0],
        "effort": parts[1],
        "task_class": parts[2],
        "tokens_out": tokens_out,
    }


def _model_usage_sessions(path: Path) -> set[str]:
    """Return the session slugs already recorded at ``path`` (dedupe key)."""
    sessions: set[str] = set()
    try:
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                record = json.loads(line)
            except ValueError:
                continue
            if isinstance(record, dict) and record.get("session"):
                sessions.add(str(record["session"]))
    except OSError:
        pass
    return sessions


def harvest_model_usage(root: Path, session_log: Path | None) -> list[str]:
    """Harvest the 📊 line from ``session_log`` into the model-usage JSONL.

    Returns human-readable result lines for the CLI to emit (advisories when
    the line is missing or the task class is off-taxonomy). The record is the
    PL-004 shape: ``{session, date, model, effort, task_class, tokens_out,
    outcome}``, ``outcome`` an all-null object until the lab sweep backfills
    it. One record per session slug — a re-run session-close never
    double-appends. Fail-open: any unexpected failure reports itself as an
    advisory rather than raising into session-close.
    """
    try:
        if session_log is None:
            return [f"no session log — no {MODEL_LINE_NEEDLE} line to harvest."]
        parsed = parse_model_line(session_log.read_text(encoding="utf-8"))
        if parsed is None:
            return [
                f"session log {session_log.name} has no "
                f"`{MODEL_LINE_NEEDLE}` line — add "
                "`- **\N{BAR CHART} Model:** <model> · <effort> · <task-class>` "
                "so the PL-004 dataset gets this session's row.",
            ]
        lines: list[str] = []
        if parsed["task_class"] not in TASK_CLASSES:
            known = " | ".join(TASK_CLASSES)
            lines.append(
                f"task_class {parsed['task_class']!r} is not one of the "
                f"{len(TASK_CLASSES)} PL-004 classes ({known}) — recorded "
                "verbatim; fix the line or the taxonomy.",
            )
        session = session_log.stem
        path = root / MODEL_USAGE_RELPATH
        if session in _model_usage_sessions(path):
            lines.append(f"model-usage: {session} already recorded (skipped).")
            return lines
        match = _DATE_PREFIX_RE.match(session)
        record = {
            "session": session,
            "date": match.group(1) if match else date.today().isoformat(),
            "model": parsed["model"],
            "effort": parsed["effort"],
            "task_class": parsed["task_class"],
            "tokens_out": parsed["tokens_out"],
            "outcome": {
                "ci_green_first_push": None,
                "checker_findings": None,
                "merged_pr": None,
                "reverted_within_window": None,
            },
        }
        _append_jsonl(path, record)
        lines.append(f"model-usage: recorded {session} -> {MODEL_USAGE_RELPATH}")
        return lines
    except Exception:  # noqa: BLE001 — telemetry fails open by contract
        return ["model-usage: harvest failed (fail-open) — row not recorded."]
