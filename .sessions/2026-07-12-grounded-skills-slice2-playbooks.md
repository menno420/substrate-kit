# 2026-07-12 — grounded-skills program, slice 2: playbook bodies + grounds + advisory checker

> **Status:** `in-progress`

- **📊 Model:** Claude 5 family · seat-worker · grounded-skills slice 2

## Scope (what is about to happen)

Implementing §7 slice 2 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263):
upgrade `session-close` to the full landing-path playbook, add
`upgrade-distribution` (wave runbook) and `release` (cut runbook) as
playbook-grade skill bodies with exact command groundings; add a per-skill
`grounds` field surfaced as a new `skills_index_table()` column (the exact-
commands column slice 1 deferred); ship the slice-1 💡 idea as an advisory
grounds checker (`src/engine/checks/`), never exit-affecting (Q2=B); tests +
dist rebuild.

**Provenance flag:** proceeding on the plan's §8 recommended defaults per the
coordinator — **Q2=B** (advisory-first; graduation to CI-red only once
proven) and **Q4=A** (program supersession covers this slice under the
2026-07-11 freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice2.md` (deleted at
close).
