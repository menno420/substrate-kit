"""The seat-digest render surface (grounded-skills plan §7 slice 6, §8 Q3=A).

Why + provenance: the grounded-skills program's slice 6
(``docs/planning/2026-07-12-grounded-skills-program.md`` §7.6, owner default
Q3=A) makes the kit the single source for the fleet-manager seat prompts'
skill-index and WALLS content — the drift class it kills (a seat prompt
contradicting kit truth) is the hardening report's "highest-leverage single
change". Fleet-manager's prompt system v3.3 consumes committed files by tree
scan + fence extraction + byte match (its ``regen_b_files.py``
``--check-registry`` model), never by executing kit code — so the kit ships
ONE generated planted doc, ``docs/seat-digest.md``, carrying two
fence-marked blocks (``engine.grammar``'s ``substrate-kit:skills-digest`` /
``substrate-kit:walls-digest`` prefix pairs):

- **Skills digest** — one line per registered skill, rendered FROM the
  :data:`engine.skills.skills.SKILLS` list (the same source that emits the
  skills — the "render from ONE source" rule), pointer to the full index.
- **Walls digest** — the capability ledger's verified walls, filtered
  mechanically by venue token (Project-seat default
  ``autonomous-project`` + ``any``; the slice-5 venue column makes this a
  filter, not an editorial pass), pointer to the full ledger.

Design invariants: **digest + pointer, never inline** (plan §2 — the
consuming seat pastes sit at 7,943–7,998 of 8,000 chars); every block stays
within :data:`engine.grammar.SEAT_DIGEST_BLOCK_BUDGET` by truncating rows
into an explicit "+N more — read the source" overflow line, never by
silently overflowing. **No third copy** (plan §4.2e): the adopter's
``docs/CAPABILITIES.md`` ledger is the seat-local source of truth; this doc
is a DERIVED RENDER of it (regenerated — by adopt, upgrade, or
``bootstrap.py seat-digest`` — never edited, never a copy of record);
fleet-manager's ``docs/capabilities.md`` master is the fleet aggregation
point; no third authored copy is ever minted.

Layering: below ``adopt.py`` on purpose (adopt plants the doc, upgrade
refreshes it, the checker byte-compares it — all import from here; this
module imports only grammar/skills/config). Pure stdlib.
"""

from __future__ import annotations

from pathlib import Path

from engine.grammar import (
    CAPABILITY_LOG_LINE_RE,
    CAPABILITY_SEED_BEGIN_PREFIX,
    CAPABILITY_SEED_END_PREFIX,
    CAPABILITY_VENUE_SHAPE_RE,
    CAPABILITY_VENUE_TOKENS,
    SEAT_DIGEST_BLOCK_BUDGET,
    SEAT_DIGEST_DEFAULT_VENUES,
    SKILLS_DIGEST_BEGIN,
    SKILLS_DIGEST_END,
    WALLS_DIGEST_END,
    WALLS_DIGEST_VENUES_RE,
    walls_digest_begin_marker,
)
from engine.lib.config import Config
from engine.skills.skills import SKILLS

# Max characters for one digest row (unwrapped, before the truncation
# ellipsis) — compact enough that ~8 rows + fences + pointer stay inside the
# block budget, long enough to keep a wall's workaround arrow readable.
_ROW_LIMIT = 160

# Readability floor for the ADAPTIVE skills-description clip (see
# ``_adaptive_skill_clip``): below ~40 chars a truncated description reads
# worse than no description, so rows drop to name-only before any skill NAME
# is ever dropped — the digest's whole job is "these procedures exist, don't
# improvise", and the pointer line carries the detail.
_SKILL_CLIP_FLOOR = 40

_WALLS_HEADING = "## Walls"
_LEDGER_APPEND_LOG_HEADING = "## Append log"


def seat_digest_relpath(config: Config) -> str:
    """Return the planted seat-digest relpath under the host's docs root."""
    return f"{config.docs_root}/seat-digest.md"


def _truncate(text: str, limit: int = _ROW_LIMIT) -> str:
    """Collapse whitespace and word-boundary-truncate ``text`` to ``limit``."""
    flat = " ".join(text.split())
    if len(flat) <= limit:
        return flat
    cut = flat[: limit - 1].rsplit(" ", 1)[0].rstrip(" ·—-")
    return cut + "…"


