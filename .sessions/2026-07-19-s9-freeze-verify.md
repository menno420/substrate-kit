# S9 — `--freeze --verify` companion (re-hash sidecar, non-zero on mismatch)

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S9 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md) — "`--freeze --verify` companion — re-hash sidecar, non-zero on mismatch." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S8 shipped #527; baton advanced to S9).

## What I'm about to do

Add a `--verify PATH` mode to `scripts/measure_grounded_skills.py`, the automated inverse of the R10 `--freeze` self-citation: given a previously `--freeze`'d artifact (or its `<artifact>.freeze` sidecar), re-hash the artifact's exact bytes with sha256 and compare to the digest the sidecar pinned. Exit 0 on match, non-zero on mismatch / missing artifact / missing-or-malformed sidecar. Standalone mode — performs no measurement, so it needs no `--clone`/`--local`/`--json`. Tests include the round-trip (`--freeze` then `--verify` passes) and a tampered-artifact case (`--verify` fails non-zero). Standalone `scripts/` file — not in MODULE_ORDER, dist untouched.

- **📊 Model:** opus-4.8 · medium · feature build
- **⚑ Self-initiated:** [[fill: at flip]]
- **💡 Session idea:** [[fill: at flip]]
- **⟲ Previous-session review:** [[fill: at flip]]
