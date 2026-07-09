# B2 model-allocation A/B — the judge rubric

> **Status:** `binding` *(rubric v1 — same pin as the cold-start rubric: first
> version owner-blessed per founding plan §5.0; changes ride `do-not-automerge`
> PRs, never merged by their author.)*

The B2 paired A/B (plan §5.2) gives the **same real task to two model tiers**
in cold contexts and asks: did the cheaper tier match the dearer one on this
task class? The dataset it feeds is the PL-004 `model · effort · task-class ·
outcome` record; the ladder (`telemetry/allocation-ladder.md`) is revised only
with a citation to dataset rows.

## §1 Decision order (fixed)

1. **Objective gates decide first, and alone when they disagree**: CI on the
   produced diff, the repo's checkers, the task's own tests. A tier whose
   output fails an objective gate loses regardless of judged quality.
2. **The judge scores quality only between objectively-passing outputs**
   (§2), per task class.
3. **Cost tiebreaks**: objectively equal + judged tie → the cheaper tier wins
   the row.

Judge instructions carry over from the cold-start rubric §1: score behavior
and output, not model identity; tier labels stripped where feasible; quote
evidence.

## §2 Quality items (score each output; compare per item)

**All classes:** correct to the task spec · no invented facts/APIs (check
against the repo) · scope discipline (did what was asked; no drive-by churn)
· the output's own verification story (tests run/added, checkers run).

**Per class, additionally** (the 8 PL-004 classes):

| Task class | What distinguishes quality |
|---|---|
| docs-only | accuracy against source; reads in the house voice; links/badges valid |
| mechanical refactor | behavior-preservation evidence; completeness of the sweep (no stragglers) |
| test writing | failure-mode coverage, not line-coverage theater; tests fail when the code is broken |
| runtime bugfix | root cause over symptom; regression test present; blast radius named |
| kernel/architecture design | options genuinely weighed; constraints/invariants stated; reversibility of the chosen path |
| review/verify | real defects found vs missed (seed known defects where possible); false-positive rate |
| research | source quality + verification against ground truth; honest uncertainty |
| idea/planning | actionability (lands-at anchors, verifiable claims); honest depth vs padding |

## §3 Verdict + record

Per pair: `{task_class, task, tier_a, tier_b, objective_gates: {a, b},
judge_verdict: a|b|tie, cost_decides: bool, winner, rationale}` → the run dir
under `bench/results/allocation/<date>-runNN/` + one appended row in
`bench/results/allocation/index.json`. Ladder revisions cite rows; escalation
N=2 / de-escalation M=3 per KF-8 stand until the data revises them.
