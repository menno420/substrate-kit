# Session 2026-07-09 — PL-004 amendment: the `feature build` task class

> **Status:** `complete` *(PR #22 — discuss-first, `do-not-automerge`,
> deliberately LEFT OPEN for owner review: the merge is the ratification.)*

**Scope (agent-queue item from the run close-out):** the discuss-first
ruling PR that adds a 9th task class **`feature build`** to the Q-0248/PL-004
taxonomy. Provenance implemented, not paraphrased: friction issue #15
report 3 + its KL-4 triage disposition (routed discuss-first, recommended
shape = a 9th class) + `docs/ideas/feature-build-task-class-2026-07-09.md`
(option 1 of its two candidate fixes).

## What shipped (one coherent PR, all surfaces)

- **`docs/program/rulings.md` [PL-010]** — a new decided block that
  **amends (extends) PL-004, never supersedes it**: superseding would force
  restating the whole three-layer discipline to change one list, and the
  checker requires a `superseded` block to name `superseded-by` while the
  register stays append-only — a fresh sequential PL-010 with an explicit
  `scope: amends, does not supersede` line is the legal shape
  (`check_program_law.py`: heading grammar · gap-free monotonic IDs ·
  provenance-required · status enum — all green with this shape).
- **`src/engine/loop/telemetry.py`** — `TASK_CLASSES` gains the exact
  string **`feature build`** (9th, appended); the off-taxonomy advisory now
  derives its count from `len(TASK_CLASSES)` (the count was hardcoded
  prose); `dist/bootstrap.py` regenerated + byte-pinned.
- **Tests** — the pinning test asserts the 9-tuple verbatim
  (`test_task_classes_are_the_nine_pl004_classes_verbatim`); the advisory
  test tracks the new wording; `test_real_register_has_the_founding_census`
  now allows appended amendments while still requiring gap-free sequential
  IDs and the founding Q-provenance census.
- **`telemetry/allocation-ladder.md`** — `feature build` row added
  **observe-first with NO seeded tier** (PL-005: telemetry before defaults;
  B2 data seeds it) + a revision-log line marking it a taxonomy amendment,
  not a data revision. `telemetry/README.md` lists the 9 classes.
- **B4 bookkeeping** — idea frontmatter `state: routed → promoted`
  (`outcome: open` until the owner merge flips it `shipped`); ideas README
  updated; `docs/current-state.md`: moved from agent queue to **owner gate
  2, beside #17**; CHANGELOG `[Unreleased]` Added entry (placed at the
  bottom of Added, away from #17's pending insert hunk).

## Run report

- **📊 Model:** fable-5 · high · feature build
  *(the class this PR mints, deliberately its first row — net-new
  capability across register + engine + ladder; nearest-neighbor before
  this ruling would have been the exact mislabel the ruling ends).*

### ⚑ Self-initiated (decide-and-flag, PL-001)

1. **Census pinning test loosened** to "founding 9 + gap-free appended
   amendments" — the old `range(1, 10)` hard-pin would red every future
   lawful amendment; goal-approves-path, but it edits a guard, so flagged.
2. **Advisory count derived from `len(TASK_CLASSES)`** — adjacent
   count-drift root-caused rather than bumping 8 → 9 in prose.
3. **This session self-classified with the class it mints** (first
   `feature build` row) — self-demonstrating; the owner may prefer it
   re-filed and can say so on the PR thread.
4. **New idea filed** (below) rather than only noted — one more backlog
   file, but it keeps the B4 conveyor honest.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Taxonomy-surface sync checker** — filed with B4 frontmatter at
`docs/ideas/taxonomy-surface-sync-checker-2026-07-09.md` + README entry.
Evidence from THIS session: the taxonomy lives on three surfaces
(`TASK_CLASSES` · ladder table · telemetry README) that must agree, all
updated by hand here, with nothing enforcing agreement; guard recipe in the
file (`scripts/check_taxonomy_sync.py` + test + kit-quality step).

### ⟲ Previous-session review — run-closeout (PR #21)

Genuinely strong: every drift claim was *verified before being called
drift* (the #44-vs-#46 upgrade credit checked against live GitHub), and it
deliberately left the stale "#16 (this session)" hunks alone because PR
#17's patch rewrites exactly those lines — conflict hygiene this session
copied (CHANGELOG entry at the bottom of Added; current-state edits kept
out of the In-flight/Stability hunks). One concrete system improvement it
surfaced by omission: its pending-only Next action **cross-references queue
items by ordinal** ("agent queue item 5") — this session inserted one owner
gate and had to renumber, and any future insertion rots such references
again. Cross-reference pending items by stable name (e.g. "the
legacy-alias deletion"), never by position; adopted in the lines this
session touched.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **618 passed** (617 + the census test
  reworked; suite count net unchanged — no new test files).
- Dist byte-pin: `python3 src/build_bootstrap.py` → regenerated;
  `git diff` clean post-commit (CI re-verifies).
- `python3 -m ruff check src/engine/` → clean.
- `python3 scripts/check_program_law.py` → **OK with PL-010** (the
  amendment shape passes grammar, IDs, provenance, pointer rules).
- `python3 scripts/check_idea_index.py` → OK (promoted frontmatter + the
  new idea file + README entries).
- `python3 dist/bootstrap.py check --strict --require-session-log
  --session-log .sessions/2026-07-09-pl004-feature-build.md` → held red on
  the born-red card exactly as designed; green at this flip.
- Governance gate: PR #22 labelled `do-not-automerge` at creation;
  auto-merge verified **not armed** (and disarmed if ever found armed);
  PR left OPEN with the decision brief as its body.
