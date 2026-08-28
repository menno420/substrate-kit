# 2026-08-28 — OD-24 review round session 2: worklist pointer + false negatives 13/17/18

> **Status:** `in-progress` — born-red hold; flip is the deliberate last step.

- **📊 Model:** fable-5 · high · runtime bugfix
- **📍 Venue:** cloud-container

## Mission

The review round's step-3 first fixes, per fleet-manager's genesis dig
(fm `docs/findings/2026-08-28-substrate-kit-genesis-dig.md` §11) and the
v1.21.0 follow-up worklist's own restated fix order (fm
`docs/findings/2026-08-13-substrate-kit-v1210-followups.md`, tail):

1. **Route the kit to its own worklist** (gap #5, the smallest unrouted fix):
   supersede `docs/NEXT-TASKS.md` — actively false since 2026-07-17 (it tells
   the next session to distribute v1.18.0; v1.21.0 has been current since
   2026-08-13) — with a pointer to the fm-side worklist and round thread.
2. **Fix the false-negative family in `src/engine/checks/check_no_false_walls.py`**
   — the checker failing at its one job, each reproduced against the
   published v1.21.0 asset before the fix:
   - row 13 (dist `:5873`): a qualified reassertion after a mention
     predicate (`…rule is false in staging but true in production`) clears;
   - row 17 (dist `:5780`): the occurrence mask never reaches
     `_DATED_LINE`/`_FALSE_LABEL`, so `FALSE "agents cannot merge", agents
     cannot merge` and the dated-supersession variant pass strict;
   - row 18 (dist `:6036`): an unterminated digest BEGIN fence exempts every
     remaining line of the render path — fails open.
3. Regenerate `dist/bootstrap.py` via `python3 src/build_bootstrap.py`;
   tests + `scripts/preflight.py` green on real exit codes.

Out of scope, owner-gated or held: any release or adopter rollout (fixes
land on `main`; the cut is its own owner-said-go session), Move 1, all §10
dispositions, AGENTS.md.
