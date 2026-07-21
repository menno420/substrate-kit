# false-wall clause split — bare (comma-less) conjunctions (v1.20.2, unreleased)

> **Status:** `in-progress`

**Session:** 2026-07-21 · substrate-kit · engine checker fix (required fleet-wide gate)

**About to do:** the merged #558 comma-anchored clause split (`,\s*(?:and|but|so|…)`) still
lets a BARE conjunction (no preceding comma) bleed a capability-agnostic cue across to blind
a genuine wall — reviewer probe `The freeze does not reproduce and agents cannot merge to
main.` currently CLEARS. Extend `_CLAUSE_SEP` to break on a whitespace-surrounded bare
` and | but | so | yet | however | though | although | whereas | while ` too, so the wall
lands in its own cue-less clause → RED. Stricter direction (more FPs stay red) is the safe
one; will report any real-adopter line newly red from over-split for allowlist/reword
routing. Version stays 1.20.2 (unreleased); CHANGELOG note appended to the existing entry.

- **📊 Model:** opus-4.8 · high · runtime bugfix
- **⚑ Self-initiated:** NOT self-initiated — coordinator-relayed reviewer finding at merged
  SHA 6ac9d3c; fresh PR on top of merged main.

## What shipped (PR #TBD)

_(to be completed as the deliberate final step — this card holds the PR born-red)_
