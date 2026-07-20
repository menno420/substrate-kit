"""Capability dateless-wall advisory — warn-only, NEVER exit-affecting.

Provenance: ``docs/planning/2026-07-19-night-run-idea-groom-wave2.md`` S14 (the
seeded follow-up named in R5's ``check_stale_walls``). This is the exact NEGATIVE
complement of the R5 stale-wall advisory: R5 flags a *dated* wall whose date has
aged past the re-verify window, and DELIBERATELY skips a wall row with no
parseable date as "a separate concern" (``check_stale_walls`` docstring). This
checker IS that separate concern.

Why this exists: ``docs/CAPABILITIES.md`` is the durable "what agent sessions
CAN and CANNOT do here" ledger, and THE DISCOVERY RULE says a recorded *wall*
(a blocked capability) must be *re-verified* on a cadence or it decays from a
fact into a stale claim. R5's ``check_stale_walls`` enforces that cadence — but
it can only fire on a wall that carries a parseable date. A wall row with NO date
therefore escapes the re-verify cadence forever: it can never age out, never
nudge a re-check, and silently hardens into an un-auditable claim. This checker
closes that gap by nudging the owner to stamp every wall with a date
(``LAST-VERIFIED: YYYY-MM-DD`` on a seed row, or a leading append-log date), so
the R5 staleness rule can then fire on it. Together the two checkers cover every
wall row exactly once: dated → R5 stale-checks it; dateless → S14 flags it.

What it does: parse the ``## Walls`` seed rows and the ``## Append log`` rows of
``docs/CAPABILITIES.md`` under ``target``; for any *wall* row (never a capability
row) that carries no parseable date, emit ONE advisory naming the wall. A wall
row is dated (and therefore silent here) when:
  * an append-log ``- YYYY-MM-DD · wall · ...`` row carries its leading log date,
    or
  * any wall row carries a trailing ``LAST-VERIFIED: YYYY-MM-DD`` stamp.
Capability rows are never flagged (walls only, matching R5), and a *dated* wall
row is never flagged (that is R5's domain).

The grammar for "what is a wall row" is imported wholesale from
``check_stale_walls`` (``_iter_bullets`` / ``_is_wall_section`` / ``_title`` /
``_parse_date`` and the ``_RE_APPENDLOG`` / ``_RE_LAST_VERIFIED`` regexes) as the
SINGLE SOURCE OF TRUTH, so the two complementary checkers can never disagree on
which rows are walls. The dist flattens every engine module into one namespace
and strips this intra-package import, so the names resolve there too
(``check_stale_walls`` precedes this module in ``MODULE_ORDER``).

Posture — ADVISORY only (warn-only, never exit-affecting): this returns a single
``list[Finding]`` with no gate tier, wired on the advisory path in ``cli.py``
(``posture="advisory"``) exactly like its R5 stale-wall sibling. It is
deliberately NOT in ``STRICT_SUBCHECKS`` — a hard red would break every repo
whose ledger legitimately carries an as-yet-undated wall, which is the opposite
of the "stamp it, don't panic" nudge intended. Input-gated + fail-open like every
checker: no ``docs/CAPABILITIES.md``, or an unreadable file, yields nothing (an
absent/unreadable ledger is not a verdict). Stdlib only.
"""

from __future__ import annotations

import re

from engine.checks.check_docs import Finding

# Single source of truth for the wall-row grammar — reuse R5's parser + regexes so
# the stale-wall lint and this dateless lint can never disagree on what a wall row
# is. The dist flattens every engine module into one namespace and strips this
# intra-package import, so the names resolve there too (check_stale_walls precedes
# this module in MODULE_ORDER). Un-aliased on purpose: the flat-namespace strip
# requires the exact top-level names check_stale_walls defines.
from engine.checks.check_stale_walls import (
    _CAPABILITIES_RELPATH,
    _RE_APPENDLOG,
    _RE_LAST_VERIFIED,
    _is_wall_section,
    _iter_bullets,
    _parse_date,
    _title,
)

