# A "feature build" task class for the Q-0248/PL-004 taxonomy (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured → routed **discuss-first** (program-law change).
> **Origin:** consumer:menno420/superbot (friction issue
> [#15](https://github.com/menno420/substrate-kit/issues/15), report 3) +
> the kit's own KL-3 session idea (`.sessions/2026-07-09-kl3-telemetry.md`).

## The gap

The 8-class task taxonomy (`docs/program/rulings.md` PL-004;
`TASK_CLASSES` in `src/engine/loop/telemetry.py`) has **no class for
new-capability building**: engine feature work files as nearest-neighbor
`kernel/architecture design` (KL-3, KL-4 both did), and KL-2 filed an
off-taxonomy compound the harvest now warns on. Every band is quietly
mislabeling the B2 dataset's most common session shape.

## The two candidate fixes (pick one, then it's cheap; after a thousand rows it isn't)

1. **A 9th class `feature build`** — a PL-004 amendment (program law: needs
   the provenance discipline, a superbot-router rider, and a `TASK_CLASSES`
   + allocation-ladder row in the same PR; existing rows are NOT rewritten —
   the dataset keys on class strings per-date).
2. **A documented mapping rule** — "a mixed/feature session files its
   dominant-cost class" — zero schema motion, but keeps the mislabel for
   pure feature work.

Recommendation (decide-and-flag, PL-001): option 1 — the class is real,
frequent, and the ladder needs its own row (feature build ≠ kernel design in
required tier). **Why not shipped in KL-4:** it amends program law (PL-004),
which carries the §8.3 provenance discipline and deserves its own focused PR
with the superbot-side rider; bundling it into a band PR would bury a law
change. Route: next lab-loop firing or a dedicated session; the ruling PR
flags prominently on its run report.

## Done-when

`TASK_CLASSES` + `docs/program/rulings.md` PL-004 block +
`telemetry/allocation-ladder.md` agree; the harvest accepts the new class;
friction issue #15's report 3 is cite-closed against the ruling PR.
