# 2026-07-11 — run-8 countermeasure: close the CONTENT gap

> **Status:** `in-progress`

- **📊 Model:** fable-5 · high · feature build

## Scope (what is about to happen)

Coordinator-dispatched worker slice (claim `control/claims/run8-content-gap.md`
on main @ 83c5c39 before build). Run-8 (PR #215, report
`bench/results/cold-start/2026-07-11-run08/report.md`) proved the delivery
chain works — ON arms opened `HANDOFF.md` in their FIRST tool call, first
card-continuity conversion — but the payload was empty: the auto-draft card
carried 8 unresolved `[[fill:]]` slots, ON ended `check --strict` exit=1, and
the judge ruled "orientation cost paid; intended benefit not realized" (ON M1
2223/2506 vs OFF 905/1628 on T2/T4). Three deliverables, each with tests:

1. **Substantive arrival surface** — pre-fill the auto-draft from harvestable
   facts (reflog commit subjects, prior card's resolved pointer, the existing
   changed-file evidence), reserve `[[fill:]]` for the genuinely unknowable,
   and let `HANDOFF.md` carry an auto-derived trail when the card's pointer
   is unresolved (`src/engine/loop/handoff.py`, `handoff_pointer.py`).
2. **Cut orientation cost** — trim the run-8-observed ceremony reads:
   dedupe the CLAUDE.md/AGENT_ORIENTATION read-first lists + verify blocks,
   route (not front-load) CAPABILITIES/orientation, condense CONSTITUTION
   boilerplate (`src/engine/templates/*.tmpl`). Bounded to observed waste.
3. **Unfilled-slots → strict-RED fix** — an unadopted auto-draft (engine-
   authored `drafted` card nobody touched) is ADVISORY in the bare
   `check --strict` mtime-fallback lane; gate mode (`--require-session-log`
   / `--session-log` / `--added-card`) keeps blocking
   (`src/engine/checks/check_session_log.py`, `src/engine/cli.py`).

CHANGELOG `[Unreleased]` entries (next-release payload; NO release cut this
slice). Dist regenerated (byte-pin). NOT touched: `bench/rubric*` (parallel
§3 pin lane, claim `rubric-t5-v2-align.md`), `control/inbox.md`, sibling
cards, index.json.

## Close-out

(to be written — this card flips complete as the deliberate last step)
