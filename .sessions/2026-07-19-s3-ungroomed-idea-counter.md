# 2026-07-19 — S3 un-groomed-idea counter advisory (`ungroomed-ideas`)

> **Status:** `in-progress`

- **📊 Model:** opus-4.8 · medium · feature build

Building the wave-2 rank-3 advisory `check` sub-check per
`docs/planning/2026-07-19-night-run-idea-groom-wave2.md` (S3) —
`src/engine/checks/check_ungroomed_ideas.py` (advisory, never exit-affecting):
counts 💡 lines on session cards newer than the newest groom doc and warns so a
false "backlog DRY" claim can't be made + cli.py wiring + MODULE_ORDER + tests +
dist rebuild. Also registers S17 (applies-when discovery nudge) in the wave-2
ladder.

## 💡 Session idea (Q-0089)

**Groom-doc freshness advisory.** The S3 counter warns when 💡 ideas sit on
cards newer than the newest groom doc. A sibling worth having: warn when the
newest groom doc itself has aged past a `cadence.groom_staleness_days` horizon
(mirroring `check_stale_walls`'s cadence read) — a groom pass that has not run
in N days is its own drift signal, independent of whether new 💡 lines exist yet.
Deduped against `docs/ideas/` — the stale-walls advisory covers CAPABILITIES
rows, not groom cadence; no existing idea file names groom-doc staleness. Worth
having because it catches the "backlog is stale" case even in a quiet window
where no new session ideas have accrued.

## ⟲ Previous-session review (Q-0102)

The previous session (S2 — advisory→born-red-gate graduation recipe, PR #516)
shipped its recipe cleanly and left the wave-2 ladder in
`docs/planning/2026-07-19-night-run-idea-groom-wave2.md` as the baton, so this
session started with an unambiguous next pick (S3) and zero re-deciding. What it
could have done better: the wave-2 ladder lists buildable ranks but does not
carry a one-line "keeps `check --strict` green on the kit's own tree?" note per
rank — an advisory that fired on the kit's own cards would redden every adopter's
`check` output on upgrade. Concrete workflow improvement it surfaces: each
advisory-rank entry in a groom ladder should carry an explicit "input-gated +
fail-open, zero findings on a clean tree" acceptance line, so the build agent
verifies non-regression against the kit's own tree by design rather than by
memory.
