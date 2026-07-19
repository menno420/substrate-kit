# Session · 2026-07-19 · stale-wall-advisory

> **Status:** `in-progress`

Intent: task R5 under the night-run groom (`docs/planning/2026-07-19-night-run-idea-groom.md`
R5 entry) — add an ADVISORY-only engine check `src/engine/checks/check_stale_walls.py`
that surfaces any `wall` ledger row in `docs/CAPABILITIES.md` whose verification date is
older than the staleness window (`cadence.staleness_days`, default 14). It is the
enforcement analogue of the DISCOVERY RULE's staleness step — warn-only, NEVER exit-affecting.

- **📊 Model:** Opus 4.8 · high · feature build
- ⚑ Self-initiated: none — R5 is baton-directed work (dispatched from the night-run groom
  R5 entry), not self-initiated.

About to: mirror `check_folded_gate` — create the advisory check + `FINDING_KIND =
"stale-wall"`, wire it on the `posture="advisory"` seam in `cmd_check` (NOT
`_extra_check_findings`, which is exit-affecting — deviation from the recipe to honor
"advisory, not red"), add `checks/check_stale_walls.py` to `MODULE_ORDER` in
`src/build_bootstrap.py`, rebuild `dist/bootstrap.py`, and add
`tests/test_check_stale_walls.py` mirroring `tests/test_check_folded_gate.py` (incl.
`test_not_in_strict_subchecks`). Born-red card holds the PR on the Session-gate HOLD; flips
to `complete` last.

## What shipped

_(pending — flipped to `complete` as the deliberate final step.)_
