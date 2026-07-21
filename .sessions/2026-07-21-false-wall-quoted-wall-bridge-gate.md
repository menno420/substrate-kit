# false-wall quoted-wall bridge gate — the definitive root fix (v1.20.2, unreleased)

> **Status:** `in-progress`

**Session:** 2026-07-21 · substrate-kit · engine checker fix (required fleet-wide gate)

**About to do:** the reviewer diagnosed the ROOT cause behind three rounds of cue-by-cue
patching: the cross-line bridge itself (the `is_cleared` lookback AND the G1 lookforward) is
the hole. It rejoins `prev+wall` / `wall+fwd` and re-runs `_clause_cleared`; the family gate
can't block an empty-family neighbour cue, so ANY cue — weak OR strong — reattaches to an
unrelated BARE wall on the next line (probes S1/S2/S3/S5). Definitive fix (reviewer-designed):
gate BOTH cross-line bridges on **the matched wall phrase being QUOTED** — bridge across a
newline only when the wall sits inside `"…"`. Every legitimate cross-line clear MENTIONS
(quotes) the wall; every hole ASSERTS it bare. Unquoted wall → no bridge (same-line clearing
unchanged); quoted wall → bridge with the full cue set. This SUPERSEDES the #560 weak/strong
bridge restriction (drop `strong_only`). Family gate + punctuation guard unchanged. Version
stays 1.20.2 (unreleased); CHANGELOG appended.

- **📊 Model:** opus-4.8 · high · runtime bugfix
- **⚑ Self-initiated:** NOT self-initiated — reviewer-designed root fix at merged 7e92d1c;
  fresh PR on merged main.

## What shipped (PR #TBD)

_(to be completed as the deliberate final step — this card holds the PR born-red)_
