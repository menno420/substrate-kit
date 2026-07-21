# false-wall quoted-wall bridge gate — the definitive root fix (v1.20.2, unreleased)

> **Status:** `complete`

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

## What shipped (PR #561)

Gated BOTH cross-line bridges (the `is_cleared` lookback + the G1 lookforward) on
`_wall_is_quoted(line, match_span)` — a wall clears across a line break ONLY when its phrase
sits inside a `"…"` / `` `…` `` quote on its own line. Legitimate cross-line clears MENTION
(quote) the wall; every hole ASSERTS it bare. This supersedes the #560 weak/strong bridge
restriction (`strong_only` and `_STRONG_REPUDIATION_CUES` dropped; same-line clearing keeps
the full cue set). Family gate + punctuation guard unchanged. Reworded the adopter
`CONSTITUTION.md` template so its `no standing … wall` repudiation clears same-line (no
cross-line dependency) — fixes the kit's own tree and the rendered adopter copy on re-render.

Verified: probes N8/N9/S1/S2/S3/S5 RED; the full {quoted,unquoted}×{weak,strong}×{lookback,
lookforward} 8-cell matrix (4 RED, 4 CLEAR); C1/C2/C4/C5/C6 clear. Adopter re-scan vs baseline:
3 newly-red (all legit two-line-quote repudiations — idea-engine CONSTITUTION render clears on
re-render, venture-lab guards/owner-action need reword/allowlist), 0 newly-clear. Suite green
(2073), ruff clean, dist byte-stable, version stays 1.20.2 (unreleased).

## 💡 Session idea

Every one of the four rounds broke on a two-line construct the fixture set didn't cover, and
this round surfaced a NEW failure axis at adopter-scan time (two-line-spanning quotes) that no
fixture predicted. Idea: add a **corpus-replay guard** — a checked-in file of the real adopter
repudiation lines (the idea-engine/venture-lab/superbot-next constructs), each tagged
clear/red with its rationale, run as a parametrized test. It turns "the reviewer found another
adopter line" into a fixture the moment it's seen, so the checker is always validated against
the actual shapes the fleet writes, not just synthetic minimal probes.

## ⟲ Previous-session review

The #560 pass (weak/strong partition) correctly localized the problem to cues but fixed the
wrong variable: it asked "which cues may cross a line?" when the reviewer's root analysis shows
the right question is "may THIS OCCURRENCE cross a line at all?" — a property of the wall's
form (quoted vs asserted), not the cue's strength. That's why a strong cue still leaked. The
quote-gate reframes the whole bridge around the wall, which is why it closes weak AND strong in
one rule. **System improvement:** the three-round escalation (same-clause → comma → bare-conj →
cross-line) shows the checker's clearing surface is under-specified; the corpus-replay guard
above plus a one-paragraph "clearing contract" doc (what may clear a wall, and the single
`quoted-wall ⇒ may bridge` invariant) would give the next editor the whole rule at a glance
instead of reverse-engineering it from four layered fixes.
