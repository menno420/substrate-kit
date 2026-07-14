# 2026-07-14 — ORDER 023: kit-templated scheduled branch-sweep workflow (BUILD half)

> **Status:** `in-progress`

About to (opening declaration): execute inbox ORDER 023 (BUILD half) — ship a
kit-templated SCHEDULED sweep workflow (`branch-sweep.yml`, daily cron +
`workflow_dispatch` with a `dry_run` input) that enumerates merged+closed
PRs, deletes their same-repo head refs matching the agent-branch patterns
(`claude/*`, `codex/*`, `bot/*`), skips any ref that is the head of an OPEN
PR, never touches the default branch, and logs every deletion and skip
reason. Deliberately NOT built on `pull_request: closed` (GITHUB_TOKEN-driven
merges never trigger workflows — the recursion-guard trap the ORDER names).
Mirrors the auto-merge-enabler's exact staging/install mechanism: staged
always under `<state_dir>/ci/`, installed live by `adopt
--wire-enforcement`, kit-owned regen once it exists. Release + adopter regen
half = v1.17.0 wave, coordinator-sequenced (not this session).

- **📊 Model:** Claude Fable 5 · high · feature build

Run type: worker session (coordinator-dispatched, ORDER 023).
