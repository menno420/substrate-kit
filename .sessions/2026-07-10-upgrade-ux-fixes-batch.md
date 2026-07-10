# 2026-07-10 — gen-2: four upgrade-UX fixes (v1.6.0 rollout)

> **Status:** `in-progress`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side upgrade-UX batch (one
  PR bundling four ordinary-lane fixes filed live during the v1.6.0 fleet
  rollout)

## Scope

Four `docs/ideas/upgrade-*-2026-07-09.md` idea files, each a guard-recipe fix
observed on the two consumer upgrade runs (superbot-next#96 + websites#45),
bundled into ONE PR:

1. **idempotent-archive report line** (`upgrade-archive-report-line-gap`): the
   idempotent early return in `archive_dist` (`src/engine/adopt.py`) was silent,
   so an upgrade whose OLD dist was already banked printed no `archived:` line
   for it — the report's only such line named the NEW version and readers
   (three times) concluded the old dist was never banked. Fix: the idempotent
   path appends `archived: <rel> (already banked)` instead of nothing.

2. **release.json placement checklist line**
   (`upgrade-checklist-release-json-placement`): `ADOPTER_CHECKLIST` in
   `src/build_release_json.py` never told adopters to download `release.json`
   next to `bootstrap.py.new`, so a to-the-letter follow leaves the sha256
   self-verification silently skipped. Fix: step 1 now names `release.json` and
   the skip consequence. (The companion "report says so" note the idea offered
   as a second line of defense already shipped — `run_upgrade` emits
   `note: no release.json found — sha256 verification skipped`.)

3. **rollback-loses-hash-records** (`upgrade-rollback-loses-doc-hash-records`):
   `upgrade --rollback` restores the pre-upgrade `state.json`, discarding every
   `planted_doc_hashes` entry the upgrade's adopt pass recorded — so on a re-run
   a kit-written doc carries no hash and classifies consumer-diverged, out of
   `--apply-docs`' reach. Fix (self-heal): in `classify_planted_docs`, when a
   doc byte-matches the NEW template render (date-normalized) it is provably
   untouched kit-form, so its hash is recorded from ground truth. A consumer
   edit never byte-matches and stays honestly diverged; a new-render byte-match
   only ever yields `unchanged`, so nothing is auto-applied that would not be.

4. **`--apply-docs` single-shot window** (`upgrade-apply-docs-single-shot-window`)
   — **interim slice only**: the misleading report hint said "re-run with
   --apply-docs to take them", a no-op after the transition (the vendored dist
   is already new, so no template-improved row can recur). Fix: the note now
   names the recovery that works — `upgrade --rollback` then a re-run with
   `--apply-docs`. The idea's full mechanism (post-hoc apply against the banked
   archived dist, no rollback needed) is **larger than this bundle** and stays
   open; only the hint correction ships here.

Touches only `src/engine/adopt.py`, `src/engine/upgrade.py`,
`src/build_release_json.py`, `dist/bootstrap.py` (regenerated), their tests
(`tests/test_adopt.py`, `tests/test_upgrade.py`, `tests/test_release_assets.py`),
the three shipped idea files' lifecycle marks + `docs/ideas/README.md`, and this
card. NEVER touched: `control/inbox.md`, `control/status.md`, or anything under
`bench/`.

## 💡 Session idea

All four field reports share a root cause: the upgrade flow *does the right
thing on disk* (archives, self-verifies, keeps hashes recoverable) but is
**silent or misleading about it in the report/checklist the operator actually
reads**. Three of the four are pure observability fixes (a missing line, a
missing checklist step, a hint that lies), and the fourth (self-heal) recovers
provenance from ground truth rather than trusting a stored record. The pattern
worth generalizing: an upgrade's report is a UI contract — every covenant the
flow honors on disk (archive-first, sha-verify, hash provenance) needs a report
line that says so, or the operator invents doubt the covenant existed to remove.

## ⟲ Previous-session review

The prior card (2026-07-10 gen-2: telemetry write-at-card-commit + backfill)
closed `complete`, `check --strict` green, shipped as #91. No defect inherited;
this session picks up the four upgrade-UX idea files filed during the v1.6.0
rollout.

## Outcome

*(filled at close-out — see the final commit.)*
