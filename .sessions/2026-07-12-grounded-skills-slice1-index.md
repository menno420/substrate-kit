# 2026-07-12 — grounded-skills program, slice 1: skill index + boot-set wiring

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 1

## Scope (what is about to happen)

Implementing §7 slice 1 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263,
squash b820b0f — owner directive 2026-07-12): a generated `docs/SKILLS.md`
skill index rendered FROM the kit's `SKILLS` list (engine-computed table,
one source — plan §2 artifact classification), planted via one `ADOPT_PLAN`
tuple, wired into the boot/orientation set (pointer lines in
`AGENT_ORIENTATION.md.tmpl`, `CONSTITUTION.md.tmpl`, `CLAUDE.md.tmpl` —
the CAPABILITIES.md wiring pattern), with tests for index generation and
adopt-time planting, plus a dist rebuild. Advisory only — no CI enforcement
in this slice. No slice-2 (playbook bodies) or slice-5 (capability refresh)
content.

**Provenance flag:** the coordinator is proceeding on the plan's §8
recommended defaults — Q2=B (advisory-first, grammar checks graduate later)
and Q4=A (the program supersession covers its slices under the 2026-07-11
freeze). Vetoable at the owner's normal window.

Lane claim: `control/claims/claude-grounded-skills-slice1-index.md`
(deleted at close).

## Close-out

(withheld until complete)
