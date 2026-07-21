# false-wall clearing exemptions — v1.20.2 (G1/G2/G4 + generated-render + allowlist)

> **Status:** `complete`

**Session:** 2026-07-21 · substrate-kit · engine checker fix (required fleet-wide gate)

**About to do:** relax `check_no_false_walls` CLEARING logic (v1.20.1 → v1.20.2) so it
stops retroactively redding adopter upgrade PRs on ALREADY-correct repudiation notes,
WITHOUT reopening the ancestor/section-sheltering hole #549 deliberately closed.

- **📊 Model:** opus-4.8 · high · runtime bugfix
- **⚑ Self-initiated:** NOT self-initiated — coordinator-directed engine checker fix
  packaged as v1.20.2, then two rounds of coordinator-relayed adversarial review fixes.

## What shipped (PR #558)

Attachment-based, family-gated clearing relaxations for the `false-wall` gate, plus the
two adversarial reviews' hardening. Genuine standing walls stay red; the standing bar held
throughout — a false positive that stays red is cheaper than a real wall that goes green.

- **G2** — same-clause repudiation-cue vocab (`never/not a standing "…" wall`,
  `was (based on) a false (standing) wall`, `does not reproduce`, and bare `false standing
  wall` only with a `superseded`/`proven` second signal).
- **G4** — position-aware `false`/`superseded` marker immediately AFTER a quote whose
  content is the wall phrase.
- **G1** — bounded same-family lookforward mirroring the wrapped lookback (1–2 lines,
  stops at blank line / new bullet / heading / dated bullet / contrast).
- **Class (b)** — generated-render exemption honoured ONLY on the known render path
  (`seat_digest_relpath` → `docs/seat-digest.md`), so the marker can't blanket-exempt a
  real doc (FIX B).
- **Class (c)** — false-wall findings ride the repo's generic REASON-REQUIRED allowlist
  seam (`engine.checks.allowlist`); the bespoke fail-open path was deleted (FIX D).
- **FIX A** — a mid-line comma+conjunction is now a clause boundary (closes the
  capability-agnostic comma-bleed blind); a same-clause different-family cue no longer
  clears (hardening).
- **G3 dropped as UNSAFE** (would clear genuine walls); motivating cases clear via G1+G2.

Verified: full suite green, ruff clean, `dist/bootstrap.py` rebuilt byte-stable, `check
--strict` clean except the designed born-red HOLD. Version homes all read 1.20.2.

## 💡 Session idea

The blocklist emits `agent-unlandable` under the `standing-platform-wall` rule (earlier in
order), which surprised the allowlist test — the emitted `kind` isn't obvious from the
phrase. Idea: have `check --explain-wall <phrase>` ALSO print the exact `false-wall:<rule>`
kind string a triager should paste into `check-exceptions.yml`, so an allowlist entry is
copy-paste-correct on the first try rather than discovered by a failing gate. Low-cost,
high-leverage for the venture-lab product-copy re-vendor that will use this seam.

## ⟲ Previous-session review

The predecessor v1.20.2 pass (this session's first cut) shipped the five gaps with a
both-directions fixture matrix but had two real holes the reviews caught: (1) it treated
comma as a non-separator without noticing a capability-AGNOSTIC cue could then bleed across
`, but` to blind a genuine merge wall — the family gate it leaned on doesn't fire for
empty-family cues; and (2) it built a parallel fail-open allowlist path when the repo
already had an audited reason-required seam. Both are now fixed. **System improvement it
surfaces:** an adversarial-review lane that specifically fuzzes each NEW clearing path with
"cue-of-a-different-capability-in-the-same-sentence" mutations would have caught FIX A
mechanically — worth a standing `_MUST_STAY_RED` generator that pairs every added cue with a
comma/conjunction-bleed negative, so the both-directions discipline extends to the bleed
axis automatically.
