# Session — R2 /scope-backlog-item skill

> **Status:** `complete`

📊 Model: Opus 4.8 · high · feature build
🌿 Branch: `claude/scope-backlog-item-skill`
📅 2026-07-19

## Scope
Build the R2 `/scope-backlog-item` skill — turn a raw backlog item into a turnkey recipe
or an owner ask (chase-origin → fuller-picture → classify → sized recipe with traps →
retarget baton), making the standing "when no executable work is left, plan" order turnkey.

## What shipped (PR #490)

- **R2 `/scope-backlog-item` skill** added to `src/engine/skills/skills.py`: a new
  registry-dict entry (`name: scope-backlog-item`, `capabilities: []`, `grounds: []`,
  inserted after `intake`) plus the `_SCOPE_BACKLOG_ITEM_BODY` prose. The skill scaffolds
  the planning-recipe arc turnkey — chase the item's origin → Q-0254 fuller picture →
  classify (buildable-now sized recipe with traps / owner-gated six-field ⚑ / dead) →
  **step 5: retarget the coordinator's `## Next-2 baton` in `control/status.md`** so the
  next cold-start session lands on real, resolvable work. This makes the standing "when no
  executable work is left, plan" order a one-command procedure instead of improvised prose.
- **Ordered test list** in `tests/test_skills.py` updated to include `scope-backlog-item`
  in registry order (after `intake`).
- **Dist rebuilt** via `python3 src/build_bootstrap.py` (byte-pin clean).
- **Adopter `docs/SKILLS.md` index** auto-regenerates from the registry — no hand edit.

## Verification

- `python3 -m pytest tests/ -q` → **1822 passed** (full suite green).
- Skills suite: **43 skills tests pass**.
- `python3 dist/bootstrap.py check --strict` → byte-pin clean (`test_committed_bootstrap_is_current`).
- PR #490 auto-merges on green CI once this card flips `complete` (born-red hold released).

## 💡 Session idea

**A `check_baton_resolves` advisory (kit-quality / `check`) that verifies every
`## Next-2 baton` entry in `control/status.md` names a *real, resolvable* recipe or
plan path** — e.g. the `docs/planning/*.md` file and the `R<n>` anchor it cites must
exist on disk. Step 5 of the very skill shipped this session is "retarget the baton …
leave it pointing at real, cold-startable work" — but nothing mechanically checks that
the pointer resolves, so a baton can silently name a groom entry that was renamed,
consumed, or never written, and the next cold-start session boots onto a dangling
reference. This is the enforcement companion to the skill's prose promise: advisory-only
(same posture as `check_status_current` / `check_model_line`), so it nudges without
pre-reddening adopters. Deduped: grepped `docs/ideas/` + the groom doc — the three
`baton`-mentioning ideas are about currency-line drift, guard-parity queueing, and the
gate verify-command slot; none checks baton path-resolvability. Worth having because it
closes the one unguarded seam in the workflow this session just made turnkey.

## ⟲ Previous-session review

Previous session — **R1 cut_release dist-before-self-restamp (PR #488)**. Did well: it
root-caused a subtle two-source-of-truth bug (self-row `tree_version` from stale
`dist/bootstrap.py` vs `config_pin` from the just-bumped config) instead of patching the
symptom, and tied its pinning test to the *real* `currency.drifts()`/`verdict()` path so a
future reorder reddens CI rather than a synthetic assertion. What it could improve: its own
💡 (`cut_release --rebuild-dist` to fold the manual FOLLOWUP dist rebuild into the cut) was
left as a card note with no `docs/ideas/` file, so it risks the exact orphaning the groom
doc exists to prevent — a strong buildable idea should seed its idea file the same session,
not wait a groom cycle. System improvement it surfaces: the **un-groomed-idea counter** the
#487 card already named is the right shape, but it should also assert that any 💡 flagged
"substantial enough to earn a `docs/ideas/` file" *has* one — a card-local `💡 → ideas-file`
presence check would catch the seed-the-file gap at session-close, where it is cheap to fix.

## ⚑ Self-initiated

⚑ Self-initiated: none — R2 was a dispatched baton item (from
`docs/planning/2026-07-19-night-run-idea-groom.md`, retargeted onto R2 by the R1/#488
session), not self-initiated.
