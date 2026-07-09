# Session 2026-07-09 — P0: close the render/engage adoption gap (band KL-7)

> **Status:** `in-progress`

**Scope (owner directive, routed from the independent fleet review — superbot
`docs/eap/fleet-review-2026-07-09.md` §4):** both fresh adopters (superbot-next
AND websites) stranded identically — planted docs still under UNRENDERED
banners, `${...}` slots unfilled, `session_count` 0, `.claude/` inert, no CI.
Root cause is upstream in the kit: `adopt` plants-and-banners, but rendering
and enforcement are separate opt-in steps nothing forces. This band ships the
**born-red post-adopt engagement gate**: `check --strict` holds RED in an
adopted host until every UNRENDERED banner + `${...}` slot is gone, a CI
workflow runs the check, and the session loop has engaged — "enforce, don't
exhort" (PL-007) applied to onboarding itself. Plus: adopt stages the live
`substrate-gate.yml`, adopt output prints the engagement checklist, the
cold-adopt smoke asserts the full RED→ENGAGED→GREEN arc, D-ledger entry.

- **📊 Model:** fable-5 · high · feature build
