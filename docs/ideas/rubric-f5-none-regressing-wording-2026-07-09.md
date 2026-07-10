---
state: historical
origin: lab
shipped_pr: 128
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# Rubric F-5 wording: "none regressing" vs the 7k-budget-as-M1-yardstick intent (2026-07-09)

> **RULED 2026-07-10 — Reading A (the strict, pinned letter).** Delivered by
> inbox **ORDER 011** (P0, owner delegation Q-0262.1, superbot router; ruling
> record shipped by PR #128). This is fix option 3 below — "the strict text
> stands": no rubric wording change was needed, so no pin-path PR rides it.
> Runs 2–3 stand as un-caveated FAILs; family headline **1 PASS / 3 FAIL**;
> B-benches unpaused. Record:
> `bench/results/cold-start/f5-ruling-order-011.md`. The brief below is
> preserved as written (historical).

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run `2026-07-09-run02`). This is
> a **decision brief for the OWNER** — `bench/rubric/` is a PIN PATH
> (`check_bench_integrity.py` rule 1), so ANY wording change must ride a
> `do-not-automerge` owner-review PR. Agents do not resolve this one;
> two readings of the pinned text now produce opposite verdicts on the
> same evidence, and only the owner can pick which the rubric means.

## The decision

F-5's pass bar reads: ON beats OFF on **≥2 of 3 measures with none
regressing** (plus the ≤7,000-word M1 budget "additionally checked" and
the zero-unrecoverable-errors clause). Question for the owner: **what
counts as an M1 "regression"?**

- **Reading A — strict (the pinned letter):** any per-measure M1 loss
  (ON reads more words than OFF before first mutation) is a regression.
  Run-2 verdict under A: **FAIL**.
- **Reading B — purposive (the budget as M1's yardstick):** expected kit
  orientation reading is not a regression as long as ON stays inside the
  ≤7k budget; M1 "regresses" only when the budget is blown (or blown
  relative to it). Run-2 verdict under B: **PASS**.

The run-2 judge (claude-opus-4-8, independent) applied A explicitly and
said so: *"Under a purposive reading in which the ≤7,000-word budget is
M1's yardstick and expected kit reading is not a 'regression', this run
would PASS — but the rubric text as pinned does not license that reading,
so FAIL stands."* (`bench/results/cold-start/2026-07-09-run02/report.md`
§4.)

## Evidence from both runs

- **Run 1 (`2026-07-09-run01`, PASS):** M1 was **unmeasurable** — all 3
  pairs scorer-tainted (the #40-fixed artifacts) — so the "none
  regressing" clause was never actually exercised; the PASS rested on
  M2+M3 with M1 silent.
- **Run 2 (`2026-07-09-run02`, FAIL):** first **clean** M1 measurement
  (fixed scorer, all six values scripted): OFF wins T2 (556 vs 1706) and
  T4 (1481 vs 2272) at ~2–3×, T5 a 20-word tie (511 vs 531). Every ON
  value is far inside the 7k budget (max 2,272); ON wins M2 + M3; zero
  unrecoverable errors. The structural shape (judge §5.5 item 4): ON's
  M1 endpoint is the born-red card Write (a ritual step), OFF's is its
  first code edit — the kit *by design* spends orientation words before
  its first mutating act. Under Reading A the kit can essentially never
  pass on a small clean seed repo, because its own conventions are
  counted against it.

## What a fix could look like (owner picks; all pin-path)

1. Amend F-5 to Reading B: "none regressing" → M1 regression = ON
   exceeding the 7k budget (keep the raw numbers recorded either way).
2. Keep Reading A but rebase M1's endpoint (words before first *code*
   mutation, excluding ritual writes) — changes `score_m1.py` semantics
   too (NOT pin-path itself, but the rubric text naming it is).
3. Keep the strict text as-is, accepting that FAIL rows on M1-only
   regressions are the honest advisory signal (KF-5 keeps verdicts
   advisory; KF-8 trend needs ≥3 rows regardless).

## Done-when

The owner rules on a `do-not-automerge` PR that either amends the rubric
text (readings B/2) or records "strict text stands" (reading 3) in the
rubric or the decisions ledger; subsequent B1 runs are judged under the
ruled reading.
