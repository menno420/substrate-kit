# Session 2026-07-10 — adopter-registry regen after the v1.7.1 upgrade wave (kit seat)

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** v1.7.1 distribution-wave close-out, kit-seat
slice — regenerate the GENERATED `docs/adopters.md` via `python3
dist/bootstrap.py currency` now that this seat's four adopters merged their
v1.7.0 → v1.7.1 upgrades on green (superbot-next #122 @ 1ba8607 · websites #74
@ a057140 · gba-homebrew #27 @ 16e64d7 · venture-lab #14 @ 7558cb2). A PARALLEL
worker is mid-flight on fleet-manager / superbot-games / trading-strategy —
their rows are expected possibly-stale in this snapshot (the `Generated:`
stamp is the snapshot time); their rows are NEVER hand-fixed. Registry-only +
this card; NEVER touched: `control/inbox.md`, `control/status.md` (the
coordinator owns the seat heartbeat — no `claimed-by:` line accompanies this
session per the #135 precedent; this born-red card + the immediately-opened PR
is the in-flight signal). Verified pre-flight at origin/main HEAD 415c37e: no
open PRs, no live claim in any `control/status*.md` touching
`docs/adopters.md` or the currency checker, no ORDER 012+ in the inbox.

## Close-out

(to be written)
