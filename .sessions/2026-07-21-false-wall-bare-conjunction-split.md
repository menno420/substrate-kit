# false-wall clause split — bare (comma-less) conjunctions (v1.20.2, unreleased)

> **Status:** `complete`

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

## What shipped (PR #559)

`_CLAUSE_SEP` now also breaks on a whitespace-surrounded bare (comma-less) conjunction
` and / but / so / yet / however / though / although / whereas / while `, closing the deeper
blind the reviewer found at merged 6ac9d3c — `does not reproduce and agents cannot merge`
now REDs. Whitespace on BOTH sides is required, so a conjunction that ends a wrapped line
stays a genuine sentence continuation for the lookback (no `p2_same_capability_wrap`
regression). Verified: all 5 bare-conjunction probes RED, 4 intended-clears GREEN, **0
`_FP_CLEAR` regressions, 0 real-adopter lines newly red** (fleet-wide diff of new vs the
merged-main baseline). Pinned one `_MUST_STAY_RED` variant per conjunction plus a
both-directions mutation guard. Suite green, ruff clean, dist byte-stable, version stays
1.20.2 (unreleased); CHANGELOG note appended to the existing false-wall entry.

## 💡 Session idea

The clause-split grammar (`_CLAUSE_SEP`) is now the single most safety-critical regex in the
gate, yet it's only exercised indirectly through clearing fixtures. Idea: a tiny property
test that asserts an INVARIANT — "for every `_REPUDIATION_CUES` cue C and every blocklist
wall trigger W, the string `C <sep> W` (each strong separator + each bare conjunction) leaves
W red" — generated combinatorially. That turns each future cue/conjunction addition into an
automatic bleed-negative, so the both-directions discipline extends to the separator axis
without hand-writing a fixture per pair (the exact gap that let the bare-conjunction blind
ship in #558).

## ⟲ Previous-session review

The #558 pass (this session's predecessor) correctly identified comma-bleed and added the
comma-anchored split, but anchored on the comma rather than on the conjunction — so the
bare form slipped through, caught only by a third re-verification. Good: it kept the
family-gate hardening as a second layer and the safety bar held (the miss was an
under-clear-of-nothing, i.e. it left a real wall green, which is the dangerous direction — a
useful reminder that "stricter" bugs hide better than "looser" ones and deserve the
combinatorial invariant above). **System improvement:** the fix and its predecessor both
edited one regex that three separate reviews probed; a `_CLAUSE_SEP`-specific unit test that
enumerates the boundary tokens (comma-conj, bare-conj, `; — : .`) with a labelled expectation
per token would make the regex's contract explicit and self-documenting for the next editor.
