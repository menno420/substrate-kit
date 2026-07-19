"""Un-groomed-idea counter advisory — warn-only, NEVER exit-affecting.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md S3 (this PR).
Sibling of the R5/R7/R8/R11 advisories on the same posture="advisory" seam.

Why this exists: every session ends by adding a 💡 session idea to its
``.sessions/`` card (Q-0089). Those ideas are meant to be periodically GROOMED —
swept out of the session logs and routed into the idea backlog by a groom pass,
which lands a ``docs/planning/*groom*.md`` doc. Between groom passes the 💡 lines
accumulate on cards. A session that claims the backlog is "DRY" while un-groomed
💡 ideas still sit on cards newer than the last groom doc is making a FALSE
claim — the ideas have not been groomed, they have just not been counted.

What it does: (a) finds the newest groom doc under ``docs/planning/`` (a file
whose name contains ``groom``, dated by the ``YYYY-MM-DD`` prefix in its
filename; newest date wins); (b) finds session cards under ``.sessions/`` whose
filename date is STRICTLY newer than that groom doc's date; (c) counts the lines
containing the ``💡`` character across those newer cards (each 💡 line = one
un-groomed session idea); (d) if the count is > 0, returns ONE advisory naming
the count and the newest groom doc, so a "backlog dry" claim can't be made
falsely. If nothing is newer, returns [].

Date is parsed from the FILENAME prefix, not file contents or mtime: cards and
groom docs are date-prefixed by convention (``2026-07-19-<slug>.md``), and a
fresh checkout flattens every mtime to checkout time, so a filename date is the
only stable ordering key (decide-and-flag — same reasoning check_model_line uses
for name-order-is-date-order). Only the top level of ``.sessions/`` is scanned
(cards live there directly; no recursion into subpaths) — contained + reversible.

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_recipe_applies_when / check_fastlane_symmetry. NOT in STRICT_SUBCHECKS
— un-groomed ideas are a nudge to run a groom pass, not a defect to fail an
adopter on. Input-gated + fail-open: no ``.sessions/`` dir, no groom doc found,
or an unreadable file yields nothing. Never raises. Stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

_PLANNING_RELDIR = "docs/planning"
_SESSIONS_RELDIR = ".sessions"

# The 💡 character — one occurrence on a line marks that line as an un-groomed
# session idea (the Q-0089 session-idea flag).
_IDEA_CHAR = "\N{ELECTRIC LIGHT BULB}"  # 💡

# The leading ``YYYY-MM-DD`` date prefix a card / groom doc filename carries by
# convention. Group 1 is the ISO date string; string comparison of ISO dates is
# chronological, so no datetime parse is needed.
_RE_DATE_PREFIX = re.compile(r"^(\d{4}-\d{2}-\d{2})")

# Named UNGROOMED_IDEAS_KIND (not a bare FINDING_KIND) — the dist concatenates
# every engine module into one namespace, so a second top-level FINDING_KIND
# would collide. The value is the finding kind.
UNGROOMED_IDEAS_KIND = "ungroomed-ideas"


def _filename_date(path: Path) -> str | None:
    """The ISO ``YYYY-MM-DD`` prefix of ``path``'s filename, or None without one."""
    match = _RE_DATE_PREFIX.match(path.name)
    return match.group(1) if match else None


def check_ungroomed_ideas(target: Path, config=None) -> list[Finding]:
    """Advisory: count 💡 session-idea lines on cards newer than the newest groom doc.

    Advisory only — the caller wires this on posture="advisory" and never counts
    it toward the exit code. Input-gated + fail-open. config accepted for
    signature parity with the other advisory checks; unused today."""
    sessions_dir = target / _SESSIONS_RELDIR
    if not sessions_dir.is_dir():
        return []  # input-gated: no session cards shipped here

    planning_dir = target / _PLANNING_RELDIR
    if not planning_dir.is_dir():
        return []  # input-gated: no planning dir → no groom docs to date against

    # (a) newest groom doc by filename date. A groom doc is any docs/planning/
    # *.md whose name contains "groom" and carries a parseable date prefix.
    groom_dates: list[tuple[str, str]] = []  # (iso_date, filename)
    for path in sorted(planning_dir.glob("*groom*.md")):
        date = _filename_date(path)
        if date is not None:
            groom_dates.append((date, path.name))
    if not groom_dates:
        return []  # fail open: no dated groom doc → nothing to measure against
    newest_groom_date, newest_groom_name = max(groom_dates)

    # (b) session cards strictly newer than the newest groom doc's date, and
    # (c) count 💡 lines across them.
    idea_lines = 0
    for path in sorted(sessions_dir.glob("*.md")):
        if path.name == "README.md":
            continue
        card_date = _filename_date(path)
        if card_date is None or card_date <= newest_groom_date:
            continue  # not dated, or not strictly newer than the groom doc
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable card is not a verdict
        idea_lines += sum(1 for line in text.splitlines() if _IDEA_CHAR in line)

    # (d) one advisory when un-groomed idea lines exist; silence otherwise.
    if idea_lines == 0:
        return []
    plural = "s" if idea_lines != 1 else ""
    return [
        Finding(
            f"{_SESSIONS_RELDIR}/",
            UNGROOMED_IDEAS_KIND,
            f"{idea_lines} un-groomed \N{ELECTRIC LIGHT BULB} idea line{plural} on "
            f"session card{plural} newer than the newest groom doc "
            f"({_PLANNING_RELDIR}/{newest_groom_name}) — a 'backlog dry' claim "
            "would be false; run a groom pass to route these ideas into the "
            "backlog.",
        ),
    ]
