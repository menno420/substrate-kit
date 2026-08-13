# 2026-08-13 — Regenerate docs/adopters.md after the v1.21.0 phase-3 wave

> **Status:** `complete` — branch `claude/adopters-regen-phase3`, PR #584. The
> regen commit precedes this card; the work is one generated file, complete at
> push, so the card lands complete (nothing partial exists for a born-red hold
> to protect).

- **📊 Model:** fable-5 · high · docs-only

## previous-session review

kit #583 (the phase-2 regen, `b9e9a57`) landed the registry with the stamp
`15:55:41Z` and carried the currency raw-step finding in its thread; its
citation correction (`:398-402`, not `:90`) was verified against this tree by
the fleet-manager review session (fm #855) before this regen built on it.
One thing it left that this session hit: no session card accompanied it, and
this PR's first CI round measured `--require-session-log` holding the merge —
hence this card.

## Shipped

- `docs/adopters.md` regenerated (`python3 dist/bootstrap.py currency`, stamp
  `2026-08-13T19:23:46Z`) over authenticated transports: 8 rows current
  (websites #499 · venture-lab #289 · idea-engine #899 · superbot-mineverse
  #144 landed this wave; superbot's `⚠️ DRIFT · v1.0.0` pin cell healed — the
  stale unauthenticated-raw copy expired), 4 rows honestly stale
  (superbot-games +DRIFT · trading-strategy, owner-skipped pending archive
  decision · gba-homebrew, upgrade parked on the BlocksDS rotation ·
  pokemon-mod-lab).
- pokemon-mod-lab reads clean instead of `unreadable`: private repos need the
  session's `add_repo` scope — the fleet-manager capabilities ledger carries
  the measured route.

## Verify

- `currency` exit 0, `UNREADABLE 0`, DRIFT only the true superbot-games rows.

💡 `--require-session-log` held this card-less regen PR while kit #583's
identical shape merged card-less hours earlier — worth one line in the kit's
CONTRIBUTING or the currency docs saying regen PRs carry a card like any
other, so the next regen session doesn't re-derive it from a red.
