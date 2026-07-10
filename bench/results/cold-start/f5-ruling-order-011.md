# F-5 ruling — Reading A (strict) · applied to this family 2026-07-10

> **Provenance:** inbox **ORDER 011** (2026-07-10T15:33Z, P0) — owner delegation
> **Q-0262.1** (superbot router, 2026-07-10), routed by the owner's dispatch
> session. Decision brief the ruling answers:
> `docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`.

## The ruling

F-5's "none regressing" clause means **Reading A — the strict, pinned letter**:
any per-measure M1 loss (ON reads more words than OFF before first mutation) is
a regression. Reading B (7k-budget-purposive) is rejected. Honest-negative
headlines are the fleet's credibility asset — that is the why behind A.

## What it does to the recorded rows (re-score of runs 2–3)

`bench/results/` history is immutable (append-only law,
`scripts/check_bench_integrity.py`), so the rows and run-dir reports are not
edited; this file is the family-level annotation that supersedes their
dual-reading caveats:

- **run01 (`2026-07-09-run01`)** — PASS. Unaffected by the ruling.
- **run02 (`2026-07-09-run02`)** — recorded verdict **FAIL** (strict) was
  already the verdict of record; its "purposive Reading B would PASS" caveat is
  **retired** — under the ruling the verdict is an un-caveated **FAIL**.
- **run03 (`2026-07-10-run03`)** — recorded verdict **FAIL** (strict) was
  already the verdict of record; its "wording disputed and unruled (purposive
  Reading B would PASS)" caveat is **retired** — un-caveated **FAIL**.
- **run04 (`2026-07-10-run04`)** — **FAIL** under both readings
  (ruling-independent); Reading A is now simply the reading of record.

## The family headline (KF-8 trend, 4 rows)

**1 PASS / 3 FAIL** — run 1 PASS; runs 2, 3, 4 FAIL. No dual-reading caveat
travels with this headline anymore. Future rows are scored under Reading A
only; dual-scoring while the ruling was pending (the run-4 practice) ends here.