def _fit_rows(
    header: list[str],
    rows: list[str],
    footer: list[str],
    more_pointer: str,
) -> str:
    """Compose a fenced block, truncating ``rows`` into the budget.

    The budget is enforced mechanically (never trusted to content size): rows
    are added while the assembled block stays within
    :data:`SEAT_DIGEST_BLOCK_BUDGET`; the remainder collapses into one
    "+N more" overflow line pointing at the source doc — digest + pointer,
    never inline (plan §2).
    """

    def compose(kept: list[str], extra: list[str]) -> str:
        return "\n".join(header + kept + extra + footer)

    for drop in range(len(rows) + 1):
        kept = rows[: len(rows) - drop]
        extra = (
            [f"- …plus {drop} more — {more_pointer}"] if drop else []
        )
        block = compose(kept, extra)
        if len(block) <= SEAT_DIGEST_BLOCK_BUDGET:
            return block
    return compose([], [f"- …plus {len(rows)} more — {more_pointer}"])


def _skill_rows(skills: list[dict], clip: int | None) -> list[str]:
    """Render one digest row per skill at ``clip`` (``None`` → name-only)."""
    if clip is None:
        return [f"- `{skill['name']}`" for skill in skills]
    return [
        f"- `{skill['name']}` — {_truncate(skill['description'], clip)}"
        for skill in skills
    ]


def _adaptive_skill_clip(
    skills: list[dict],
    header: list[str],
    footer: list[str],
) -> int | None:
    """Compute the description clip that fits EVERY skill in the budget.

    Replaces the hand-ratcheted constant this module carried through
    2026-07-13 (120 → 85 → 72, one manual lowering per new skill — every
    registry addition was a latent test failure until a session paid the
    ratchet toll again). Instead: scan down from the row ceiling
    (:data:`_ROW_LIMIT`) for the LARGEST clip where the assembled block —
    header + all rows + footer — stays within
    :data:`SEAT_DIGEST_BLOCK_BUDGET`, floored at :data:`_SKILL_CLIP_FLOOR`;
    if even the floor overflows, return ``None`` → name-only rows (drop
    descriptions before ever dropping a name). Pure function of its inputs,
    so the render stays deterministic and byte-reproducible. The descending
    linear scan is deliberate: ~120 candidate renders is negligible, and it
    needs no monotonicity assumption about word-boundary truncation.
    """
    for clip in range(_ROW_LIMIT, _SKILL_CLIP_FLOOR - 1, -1):
        block = "\n".join(header + _skill_rows(skills, clip) + footer)
        if len(block) <= SEAT_DIGEST_BLOCK_BUDGET:
            return clip
    return None


def skills_digest_block(
    docs_root: str = "docs",
    skills: list[dict] | None = None,
) -> str:
    """Render the fenced skills-index digest block from :data:`SKILLS`.

    One row per registered skill — name + when-to-reach-for-it one-liner,
    never the grounds column (that detail is the index's job; the digest's
    job is "these procedures exist, don't improvise"). The description clip
    is COMPUTED per render (``_adaptive_skill_clip``): every skill name
    survives within the block budget at the widest clip that fits, degrading
    to name-only rows below the readability floor — no manual ratchet.
    Deterministic given the skills list. ``skills`` defaults to the
    registered :data:`SKILLS` (parameterized for growth-proof tests).
    """
    if skills is None:
        skills = SKILLS
    index_path = f"{docs_root}/SKILLS.md"
    header = [SKILLS_DIGEST_BEGIN, "## Skills digest", ""]
    footer = [
        "",
        f"Full index (grounds + capabilities): `{index_path}` — the source "
        "this block derives from.",
        SKILLS_DIGEST_END,
    ]
    rows = _skill_rows(skills, _adaptive_skill_clip(skills, header, footer))
    # _fit_rows stays as the LAST safety net: if even name-only rows overflow
    # (a registry so large the budget cannot name every skill), the explicit
    # "+N more" pointer line still beats a silent overflow.
    return _fit_rows(header, rows, footer, f"read `{index_path}`.")


def _unwrapped_bullets(lines: list[str]) -> list[str]:
    """Join ``- `` bullets with their indented continuation lines."""
    bullets: list[str] = []
    for line in lines:
        if line.startswith("- "):
            bullets.append(line[2:].strip())
        elif bullets and line.startswith((" ", "\t")) and line.strip():
            bullets[-1] += " " + line.strip()
    return bullets


def _section_lines(lines: list[str], heading: str) -> list[str]:
    """Return the lines under ``heading`` up to the next ``## ``/fence-END."""
    out: list[str] = []
    inside = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith(heading):
            inside = True
            continue
        if inside and (
            stripped.startswith("## ")
            or stripped.startswith(CAPABILITY_SEED_END_PREFIX)
        ):
            break
        if inside:
            out.append(line)
    return out


