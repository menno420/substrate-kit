# 2026-07-12 — auto-merge-enabler: arm claim/* branches (end the #293 stall class)

> **Status:** `complete`

- **📊 Model:** fable-5 · seat worker slice

## Scope (what is about to happen)

Widen the auto-merge-enabler's branch-prefix arming from `claude/`-only to
`claude/` + `claim/` — the verified stall class from kit PR #293 (a control
fast-lane claim PR on a `claim/*` head sat green+clean unarmed for ~2 h until
superseded by #297 on a claude/* branch). Both copies: (1) the kit's OWN
`.github/workflows/auto-merge-enabler.yml`; (2) the kit-owned generated
adopter enabler (`engine.adopt.automerge_enabler_workflow` defaults +
`config._default_automerge`), so the fix reaches the fleet at the next
release wave. Plus: regression tests, the guards-playbook note, CHANGELOG
`[Unreleased]`, dist rebuild (byte-pin). Claim: kit PR #299.

## What happened

- **Option (a) taken — widen the prefix condition, not doctrine-pin
  claude/-only.** Decide-and-flag rationale: no doctrine anywhere mandates
  claude/-only heads (the enabler is explicitly parameterized via
  `substrate.config.json → automerge.branch_patterns`, and the wave-A
  close-out's own session idea proposed carrying both prefixes); `claim/*`
  is a live seat convention (#293). One-line condition widening ends the
  class; renaming a convention fleet-wide would not.
- **Kit's own workflow:** `.github/workflows/auto-merge-enabler.yml` job
  `if:` now arms `claude/*` OR `claim/*` (comment cites #293).
- **Adopter-shipped generated enabler:** `engine.adopt.
  DEFAULT_AUTOMERGE_BRANCH_PATTERNS` → `("claude/*", "claim/*")` and
  `engine.lib.config._default_automerge()` → same list, so every
  adopt/upgrade regen carries the fix fleet-wide at the next release wave.
  Residual edge (playbook-noted): a config-baked explicit
  `branch_patterns` pins the adopter's own list.
- **Regression tests:** `tests/test_adopt.py` —
  `test_automerge_enabler_default_arms_claim_branches` pins both prefixes
  in the constant, the generated workflow expression, and the config
  default; shape + fallback-on-empty tests widened. Suite 1203 → 1204,
  all green on 3.10.
- **Playbook:** `docs/operations/auto-merge-guards.md` — new default +
  the "branch-prefix stall gotcha" subsection (green+clean forever,
  enabler job skipped; the two residual edges).
- **CHANGELOG:** `[Unreleased]` Fixed entry.
- **Dist:** rebuilt via `python3 src/build_bootstrap.py` (829339 B,
  print==disk); `python3 dist/bootstrap.py check --strict` green except
  this card's designed born-red hold, cleared by this flip.
- Mid-flight coordinator ping on #300's three reds triaged: all three were
  the DESIGNED born-red hold (kit-quality's log prints "HOLD (by design)
  ... nothing to investigate"; "Kit test suite" + "Cold-adoption smoke"
  are legacy alias contexts that hard-fail whenever kit-quality is not
  success). No real failure existed.

## 💡 Session idea

A convention-drift guard for the enabler patterns: a small advisory in
`currency`/`upgrade` that diffs an adopter's config-baked
`automerge.branch_patterns` against the kit default and flags a baked list
that is missing a kit-default prefix — the residual edge this fix cannot
reach (a config written before this release pins `["claude/*"]` silently
and re-inherits the #293 stall class the day its seats open a claim/* PR).

## ⟲ Previous-session review

The wave-A v1.15.0 close-out (#298 card) did exactly what a close-out
should: it converted its live friction into a STRUCTURAL flag on the
heartbeat AND a session idea naming the two candidate fixes — this slice
executed that idea nearly verbatim, which is the friction → guard loop
working end-to-end within 24 h. Improvement it surfaces: the stall was
visible for ~2 h as a green+clean PR with the enabler job SKIPPED — a
skipped arming job is silent by design, so the class was only caught by a
human-shaped "why hasn't this merged" check; the session-idea guard above
(or an unarmed-green sweep in the failsafe wake) would make it
self-announcing.
