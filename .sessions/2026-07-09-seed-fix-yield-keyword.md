# Session 2026-07-09 — make_seed yield-keyword fix + prepare seed-suite smoke (pin-path, do-not-automerge)

> **Status:** `complete` *(PR #49 — do-not-automerge by pin-path law, LEFT OPEN for owner ratification)*

**Scope (about to do):** fix the run-2 make_seed bug (idea
`docs/ideas/make-seed-yield-keyword-bug-2026-07-09.md`): seed 424242 draws
the harvest/`yield` domain and `yield` is a Python keyword, so the generated
seed project is a SyntaxError. Ship (1) a keyword/builtin-safe measure
vocabulary + an identifier screen in `bench/seeds/make_seed.py` (seed 424242
generates a valid project), (2) a `prepare` smoke leg in `bench/run_ab.py`
that runs the generated seed's own pytest in BOTH arms and aborts prepare on
red, (3) regression tests pinning 424242 + a seed-sweep keyword-safety test.
`bench/seeds/` is a PIN PATH — this PR carries `do-not-automerge` from
creation and is LEFT OPEN for owner review (merge = ratification; unblocks
B1 run-3).

## What shipped (PR #49)

- **`bench/seeds/make_seed.py`**: harvest domain's measure token `yield` →
  `bushels` (the SyntaxError source); new `_identifier_safe()` (rejects
  keywords, soft keywords, and builtins) enforced on EVERY drawn token in
  `_names()` — an unsafe pool entry now dies at generation time with the
  token named (`ValueError`), never as a broken seed project. Docstring
  records the 424242 lesson + the per-version determinism clarification.
- **`bench/run_ab.py`**: new `_seed_suite_smoke()` — `prepare` runs the
  generated seed's OWN pytest in both arms right after the seed commit and
  aborts on red ("SEED SUITE RED"); result lines join the manifest `smoke`
  list.
- **Tests (suite 705 → 711)**: seed-424242 regression (all modules
  compile), full-pool identifier screen, seed sweep (draws 0–499 step 7 +
  compile spot-checks incl. 424242/424243), screen-rejects-keyword
  (monkeypatched bad domain), smoke green + smoke aborts-on-red (the exact
  run-2 SyntaxError shape).

## Run report

- **📊 Model:** fable-5 · high · runtime bugfix

### ⚑ Flags

1. **⚑ Pin-path law observed end-to-end**: `do-not-automerge` applied at
   creation; the enabler's fresh-label re-read guard verified live —
   workflow run 29036036799 step "Enable native auto-merge (squash)"
   concluded `skipped`; the PR is NOT armed. LEFT OPEN deliberately:
   owner merge = ratification, and merging unblocks B1 run-3.
2. **⚑ Vocabulary change shifts seed surfaces across kit versions**
   (424242 now draws a valid project instead of erroring) — acceptable by
   design: determinism is per-version; cross-run comparability rests on
   shape, not surface (anti-memorization actively WANTS fresh surfaces).
3. **⚑ Fix + guard shipped as one PR** (the idea file's stated preference)
   even though `run_ab.py` is not pin-path — one reviewable unit.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**A pin-path vocabulary lint in `check_bench_integrity.py`.** Rule 3
candidate: when a diff touches `bench/seeds/`, run the seed generator's
own screen across the full pool space (all domain/verb/adjective combos)
in CI — the label gate makes seeds changes reviewed, but the reviewer is
human and `yield` sat in the pool through an owner-blessed review (#17).
Mechanical screen + human review > human review alone. Anchors:
`scripts/check_bench_integrity.py` (add rule), `make_seed._identifier_safe`
(already importable), tests in `tests/test_check_bench_integrity.py`.

### ⟲ Previous-session review — B1 run-2 record (#44)

Strong: the runner's deviate-by-rule discipline (424242 → 424243, recorded
in `runner_notes` with the reason) is exactly why this bug arrived as a
clean, reproducible idea file instead of a mid-run mystery — and filing
the fix as an idea rather than smuggling it into the recording PR kept the
append-only recording clean. Miss: the idea file's "done-when" asks for
the 424242 regression but not for a POOL-WIDE screen — this PR added the
sweep anyway; the narrower spec would have left the same class open for
the next keyword ("match"-class soft keywords, builtins). **Workflow
improvement:** idea-file done-whens for bug classes should name the CLASS
("no pool token may be keyword/builtin-unsafe"), not just the instance —
same generalize-the-guard instinct as the friction→guard rule.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **711 passed** (705 + 6 new).
- `python3 -m pytest tests/test_bench.py -q` → 21 passed.
- Enabler: arm step `skipped` on run 29036036799 (fresh-label guard);
  auto_merge unset on #49.
- `python3 scripts/check_bench_integrity.py --base origin/main` locally:
  pin-path change correctly demands the label (present on the PR).
