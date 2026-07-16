# Session · 2026-07-16 · archive-ready-s1

> **Status:** `complete`

Intent: baton item 1 — archive-ready close-out slice S1 (checklist doctrine + note template, docs-only) per docs/planning/2026-07-15-archive-ready-close-out-plan.md §5.

- **📊 Model:** Claude Fable · low · docs build
- ⚑ Self-initiated: no — baton-named (control/status.md Next-2 item 1 at sync HEAD e8a00fc); failsafe wake 2026-07-16T00:05Z, no ORDER >024, `currency --check` exit 0.

## What shipped (PR #412)

- `src/engine/templates/archive-ready.md.tmpl` — the archive-ready note skeleton carrying the plan-§2 section table as sections in the KL-5 `[[fill:]]` slot grammar: true state · open PR/claims/branch disposition · routine state · unreleased-payload park · ⚑ owner-actions · fresh-session resume path · chat-only confirmation. Routine state is a REQUIRES-PROBE slot (wholesale replacement with live probe output only — the realized stale-routine-record failure, plan §4.2); the confirmation slot is never drafted complete. No `${}` placeholders (bank-slot guard) and every backticked pointer resolves per the template pointer guard.
- `docs/operations/archive-ready-close-out.md` — the binding checklist doctrine: when the ritual runs, the section-by-section checklist, the slot rules (live facts only; REQUIRES-PROBE; confirmation written last), and the engine⇄session division of labor (plan §3). Linked from the operations index (`docs/operations/README.md`).
- `tests/test_template_pointer_guard.py` — one `_KIT_SELF_REFS` entry for the doctrine home the template names (the guard's own category-(c) mechanism; file exists in this repo).
- CHANGELOG `[Unreleased]` `### Added` entry; `dist/bootstrap.py` regenerated for the template embed only — no engine logic changed.
- Decide-and-flag: the badge allowlist (check_badges) has no draft token, so the template's badge is the terminal `archive` and an unresolved `[[fill:]]` slot IS the draft-state signal — one signal, and exactly what S4's advisory will key on (plan §6 "zero fill remnants"). Rejected for S1: adding an `archive-draft` badge token (engine-code change, out of the docs-only slice).
- Verify at b8250d9: `scripts/preflight.py` 9/9 green (pytest 1652 passed, 1 skipped); `dist/bootstrap.py check --strict` shows only the designed born-red HOLD (this card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the heartbeat commit.

## 💡 Session idea

Draft-state doctrine for evidence-drafted docs/ artifacts: KL-5 cards use Status `drafted` and escape check_badges only because `.sessions/` is not badge-scanned — but S2's `archive-prep` verb will draft into `docs/retro/`, where check_badges DOES run and the allowlist (archive, audit, binding, historical, ideas, living-ledger, owner-guidance, plan, reference) has no draft state; this session hit that as a red pytest leg (test_rendered_templates_are_badge_and_link_clean rejecting `archive-draft`). Before S2 ships, canonicalize the rule this session decided ad hoc — "badges are terminal; unresolved `[[fill:]]` slots are the draft-state signal" — as one line in the badge checker's doc/docstring plus an S2 test asserting a drafted note carries an allowed badge, so the next drafting verb doesn't rediscover the wall. Dedup: zero draft-state/badge-token hits in docs/ideas/ (grepped this session; nearest neighbors are model-line-checker-false-red and the archive-ready idea itself).

## ⟲ Previous-session review

The #411 ender left the cheapest possible failsafe pickup: baton item 1 named the plan path, the slice (S1), and the sizing ("docs-only") verbatim, and the routine-state record (failsafe armed as dead-man bridge, ⚑ discrepancy vs ORDER 024 recorded neutrally) matched exactly what this wake observed — zero re-derivation, zero surprise. Miss, small: neither the plan's S1 text nor the baton named the standing walls every template addition hits, and this session found one as a red pytest leg (badge-token allowlist) after preflight was already running. Workflow improvement: a template-add checklist line for plan slices that touch `src/engine/templates/` — badge token from the allowed set · pointer-guard resolution tables · no `${}` outside bank slots · dist regen — would turn that predictable first-red into a pre-write checklist; this card's "What shipped" bullets carry it for the S2 reader.
