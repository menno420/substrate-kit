# 2026-07-10 — gen-2: run-2 ordinary-lane follow-ups (queue item 3)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · high · engine+bench fix (one scoped PR: the three
  run-2 ordinary-lane follow-up idea files)

## Scope (about to do)

Implement the three run-2 follow-up fixes the B1 record sessions filed as idea files
(queue item 3, claimed on `control/status.md` by kit-lab-gen2 via PR #94 — the status
close is the orchestrator's, not this PR's):

1. `run-ab-prepare-engagement-arc-2026-07-09.md` — teach `bench/run_ab.py::cmd_prepare`
   the ON-arm RED→ENGAGED→GREEN arc (deterministic seed-derived answers,
   `render --live`, first session card, seed heartbeat), assert `check --strict` exit 0,
   and write `manifest.json` on the failure path too (`smoke_failed` marker).
2. `render-live-claude-md-gap-2026-07-09.md` — `render --live` includes
   `.claude/CLAUDE.md` (option (a), preferred per the idea file); smoke/test leg pins
   zero unrendered findings across ALL engagement-scoped files after the arc.
3. `model-line-checker-false-red-2026-07-09.md` — `_adopt_sessions_readme()` plants
   `label (needle)` byte-forms; the session-log checker names the expected marker form
   on a miss. (Distinct from the PR #40 `parse_model_line` shadowing fix.)

Engine changes → dist regen + byte-pin. No pin paths (bench/rubric|tasks|seeds),
no `control/` writes.
