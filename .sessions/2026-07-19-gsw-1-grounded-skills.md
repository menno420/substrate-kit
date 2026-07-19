# Session card — GSW-1..3 grounded-skills measurement window run

> **Status:** `complete`
> **📊 Model:** Claude Opus 4.8 (1M) · high · review/verify

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

## Shipped
- **GSW-1 — harness run:** `scripts/measure_grounded_skills.py --clone` ran once
  over FRESH FULL (non-shallow) clones of the 12-repo roster in
  `docs/fleet-repos.txt`; every clone verified `shallow:false`, so M4 history is
  complete (Trap 1 cleared).
- **GSW-2 — verification:** 4/4 spot-checks MATCH against git/source ground truth
  (the PL-008-unverified harness spot-checked, Trap 2 cleared).
- **Frozen raw data:** `docs/reports/data/2026-07-19-grounded-skills-results.json`
  committed as the auditable, reproducible artifact (sha256
  `dc8d8399…af10fc9`, carried in the report header).
- **GSW-3 — published `audit` report:** `docs/reports/2026-07-19-grounded-skills-measurement.md`
  (before/after M1–M4), linked from `docs/operations/README.md` (Trap 3 docs-gate
  reachability cleared).
- **Heartbeat + window close:** `control/status.md` baton advanced (GSW-1..3 DONE →
  GSW-4 / next Part-B item) and the standing ⚑ "silence accepts" window-acceptance
  block flipped to CLOSED (published 2026-07-19, PR #476). Claim removed.
- Full suite 1796 passed / 1 skipped; `check --strict` red only on the born-red
  session-card hold.

## 💡 Session idea
**Make measurement harnesses commit their raw `results.json` as a durable artifact**
(e.g. a `--commit-results PATH` flag, or a plan mandate), so a GSW-style
measure→verify→publish chain survives being split across ephemeral containers.
*Why it's worth having:* this run had to persist `results.json` by hand because the
frozen plan wrote it only to ephemeral `/tmp` — had GSW-2/3 run on a later day, the
missing frozen data would have silently shifted `--end` and changed the published
numbers, breaking reproducibility. A committed-results contract makes the numbers
frozen-by-construction. Dedupe-checked: no `commit-results`/`results.json`/`durable
artifact` idea exists under `docs/ideas/` (grep returned zero hits).

## ⟲ Previous-session review
Of the 2026-07-18 B-3 fast-lane branch-prefix symmetry lint wake (PR #474): genuine
credit — it pinned the fast-lane branch-prefix set (`claude/`→carded,
`claim/`→card-less) into `FASTLANE_PREFIX_REGISTRY` and asserted **bidirectional**
set-equality across the three duplicating surfaces (enabler workflow, `ci.yml`
claims-only guard, engine defaults), so drift in *either* direction reds CI — the
right shape for a symmetry lint. What it could improve / a concrete system
improvement it surfaces: B-1/B-2/B-3 each pinned a *different* enforcing surface
(job census, strict sub-checks, branch-prefix set) with its own bespoke
bidirectional-equality test, which is now a recognizable, repeating pattern —
folding those into one parameterized "surface-parity" test harness
(`registry ⇄ live-source`, table-driven) would cut the per-surface boilerplate and
guarantee any *future* pinned surface is covered by construction rather than by a
remembered hand-written test.

## Docs audit
Ledger/reachability clean: the `audit` report is linked from
`docs/operations/README.md` (line 49) and carries its frozen `results.json`
pointer + sha256; `check --strict` shows no docs-gate / badge / reachability red on
this wake's report — the only exit-affecting red is the by-design born-red
session-card hold. No drift spotted.
