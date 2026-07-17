# Session card — kit self-pin version-truth

> **Status:** `complete`
> **📊 Model:** opus-4.8 · high · mechanical refactor

## Scope
Decide-and-flag (MANDATE / fm ORDER 048) the parked "kit self-pin version-truth" ⚑ ruling: option **A** — make the kit's own `substrate.config.json` `kit_version` track its release, so `currency` / `docs/adopters.md` stops emitting the only permanent tree-internal false-DRIFT on substrate-kit itself.

## What I'm about to do
- Bump `substrate.config.json` `kit_version` 1.0.0 → 1.18.0 (make the data true).
- Add `substrate.config.json` as a third synced write target in `scripts/cut_release.py` so the pin advances at every release cut (root cause: the release path never touched it).
- Extend the version-equality test to include `substrate.config.json` `kit_version` so it cannot silently re-drift.

## Provenance
Coordinator-decided under fm ORDER 048 (decide-and-flag reversible calls). The prior heartbeat parked this as an A/B owner ⚑; RISK ✅ contained + reversible, no adopter writes → decided A and shipped.

## Shipped
- `substrate.config.json` `kit_version` 1.0.0 → 1.18.0 (data made true).
- `scripts/cut_release.py` — `substrate.config.json` added as a third synced version-home write target (was config.py + pyproject.toml); dry-run `cut_release.py 1.19.0` now emits the third diff.
- `tests/test_bootstrap.py` — new drift-brake `test_substrate_config_kit_version_matches_kit_version`; `tests/test_cut_release.py` fixtures extended for the third home.
- Verify: `python3 -m pytest tests/ -q` → 1721 passed, 1 skipped; `dist/bootstrap.py check --strict` passes except the intended born-red HOLD. Post-merge: `dist/bootstrap.py currency` flips substrate-kit's own row ⚠️ DRIFT → `current` (currency is a remote origin/main scan; self-heals after landing).

## 💡 Session idea (Q-0089)
`currency` is remote-only — it reads `substrate.config.json` from origin/main, so a pin/version fix like this one cannot be shown green in-session and must be trusted to "self-heal post-merge." Add a `currency --local` / `--self` mode that scans the working tree for the SOURCE repo's own row, so version-truth fixes are verifiable in the same session that makes them. Closes the "can't verify until landed" gap this very PR hit — turns a trust-me into a proof.

## ⟲ Previous-session review (Q-0102)
Prev session (2026-07-16→17 fresh-start cleanup, #437 + close #436): did well — recorded the ~07-15 auto-mode classifier freeze as durable doctrine (CAPABILITIES append-log + CONSTITUTION template correction) and left the failsafe armed as the successor's dead-man bridge (good stateless hygiene). Missed — it parked the kit-self-pin §7 ruling as an owner A/B ⚑ though its OWN RISK line marked both options ✅ contained + reversible + no adopter writes: that is the exact decide-and-flag profile (fm ORDER 048 / Q-0240), so it should have been decided in-session, not routed to the owner (ORDER 008's own principle — owner attention is the scarcest resource). System improvement (friction → guard, Q-0194): an advisory that flags any ⚑ owner block whose RISK is all-✅ AND whose HOW names no console/settings/secret/money action as "decide-and-flag, not an owner ask." Captured as a later slice, not built here (single-slice discipline).
