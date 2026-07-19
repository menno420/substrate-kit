"""Append-log ⇄ Walls-correction disagreement advisory — warn-only, NEVER exit-affecting.

Provenance: ``docs/planning/2026-07-19-night-run-idea-groom.md`` R7 (from the
``capabilities-mergedoctrine-correction`` card). Sibling of R5's
``check_stale_walls`` on the same advisory seam.

Why this exists: ``docs/CAPABILITIES.md`` records a capability's status in two
places that can drift apart — a durable ``## Walls`` *correction* row ("X is NOT
a wall") and the newest ``## Append log`` verdict on that same capability (its
``capability|wall`` type token). When a correction lands in one place but the
other is not updated, the ledger contradicts itself. That exact self-
contradiction persisted for a full day on the merge/arm/flip capability (a
``## Walls`` "Merging own PRs is NOT a wall" correction while an append-log
``wall`` entry still called it blocked). Nothing warned. This checker is the
enforcing readout: for each tracked capability family it compares the newest
append-log verdict against the Walls-correction verdict and emits ONE advisory
when they disagree.

What it does: for each capability family (seeded: merge/arm/flip), find (a) the
newest — topmost, "newest first" — ``## Append log`` entry mentioning the family
and read its ``capability`` (AVAILABLE) vs ``wall`` (BLOCKED) type token, and
(b) a ``## Walls`` *correction* row mentioning the family (a bullet carrying a
correction token — ``corrected`` / ``superseded`` / a ``not a wall`` negation)
and read its polarity (a "not a wall" phrasing = AVAILABLE, else BLOCKED). Fire
iff both sides exist AND disagree. A family with no Walls-correction row, or no
append-log entry, is silent — there is nothing to cross-check. The append-log
side keys on the explicit ``capability|wall`` type token (no prose
interpretation); the Walls side keys on the ``not a wall`` negation.

"Newest append-log entry" means the newest entry *mentioning that family* (a
same-capability comparison), not the globally newest row — a newest row about an
unrelated capability is irrelevant to this family's agreement.

Posture — ADVISORY only (warn-only, never exit-affecting), wired on the
``posture="advisory"`` seam in ``cli.py`` exactly like ``check_stale_walls``.
Deliberately NOT in ``STRICT_SUBCHECKS`` — a hard red would break every adopter
whose ledger momentarily drifted, the opposite of the "reconcile the two, don't
panic" nudge. Input-gated + fail-open: no/unreadable ``docs/CAPABILITIES.md``
yields nothing. Stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

# The capability ledger this checker reads (same relpath as check_stale_walls).
_WLA_CAPABILITIES_RELPATH = "docs/CAPABILITIES.md"

# Capability families this lint cross-checks. Each is a (name, keyword regex)
# pair; a ledger row is "about" the family when its text matches. Seeded with the
# merge/arm/flip family — the capability whose day-long self-contradiction
# motivated R7 (groom doc). Add families here as the ledger grows other
# correction-prone capabilities.
_FAMILIES: tuple[tuple[str, "re.Pattern[str]"], ...] = (
    (
        "merge/arm/flip",
        re.compile(
            r"\b(?:merg\w*|auto-merge|arm\w*|ready-flip|"
            r"draft\s*(?:→|->|to)\s*ready|flip\w*)\b",
            re.IGNORECASE,
        ),
    ),
)

# A ``## `` section header.
_WLA_RE_SECTION = re.compile(r"^##\s+(.*)$")

# An append-log row: ``- YYYY-MM-DD · <type> · ...`` — group 1 = type token.
_WLA_RE_APPENDLOG = re.compile(r"^-\s+\d{4}-\d{2}-\d{2}\s+·\s+(\S+)")

# Correction tokens that mark a ``## Walls`` bullet as a *correction* row.
_RE_CORRECTION = re.compile(r"\b(?:corrected|superseded)\b", re.IGNORECASE)

# A "not a wall" negation — the AVAILABLE polarity signal on a Walls correction.
_RE_NOT_A_WALL = re.compile(r"not\s+a\s+wall", re.IGNORECASE)

AVAILABLE = "available"
BLOCKED = "blocked"

# Named WALL_LEDGER_DISAGREE_KIND, not FINDING_KIND: the dist concatenates every
# engine module into one namespace, so a second top-level ``FINDING_KIND`` would
# collide and red ``test_check_namespace``. The value is the finding kind.
WALL_LEDGER_DISAGREE_KIND = "wall-ledger-disagree"


def _is_walls_section(header: str | None) -> bool:
    """True when a ``## `` header denotes the Walls section (not Capabilities,
    not Append log)."""
    if header is None:
        return False
    low = header.lower()
    return "wall" in low and "capabilit" not in low and "append" not in low


def _is_appendlog_section(header: str | None) -> bool:
    """True when a ``## `` header denotes the Append-log section."""
    return header is not None and "append log" in header.lower()


