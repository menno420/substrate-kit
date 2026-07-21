# false-wall clearing exemptions — v1.20.2 (G1/G2/G4 + generated-render + allowlist)

> **Status:** `in-progress`

**Session:** 2026-07-21 · substrate-kit · engine checker fix (required fleet-wide gate)

**About to do:** relax `check_no_false_walls` CLEARING logic (v1.20.1 → v1.20.2) so it
stops retroactively redding adopter upgrade PRs on ALREADY-correct repudiation notes,
WITHOUT reopening the ancestor/section-sheltering hole #549 deliberately closed. Every
relaxation stays attachment-based (same-clause / same-bullet / immediately-adjacent) and
family-gated. Gaps: G2 cue vocab · G4 false-after-quote (both sides) · G1 bounded
same-family lookforward · class (b) generated-render exemption (marker-keyed) · class (c)
optional `.substrate/check-exceptions.yml` product-copy allowlist. G3 (dated-bullet
continuation) evaluated and DROPPED as unsafe/redundant with G1 — noted, resident-reword
fallback. Full fixture matrix (both directions), dist rebuilt, packaged as v1.20.2.
Standing bar: a false positive that stays red is cheaper than a real wall that goes green.

- **📊 Model:** opus-4.8 · high · runtime bugfix
- **⚑ Self-initiated:** NOT self-initiated — coordinator-directed engine checker fix
  packaged as v1.20.2; PR left born-red pending independent adversarial review.

## What shipped (PR #TBD)

_(to be completed as the deliberate final step — this card holds the PR born-red)_
