---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Engage slot lists: derive from the bank instead of triple-pinning (2026-07-13)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win checker or derivation (bench +
> CI), engine untouched.
> **Origin:** lab — paid in the rider-graduation session (ORDER 016
> seat-item 4): adding three bank slots (Q-014..Q-016) silently missed the
> full-slot lists pinned in `bench/run_ab.py` `ENGAGE_SLOTS` and the
> `.github/workflows/ci.yml` cold-adopt walk, surfacing only as a red
> bench-arc test. The same shape as the seat-digest clip ratchet
> (`seat-digest-adaptive-clip-2026-07-13.md`): a constant hand-pinned to
> "just fit" current data, wrong again on the next growth step.

## The gap

Three surfaces enumerate "every interview slot": the question bank (source
of truth), `ENGAGE_SLOTS` in `bench/run_ab.py`, and the ci.yml cold-adopt
`for slot in …` loop. The bench list is deliberately pinned for
byte-reproducibility, but nothing asserts the pin still covers the bank —
each bank growth is a latent red until a test trips over it.

## The fix shapes

- Cheapest: a test asserting `set(ENGAGE_SLOTS) == {q["slot"] for q in
  QUESTIONS}` (reproducibility keeps the pinned ORDER, coverage becomes
  checked), plus the same assertion parsing the ci.yml slot loop.
- Alternative: derive both walks from the bank at run time and pin only
  the answer-value derivation (seed-derived strings stay deterministic).
