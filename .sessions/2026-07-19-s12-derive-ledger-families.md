# S12 — auto-derive lint families from ledger bold titles

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S12 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md line 34) — "auto-derive lint families from ledger bold titles." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S11 shipped #533; baton advanced to S12).

## What I'm about to do

Generalize the R7 advisory `check_wall_ledger_agreement` (PR #498) from its
hardcoded `_FAMILIES` tuple (seeded only with merge/arm/flip) into the fuller
form its own R7 session-idea named: **auto-derive supplemental capability
families from the ledger's own `**bold title**` noun-phrases.** For each bold
title that appears in BOTH a `## Walls` correction row and a `## Append log`
entry (by canonical key), cross-check the two verdicts — turning R7 from
"catches the one known contradiction" into "catches any Walls⇄Append-log
disagreement." Purely additive (seeded families untouched → zero regression),
advisory-only, off `STRICT_SUBCHECKS`. +tests, dist rebuilt + byte-pinned.

- **📊 Model:** opus-4.8 · medium · feature build