def _seed_wall_rows(ledger_text: str) -> list[tuple[str, str]]:
    """Return ``(venue, text)`` rows from the seed fence's Walls section.

    Seed rows are `` - `venue` · finding … — LAST-VERIFIED: date`` bullets
    (possibly wrapped); the freshness stamp is stripped for the digest (the
    ledger keeps it — the digest points there). A bullet without a leading
    backticked venue token fails open as venue ``any`` (the ledger's own
    backward-compatibility rule).
    """
    lines = ledger_text.splitlines()
    begin = next(
        (
            i
            for i, line in enumerate(lines)
            if line.strip().startswith(CAPABILITY_SEED_BEGIN_PREFIX)
        ),
        None,
    )
    if begin is None:
        return []
    rows: list[tuple[str, str]] = []
    for bullet in _unwrapped_bullets(_section_lines(lines[begin:], _WALLS_HEADING)):
        venue = "any"
        text = bullet
        if bullet.startswith("`"):
            token, sep, rest = bullet[1:].partition("`")
            if sep and token in CAPABILITY_VENUE_TOKENS:
                venue = token
                text = rest.lstrip(" ·")
        stamp = text.find("— LAST-VERIFIED:")
        if stamp != -1:
            text = text[:stamp].rstrip()
        rows.append((venue, text))
    return rows


def _append_wall_rows(ledger_text: str) -> list[tuple[str, str]]:
    """Return ``(venue, text)`` rows for ``wall``-tagged append-log entries.

    Consumes the grammar's taught line format (``- YYYY-MM-DD · tag ·
    <venue> · finding · evidence · workaround``); a legacy five-field line
    without a venue token reads as venue ``any`` and is never dropped
    (the pinned backward-compatibility contract). ``capability`` entries are
    not walls and stay out of this digest.
    """
    lines = ledger_text.splitlines()
    heading = next(
        (
            i
            for i, line in enumerate(lines)
            if line.strip().startswith(_LEDGER_APPEND_LOG_HEADING)
        ),
        None,
    )
    if heading is None:
        return []
    rows: list[tuple[str, str]] = []
    for bullet in _unwrapped_bullets(lines[heading:]):
        match = CAPABILITY_LOG_LINE_RE.match(f"- {bullet}")
        if not match:
            continue
        fields = [f.strip() for f in match.group(2).split(" · ")]
        if not fields or fields[0] != "wall":
            continue
        rest = fields[1:]
        venue = "any"
        if (
            rest
            and CAPABILITY_VENUE_SHAPE_RE.match(rest[0])
            and rest[0] in CAPABILITY_VENUE_TOKENS
        ):
            venue = rest[0]
            rest = rest[1:]
        if rest:
            rows.append((venue, " · ".join(rest)))
    return rows


def walls_digest_block(
    ledger_text: str | None,
    venues: tuple[str, ...] = SEAT_DIGEST_DEFAULT_VENUES,
    docs_root: str = "docs",
) -> str:
    """Render the fenced venue-filtered walls digest block.

    ``ledger_text`` is the adopter's planted ``docs/CAPABILITIES.md`` — the
    seat-local source of truth this block derives from (``None`` renders an
    honest placeholder, never a guess). Filtering is mechanical: a row ships
    when its venue token is in ``venues`` (seed fence Walls rows + append-log
    ``wall`` entries; legacy venue-less lines count as ``any``).
    """
    ledger_path = f"{docs_root}/CAPABILITIES.md"
    header = [
        walls_digest_begin_marker(venues),
        f"## Walls digest (venues: {', '.join(venues)})",
        "",
    ]
    if ledger_text is None:
        rows = [
            f"- (no capability ledger found at `{ledger_path}` — walls "
            "unknown; plant the ledger, then regenerate this digest)",
        ]
    else:
        rows = [
            f"- `{venue}` · {_truncate(text)}"
            for venue, text in _seed_wall_rows(ledger_text)
            + _append_wall_rows(ledger_text)
            if venue in venues
        ]
        if not rows:
            rows = [f"- (no walls recorded for these venues in `{ledger_path}`)"]
    footer = [
        "",
        f"Full ledger (all venues, evidence, freshness): `{ledger_path}` — "
        "the seat-local source of truth; append findings THERE, never here.",
        WALLS_DIGEST_END,
    ]
    return _fit_rows(header, rows, footer, f"read `{ledger_path}`.")


def walls_digest_venues(text: str) -> tuple[str, ...]:
    """Parse the venue filter off a committed doc's walls-digest BEGIN line.

    Regens and drift checks must re-render with the SAME venues the
    committed doc chose; an absent/unparseable marker falls back to the
    Project-seat default (never a crash, never a silent venue reset to
    something the doc did not say).
    """
    match = WALLS_DIGEST_VENUES_RE.search(text)
    if not match:
        return SEAT_DIGEST_DEFAULT_VENUES
    venues = tuple(
        token
        for token in match.group(1).split(",")
        if token in CAPABILITY_VENUE_TOKENS
    )
    return venues or SEAT_DIGEST_DEFAULT_VENUES


