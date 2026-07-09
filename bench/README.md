# bench/ — the lab's pinned benchmark harness

> **Status:** `reference` *(band KL-5, founding plan §5.0. The harness is
> PINNED: this tree's `rubric/`, `tasks/`, and `seeds/` change only via
> `do-not-automerge` PRs, and `results/` is append-only —
> `scripts/check_bench_integrity.py` enforces both in CI from birth; the P10
> ruleset adds path-scoped required review when the owner arms it.)*

## The integrity law (why this tree is special)

The graded subject is never the grader; the runner orchestrates but a
different, pinned-rubric judge scores; **the lab loop never merges its own
change to `rubric/`, `tasks/`, or `seeds/`** — every such change rides a
`do-not-automerge` PR for separate review (the FIRST rubric version was
owner-blessed on exactly such a PR), and **existing rows/artifacts under
`results/` are immutable** — appending new rows/run dirs is what a benchmark
run does and is allowed; editing or deleting recorded history is not. Raw run
artifacts (transcripts, diffs, reports) are **committed** — the Phase-2.5
raw-artifacts-were-lost failure must not recur.

## Layout

```
rubric/cold-start-rubric.md    # THE B1 judge rubric (v1 owner-blessed)
rubric/allocation-rubric.md    # THE B2 judge rubric
tasks/T1.md … T5.md            # fixed task prompt texts (T5 = break-a-rule, D-17)
seeds/make_seed.py             # seed-corpus generator: fresh names, same shape, 1 seeded bug
score_m1.py                    # scripted M1 (words before first mutating action)
run_ab.py                      # prepare arms · collect artifacts · record rows
results/<family>/index.json    # append-only row per run (families: cold-start,
results/<family>/<date>-runNN/ #   allocation, guards, ideas) + committed artifacts
```

## Spec provenance (absolute URLs — the spec survives this plan's travel)

- Protocol, measures, task shapes T1–T4, and the **F-5 pass bar**: companion D —
  <https://github.com/menno420/superbot/blob/main/docs/planning/rebuild-phase-2.5-procedure-2026-07-06.md>
- The twice-failed baseline this series starts from (and T5's motivation):
  <https://github.com/menno420/superbot/blob/main/docs/planning/phase-2.5-cold-start-report-2026-07-07.md>
- The harness + integrity spec: `docs/planning/kit-lab-founding-plan-2026-07-07.md` §5.0–§5.1 (this repo).

## Running B1 (who does what)

1. **The runner** (a dedicated fresh session the loop spawns — never the
   loop's own warm context): `python3 bench/run_ab.py prepare --run-id
   <date>-runNN --seed <fresh int> --tasks T2,T4,T5 --out <scratch>` —
   builds both arms, adopts the kit on ON (`--wire-enforcement` when T5 is in
   the set), runs the §5.1 smoke step.
2. Spawn each task's **cold session** per arm (same model both arms,
   Sonnet-class; prompt = the fenced block in `tasks/<T>.md`; the session
   sees only its arm repo). T4 runs on the arm's own post-T2 state.
3. `run_ab.py collect` each transcript (event JSONL — format in
   `score_m1.py`) + diff; M1 is scored on collect.
4. **The judge** — a different, stronger model, separate invocation, sees
   only transcripts + `rubric/cold-start-rubric.md`; judge model+version
   recorded in the row.
5. `run_ab.py record --family cold-start --row '<json>'` appends the index
   row; commit the run dir (report.md, metrics.json, transcripts/) with it.

**Sequencing note:** B1's FIRST firing happens only after the auto-drafted
handoff build (KL-5 first half — shipped) **and** after this tree's rubric is
owner-blessed and merged. A trend claim needs ≥3 paired runs (KF-8).
