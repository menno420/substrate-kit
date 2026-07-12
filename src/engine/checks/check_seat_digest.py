"""check_seat_digest — seat-digest drift guard (grounded-skills slice 6, §7.6).

Why + provenance: slice 6's accept criterion is a ``--check-registry``-style
drift guard "proving prompt blocks equal kit truth"
(``docs/planning/2026-07-12-grounded-skills-program.md`` §7.6, §8 Q3=A).
Fleet-manager's seat-prompt regen consumes the planted
``docs/seat-digest.md`` by fence extraction + byte match — so the kit-side
guard is a byte compare of the committed doc against a fresh
:func:`engine.seatdigest.seat_digest_text` render (the ONE render path
adopt/upgrade/CLI share), re-rendered with the committed doc's own venue
filter. A stale digest means every downstream seat prompt ships yesterday's
walls or a retired skill; the finding names the exact regenerate command.
Added 2026-07-12 (grounded-skills slice 6, §8 Q2=B advisory-first).
Reliability (PL-008): UNVERIFIED — confirm its findings against ground
truth a few times across sessions before trusting it; **delete this if it
proves unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** (§8 Q2=B: no CI-red
until proven; graduation is a later, deliberate step) — the same
nudge-never-door contract as ``check_claims`` / ``check_skill_grounds`` /
``check_capability_xref``. Input-gated: engages only when the planted
digest exists (a bare or pre-slice-6 tree adds nothing); unreadable files
fail open (no verdict). Pure stdlib, no ``subprocess`` (§3.2) — the fresh
render is a pure function of tree content.

What it flags:

- ``seat-digest-stale`` — the committed doc's bytes differ from a fresh
  render (ledger appends, skill-set changes, or a hand edit — the doc is a
  derived render either way). Fix: ``python3 bootstrap.py seat-digest``.
- ``seat-digest-over-budget`` — a fenced block exceeds
  :data:`engine.grammar.SEAT_DIGEST_BLOCK_BUDGET`. A fresh render can never
  overflow (the renderer truncates into a "+N more" pointer row), so this
  only fires on hand-grown blocks — but it is the one drift class that
  breaks the downstream 8,000-char seat-prompt budget outright, so it gets
  its own sharper finding on top of the stale nudge.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.checks.check_docs import Finding
from engine.grammar import (
    SEAT_DIGEST_BLOCK_BUDGET,
    SKILLS_DIGEST_BEGIN_PREFIX,
    SKILLS_DIGEST_END_PREFIX,
    WALLS_DIGEST_BEGIN_PREFIX,
    WALLS_DIGEST_END_PREFIX,
)
from engine.seatdigest import (
    seat_digest_relpath,
    seat_digest_text,
    walls_digest_venues,
)


def _fenced_block(text: str, begin_prefix: str, end_prefix: str) -> str | None:
    """Return the fenced block (markers inclusive), or None when unmatched.

    Prefix-matched line-anchored, exactly like the upgrade refresher's
    ``_capability_fence`` — an unmatched fence is no verdict, never a guess.
    """
    lines = text.splitlines(keepends=True)
    begin = end = None
    for i, line in enumerate(lines):
        stripped = line.strip()
        if begin is None and stripped.startswith(begin_prefix):
            begin = i
        elif begin is not None and stripped.startswith(end_prefix):
            end = i
            break
    if begin is None or end is None:
        return None
    return "".join(lines[begin : end + 1])


def check_seat_digest(
    target: Path,
    config: Any,
    *,
    context: dict[str, str] | None = None,
) -> list[Finding]:
    """Return advisory drift findings for the planted seat-digest doc.

    ``context`` is the caller's render context (``build_context`` output);
    only ``project_name`` matters to the render. Advisory by contract:
    callers must NEVER count these findings toward an exit code (§8 Q2=B —
    see module docstring).
    """
    rel = seat_digest_relpath(config)
    path = target / rel
    if not path.is_file():
        return []
    try:
        text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable file is not a verdict
    findings: list[Finding] = []
    fresh = seat_digest_text(
        target,
        config,
        context or {},
        venues=walls_digest_venues(text),
    )
    if text != fresh:
        findings.append(
            Finding(
                rel,
                "seat-digest-stale",
                "committed digest differs from a fresh render of its "
                "sources (skill index + capability ledger) — downstream "
                "seat prompts extract these bytes, so drift here ships "
                "stale walls/skills fleet-wide; regenerate with "
                "`python3 bootstrap.py seat-digest` (never hand-edit — it "
                "is a derived render).",
            ),
        )
    for label, begin_prefix, end_prefix in (
        ("skills", SKILLS_DIGEST_BEGIN_PREFIX, SKILLS_DIGEST_END_PREFIX),
        ("walls", WALLS_DIGEST_BEGIN_PREFIX, WALLS_DIGEST_END_PREFIX),
    ):
        block = _fenced_block(text, begin_prefix, end_prefix)
        if block is not None and len(block) > SEAT_DIGEST_BLOCK_BUDGET:
            findings.append(
                Finding(
                    rel,
                    "seat-digest-over-budget",
                    f"the {label}-digest block is {len(block)} chars "
                    f"(budget {SEAT_DIGEST_BLOCK_BUDGET}) — the consuming "
                    "seat-prompt pastes have no headroom (digest + "
                    "pointer, never inline); regenerate with "
                    "`python3 bootstrap.py seat-digest` (a fresh render "
                    "truncates into a '+N more' pointer row).",
                ),
            )
    return findings