def seat_digest_document(
    project_name: str,
    ledger_text: str | None,
    venues: tuple[str, ...] = SEAT_DIGEST_DEFAULT_VENUES,
    docs_root: str = "docs",
) -> str:
    """Compose the full ``docs/seat-digest.md`` text (deterministic).

    Both fenced blocks plus the two contracts a consumer needs stated where
    the artifact lives: the machine extraction contract (the three
    fence-prefix pairs) and the no-third-copy deferral chain (plan §4.2e).
    No dates, no environment reads — the render is a pure function of the
    SKILLS list, the ledger text, the venue filter, and ``project_name``,
    so a byte-compare drift guard is meaningful.
    """
    index_path = f"{docs_root}/SKILLS.md"
    ledger_path = f"{docs_root}/CAPABILITIES.md"
    return "\n".join(
        [
            f"# {project_name} — seat digest",
            "",
            "> **Status:** `reference`",
            ">",
            "> Generated by substrate-kit — a **derived render**, never a "
            "copy of record.",
            f"> Sources: `{index_path}` (skill index) + `{ledger_path}` "
            "(capability ledger).",
            "> NEVER edit this file: regenerate with `python3 bootstrap.py "
            "seat-digest`",
            "> (adopt and upgrade also refresh it). Hand edits are drift by "
            "definition.",
            "",
            "## What this is",
            "",
            "The seat-prompt-feeding digest (grounded-skills plan §7 slice "
            "6): the two",
            "fence-marked blocks below are canonical, machine-extractable "
            "renders of this",
            "repo's registered skills and its venue-relevant verified walls "
            "— sized for",
            "prompt budgets that have no headroom. **Digest + pointer, "
            "never inline**:",
            "each block ends with a pointer to the full source doc.",
            "",
            skills_digest_block(docs_root),
            "",
            walls_digest_block(ledger_text, venues, docs_root),
            "",
            "## Extraction contract — the machine interface",
            "",
            "Consumers (fleet-manager's seat-prompt regen tool above all) "
            "extract blocks",
            "by fence-prefix match + byte compare — never by executing kit "
            "code, never by",
            "parsing prose. The contract is the three HTML-comment prefix "
            "pairs (match the",
            "PREFIX only; trailing marker wording may evolve without "
            "orphaning a fence):",
            "",
            "| block | BEGIN prefix | END prefix | lives in |",
            "|---|---|---|---|",
            "| skills digest | `<!-- substrate-kit:skills-digest BEGIN` | "
            "`<!-- substrate-kit:skills-digest END` | this file |",
            "| walls digest | `<!-- substrate-kit:walls-digest BEGIN` | "
            "`<!-- substrate-kit:walls-digest END` | this file |",
            "| capability seed | `<!-- substrate-kit:capability-seed BEGIN` "
            f"| `<!-- substrate-kit:capability-seed END` | `{ledger_path}` |",
            "",
            "The walls-digest BEGIN marker carries its venue filter "
            "(`venues=<tokens>`);",
            "regens preserve it. The bytes between a BEGIN/END pair are the "
            "canonical",
            "block — a consumer's byte-match drift guard compares against "
            "exactly them.",
            "",
            "## No third copy — which record defers to which",
            "",
            f"1. **`{ledger_path}` (this repo)** — the seat-local source of "
            "truth for",
            "   capabilities and walls; sessions append verified findings "
            "there.",
            "2. **This file** — a derived render of that ledger (walls) and "
            "the kit's",
            "   `SKILLS` list (skills). Regenerated, never edited; never a "
            "copy of record.",
            "3. **fleet-manager `docs/capabilities.md`** — the fleet "
            "aggregation point;",
            "   cross-repo findings are consolidated there by the manager.",
            "",
            "No third authored copy is ever minted (grounded-skills plan "
            "§4.2e). A prompt",
            "block, a seat paste, or any downstream copy is a RENDER of "
            "step 2 and is",
            "regenerated from it — divergence between them is drift to fix "
            "at the source,",
            "never content to merge back by hand.",
            "",
        ],
    )


def seat_digest_text(
    root: Path,
    config: Config,
    context: dict[str, str],
    venues: tuple[str, ...] = SEAT_DIGEST_DEFAULT_VENUES,
) -> str:
    """Render the seat-digest doc for ``root`` (reads the planted ledger).

    The ONE render path every surface shares — adopt's plant, upgrade's
    refresh, the ``seat-digest`` CLI regen, and the drift checker's fresh
    render all call this, so "planted file == fresh render" is a meaningful
    byte contract. A missing/unreadable ledger renders the honest
    placeholder (fail open, never a crash).
    """
    ledger_path = root / config.docs_root / "CAPABILITIES.md"
    try:
        ledger_text: str | None = ledger_path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        ledger_text = None
    project_name = context.get("project_name") or root.name
    return seat_digest_document(
        project_name,
        ledger_text,
        venues,
        config.docs_root,
    )
