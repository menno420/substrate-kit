# false-wall weak-cue cross-line bridge (v1.20.2, unreleased)

> **Status:** `complete`

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

## What shipped (PR #560)

Repudiation cues are partitioned into STRONG (wall-referential — `_STRONG_REPUDIATION_CUES`,
a strict subset of `_REPUDIATION_CUES`) and WEAK (everything else, subject-dependent). The
cross-line lookback and the G1 lookforward now call `_clause_cleared(strong_only=True)`, so a
WEAK cue (`does not reproduce`) can no longer re-attach to a genuine standing wall on the
neighbouring line — it clears same-clause only. Same-line clearing keeps the full set;
`repudiat` + `superseded` were added to both sets (preserving strong ⊆ full). Family gate and
punctuation guard unchanged.

Verified: probes N8/N9 + `but`/`so` newline + reversed-order + N10 all RED; C1–C5 clear;
same-line weak cue still clears; STRONG cues still bridge (lookback + G1). Adopter re-scan vs
merged-main baseline: **exactly 1 newly-red line** — superbot-next `docs/current-state.md:118`
(the weak-cue-next-line correction, the anticipated acceptable FP-red; #602 is blocked on its
L97 wall regardless) — **0 other** newly-red lines. Suite green (2073), ruff clean, dist
byte-stable, version stays 1.20.2 (unreleased).

## 💡 Session idea

Three consecutive reviews each found the SAME wall-green class one notch further out
(same-clause → comma-bleed → bare-conjunction → cross-line). The pattern is "a repudiation
signal reaches a wall it doesn't own." Idea: replace the ad-hoc cue list with a single
**`clears(cue, wall) = strong(cue) AND same_scope(cue, wall) AND same_or_empty_family`**
predicate, where `same_scope` is computed once (same clause / same line / bridge-eligible) and
STRONG-ness is a property of the cue — then every clearing path (same-line, lookback,
lookforward, future ones) routes through the one predicate instead of each re-deriving the
rule. That collapses the surface the reviewers keep probing into a single testable function.

## ⟲ Previous-session review

The #559 pass fixed the bare-conjunction bleed correctly but treated it as a *lexical* problem
(add a separator token) when the reviewer's N9 probe (no conjunction at all) shows the real
axis is *scope*: a weak cue must not cross a line boundary regardless of what punctuation or
conjunction sits between. This pass fixes the axis, not the token — the right altitude. **System
improvement it surfaces:** the `_MUST_STAY_RED` matrix should carry a small **generator** that,
for each weak cue, emits the same-clause-clears / cross-line-reds pair automatically (the idea
above), so the "one notch further out" regression can't recur a fourth time — the reviewers have
now demonstrated three times that hand-written fixtures trail the actual failure class.
