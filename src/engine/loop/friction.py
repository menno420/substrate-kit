"""The friction-report protocol's consumer half (founding plan §9.1, KL-4).

The context-delta loop, cross-repo: a consumer collects its kit-friction ⚑
records, wraps them in a small envelope, and files them as a **GitHub issue
labeled ``friction`` on the kit repo** (⚑ KF-7). The engine is stdlib-only
and holds no network credentials, so the split is explicit:

- **The engine (``friction export``)** builds the envelope and writes it to
  the outbox at ``<state_dir>/friction-outbox/`` — the same outbox §9.1
  prescribes for network/credential failure, used unconditionally: every
  export lands there first, and the file doubles as the retry buffer.
- **The session/agent files the issue** (its GitHub surface — MCP, ``gh``,
  Actions) using the issue-ready title + body ``friction export``/``show``
  print, then deletes the drained outbox file. Session-close advises on
  pending files (best-effort, fail-open — the lab cannot drain a consumer's
  outbox; it has no consumer write access).

Envelope (§9.1, D-14 — the payload IS the reflection record shape)::

    { "schema": 1, "repo": "<github full name>", "project_id": "<config id>",
      "kit_version": "1.0.0", "reports": [ {reflection-record…}, … ] }

Reports = the reflection buffer's ``flag``-tagged records **plus** a direct
session-log scan for un-mined ⚑ lines — the buffer is a 5-slot rolling
window, not an archive, so export never depends on it alone (D-14).
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path
from typing import Any

from engine.lib.atomicio import atomic_write_text
from engine.loop.reflections import (
    REFLECTIONS_FILENAME,
    load_reflections,
    mine_reflections,
)

FRICTION_SCHEMA = 1
FRICTION_OUTBOX_DIRNAME = "friction-outbox"
FRICTION_LABEL = "friction"

# owner/repo out of a git remote URL — tolerant of https, ssh, and proxy
# forms (…github.com/owner/repo.git · git@github.com:owner/repo ·
# http://proxy/git/owner/repo). Fail-open: no match reads as "".
_REMOTE_REPO_RE = re.compile(r"[:/]([\w.-]+/[\w.-]+?)(?:\.git)?\s*$")


def detect_repo(root: Path) -> str:
    """Best-effort ``owner/repo`` from ``.git/config``'s origin URL ("" if not).

    Pure file parsing (the engine may not shell out): finds the
    ``[remote "origin"]`` section's ``url =`` line and extracts the last two
    path components. Any failure — no repo, detached layouts, exotic
    remotes — returns ``""`` so the caller can require ``--repo`` instead.
    """
    config_path = root / ".git" / "config"
    try:
        text = config_path.read_text(encoding="utf-8")
    except OSError:
        return ""
    in_origin = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("["):
            in_origin = stripped.replace("'", '"') == '[remote "origin"]'
            continue
        if in_origin and stripped.startswith("url"):
            _, _, url = stripped.partition("=")
            match = _REMOTE_REPO_RE.search(url.strip())
            return match.group(1) if match else ""
    return ""


def friction_reports(target: Path, config: Any) -> list[dict]:
    """Collect the ⚑ friction records for one export (D-14, both sources).

    Buffer records tagged ``flag`` come through verbatim (full reflection
    record shape); the direct session-log scan adds un-mined ⚑ lines as
    ``{lesson, evidence, tags}`` records, deduplicated against the buffer
    (and against each other) by lesson text.
    """
    reflections_path = target / config.state_dir / REFLECTIONS_FILENAME
    reports = [
        entry
        for entry in load_reflections(reflections_path)
        if "flag" in (entry.get("tags") or [])
    ]
    seen = {str(entry.get("lesson", "")) for entry in reports}
    # A deliberately huge last_n: the export scans EVERY session log — the
    # buffer's 5-slot window must never bound what gets reported.
    for candidate in mine_reflections(target / config.sessions_dir, last_n=100000):
        if "flag" not in candidate.get("tags", []):
            continue
        lesson = str(candidate.get("lesson", ""))
        if not lesson or lesson in seen:
            continue
        seen.add(lesson)
        reports.append(candidate)
    return reports


def build_envelope(
    *,
    repo: str,
    project_id: str,
    kit_version: str,
    reports: list[dict],
) -> dict:
    """Return the §9.1 wire envelope for ``reports``."""
    return {
        "schema": FRICTION_SCHEMA,
        "repo": repo,
        "project_id": project_id,
        "kit_version": kit_version,
        "reports": reports,
    }


def outbox_dir(target: Path, state_dir: str) -> Path:
    """Return the friction-outbox directory for one install."""
    return target / state_dir / FRICTION_OUTBOX_DIRNAME


def list_outbox(target: Path, state_dir: str) -> list[Path]:
    """Return the pending outbox envelopes, oldest first ([] when none)."""
    box = outbox_dir(target, state_dir)
    if not box.is_dir():
        return []
    return sorted(p for p in box.glob("*.json") if p.is_file())


def write_outbox(target: Path, state_dir: str, envelope: dict) -> Path:
    """Write ``envelope`` to a fresh outbox file (atomic); return its path."""
    box = outbox_dir(target, state_dir)
    stamp = date.today().isoformat()
    serial = 1
    while (path := box / f"{stamp}-friction-{serial:02d}.json").exists():
        serial += 1
    atomic_write_text(path, json.dumps(envelope, indent=2, sort_keys=True) + "\n")
    return path


def load_envelope(path: Path) -> dict | None:
    """Read one outbox envelope; None on a missing/corrupt file (fail-open)."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None
    return raw if isinstance(raw, dict) else None


def friction_issue_title(envelope: dict) -> str:
    """Return the friction issue's title line."""
    repo = envelope.get("repo") or envelope.get("project_id") or "unknown consumer"
    count = len(envelope.get("reports") or [])
    version = envelope.get("kit_version") or "unrecorded"
    plural = "s" if count != 1 else ""
    return f"[friction] {repo}: {count} report{plural} @ kit v{version}"


def friction_issue_body(envelope: dict) -> str:
    """Return the friction issue's body: one-line summary + fenced JSON (§9.1)."""
    reports = envelope.get("reports") or []
    lessons = [str(r.get("lesson", ""))[:120] for r in reports[:3]]
    summary = "; ".join(lesson for lesson in lessons if lesson) or "(no lessons)"
    if len(reports) > 3:
        summary += f"; … +{len(reports) - 3} more"
    payload = json.dumps(envelope, indent=2, sort_keys=True)
    return (
        f"Consumer friction report — {summary}\n"
        "\n"
        f"```json\n{payload}\n```\n"
        "\n"
        f"*Filed per founding plan §9.1 (label `{FRICTION_LABEL}`; triage = "
        "the lab loop's step 5 three-clause bar; disposition comment + "
        "close).*\n"
    )
