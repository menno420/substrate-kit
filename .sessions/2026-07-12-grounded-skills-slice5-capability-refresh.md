# 2026-07-12 — grounded-skills program, slice 5: capability refresh + venue-scoping + staleness

> **Status:** `in-progress`

- **📊 Model:** fable-5 · seat-worker · grounded-skills slice 5

## Scope (what is about to happen)

Implementing §7 slice 5 of the grounded-skills program plan
(`docs/planning/2026-07-12-grounded-skills-program.md`, merged PR #263) —
§4.2 in full: venue-scoped capability-ledger schema (venue tokens + extended
append-line grammar, homed in `src/engine/grammar.py` from the start per the
slice-4 lesson), CAPABILITIES.md.tmpl refresh (marker-fenced kit-owned seed
section, venue × operation seed rows with LAST-VERIFIED dates, two-line
posture decision rule, DISCOVERY RULE step 5 staleness clause on the
`cadence.staleness_days` knob), the NEW upgrade-time fenced-seed refresh in
`src/engine/upgrade.py` (the only channel reaching consumer-edited ledgers;
modified fences downgrade to a report line, never clobbered; the report
carries the Q-0270 collapse wording), and `check_capability_xref` extended in
place, advisory-only (append-line grammar + staleness advisories). Tests +
CHANGELOG `[Unreleased]` entry + dist rebuild. No other slices, no adopter
work, no release.

**Provenance flag:** Coordinator proceeded on plan §8 defaults (Q2=B
advisory, Q4=A) — provenance flagged per program rules.

Lane claim: `control/claims/claude-grounded-skills-slice5.md`
(deleted at close).