def _is_correction_row(text: str) -> bool:
    """A Walls bullet counts as a *correction* row if it carries a correction
    token or a ``not a wall`` negation (which is itself a correction of the
    default wall assumption)."""
    return bool(_RE_CORRECTION.search(text) or _RE_NOT_A_WALL.search(text))


def _wla_iter_bullets(text: str):
    """Yield ``(section_header, bullet_text)`` for every column-0 ``- `` bullet,
    tracking the enclosing ``## `` section. Continuation (indented / non-bullet)
    lines fold into the bullet until the next bullet, blank line, or header — so
    a multi-line ledger row is one logical bullet."""
    section: str | None = None
    buf: list[str] | None = None
    for raw in text.splitlines():
        header = _WLA_RE_SECTION.match(raw)
        if header is not None:
            if buf is not None:
                yield section, "\n".join(buf)
                buf = None
            section = header.group(1)
            continue
        if raw.startswith("- "):
            if buf is not None:
                yield section, "\n".join(buf)
            buf = [raw]
            continue
        if buf is not None:
            if raw.strip() == "" or raw.startswith("#"):
                yield section, "\n".join(buf)
                buf = None
            else:
                buf.append(raw)
    if buf is not None:
        yield section, "\n".join(buf)


def check_wall_ledger_agreement(target: Path, config=None) -> list[Finding]:
    """Return advisory findings where a ``## Walls`` correction and the newest
    same-capability ``## Append log`` entry disagree on a capability's status.

    Advisory only — the caller wires this on the ``posture="advisory"`` path and
    NEVER counts it toward the exit code. Input-gated + fail-open: an absent or
    unreadable ``docs/CAPABILITIES.md`` yields no finding. ``config`` is accepted
    for signature parity with the other advisory checks; unused today."""
    ledger = target / _WLA_CAPABILITIES_RELPATH
    if not ledger.is_file():
        return []  # input-gated: no ledger to scan
    try:
        text = ledger.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable ledger is not a verdict

    bullets = list(_wla_iter_bullets(text))
    findings: list[Finding] = []
    for family_name, family_re in _FAMILIES:
        # (a) newest append-log verdict for the family (topmost = newest first).
        appendlog_verdict: str | None = None
        for section, bullet in bullets:
            if not _is_appendlog_section(section):
                continue
            head = _WLA_RE_APPENDLOG.match(bullet.splitlines()[0])
            if head is None:
                continue
            if not family_re.search(bullet):
                continue
            type_token = head.group(1).lower()
            appendlog_verdict = (
                AVAILABLE if type_token.startswith("capabilit") else BLOCKED
            )
            break  # newest-first: the first match encountered is the newest
        if appendlog_verdict is None:
            continue  # nothing in the append log to cross-check

        # (b) Walls-correction verdict for the family.
        walls_verdict: str | None = None
        for section, bullet in bullets:
            if not _is_walls_section(section):
                continue
            if not family_re.search(bullet):
                continue
            if not _is_correction_row(bullet):
                continue
            walls_verdict = AVAILABLE if _RE_NOT_A_WALL.search(bullet) else BLOCKED
            break
        if walls_verdict is None:
            continue  # no Walls correction row for this family

        if walls_verdict != appendlog_verdict:
            findings.append(
                Finding(
                    _WLA_CAPABILITIES_RELPATH,
                    WALL_LEDGER_DISAGREE_KIND,
                    f"capability '{family_name}' disagrees across the ledger: the "
                    f"## Walls correction reads {walls_verdict!r} but the newest "
                    f"## Append log entry reads {appendlog_verdict!r} — reconcile "
                    "the two (a correction must land in both places, or the ledger "
                    "contradicts itself).",
                ),
            )
    return findings
