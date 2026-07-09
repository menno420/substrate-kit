# Model-for-task allocation ladder (program-wide)

> **Status:** `living-ledger`
>
> PL-004 layer 2 (`docs/program/rulings.md`), seeded per founding plan §5.2
> at band KL-3. **One home for the whole program** — consumer repos consult
> this ladder, they do not fork it. Rows are **defaults revised only with a
> citation to dataset rows** (`telemetry/model-usage.jsonl` aggregates + B2
> paired A/B results); a revision without cited rows is drift, not tuning.

## The ladder (seeded defaults — B2 data revises them)

| Task class (Q-0248, verbatim) | Default tier | Notes |
|---|---|---|
| kernel/architecture design | Opus/Fable-class, effort xhigh–max | frozen-grammar / kernel contact always lands here |
| idea/planning | top tier | plan quality compounds; cheap plans are expensive |
| research | Opus-class lead + Sonnet-class fan-out | the seven-lane pattern |
| review/verify | a **different model than built it** | the graded subject is never the grader (A-16) |
| runtime bugfix | Sonnet-class workhorse, conditional on an objective gate (CI/checkers) | escalate on the triggers below |
| mechanical refactor | Sonnet-class workhorse, conditional on an objective gate | same condition |
| test writing | Sonnet-class | |
| docs-only | Haiku/Sonnet-class ⚑ | the cheap-tier experiment class — B2's first paired A/B candidate |

## Escalation / de-escalation (mechanical — KF-8 seeds, data-revisable)

- **Escalate one tier when:** two red CI rounds on the same task · a review
  with ≥ **2** confirmed defects (N=2) · frozen-grammar/kernel contact.
- **De-escalate one tier after:** **3** consecutive matching-quality tasks
  of the class (M=3).
- **Outcome windows:** rework/revert window = **14 days**; a trend claim
  needs ≥ **3** paired runs (KF-8/D-15).

## What decides (PL-004)

Objective gates first (CI green on first push, checker findings on the
produced diff), judge-scored quality second (paired same-task A/Bs per the
allocation rubric, band KL-5), cost as tiebreaker.

## Revision log

| Date | Row changed | Cited rows | By |
|---|---|---|---|
| 2026-07-09 | (seed — no revisions yet) | — | band KL-3 |
