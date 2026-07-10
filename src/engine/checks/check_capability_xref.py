"""OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (kit-lab queue item 8).

Why + provenance: the #68 session card's 💡 idea
(``.sessions/2026-07-09-order008.md``) — the OWNER-ACTION
``VERIFIED-NEEDED`` field (ORDER 008) and ``docs/CAPABILITIES.md`` (ORDER
006) are two halves of one loop that nothing closes: when an ask's
VERIFIED-NEEDED cites a technical wall that is NOT yet in the capability
ledger, the wall should be appended there in the same session (THE
DISCOVERY RULE step 4 — "an unrecorded discovery is re-paid by every
future session"); and a ledger entry that records the cited surface as a
verified WORKING capability means the ask may be resting on a wall that
has since fallen. This checker cross-references the two files and nudges
both ways, turning every owner-ask into a capability-ledger contribution
for free.

What it flags (both **advisory** — a nudge, never a locked door, the same
posture as ``check_claims`` / ``check_owner_actions``):

- ``owner-ask-wall-unrecorded`` — a wall-shaped OWNER-ACTION (its
  VERIFIED-NEEDED cites a technical block: a 403, an access-denied, an
  owner-only surface) whose wall the capability ledger does not record.
  The nudge: append the wall to the ledger this session.
- ``owner-ask-capability-resolved`` — a wall-shaped OWNER-ACTION whose
  cited surface the ledger records ONLY as a verified-working capability
  (no matching wall entry). The nudge: re-verify the ask — the wall may
  have fallen — and withdraw it or record the residual wall.

Detection is deliberately coarse, mirroring ``check_owner_actions``'s
posture note: VERIFIED-NEEDED texts are free prose, so the cross-check is
distinctive-token overlap against the ledger's Walls/Capabilities sections
(headings + tagged append-log entries), not a parser for every shape a
wall citation can take. Judgment-shaped asks (license calls, product
rulings — "product judgment", "not a technical wall") are out of the
ledger's scope and are skipped entirely; an ask with no wall marker at all
is skipped too. False nudges cost one glance; an unrecorded wall costs
every future session a rediscovery.

Posture is **advisory-only, never exit-affecting** — existing adopters
carry free-prose asks today, and token overlap can never be a verdict.
Input-gated on the ``control/`` protocol and per heartbeat file, like
every control-band checker. Pure stdlib — no ``subprocess`` (§3.2); it
only reads the heartbeat files the fast lane already validates plus the
planted capability ledger. Unreadable files fail open (no verdict).
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    INBOX_RELPATH,
    heartbeat_relpaths,
)

# Where adopt plants the capability ledger (src/engine/adopt.py PLANTED_DOCS:
# CAPABILITIES.md.tmpl → docs/CAPABILITIES.md) — same fixed relpath here.
CAPABILITIES_RELPATH = "docs/CAPABILITIES.md"

# An OWNER-ACTION block heading: `⚑ OWNER-ACTION <id> — <title>` (control/
# README.md § OWNER-ACTION format). The id token is free-form (`1`, `10`).
_OWNER_ACTION_RE = re.compile(r"^⚑ OWNER-ACTION\s+(\S+)[ \t]*(.*)$", re.MULTILINE)

# The six ORDER 008 field labels — used to bound the VERIFIED-NEEDED value.
_FIELD_LABELS = (
    "WHAT:",
    "WHERE:",
    "HOW:",
    "WHY-IT-MATTERS:",
    "UNBLOCKS:",
    "VERIFIED-NEEDED:",
)

# Wall-shaped evidence markers (lowercase substring match on VERIFIED-NEEDED):
# the hard-block vocabulary the ledger's Walls section exists to record.
_WALL_MARKERS = (
    "403",
    "denied",
    "refused",
    "blocked",
    "wall",
    "owner-only",
    "owner-click",
    "owner ui",
    "console ui",
    "no agent path",
    "no mcp",
)

# Judgment-shaped asks are OUT of the ledger's scope — a license choice or a
# rubric ruling is owner judgment by nature, not a technical wall to record.
_JUDGMENT_MARKERS = (
    "product judgment",
    "owner judgment",
    "not a technical wall",
    "legal",
)

# Generic tokens that would match any prose — excluded from anchor sets so
# overlap means the SAME surface, not the same register.
_STOPWORDS = frozenset(
    """
    about action actions after agent agents already also and any are because
    been before being between both but can cannot capability capabilities
    could did does doing done each either else enumerated environment error
    every exact exists file files for from had has have how into item items
    its itself may more most must need needed needs never none not nothing
    now one only other our out over own path paths per proves same section
    see session sessions should since some such than that the their them
    then there these they this those through today under until upon verified
    very wall walls was were what when where which while who whose will with
    would yet you your
    """.split()
)

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9._/:\-]*")


def _tokens(text: str) -> set[str]:
    """Return the lowercase token set of ``text`` (ledger side — unfiltered)."""
    return {tok.strip("./:-_") for tok in _TOKEN_RE.findall(text.lower())}


def _anchors(text: str) -> set[str]:
    """Return the DISTINCTIVE token set of a VERIFIED-NEEDED value.

    A token anchors the cross-check only when it is specific enough that a
    match in the ledger plausibly means the same surface: it carries a digit
    or path/identifier punctuation, or is ≥ 6 chars — and is not a generic
    stopword. Short/common words never anchor (coarse by design, see the
    module docstring).
    """
    anchors: set[str] = set()
    for raw in _TOKEN_RE.findall(text.lower()):
        tok = raw.strip("./:-_")
        if len(tok) < 3 or tok in _STOPWORDS:
            continue
        if (
            any(ch.isdigit() for ch in tok)
            or any(ch in "./:-_" for ch in tok)
            or len(tok) >= 6
        ):
            anchors.add(tok)
    return anchors


def _owner_action_blocks(text: str) -> list[tuple[str, str, str]]:
    """Return ``(id, title, block_text)`` per ⚑ OWNER-ACTION item in ``text``.

    A block runs from its heading to the next blank line, the next ``⚑``
    heading, or EOF — the shape the control heartbeat writes (fields on
    their own lines, blocks separated by blank lines).
    """
    blocks: list[tuple[str, str, str]] = []
    for match in _OWNER_ACTION_RE.finditer(text):
        start = match.start()
        blank = text.find("\n\n", match.end())
        nxt = text.find("\n⚑", match.end())
        ends = [pos for pos in (blank, nxt) if pos != -1]
        end = min(ends) if ends else len(text)
        blocks.append((match.group(1), match.group(2).strip(), text[start:end]))
    return blocks


def _verified_needed(block: str) -> str | None:
    """Return a block's VERIFIED-NEEDED value, or None when the field is absent.

    The value runs from the label to the next field label or the block's end
    (VERIFIED-NEEDED is last in the template order, but a reordered block
    still parses).
    """
    idx = block.find("VERIFIED-NEEDED:")
    if idx == -1:
        return None
    value = block[idx + len("VERIFIED-NEEDED:") :]
    cut = len(value)
    for label in _FIELD_LABELS[:-1]:
        pos = value.find(label)
        if pos != -1:
            cut = min(cut, pos)
    return value[:cut].strip()


def _is_wall_shaped(verified: str) -> bool:
    """True when a VERIFIED-NEEDED cites a technical wall (not owner judgment)."""
    lower = verified.lower()
    if any(marker in lower for marker in _JUDGMENT_MARKERS):
        return False
    return any(marker in lower for marker in _WALL_MARKERS)


def _ledger_sides(text: str) -> tuple[set[str], set[str]]:
    """Split the capability ledger into ``(wall_tokens, capability_tokens)``.

    Sections are keyed on the planted template's headings (``## Walls`` /
    ``## Capabilities``); append-log entries (``- YYYY-MM-DD · tag · …``)
    join the side(s) their tag names — a ``wall+recipe`` entry feeds both
    the wall side (tag says wall) and stays out of the capability side
    (a recipe around a wall is not the wall's absence).
    """
    wall_parts: list[str] = []
    cap_parts: list[str] = []
    section = None
    log_side: list[str] | None = None
    for line in text.splitlines():
        if line.startswith("## "):
            lower = line.lower()
            if "wall" in lower:
                section = "walls"
            elif "capabilit" in lower:
                section = "caps"
            elif "append log" in lower:
                section = "log"
            else:
                section = None
            continue
        if section == "walls":
            wall_parts.append(line)
        elif section == "caps":
            cap_parts.append(line)
        elif section == "log":
            if line.startswith("- "):
                fields = line.split("·")
                tag = fields[1].lower() if len(fields) > 1 else ""
                log_side = wall_parts if "wall" in tag else cap_parts
                log_side.append(line)
            elif line.strip() and log_side is not None:
                log_side.append(line)  # continuation line of the entry above
    return _tokens("\n".join(wall_parts)), _tokens("\n".join(cap_parts))


def check_capability_xref(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
    capabilities_relpath: str = CAPABILITIES_RELPATH,
) -> list[Finding]:
    """Return advisory findings cross-referencing owner asks vs the ledger.

    Scans every configured heartbeat file's ``⚑ OWNER-ACTION`` blocks; each
    wall-shaped VERIFIED-NEEDED is token-matched against the capability
    ledger's Walls/Capabilities sides. Emits ``owner-ask-wall-unrecorded``
    when the wall is nowhere in the ledger (or the ledger is absent), and
    ``owner-ask-capability-resolved`` when only the capability side matches.
    Advisory by contract — callers must never count these toward an exit
    code (see module docstring). Empty when the ``control/`` protocol is
    absent; fail-open on unreadable files and anchor-less asks.
    """
    relpaths = heartbeat_relpaths(status_files)
    control_evidence = [INBOX_RELPATH, CONTROL_README_RELPATH, *relpaths]
    if not any((target / rel).is_file() for rel in control_evidence):
        return []

    ledger_path = target / capabilities_relpath
    ledger_text: str | None = None
    if ledger_path.is_file():
        try:
            ledger_text = ledger_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            return []  # fail open — an unreadable ledger is not a verdict
    wall_tokens, cap_tokens = (
        _ledger_sides(ledger_text) if ledger_text is not None else (set(), set())
    )

    findings: list[Finding] = []
    for rel in relpaths:
        path = target / rel
        if not path.is_file():
            continue  # missing heartbeat is check_status_current's finding
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        for item_id, title, block in _owner_action_blocks(text):
            verified = _verified_needed(block)
            if not verified or not _is_wall_shaped(verified):
                continue  # field-less asks are check_owner_actions' finding;
                # judgment asks are out of the ledger's scope
            anchors = _anchors(verified)
            if not anchors:
                continue  # nothing distinctive to match — no verdict
            need = min(2, len(anchors))
            label = f"OWNER-ACTION {item_id}" + (f" ({title})" if title else "")
            if len(anchors & wall_tokens) >= need:
                continue  # the cited wall is recorded — the loop is closed
            if len(anchors & cap_tokens) >= need:
                findings.append(
                    Finding(
                        rel,
                        "owner-ask-capability-resolved",
                        f"{label} cites a wall, but {capabilities_relpath} "
                        "records the matching surface only as a verified "
                        "WORKING capability — the wall may have fallen. "
                        "Re-verify the ask (THE DISCOVERY RULE step 3) and "
                        "withdraw it, or record the residual wall.",
                    ),
                )
            else:
                findings.append(
                    Finding(
                        rel,
                        "owner-ask-wall-unrecorded",
                        f"{label} cites a technical wall that "
                        f"{capabilities_relpath} does not record — append "
                        "the wall there this session (THE DISCOVERY RULE "
                        "step 4: dated, exact error, workaround), so the "
                        "ask's evidence becomes every later session's "
                        "starting fact.",
                    ),
                )
    return findings
