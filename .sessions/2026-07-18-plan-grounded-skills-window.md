# Session — plan grounded-skills window + backlog groom

> **Status:** `complete`

📊 Model: Opus (family) · high · idea/planning
🎯 Scope: Produce a docs/planning grounded-skills execution plan (measurement window opens 2026-07-19), groom the ideas backlog into sized slices, and update the control/status.md heartbeat baton to point at the groomed list.

## What I'm about to do
- Read `docs/operations/grounded-skills-measurement.md` + `docs/planning/2026-07-12-grounded-skills-program.md`; write a concrete execution plan with 2–4 sized slices a session can pick up from 2026-07-19 on.
- Groom `docs/ideas/` + the 💡 session-idea lines on recent `.sessions/` cards (#455–#468 era); classify each buildable-now / needs-planning / owner-gated / dead.
- Overwrite `control/status.md` heartbeat: corrected next-2 baton pointing at the groomed list; keep the routine block, plain `kit: v1.19.0`, standing ⚑ blocks.

## What I did
- Wrote `docs/planning/2026-07-19-grounded-skills-window-run.md` — a de-risked execution plan for the grounded-skills measurement window (opens 2026-07-19; self-authorizing via the standing baton): 4 sized slices GSW-1..4 plus the three run-corrupting traps (shallow-clone zeroes M4, harness PL-008 UNVERIFIED → spot-check, report docs-gate reachability).
- Groomed the open ideas backlog into buildable-now (B-1 guard-surface census · B-2 CI self-row stamp automation · B-3 fast-lane head-prefix ⇄ enabler symmetry lint), needs-planning, owner-gated, and dead/do-not-queue (the 3-surface guard-parity thread is CLOSED — #459/#463/#465/#466 — do not re-queue).
- Updated the `control/status.md` baton to point at the plan + groomed slices.

## Verify
- `python3 -m pytest tests/ -q` → 1768 passed, 1 skipped (commit 31bc31c).
- `python3 dist/bootstrap.py check --strict` → clean but for the by-design born-red HOLD, which this flip clears.

💡 Session idea (Q-0089): Promote the harness's "shallow-clone zeroes M4" trap from prose into an enforced refuse-to-publish. `scripts/measure_grounded_skills.py` already flags shallow repos and nulls M4; make it emit a loud REFUSE marker in the `--json` output (or exit non-zero) when JSON is requested on a shallow clone, so a window-run session physically cannot publish a null-M4 report as if it were real. Enforce-don't-exhort applied to the measurement harness — small, test-coverable, and deduped (grepped `docs/ideas/`: no existing idea covers a harness self-guard).

⟲ Previous-session review: `2026-07-18-guard-parity-strict.md` (PR #466) closed the guard-parity thread cleanly — the third enforcing surface (`bootstrap check --strict` sub-checks) pinned via a single-source `STRICT_SUBCHECKS` + a bidirectional parity test. Right "one source, no drift" instinct. What it left thin: its heartbeat marked the buildable backlog "dry" with only a one-line date baton for the grounded-skills window and no executable steps — exactly the gap this session filled. System improvement: a heartbeat that writes an honest "backlog dry" line should be required to either point at a date-gated planning doc with executable slices OR say plainly "nothing to plan beyond X" — so a dry readout never hands the next wake a bare date. (Honesty-guard extended to the dry-baton case.)
