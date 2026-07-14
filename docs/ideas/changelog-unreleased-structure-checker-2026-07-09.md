---
state: promoted
origin: lab
shipped_pr: 351
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-14
outcome: shipped
---

# CHANGELOG `[Unreleased]` structure checker (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (run close-out 2026-07-09) → promoted → **shipped**
> (PR #351, 2026-07-14 — the in-PR flip convention; merged_date is the
> anticipated park-green date). **Origin:** lab — the docs-drift audit
> found the same defect made twice independently in one run.

**One line:** a cheap kit-quality checker that validates the `[Unreleased]`
section's keep-a-changelog shape — each of
`Added/Changed/Deprecated/Removed/Fixed/Security` appears **at most once**,
in canonical order, with no bullet above the first heading — because two
sessions in one run independently broke it the same way.

## Evidence (why this is friction → guard, not ceremony)

The run close-out's docs-drift audit (2026-07-09) found the failure **twice,
independently**:

1. **KL-4 (PR #14)** inserted its `### Fixed` block *between* its own Added
   entries and the older KL-3/KL-2 Added entries — stranding six Added
   entries under `### Fixed` on main (fixed at the close-out).
2. **The bench-tree PR #17** does the same thing in its patch: its
   `### Fixed` (enabler label race) lands *above* the pre-existing
   Added entries, so merging it re-creates the defect (flagged on the #17
   thread; the post-blessing session fixes it in one line).

Two independent sessions making the identical mistake is a **pattern**: the
house habit of inserting a PR's entries newest-first at the top of the
section collides with keep-a-changelog's grouped-by-type shape, and nothing
catches it — `check --strict` covers docs hygiene but not CHANGELOG
structure, and the release workflow only checks that a version *has* a
section.

## Guard recipe (anchors for the shipping session)

- **Checker:** `scripts/check_changelog_structure.py` (stdlib, ~60 lines) —
  parse the `## [Unreleased]` block up to the next `## [` heading; enforce
  (a) only known `### ` headings, (b) each at most once, (c) canonical
  keep-a-changelog order, (d) no list item before the first `### `.
- **Wire:** one step in `ci.yml` `kit-quality`, next to
  `check_idea_index.py` / `check_program_law.py`.
- **Test:** `tests/test_check_changelog_structure.py` — green on the real
  file, red on a synthetic mid-section `### Fixed`, red on a duplicate
  heading.
- **Consider:** graduating it into the engine's docs checks later so it
  travels to consumers; script-first is the cheap, provable start
  (Q-0105-class: adopt with provenance, delete if it proves unreliable).

## Routing

Quick-win lane — a groomed-ideas increment ships checker + test + CI step in
one small PR. **Sequencing note:** land it AFTER PR #17 merges and its
heading-order touch-up is applied, so the checker is born green on main.
