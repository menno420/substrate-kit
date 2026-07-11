# Session 2026-07-11 — adopter-registry regen after the v1.8.0 upgrade wave (kit seat)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** v1.8.0 distribution-wave close-out, kit-seat
slice — regenerate the GENERATED `docs/adopters.md` via `python3.10
dist/bootstrap.py currency` now that this seat's four adopters merged their
v1.7.1 → v1.8.0 upgrades on green (superbot-next #135 @ 3dfc194 · websites #85
@ 8abfe0a · gba-homebrew #28 @ 0a7689f · venture-lab #17 @ fb5ef4b). A PARALLEL
worker is mid-flight on fleet-manager / superbot-games / trading-strategy —
their rows read whatever the tree says at snapshot time (the `Generated:`
stamp is the snapshot time); their rows are NEVER hand-fixed. Registry-only +
this card; NEVER touched: `control/inbox.md`, `control/status.md` (no claim
file accompanies this session per the #135/#142 precedent — this born-red card
+ the immediately-opened PR is the in-flight signal). Verified pre-flight at
origin/main HEAD e88af57: no open PRs, `control/claims/` empty (README only),
no new inbox ORDER touching the registry.