# Named DATELESS_WALL_KIND, not a bare FINDING_KIND: the dist concatenates every
# engine module into one file, and check_folded_gate.py already owns a
# module-level ``FINDING_KIND`` — a second top-level ``FINDING_KIND`` would
# collide (last wins) and reds ``test_check_namespace``. The value is the finding
# kind (paired to a ``check_remediate.REMEDIATIONS`` entry, S8 coverage lesson).
DATELESS_WALL_KIND = "dateless-wall"

# A dateless append-log row: ``- <type> · ...`` with NO leading date (the R5
# ``_RE_APPENDLOG`` requires a leading ``YYYY-MM-DD``, so a dateless log row never
# matches it). The type token (group 1) classes it — ``wall`` / ``wall+recipe``
# both start with "wall".
_RE_APPENDLOG_DATELESS = re.compile(r"^-\s+(\S+)\s+·")


def _dateless_wall_title(section, first_line, bullet_text) -> str | None:
    """Return a short title if the bullet is an *undated* wall row, else ``None``.

    Complements ``check_stale_walls._wall_row_date`` (which returns dated walls):
    this returns exactly the wall rows that carry no parseable date — capability
    rows, non-wall rows, and *dated* wall rows are all skipped. Branches by
    enclosing section so a dateless append-log row and a seed row are classed by
    where they live, never by shape alone.
    """
    header = section.lower() if section is not None else ""
    in_append_log = "append" in header

    if in_append_log:
        # Append-log section. A DATED wall row (leading YYYY-MM-DD) is R5's job —
        # skip it here. A dateless log row is our concern iff its type is a wall.
        if _RE_APPENDLOG.match(first_line) is not None:
            return None  # has a leading log date -> dated, not our concern
        dateless = _RE_APPENDLOG_DATELESS.match(first_line)
        if dateless is None:
            return None  # not a recognizable append-log row shape
        row_type = dateless.group(1).lower()
        if not row_type.startswith("wall"):
            return None  # capability (or other) dateless log row — skip
        if _has_parseable_last_verified(bullet_text):
            return None  # a LAST-VERIFIED stamp dates it -> R5's domain
        fields = first_line.split(" · ")
        finding = fields[1] if len(fields) >= 2 else None
        return _title(bullet_text, first_line, finding)

    if _is_wall_section(section):
        # Seed / prose wall row: classed a wall by its ``## Walls`` section (no
        # type token). Dated iff it carries a parseable LAST-VERIFIED stamp.
        if _has_parseable_last_verified(bullet_text):
            return None  # dated seed wall -> R5's domain
        return _title(bullet_text, first_line, None)

    return None  # capability section / prose section — not a wall row


def _has_parseable_last_verified(bullet_text: str) -> bool:
    """True when the bullet carries a well-formed ``LAST-VERIFIED: YYYY-MM-DD``
    stamp (a malformed date does not count as dated — it is still un-checkable)."""
    match = _RE_LAST_VERIFIED.search(bullet_text)
    if match is None:
        return False
    return _parse_date(match.group(1)) is not None


def check_dateless_walls(target, config=None) -> list[Finding]:
    """Return advisory findings for ``wall`` ledger rows carrying no parseable date.

    Advisory only — the caller wires this on the ``posture="advisory"`` path and
    NEVER counts it toward the exit code. Input-gated + fail-open: an absent or
    unreadable ``docs/CAPABILITIES.md`` yields no finding. ``config`` is accepted
    for call-site symmetry with its R5 sibling but unused (there is no threshold —
    dateless is a binary property, not a window).
    """
    ledger = target / _CAPABILITIES_RELPATH
    if not ledger.is_file():
        return []  # input-gated: no ledger to scan
    try:
        text = ledger.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable ledger is not a verdict

    findings: list[Finding] = []
    for section, first_line, bullet_text in _iter_bullets(text):
        title = _dateless_wall_title(section, first_line, bullet_text)
        if title is None:
            continue
        findings.append(
            Finding(
                _CAPABILITIES_RELPATH,
                DATELESS_WALL_KIND,
                f"dateless wall '{title}' carries no parseable date — add a "
                "LAST-VERIFIED: YYYY-MM-DD stamp (seed row) or a leading "
                "append-log date so the DISCOVERY RULE's re-verify cadence "
                "(check_stale_walls) can fire on it; an undated wall never ages "
                "out and hardens into an un-auditable claim.",
            ),
        )
    return findings
