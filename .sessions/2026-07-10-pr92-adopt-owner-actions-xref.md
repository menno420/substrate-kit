# 2026-07-10 — gen-2: adopt orphaned #92 + OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (queue item 8)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · high · adopt+engine (adopt PR #92, then one scoped
  checker PR: the OWNER-ACTION ↔ CAPABILITIES cross-reference advisory)

## Scope (as declared)

Adopt the orphaned PR #92 (queue item 10, four upgrade-UX fixes — READY, CI green,
behind main, no claim; status.md hands off the branch update): merge origin/main into
its branch, resolve the docs/ideas/README.md conflict (both #92 and #95 restructured
it), land it. Then build queue item 8: an advisory checker cross-referencing
⚑ OWNER-ACTION items in control/status.md against docs/CAPABILITIES.md, mirroring
check_claims.py's advisory posture (warns, never fails the strict gate). Claimed on
`control/status.md` via PR #97 (`claimed-by: pr92-adopt+queue-item-8 kit-lab-gen2
2026-07-10T04:11:37Z`). No pin paths; `control/` writes only in the claim (#97) and
the final status close.
