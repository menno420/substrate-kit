# Run-10 spec notes (written 2026-07-11, post-run-9 — kit-dev lane)

> **Status:** `spec-notes` — input for the session that fires run-10. Not a
> result; results are immutable, this file is pre-run design notes. No bench
> run happened in the session that wrote this.

## 1. Validate the #222 drafted-card advisory lane (still UNVALIDATED)

Run-9 measure (d) hit its target number (bare `check --strict` exit 0 at ON
arm end, run-8 was exit 1) **through the wrong mechanism for validation
purposes**: ON-T4 genuinely completed the card, so the card was no longer a
draft at any strict-check point and the #222 advisory lane (an unadopted
engine-authored draft — badge `drafted` + auto-draft marker — is ADVISORY in
bare strict, while every gate lane keeps the locked door) was **never
exercised** (report §5.3 mechanism note; s-row-facts measure (d) nuance).
Two runs in a row have now failed to touch the lane from opposite sides
(run-8: no draft semantics shipped yet; run-9: the draft got adopted).

**Cheap validation shape — scripted checkpoint, no new arm, no judge cost:**
run-9 already produced the exact state the lane exists for, mid-run: between
T2 arm end (the Stop hook auto-drafts `.sessions/<date>-session.md`,
unresolved slots, unadopted) and T4 boot. Run-10 adds one scripted
checkpoint there, in the ON arm repo, harness-side:

1. `python3 bootstrap.py check --strict` (bare) — EXPECT exit **0** AND the
   advisory line naming the drafted card and its unresolved slot count.
   Capture both verbatim into `runner_notes` + s-row-facts.
2. `python3 bootstrap.py check --strict --require-session-log
   --session-log .sessions/<the-drafted-card>.md` — EXPECT exit **1** (the
   gate lane must keep holding the same state red).

Falsification readings: (1) exits 1 → the advisory lane is broken/regressed
— file the kit bug before scoring anything; (1) exits 0 with NO advisory
line → the lane is silently green (the run-4/5 confound shape) — also a
finding, not a pass. Cost: two commands + two captured lines; zero prompt
changes, zero task-file changes (`bench/tasks/` pin path untouched), no
judge involvement, no effect on any measured arm (the checkpoint runs
between arms on repo state the run already creates).

## 2. Riders run-10 inherits from the footprint-cut slice (this PR)

- The ON-T2 boot shape now renders the **fresh-state fast path** in
  `HANDOFF.md` + the SessionStart push (complete card, no pointer, no trail
  → "Fresh start — nothing in flight" + the working `grep -r
  --exclude=bootstrap.py --exclude-dir=.substrate` recipe, no "Open that
  card FIRST"). Watch ON-T2's first tool calls: the target is the 116w
  contentless card read gone and — the big axis — no 1724w-class
  kit-polluted grep (run-9 s-row-facts: 75 `bootstrap.py` lines + 75
  byte-identical `.substrate/backup/` lines, zero project-code lines).
  T4/T5-shaped renderings are byte-pinned unchanged
  (`tests/test_handoff_pointer.py` run-9 pins), so T4 comparability holds.
- `run_ab.py collect` now hard-aborts on `events_seen == 0` (the run-9
  convert_native argv-slip class) — a converter slip can no longer file an
  empty transcript or write an `m1.json`.
- Report §5.5 carry-over: a paired tie-break on a second *build* task would
  settle whether the T2 M1 gap is structural or seed noise — worth
  spec'ing only if the fresh-path cut alone doesn't close the axis.
