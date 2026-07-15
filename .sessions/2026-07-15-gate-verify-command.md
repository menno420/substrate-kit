# Session · 2026-07-15 · gate-verify-command

> **Status:** `in-progress`

Intent: baton item 1 — the substrate-gate's test step honors the interview's `verify_command` slot (the 💡 on the #403 card): `live_ci_workflow` hardcodes `-m pytest tests/ -q` while the adopt interview already records `verify_command` (src/engine/interview/question_bank.py:86, routed to templates/CLAUDE.md). Prefer the state-recorded slot (filled + non-default + gate-safe) as the test-step command, pytest as fallback, so the CI runner stops diverging from the verify line CLAUDE.md teaches. Capture the idea file with the increment.

- **📊 Model:** Claude Fable · medium · feature build
- ⚑ Self-initiated: no — baton-named (control/status.md Next-2 item 1 at sync HEAD e196936).
