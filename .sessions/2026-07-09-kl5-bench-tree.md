# Session 2026-07-09 — KL-5 (2/2): the bench/ tree

> **Status:** `in-progress` *(born-red — flips to `complete` when the close-out is written; this PR then STAYS OPEN for owner blessing per §5.0.)*

**About to do (founding plan §10 KL-5 row, second half; §5.0/§5.1):** the
pinned benchmark harness — `bench/rubric/cold-start-rubric.md` +
`bench/rubric/allocation-rubric.md` (first versions **owner-blessed**, which
is why this PR carries `do-not-automerge` and is never merged by its
author), tasks T1–T5 (T5 = the new break-a-rule task, D-17), the seed
generator (`bench/seeds/make_seed.py` — fresh surface names per run, same
shape), `bench/score_m1.py` (scripted words-before-first-mutation),
`bench/run_ab.py` (arm builder / artifact collector / append-only recorder),
append-only `bench/results/*/index.json` stubs, and
`scripts/check_bench_integrity.py` wired into kit-quality (pin-path label
gate + append-aware results immutability). NO benchmark arm is run and NO
score is produced in this session — B1's baseline firing is a separate,
later step after the rubric merges (never-grade-own-substrate).
