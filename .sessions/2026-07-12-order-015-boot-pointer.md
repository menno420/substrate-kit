# 2026-07-12 — ORDER 015: dead boot-pointer fix + gate-integrity verify

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · order-execution

## Scope (what is about to happen)

About to execute inbox ORDER 015 (2026-07-12T08:30Z, P1): kill the
dead-boot-pointer class in `src/engine/templates/AGENT_ORIENTATION.md.tmpl`
(engine-computed `${agreement_home}` slot: `.claude/CLAUDE.md` when live or
opted-in, else the always-planted root `CONSTITUTION.md`) with regression
tests + dist rebuild, and settle the VERIFY-FIRST rider: fixture-based
evidence that the shipped session gate holds an added in-progress card red,
retracting the v3.1 census's "added-card advisory loophole" /
"severity-tier drift" claims. Lane claim:
`control/claims/claude-order-015-boot-pointer.md` (merged to main via #260
@ 5bc24ac).
