# Session 2026-07-10 — ORDER 011: F-5 ruling applied (Reading A), runs 2–3 re-scored, B-benches unpaused

> **Status:** `complete`

- **📊 Model:** claude-fable-5 · medium · docs-only

**Scope (as declared, born-red):** execute inbox ORDER 011 (P0, owner delegation
Q-0262.1, superbot router, routed 2026-07-10T15:33Z): the F-5 "none regressing"
wording ruling is **Reading A** (the stricter reading). Claim:
`claimed-by: 011 kit-lab-order-011 2026-07-10T16:02Z` (landed on main via
fast-lane PR #127, merge 38a1e5a, before any build work — the ORDER 007 ritual).

Planned slice, docs/control only (no bench run is fired; no src/dist changes):

1. **Re-score runs 2–3 under Reading A** — both recorded verdicts were already
   strict-FAIL as the verdict of record (rows 2–3 of
   `bench/results/cold-start/index.json`), so re-scoring = retiring the
   dual-reading caveat, not flipping a verdict field. `bench/results/` is
   CI-immutable (append-only law, `check_bench_integrity.py`), so the ruling
   lands as a NEW annotation file in the family dir; the immutable rows' and
   run-dir reports' "disputed / Reading B would PASS" notes are superseded by
   it, never edited.
2. **Un-caveat the KF-8 trend headline** everywhere it lives: the cold-start
   family headline is **1 PASS / 3 FAIL** (run 1 PASS; runs 2, 3, 4 FAIL —
   run 4 failed under both readings). Homes: `docs/current-state.md`,
   `CHANGELOG.md` [Unreleased], `docs/gen2/queue-state.md`,
   `docs/gen2/next-boot.md`, the F-5 idea file, `control/status.md`.
3. **Unpause the B-benches** — clear the "B1 run-5 WAITS for the F-5 ruling"
   hold (next-boot.md; queue-state.md carries the OPEN/HOT crosswalk entry);
   this slice clears the hold only, it does NOT run a bench.
4. **Status heartbeat (deliberate last content step):** ack+done ORDER 011,
   OWNER-ACTION 1 RESOLVED, ROUTINE STATE cutover record (old hourly trigger
   deleted → new 2-hourly standing wake), next-coordinator-slice note.

## Close-out

**Shipped (claim #127 → session PR #128):**

- `bench/results/cold-start/f5-ruling-order-011.md` — NEW family-level ruling
  annotation (the CI-legal re-score: results history is immutable, so the
  ruling supersedes the recorded dual-reading caveats instead of editing them).
- Un-caveated Reading-A headline (**1 PASS / 3 FAIL**) in
  `docs/current-state.md` (run-2/3/4 entries + new ruling bullet + Next-action
  + owner-gates item 1 ✅ + agent-queue note) and `CHANGELOG.md` [Unreleased]
  (ruling entry + KF-5 statement). Released sections ([1.7.0] and older) left
  untouched — historical release notes are not rewritten.
- B-bench unpause: `docs/gen2/next-boot.md` "B1 run-5 WAITS" hold CLEARED +
  §4 KF-8 law note updated + ROUTINE STATE superseded-note;
  `docs/gen2/queue-state.md` owner-clicks item 3 ✅, run-2/3 captions,
  resume-points ruling record. No bench fired (the slice clears the hold only).
- `docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md` RULED
  (historical/shipped, PR #128) + README index entry updated.
- `control/status.md` overwrite (deliberate last content step): acked/done
  011, OWNER-ACTION 1 RESOLVED (items 2–12 carried verbatim, ordinals stable),
  ROUTINE STATE cutover record (old hourly trig_01FnqnAQjLU2T8d16iHwWQ2h
  DELETED → trig_016EfUawz6KxEYqUM6f1BqDw "substrate-kit 2-hourly standing
  wake" armed), next-coordinator-slice note (program review §6.1 in flight).

**Verification (local, PR #128 branch):** `python3 -m pytest tests/ -q` →
**819 passed**; `python3 dist/bootstrap.py check --strict` → clean except the
expected born-red hold on this very card (flipped by this commit);
dist byte-pin clean (`python3 src/build_bootstrap.py && git diff --exit-code
dist/bootstrap.py`); `check_idea_index` / `check_program_law --label-gate` /
`check_bench_integrity --base origin/main` / `ruff check src/engine/` all OK.

**⚑ Flags (adaptations, recorded honestly):**

- ORDER 011 said "re-score runs 2–3 → both become FAIL" — both rows were
  ALREADY recorded FAIL (strict was the verdict of record since #44/#85), so
  the re-score changed no verdict field; it retired the dual-reading caveats.
- `bench/results/` is CI-immutable — the run records could not be edited; the
  annotation-file pattern above is the adaptation.
- Live-hit: the K0 orientation budget had only **8 words** of headroom on main
  (6992/7000); this session's current-state additions reddened the gate and
  forced a condensation pass (net file: 6649 words, total 6998/7000). Evidence
  for the card-level "orientation-budget headroom advisory" idea
  (`.sessions/2026-07-10-nightcap-docs-reconcile.md` § 💡) — still unfiled;
  filing it is a ready-made next ordinary-lane increment.

**💡 Session idea:** name an **immutable-record supersession convention** for
`bench/results/` — a reserved, checker-known annotation filename pattern (e.g.
`<family>/*-ruling-*.md` or a single `ANNOTATIONS.md` per family) documented in
`bench/README.md`, so re-scores/rulings over immutable rows always land in one
predictable place and a reader of `index.json` knows where to look for
verdict-affecting annotations. This session invented the pattern ad hoc
(`f5-ruling-order-011.md`); without a named convention the next ruling will
invent a different one and readers must grep. Dedup-checked: bench/README and
docs/ideas/ have no annotation convention today.

**⟲ Previous-session review:** the gen-2 close-out pair (#124/#125) did the
right thing verifying ROUTINE STATE directly via `list_triggers` instead of
trusting a relay — that discipline is why today's cutover record could say
"both records are true in sequence" instead of relitigating. Miss: it left the
orientation budget at 6992/7000 with no signal, so the next writer (this
session) paid a surprise condensation pass at verification time; the concrete
improvement is graduating the nightcap card's headroom-advisory idea into a
filed `docs/ideas/` entry + a percent-threshold warning in
`check_orientation_budget`.

