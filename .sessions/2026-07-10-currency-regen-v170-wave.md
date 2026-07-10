# Session 2026-07-10 — adopter-registry regen after the v1.7.0 upgrade wave

> **Status:** `in-progress`

- **📊 Model:** claude-fable-5 · medium · docs-regen (fleet registry currency)

**Scope (as declared, born-red):** distribution-wave close-out — regenerate
the GENERATED `docs/adopters.md` via `python3 dist/bootstrap.py currency` now
that four adopters merged their v1.6.0 → v1.7.0 upgrades on green
(superbot-next #116 @ a700975 · websites #62 @ e671cb3 · gba-homebrew #26 @
bc73da7 · venture-lab #13 @ ce22315). Registry-only + this card; NEVER
touched: `control/inbox.md`, `control/status.md` (the coordinator owns the
seat heartbeat — which is also why no `claimed-by:` line accompanies this
session; this born-red card + the immediately-opened PR is the in-flight
signal). Verified pre-flight: no open PRs, no live claim touching
`docs/adopters.md` or the currency checker.
