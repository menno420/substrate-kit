# Session — cut_release dist-before-self-restamp (R1)

> **Status:** `complete`

**Scope:** R1 from `docs/planning/2026-07-19-night-run-idea-groom.md` — make the
committed `docs/adopters.md` self-row non-DRIFT after a version-bump cut (today
`scripts/cut_release.py` stamps the self-row from the stale pre-rebuild
`dist/bootstrap.py` header, so the bump PR momentarily commits a self-row that
shows a false tree-internal DRIFT); add a pinning test tied to the real
`currency.drifts()` / `verdict()` check.

- **📊 Model:** opus-4.8 · medium · feature build

## What shipped (PR #488)

- **Root cause:** `run()` in `scripts/cut_release.py` stamped the bump self-row
  from `local_self_scan(root)`, which reads `config_pin` from the just-bumped
  `substrate.config.json` (= the release **target**) but `tree_version` from
  `dist/bootstrap.py`'s header — still the **OLD** version, because the dist
  rebuild is a manual FOLLOWUP step, not done by `--write`. That rendered
  `tree(old) != pin(target)` → a false tree-internal DRIFT committed into the
  version-bump PR (the kit #472 regression).
- **Fix:** stamp the self-row from the release's tree truth (`target`) instead —
  `self_scan.tree_version = target` before `restamp_self_row(...)`. Justified by
  the byte-pin: `test_committed_bootstrap_is_current` blocks merge until
  `dist/bootstrap.py` is rebuilt to target, so **every mergeable PR carries
  `dist == target`** and the committed `current` self-row is honest for the
  committed state — restoring the B-2 intent ("renders a current self-row").
- **Test:** added a pinning test in `tests/test_cut_release.py` tied to the real
  `currency.drifts()` / `verdict()` check, so a future reorder that re-introduces
  the stale-tree stamp reddens CI.

Files: `scripts/cut_release.py` (+19/-4), `tests/test_cut_release.py` (+96).

## Verification

- `python3 -m pytest tests/ -q` → **1822 passed** (full suite green after the fix
  + pinning test; re-confirmed green after the card/heartbeat edits).
- `python3 dist/bootstrap.py check --strict` → exit 0 once this card reads
  `complete` (the born-red kit-quality Session-gate clears on the flip).
- PR #488 auto-merges on green CI after this flip (born-red hold released).

## 💡 Session idea

**`cut_release` should optionally run the dist rebuild itself (`--rebuild-dist`),
so the FOLLOWUP `python3 src/build_bootstrap.py` step cannot be silently
forgotten — safe *because* the byte-pin guards it.** This session's fix makes the
committed self-row *honest for the mergeable state*, but it leans on a human
remembering FOLLOWUP step 2 (dist rebuild) before merge; if forgotten, the PR
correctly reddens on `test_committed_bootstrap_is_current`, but only *after* a
wasted CI round-trip. Folding an opt-in `build_bootstrap` invocation into
`--write` (or a `--rebuild-dist` flag) would collapse the two-step cut into one
and make the byte-pin a confirmation rather than a tripwire. Guarded by the same
byte-pin, so it can't stamp a wrong dist. Not in the tree (grepped `docs/ideas/`:
no cut_release / build_bootstrap / dist-rebuild idea). Substantial enough to earn
a `docs/ideas/` file next groom; this one-line card entry seeds it.

## ⟲ Previous-session review

Previous session — **#487 night-run idea groom + heartbeat refresh**. Did well:
it caught that the night chain (#455–#486) had left `control/status.md` asserting
the buildable-now backlog was "DRY" while ~14 unbuilt buildable `💡` ideas piled
up ungroomed on the night's session cards — a genuine sweep gap, not an empty
backlog — and refilled the baton by grooming those cards into a ranked R1–R12
plan. That refill is exactly what made *this* R1 session possible. System
improvement it surfaced (and named but did not build): the **un-groomed-idea
counter** advisory — a `check`/kit-quality check that counts `💡 …` lines on
cards dated after the newest `*groom*.md` and flags when they exceed a small
threshold, so "backlog DRY" becomes mechanically impossible while ungroomed ideas
exist. Concrete next step: build that advisory (it is itself a buildable-now
backlog slice) rather than leaving it as a card note — the gap it closes just
recurred one night ago.

## ⚑ Self-initiated

⚑ Self-initiated: none — R1 was dispatched from the 2026-07-19 night-run groom
doc (`docs/planning/2026-07-19-night-run-idea-groom.md`), not self-initiated.

## Baton

R1 shipped (PR #488). Baton retargeted → **R2 — `/scope-backlog-item` skill (S):**
scaffold the planning-recipe arc as a `docs/SKILLS.md` skill so the standing
"when no exec work is left, plan" order is turnkey. Full ranked list R2–R12 in
`docs/planning/2026-07-19-night-run-idea-groom.md`; `control/status.md` Next-2
baton updated to match.
