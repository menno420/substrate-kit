# Session card — kit self-pin version-truth

> **Status:** `in-progress`
> **📊 Model:** opus-4.8 · effort high · task-class: kit-fix (drift-elimination)

## Scope
Decide-and-flag (MANDATE / fm ORDER 048) the parked "kit self-pin version-truth" ⚑ ruling: option **A** — make the kit's own `substrate.config.json` `kit_version` track its release, so `currency` / `docs/adopters.md` stops emitting the only permanent tree-internal false-DRIFT on substrate-kit itself.

## What I'm about to do
- Bump `substrate.config.json` `kit_version` 1.0.0 → 1.18.0 (make the data true).
- Add `substrate.config.json` as a third synced write target in `scripts/cut_release.py` so the pin advances at every release cut (root cause: the release path never touched it).
- Extend the version-equality test to include `substrate.config.json` `kit_version` so it cannot silently re-drift.

## Provenance
Coordinator-decided under fm ORDER 048 (decide-and-flag reversible calls). The prior heartbeat parked this as an A/B owner ⚑; RISK ✅ contained + reversible, no adopter writes → decided A and shipped.
