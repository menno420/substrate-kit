"""Reasons-required check allowlist (KL-3 — the §5.3 triage mechanism).

Port of the host project's ``*_exceptions.yml`` discipline: a finding may be
suppressed only by an allowlist entry that says **why**. The file lives at
``<state_dir>/check-exceptions.yml`` (consumer-owned, committed), a YAML list
of entries::

    # one entry per accepted finding — reason is REQUIRED
    # verdict: accepted_risk (default) or false_positive
    - path: docs/legacy-import.md
      kind: badge
      reason: "generated import, migrates at KL-5 — badge lands with the move"
      triaged: 2026-07-09
      by: session-kl3
      verdict: accepted_risk

Schema: ``{path, kind, reason (REQUIRED), triaged, by, verdict?}``. An entry
without a non-empty ``reason`` is **refused**: it suppresses nothing and is
itself reported as a finding — the door, not a nag. Creating a (valid) entry
IS the false_positive / accepted_risk verdict event for the guard-fire feed
(founding plan §5.3): the suppressed fire is recorded with the entry's
verdict + reason instead of a null awaiting triage.

The parser is a deliberate stdlib-only YAML *subset* (the engine imports no
third-party packages): comments, a flat list of flat string-valued mappings,
optional single/double quotes. Anything it cannot read is reported as a
finding rather than silently ignored — a malformed allowlist must never
silently widen (entries lost = findings resurface: fail-closed for
suppression, loud about why).
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_docs import Finding

EXCEPTIONS_FILENAME = "check-exceptions.yml"

_ENTRY_KEYS = ("path", "kind", "reason", "triaged", "by", "verdict")
_VERDICTS = ("accepted_risk", "false_positive")


def _unquote(value: str) -> str:
    """Strip one matching pair of surrounding quotes from ``value``."""
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def parse_allowlist(text: str, source: str) -> tuple[list[dict], list[Finding]]:
    """Parse the YAML-subset allowlist ``text`` into (entries, findings).

    Valid entries (with a non-empty ``reason``) go to ``entries``; refused or
    unparseable material becomes ``Finding``s with ``kind="allowlist"``
    (``path`` = ``source``, the allowlist file's own relpath).
    """
    entries: list[dict] = []
    findings: list[Finding] = []
    current: dict | None = None

    def close(entry: dict | None) -> None:
        if entry is None:
            return
        reason = str(entry.get("reason", "")).strip()
        label = entry.get("path") or entry.get("kind") or "?"
        if not reason:
            findings.append(
                Finding(
                    source,
                    "allowlist",
                    f"entry for {label!r} has no reason — refused "
                    "(reasons are required; the entry suppresses nothing)",
                ),
            )
            return
        verdict = entry.get("verdict", "accepted_risk")
        if verdict not in _VERDICTS:
            findings.append(
                Finding(
                    source,
                    "allowlist",
                    f"entry for {label!r} has unknown verdict {verdict!r} "
                    f"(allowed: {', '.join(_VERDICTS)}) — refused",
                ),
            )
            return
        entry["verdict"] = verdict
        entries.append(entry)

    for number, raw in enumerate(text.splitlines(), start=1):
        # Full-line comments only: a reason like "see PR #1770" keeps its #.
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        stripped = raw.strip()
        if stripped.startswith("- "):
            close(current)
            current = {}
            stripped = stripped[2:].strip()
            if not stripped:
                continue
        if current is None or ":" not in stripped:
            findings.append(
                Finding(
                    source,
                    "allowlist",
                    f"line {number} is not part of a `- key: value` entry — "
                    "unparseable (the allowlist accepts a flat YAML list of "
                    "flat mappings only)",
                ),
            )
            continue
        key, _, value = stripped.partition(":")
        key = key.strip()
        if key not in _ENTRY_KEYS:
            findings.append(
                Finding(
                    source,
                    "allowlist",
                    f"line {number}: unknown key {key!r} "
                    f"(known: {', '.join(_ENTRY_KEYS)})",
                ),
            )
            continue
        current[key] = _unquote(value.strip())
    close(current)
    return entries, findings


def load_allowlist(root: Path, state_dir: str) -> tuple[list[dict], list[Finding]]:
    """Load ``<state_dir>/check-exceptions.yml`` — ``([], [])`` when absent.

    An unreadable file yields no entries and one finding (never a crash: the
    checker must run on any tree).
    """
    path = root / state_dir / EXCEPTIONS_FILENAME
    source = f"{state_dir}/{EXCEPTIONS_FILENAME}"
    if not path.is_file():
        return [], []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return [], [Finding(source, "allowlist", "file unreadable — no suppression")]
    return parse_allowlist(text, source)


def apply_allowlist(
    findings: list,
    entries: list[dict],
) -> tuple[list, list[tuple]]:
    """Split ``findings`` into (kept, suppressed) by exact path+kind match.

    ``suppressed`` pairs each dropped finding with the entry that covered it,
    so the caller can record the guard fire with the entry's verdict+reason.
    Matching is deliberately exact on ``path`` and ``kind`` — a broad glob
    would let one entry silence a class of future findings its reason never
    triaged.
    """
    kept: list = []
    suppressed: list[tuple] = []
    for finding in findings:
        entry = next(
            (
                e
                for e in entries
                if e.get("path") == str(finding.path)
                and e.get("kind") == str(finding.kind)
            ),
            None,
        )
        if entry is None:
            kept.append(finding)
        else:
            suppressed.append((finding, entry))
    return kept, suppressed
