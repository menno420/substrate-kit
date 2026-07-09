"""Owner-action quality checker — ⚑ needs-owner asks must be actionable.

Why + provenance: the owner-action quality band (inbox ORDER 008, owner
directive 2026-07-09). Agents' ``⚑ needs-owner`` items were too often
(a) unnecessary — based on assumed walls nobody actually hit — or
(b) phrased so a non-technical owner couldn't act on them directly. The
owner is the scarcest resource in the program; every unclear or
unnecessary ask burns attention and stalls the asking lane. The contract
(canonical: ``control/README.md`` § the OWNER-ACTION item format) gives
every ask six REQUIRED fields:

- ``WHAT`` — one plain sentence, zero jargon
- ``WHERE`` — exact click path or URL
- ``HOW`` — paste-ready text/values where applicable
- ``WHY-IT-MATTERS`` — one sentence in product terms
- ``UNBLOCKS`` — what starts moving the moment it's done
- ``VERIFIED-NEEDED`` — the attempt made + the exact error/wall proving
  only the owner can do this (assumption-based asks are banned)

Posture: **advisory-only, never exit-affecting** — the deliberate mirror
of ``check_status_current``'s staleness warning. Existing adopters carry
free-text asks today; a gate would pre-redden every heartbeat the moment
this ships. The warning surfaces in every ``check`` run (both CI lanes —
the asks live in the heartbeat files the control fast lane already
validates) and the ``session-close`` skill asks the same question at close;
migration pressure without a locked door.

Detection is deliberately coarse (one finding per heartbeat file naming
the absent field labels, scanning the whole file so inline items and
linked blocks both count): the point is a nudge toward the format, not a
parser for every free-text shape an ask can take. Input-gated like every
checker — engages only when the ``control/`` protocol is present and the
file's ``⚑ needs-owner`` value is something other than ``none``. Stdlib
only; unreadable files fail open.
"""

from __future__ import annotations

from collections.abc import Sequence
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    INBOX_RELPATH,
    heartbeat_relpaths,
)

# The six REQUIRED field labels (ORDER 008). VERIFIED-NEEDED is the band's
# heart — the attempted-or-exact-wall proof that kills assumption-based asks.
OWNER_ACTION_FIELDS = (
    "WHAT:",
    "WHERE:",
    "HOW:",
    "WHY-IT-MATTERS:",
    "UNBLOCKS:",
    "VERIFIED-NEEDED:",
)

NEEDS_OWNER_TOKEN = "⚑ needs-owner"


def _needs_owner_value(text: str) -> str | None:
    """Return the ``⚑ needs-owner`` value, or None when the line is absent.

    The heartbeat contract writes one ``⚑ needs-owner: <...>`` line; the
    value is everything after the first colon following the token. Only the
    first occurrence counts — the format block in a README copy would
    otherwise self-trigger.
    """
    idx = text.find(NEEDS_OWNER_TOKEN)
    if idx == -1:
        return None
    line = text[idx:].splitlines()[0]
    _, _, value = line.partition(":")
    return value.strip()


def check_owner_actions(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
) -> list[Finding]:
    """Return advisory findings for unstructured ⚑ needs-owner asks.

    One ``owner-action-fields`` finding per configured heartbeat file whose
    ``⚑ needs-owner`` value is present and not ``none`` while the file lacks
    one or more OWNER-ACTION field labels (the whole file is scanned, so an
    inline item and a structured block below the list both satisfy the
    contract). Advisory by contract: callers must never count these toward
    an exit code (see module docstring). Empty when the ``control/``
    protocol is absent.
    """
    relpaths = heartbeat_relpaths(status_files)
    control_evidence = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in control_evidence):
        return []
    findings: list[Finding] = []
    for rel in relpaths:
        path = target / rel
        if not path.is_file():
            continue  # missing heartbeat is check_status_current's finding
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        value = _needs_owner_value(text)
        if value is None or value.lower().startswith("none") or not value:
            continue
        missing = [f.rstrip(":") for f in OWNER_ACTION_FIELDS if f not in text]
        if missing:
            findings.append(
                Finding(
                    rel,
                    "owner-action-fields",
                    "⚑ needs-owner carries asks without the OWNER-ACTION "
                    f"fields (missing: {', '.join(missing)}) — the owner is "
                    "the scarcest resource: structure each ask per "
                    "control/README.md § OWNER-ACTION format (attempt it "
                    "yourself or cite the exact wall — VERIFIED-NEEDED; "
                    "assumption-based asks are banned), and withdraw stale "
                    "asks.",
                ),
            )
    return findings
