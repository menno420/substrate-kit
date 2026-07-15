# Session · 2026-07-15 · template-local-sync

> **Status:** `complete`

Intent: resolve the 4 template↔local-copy heading-drift pairs surfaced by the #399 `check_template_sync` advisory's first live run — judge direction per pair (default: local syncs FROM the template; fold genuinely-newer local content INTO the template where present), leaving the advisory clean on the kit tree.

- **📊 Model:** Claude 5 family · medium · docs-only

## What shipped (PR #400)

- Direction judged per pair, all 4 resolved:
  1. `docs/collaboration-model.md` ← template: added 'Routing work to the owner' + the rationalization-checkpoint sentence in 'Friction → guard' (the program-law link divergence is deliberate localization — this repo IS the kit, relative links are correct — left as-is, body-level so the heading checker stays silent).
  2. `docs/CAPABILITIES.md` ← template: added 'Posture decision rule — establish your venue first' with a local note reading pre-venue-token ledger entries as venue `any`; the local append log (genuinely local findings) untouched.
  3. `docs/ideas/README.md` ↔ `ideas-README.md.tmpl`, BOTH directions: local Frontmatter heading renamed to the template's generalized 'Frontmatter — the idea-outcome record' (B4/§5.4 reference kept in body prose); the two local-only index sections ('Shipped (survive window open)', 'Historical / pointer stubs') folded INTO the template — the local three-section lifecycle shape was the newer doctrine, and adopters inherit it on the next wave.
  4. `control/README.md` ← template: added 'Owner-assist output standard — every owner-facing output, not just asks' (also the resolution target of collaboration-model's canonical pointer, which previously dangled locally) + 'CI + auto-merge notes (learned live, 2026-07-09)'.
- Dist regenerated (template change embedded); CHANGELOG bullet under `[Unreleased]` `### Changed`.
- Verify at 697a82d: `scripts/preflight.py` 8/8 green (pytest 1620 passed, 1 skipped); `check --strict` template-sync advisory 0 findings (was 4).
- In-session friction, caught locally: first CHANGELOG placement broke keep-a-changelog order (new `### Changed` before `### Added` + duplicate of the existing Changed block) — `check_changelog_structure` + 3 pytest legs redded in preflight; folded the bullet into the existing block instead. The guard worked exactly as designed; no red push.

## 💡 Session idea

The advisory's message says "or record the deliberate divergence in the local file's prose" — but the checker has no suppression mechanism, so a deliberate divergence keeps firing forever (advisory fatigue is how nudges die). Add an opt-out marker the checker respects: an HTML comment on the local side, e.g. `<!-- template-sync: local-only "Heading title" — <one-line why> -->`, consumed by `check_template_sync` as a documented waiver per heading (waived headings reported once as a `template-sync-waived` info line, never as drift). Keeps the advisory clean-by-default while making legitimate repo-specific sections representable — today the only clean states are "identical heading sets" or "permanent advisory noise".

## ⟲ Previous-session review

The #399 session (template-sync advisory checker) did strong work: the checker paid for itself at birth by surfacing 4 real drift pairs, fixtures were thorough (12 tests), and the false-positive firewalls (fence-aware, slot patterns, live-traffic skips) were designed up front rather than patched in later. One genuine improvement it surfaces: it shipped the checker and left ALL 4 findings unsynced, handing the whole fix to the next wake as one baton item — reasonable slicing, but the two one-section pairs (collaboration-model, CAPABILITIES) were each a 2-minute sync that could have ridden the same PR, halving the handoff. Rule of thumb worth adopting: when a new checker's first run surfaces findings, fix the trivial subset in the same PR and baton only the judgment-heavy remainder.
