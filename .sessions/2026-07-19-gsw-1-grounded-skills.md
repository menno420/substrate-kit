# Session card — GSW-1..3 grounded-skills measurement window run

> **Status:** `in-progress`
> **📊 Model:** Claude Opus 4.8 (1M) · high · measurement/audit

## Scope
Run the frozen grounded-skills measurement harness for the 2026-07-19..26
window (baton item GSW-1; plan `docs/planning/2026-07-19-grounded-skills-window-run.md`).
Self-authorizing under fm ORDER 048. Completing the full GSW-1..3 chain in one
wake (the plan blesses this: line 84 "a single unhurried wake can do all three")
because the harness output is ephemeral and splitting across containers would
shift the `--end` date and change the measured numbers.

## What I'm about to do
- Run `scripts/measure_grounded_skills.py --clone` over a FRESH FULL clone (Trap 1:
  a shallow clone silently zeroes M4).
- Spot-check ≥3 harness numbers against git/source ground truth (Trap 2: PL-008 unverified).
- Commit the frozen `results.json` into `docs/reports/data/` so the numbers are
  auditable and reproducible.
- Publish `docs/reports/2026-07-19-grounded-skills-measurement.md` (`audit`) and link
  it from `docs/operations/README.md` (Trap 3: docs-gate reachability).

## Provenance
Coordinator dispatch under fm ORDER 048; baton item GSW-1 from
`docs/planning/2026-07-19-grounded-skills-window-run.md` (on main since PR #469).
