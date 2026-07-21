# false-wall weak-cue cross-line bridge (v1.20.2, unreleased)

> **Status:** `in-progress`

**Session:** 2026-07-21 · substrate-kit · engine checker fix (required fleet-wide gate)

**About to do:** the reviewer found the wall-green class still open ACROSS A LINE BREAK — a
WEAK, subject-dependent, empty-family cue (`does not reproduce`) re-attaches to a genuine
standing wall on the next line via the `is_cleared` lookback / G1 lookforward bridge and
clears it. Probes N8 (`…reproduce and\nagents cannot merge…`) and N9 (no conjunction at all)
currently CLEAR and must RED. Root fix: partition repudiation cues into STRONG (wall-
referential — may bridge) vs WEAK (same-clause/same-line only). The cross-line lookback AND
G1 lookforward may clear only via STRONG cues (or the quote-covers G4 path); same-line
clearing keeps the full strong+weak set. Family gate + punctuation guard unchanged. Stricter
direction (safe). Version stays 1.20.2 (unreleased); CHANGELOG appended to the existing entry.

- **📊 Model:** opus-4.8 · high · runtime bugfix
- **⚑ Self-initiated:** NOT self-initiated — coordinator+reviewer-agreed root fix at merged
  SHA 1528de7; fresh PR on merged main.

## What shipped (PR #TBD)

_(to be completed as the deliberate final step — this card holds the PR born-red)_
