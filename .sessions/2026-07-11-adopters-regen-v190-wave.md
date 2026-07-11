# 2026-07-11 — adopters regen after the v1.9.0 distribution wave

> **Status:** `in-progress`

- **📊 Model:** fable-5 · medium · registry-regen — post-wave currency
  snapshot of the fleet adopter registry

## Scope (what is about to happen)

Regenerate `docs/adopters.md` via `python3 dist/bootstrap.py currency` now
that the kit-seat v1.9.0 distribution wave is merged: superbot-next #150
(d653ba1), websites #101 (7da9fbf), gba-homebrew #36 (31c8672), venture-lab
#32 (9b504e8). A PARALLEL worker is upgrading fleet-manager / superbot-games /
trading-strategy — their rows snapshot at whatever their main trees say at
regen time; the card's close-out records which of those three read v1.9.0
vs v1.8.0, tree-verified. Files: `docs/adopters.md` (generated output,
shipped as the tool emits it) and this card. No claim file — registry-regen
sessions ride the born-red card + immediately-opened PR as the in-flight
signal (precedent #135/#142/#161). NEVER `control/` or `bench/`.

## Close-out

(pending)
