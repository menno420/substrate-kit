# 2026-07-14 · cross-branch ORDER-collision guard (build the #364 groomed idea)

> **Status:** `in-progress`

About to happen (opening declaration): build the guard groomed in
`docs/ideas/order-claim-cross-branch-collision-2026-07-14.md` (landed by
PR #364, merge `2a2d92b`) — the #362/#363 duplicate-work root cause. Scope:
an optional ` · order NNN` work-claim grammar segment (kit-owned constant in
`engine.grammar`), `bootstrap claim --order NNN` rendering it (with a
refuse-unless-`--force` guard when another live claim on a DIFFERENT branch
already names that order), and a `check_claims` cross-branch order-collision
advisory (advisory-only, never exit-affecting — posture preserved). Engine
change → dist regen byte-pin; tests for the collision fixture, the
no-false-positive lane, and the refusal/--force paths.

- **📊 Model:** Claude (Fable family) · high · feature/build

Run type: self-initiated · lab (per the #364 groom's named next step)
