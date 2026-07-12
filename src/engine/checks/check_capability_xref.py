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

**Slice-5 extensions (grounded-skills plan §4.2d, added 2026-07-12;
§8 Q2=B advisory-first).** Two more advisory families, extending this
checker IN PLACE (the twice-proven pattern — slice 2 check_skill_grounds,
slice 4 check_owner_actions):

- **Append-log grammar** (the writer half is the planted template; both
  consume ``engine.grammar``'s capability-ledger constants):
  ``capability-log-malformed`` — an append-log bullet that does not open
  ``- YYYY-MM-DD · capability|wall · …``; ``capability-log-venue-unknown``
  — a venue-shaped field-3 token that is not one of the grammar's venue
  tokens. BACKWARD-COMPATIBLE by contract: an old five-field line without
  a venue token is read as venue ``any`` and NEVER flagged.
- **Staleness** (§4.2b): ``capability-entry-stale`` — a dated ledger entry
  (append-log line, or a seed row's ``LAST-VERIFIED:`` stamp) older than
  the config's ``cadence.staleness_days`` (default 14) whose surface the
  NEWEST session card cites — a claim, not a fact; re-verify with one
  cheap attempt and APPEND the result (THE DISCOVERY RULE step 5).

Reliability of the slice-5 checks (PL-008): UNVERIFIED — confirm their
findings against ground truth a few times across sessions before trusting
them; **delete these checks if they prove unreliable over multiple
sessions.** They are advisory-only by the same contract as the original
xref and must never count toward an exit code.
"""

from __future__ import annotations

import re
from collections.abc import Sequence
from datetime import date, datetime
from pathlib import Path
from typing import Any

from engine.checks.check_docs import Finding
from engine.checks.check_status_current import (
    CONTROL_README_RELPATH,
    INBOX_RELPATH,
    heartbeat_relpaths,
)
from engine.grammar import (
    CAPABILITY_ENTRY_TAGS,
    CAPABILITY_LAST_VERIFIED_RE,
    CAPABILITY_LOG_LINE_RE,
    CAPABILITY_LOG_TAUGHT_FORMAT,
    CAPABILITY_VENUE_SHAPE_RE,
    CAPABILITY_VENUE_TOKENS,
)

# Where adopt plants the capability ledger (src/engine/adopt.py PLANTED_DOCS:
# CAPABILITIES.md.tmpl → docs/CAPABILITIES.md) — same fixed relpath here.
CAPABILITIES_RELPATH = "docs/CAPABILITIES.md"

# An OWNER-ACTION block heading: `⚑ OWNER-ACTION <id> — <title>` (control/
# README.md § OWNER-ACTION format). The id token is free-form (`1`, `10`).
_OWNER_ACTION_RE = re.compile(r"^⚑ OWNER-ACTION\s+(\S+)[ \t]*(.*)$", re.MULTILINE)

# The ORDER 008 field labels, canonical + the shorthand spellings
# check_owner_actions accepts (#99 token alignment: WHY:/VERIFIED-WHEN:).
# _VERIFIED_LABELS locate the wall-evidence field; the rest bound its value.
_VERIFIED_LABELS = ("VERIFIED-NEEDED:", "VERIFIED-WHEN:")
_BOUNDARY_LABELS = (
    "WHAT:",
    "WHERE:",
    "HOW:",
    "WHY-IT-MATTERS:",
    "WHY:",
    "UNBLOCKS:",
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

    Accepts the canonical label and the VERIFIED-WHEN: shorthand (the #99
    token set check_owner_actions accepts). The value runs from the label to
    the next field label or the block's end (VERIFIED-NEEDED is last in the
    template order, but a reordered block still parses).
    """
    idx = -1
    label_len = 0
    for label in _VERIFIED_LABELS:
        pos = block.find(label)
        if pos != -1 and (idx == -1 or pos < idx):
            idx, label_len = pos, len(label)
    if idx == -1:
        return None
    value = block[idx + label_len :]
    cut = len(value)
    for label in _BOUNDARY_LABELS:
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


def _log_grammar_findings(rel: str, text: str) -> list[Finding]:
    """Grammar-check the ledger's append-log bullets (slice 5, advisory).

    Old-format compatibility is a hard contract: a five-field line without a
    venue token parses clean (field 3 carries spaces → an old-format finding,
    never judged as a venue). Only a venue-SHAPED field-3 token outside the
    grammar's venue set flags, and only date/tag misses flag as malformed.
    Continuation lines (indented wraps) are skipped like ``_ledger_sides``
    skips nothing — they never start ``- ``.
    """
    findings: list[Finding] = []
    in_log = False
    for line in text.splitlines():
        if line.startswith("## "):
            in_log = "append log" in line.lower()
            continue
        if not in_log or not line.startswith("- "):
            continue
        match = CAPABILITY_LOG_LINE_RE.match(line)
        if not match:
            findings.append(
                Finding(
                    rel,
                    "capability-log-malformed",
                    "append-log entry does not open `- YYYY-MM-DD · "
                    "capability|wall · …` — the taught grammar is "
                    f"`{CAPABILITY_LOG_TAUGHT_FORMAT}` "
                    "(src/engine/grammar.py); date the entry so the "
                    f"staleness rule can read it: {line[:60]!r}",
                ),
            )
            continue
        fields = [f.strip() for f in line.split("·")]
        tag = fields[1].lower() if len(fields) > 1 else ""
        if not any(t in tag for t in CAPABILITY_ENTRY_TAGS):
            findings.append(
                Finding(
                    rel,
                    "capability-log-malformed",
                    "append-log entry's second field names neither "
                    "`capability` nor `wall` — the ledger's two sides key on "
                    f"that tag ({CAPABILITY_LOG_TAUGHT_FORMAT}): "
                    f"{line[:60]!r}",
                ),
            )
            continue
        if len(fields) > 2:
            candidate = fields[2]
            if (
                CAPABILITY_VENUE_SHAPE_RE.match(candidate)
                and candidate not in CAPABILITY_VENUE_TOKENS
            ):
                findings.append(
                    Finding(
                        rel,
                        "capability-log-venue-unknown",
                        f"append-log entry names venue {candidate!r}, which "
                        "is not a grammar venue token "
                        f"({' · '.join(CAPABILITY_VENUE_TOKENS)}) — fix the "
                        "token, or drop the field to write the legacy "
                        "five-field form (read as venue `any`).",
                    ),
                )
    return findings


def _dated_entries(text: str) -> list[tuple[date, str]]:
    """Return ``(date, entry_text)`` per dated ledger bullet.

    Two dated shapes exist: append-log bullets (leading ISO date) and seed
    rows carrying a ``LAST-VERIFIED: YYYY-MM-DD`` stamp (§4.2b). A bullet's
    indented continuation lines belong to it — the distinctive tokens the
    citation scan matches usually live there. Unparseable dates are skipped
    (fail open — a malformed date is the grammar check's finding, never
    fabricated staleness).
    """
    entries: list[tuple[date, str]] = []

    def flush(bullet: list[str]) -> None:
        if not bullet:
            return
        block = "\n".join(bullet)
        match = CAPABILITY_LOG_LINE_RE.match(bullet[0])
        if match is not None:
            stamp = match.group(1)
        else:
            verified = CAPABILITY_LAST_VERIFIED_RE.search(block)
            if verified is None:
                return
            stamp = verified.group(1)
        try:
            entry_date = datetime.strptime(stamp, "%Y-%m-%d").date()
        except ValueError:
            return
        entries.append((entry_date, block))

    bullet: list[str] = []
    for line in text.splitlines():
        if line.startswith("- "):
            flush(bullet)
            bullet = [line]
        elif bullet and line.strip() and line[:1] in (" ", "\t"):
            bullet.append(line)  # indented continuation of the bullet above
        else:
            flush(bullet)
            bullet = []
    flush(bullet)
    return entries


def _newest_session_card(target: Path, sessions_dir: str) -> tuple[str, str] | None:
    """Return ``(relpath, text)`` of the newest date-named session card.

    Newest by FILENAME (cards are ``YYYY-MM-DD-<slug>.md``, so lexicographic
    order is date order) — never by mtime, which a fresh CI checkout
    flattens. ``None`` when no card exists or the newest is unreadable
    (fail open).
    """
    root = target / sessions_dir
    if not root.is_dir():
        return None
    cards = sorted(
        p for p in root.glob("*.md") if re.match(r"20\d{2}-\d{2}-\d{2}", p.name)
    )
    if not cards:
        return None
    newest = cards[-1]
    try:
        text = newest.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None
    rel = (
        str(newest.relative_to(target))
        if newest.is_relative_to(target)
        else str(newest)
    )
    return rel, text


def _stale_citation_findings(
    ledger_rel: str,
    ledger_text: str,
    card: tuple[str, str] | None,
    staleness_days: int,
    today: date,
) -> list[Finding]:
    """Flag stale ledger entries the newest session card cites (§4.2d ii).

    Coarse by the module's own contract: "cites" is distinctive-token
    overlap between the entry and the card (the same ``_anchors`` machinery
    as the OWNER-ACTION xref), so a false nudge costs one glance. No card,
    no dated entries, or nothing distinctive → no verdict.
    """
    if card is None:
        return []
    card_rel, card_text = card
    card_tokens = _tokens(card_text)
    findings: list[Finding] = []
    for entry_date, entry_text in _dated_entries(ledger_text):
        if (today - entry_date).days <= staleness_days:
            continue
        anchors = _anchors(entry_text)
        if not anchors:
            continue
        if len(anchors & card_tokens) >= min(2, len(anchors)):
            findings.append(
                Finding(
                    ledger_rel,
                    "capability-entry-stale",
                    f"ledger entry dated {entry_date.isoformat()} is older "
                    f"than the staleness window ({staleness_days}d) and "
                    f"{card_rel} cites its surface — an aged entry is a "
                    "claim, not a fact (THE DISCOVERY RULE step 5): "
                    "re-verify with one cheap attempt and APPEND the "
                    "result (re-verifications append, never edit).",
                ),
            )
    return findings


def check_capability_xref(
    target: Path,
    *,
    status_files: Sequence[str] | None = None,
    capabilities_relpath: str = CAPABILITIES_RELPATH,
    config: Any = None,
    today: date | None = None,
) -> list[Finding]:
    """Return advisory findings cross-referencing owner asks vs the ledger.

    Scans every configured heartbeat file's ``⚑ OWNER-ACTION`` blocks; each
    wall-shaped VERIFIED-NEEDED is token-matched against the capability
    ledger's Walls/Capabilities sides. Emits ``owner-ask-wall-unrecorded``
    when the wall is nowhere in the ledger (or the ledger is absent), and
    ``owner-ask-capability-resolved`` when only the capability side matches.

    Slice-5 extensions (see module docstring): the ledger's append-log lines
    are grammar-checked against ``engine.grammar``'s capability constants
    (``capability-log-malformed`` / ``capability-log-venue-unknown``; old
    five-field lines are never flagged), and dated entries older than
    ``config.cadence['staleness_days']`` (default 14, the triggers.py
    default-on-missing pattern) that the newest session card in
    ``config.sessions_dir`` cites emit ``capability-entry-stale``. ``today``
    is injectable for tests.

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
    if ledger_text is not None:
        findings += _log_grammar_findings(capabilities_relpath, ledger_text)
        staleness_days = 14
        sessions_dir = ".sessions"
        if config is not None:
            cadence = getattr(config, "cadence", None) or {}
            staleness_days = int(cadence.get("staleness_days", 14))
            sessions_dir = getattr(config, "sessions_dir", "") or ".sessions"
        findings += _stale_citation_findings(
            capabilities_relpath,
            ledger_text,
            _newest_session_card(target, sessions_dir),
            staleness_days,
            today if today is not None else date.today(),
        )
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
