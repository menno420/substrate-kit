# R9 — harness --commit-results PATH (durable results artifact)

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** R9 (harness `--commit-results PATH`) from docs/planning/2026-07-19-night-run-idea-groom.md

**About to do:** add a `--commit-results PATH` flag to
`scripts/measure_grounded_skills.py` that persists the machine-readable results
(the same JSON `--json` emits) to a durable, caller-named PATH — creating its
parent dirs and honoring the same shallow-clone refuse-to-publish guard — so a
GSW-style measure→verify→publish chain has a raw `results.json` artifact that
survives ephemeral-container splits; add tests.

- **📊 Model:** Opus 4.8 · high · feature build (harness --commit-results durable artifact)
- **⚑ Self-initiated:** R9 is baton work (backlog rung from the night-run groom
  R9 entry, from the gsw-1 card). Decide-and-flag semantics: [[fill: write-file vs git-commit decision]]

## What shipped (PR #[[fill: PR number]])

[[fill: what shipped summary]]

## 💡 Session idea

[[fill: one new idea]]

## ⟲ Previous-session review

[[fill: review of previous session + one system improvement]]
