# Session · 2026-07-15 · adopt-pytest-gate-step

> **Status:** `complete`

Intent: baton item 1 — the substrate-gate template plants a pytest step behind the control-fast-lane short-circuit (idea adopt-plants-pytest-gate-step-2026-07-10; the superbot-games gen-1 tests-blind-gate class, games#16), always-planted with an in-job self-skip when `tests/` is absent so it self-heals when tests arrive.

- **📊 Model:** fable-5 · medium · feature build
- ⚑ Self-initiated: no — baton-named (control/status.md Next-2 item 1 at sync HEAD 915b475).

## What shipped (PR #403)

- `live_ci_workflow` (src/engine/adopt.py) emits a new final step — "pytest suite (a test suite ships with its CI runner; self-skips when tests/ is absent)" — on the full lane only (`if: steps.lane.outputs.control_only != 'true'`; heartbeat PRs never pay the suite). Always planted, the idea's simpler variant: in-job `[ ! -d tests ]` self-skip (no adopt-time conditional to go stale; self-heals when tests arrive), `pip install --quiet -r requirements.txt` when present, `pip install --quiet pytest`, then `-m pytest tests/ -q` — all on the gate's configured interpreter (threaded, not hardcoded). Docstring paragraph documents the class and the design fork.
- Staged (`<state_dir>/ci/substrate-gate.yml`) and installed (`.github/workflows/substrate-gate.yml`) copies both flow from the same function, so wired adopters inherit on the next upgrade/regen wave via the kit-owned regen; hosts whose tests genuinely fail see an honest red where they saw a tests-blind green.
- Tests: new `test_live_ci_workflow_plants_the_pytest_step_behind_the_fast_lane` (lane condition, self-skip, requirements handling, interpreter threading) + the fast-lane heavy-step count pin updated 2 → 3. Idea flipped shipped (window closes 2026-08-14) + README index entry moved to Shipped; CHANGELOG under `[Unreleased]` `### Added`; dist byte-pin regenerated.
- Verify at 629d8c2: `scripts/preflight.py` 8/8 green (pytest 1630 passed, 1 skipped); `dist/bootstrap.py check --strict` shows only the designed born-red HOLD (this card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the session.

## 💡 Session idea

Gate test step should honor the interview's declared `verify_command`: the adopt interview already captures a `verify_command` slot (src/engine/interview/question_bank.py:86, routed to templates/CLAUDE.md) — e.g. websites' real verify line is a four-suite pytest invocation plus the kit gate, and non-pytest adopters exist in principle — yet the gate's new pytest step hardcodes `-m pytest tests/ -q`. Teach `live_ci_workflow` to prefer the state-recorded `verify_command` (when filled and non-default) as the test-step command, falling back to the pytest default — one slot read, and the CI runner stops diverging from the verify line CLAUDE.md tells every session to run. Dedup: zero `verify_command` hits under docs/ideas/ (grepped this session).

## ⟲ Previous-session review

The #402 session (engagement wiring-STRENGTH) left an unusually cheap handoff: its baton entry named the idea file, the origin class, the lane, and the size, so this wake spent zero re-derivation — and its rider (fixing the #400 card's model line in-PR instead of batoning a one-token edit) is the discipline this card tries to keep. Miss, small: its heartbeat's "This wake" verify line said the weak-form advisory "no advisory (kit ci.yml is strong-form — the designed self-silence)" without naming the test that pins that self-silence, so a later regression would be found by re-running live rather than by a named fixture. System improvement worth keeping: when a heartbeat verify line claims a designed self-silence, name the pinning test alongside it — a claim with a fixture name survives context loss; a claim alone has to be re-proven every audit.
