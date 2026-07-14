# 2026-07-14 — cut_release mechanization (release-cut preparation as one command)

> **Status:** `complete`

About to (opening declaration): build the Night-9 (#351 card) 💡 ender —
`scripts/cut_release.py`, a dry-run-by-default mechanization of the release
cut's PREPARATION (bump both version homes in one coherent edit, transform
CHANGELOG `[Unreleased]` → dated released section per the runbook +
`check_changelog_structure.py` shape, print the manual follow-up checklist);
it never commits, pushes, dispatches, or touches the network. Plus tests.

- **📊 Model:** Fable 5 · high · feature build

Run type: worker session (BUILD phase, coordinator-dispatched).

## What shipped (PR #356)

- `scripts/cut_release.py` — the release cut's PREPARATION as one command:
  `python3 scripts/cut_release.py <new-version>` dry-runs (exact unified
  diffs of all three files + the manual follow-up checklist); `--write`
  applies to the working tree. Bumps BOTH version homes
  (`src/engine/lib/config.py` `KIT_VERSION` + `pyproject.toml` `version`)
  in one coherent edit; transforms `CHANGELOG.md` `[Unreleased]` → a dated
  `[X.Y.Z]` section per the runbook + Night-9 idea wording (preamble prose
  kept verbatim where it is, `<!-- release: … -->` machine comment inserted
  before the first typed heading, fresh empty `[Unreleased]` opened above),
  self-verified against `check_changelog_structure`'s own rules (imported,
  not duplicated) before anything is written. NEVER commits, pushes,
  dispatches a workflow, or touches the network. Refusals (exit 1):
  malformed version, non-increment target, already-released target,
  version-home disagreement, empty or structurally invalid `[Unreleased]`,
  dirty git tree (`--write` only).
- **Decide-and-flag (home):** `scripts/` standalone script, not a
  `bootstrap` verb — it's kit-repo release tooling in the runbook
  audience's own directory (peer of `check_changelog_structure.py`), keeps
  `src/engine/` untouched → no dist regen, no adopter surface, byte-pin
  unaffected.
- **Decide-and-flag (machine comment):** emits
  `breaking=<true iff MAJOR> state_migration=false min_upgrade_from=1.0.0`
  (the constant values of all 19 released sections); checklist step 1
  tells the operator to verify the flags before committing.
- **Decide-and-flag (dist regen):** left to the checklist (step 2), not
  executed — `src/build_bootstrap.py`'s printed-byte-count check is an
  operator-visible verification the runbook names explicitly.
- `tests/test_cut_release.py` — 19 tests, all on tmp fixture repos (real
  tree never mutated): golden dry-run output pin, both-homes bump,
  produced CHANGELOG green under the real `check_changelog_structure`
  (library + CLI), section-shape/order pin, MAJOR→`breaking=true`,
  dirty-tree refusal (+ dry-run allowed on dirty), home-disagreement
  refusal (nothing written), malformed/non-increment/already-released/
  empty/invalid-structure/malformed-date refusals, live-repo dry-run
  green, double-transform guard.
- `docs/operations/release-runbook.md` §2 — one "Mechanized:" pointer line
  (no new docs file).

## Verify

- Baseline at HEAD bf231c3 (#355): `python3 -m pytest -q` → `1425 passed
  in 32.83s`. Final: `1444 passed in 30.23s` (+19, zero failures).
- `python3 scripts/preflight.py` → `preflight: OK — 7 leg(s) green`.
- `python3 dist/bootstrap.py check --strict` → green except the DESIGNED
  born-red hold on this very card pre-flip (plus pre-existing advisory
  model-line notes on earlier July-14 cards); green expected on the flip.
- `git status` on dist/ clean — `src/engine/` untouched, no regen needed.
- Live dry-run on the real tree (`cut_release.py 1.16.0`) reproduces the
  v1.15.0 cut's committed diff shape exactly (eaf4f23 as reference).

## Enders

💡 **Session idea:** mechanize the release's POST half too —
`scripts/verify_release.py <version>`: given a tag, mechanically run
runbook §5 (download the released `bootstrap.py` via the
browser_download_url path that works through the proxy, sha256 it,
compare against the `release.json` `sha256` field AND the committed
`dist/bootstrap.py` at the bump SHA, print the three hashes + verdict
line ready to paste into the release record). §5 says "never skip", yet
it's the one step still reassembled by hand from memory-file lore every
cut; with cut_release.py mechanizing §2, the §5 verifier would leave only
judgment steps (semver class, prose summary, dispatch click) manual.
Dedup-grepped `docs/ideas/` (42 files): only hit is the shipped adopter-
side checklist idea (#92), different surface.

⟲ **Previous-session review** (Night 13, merged-reality leg, PR #355):
excellent build — proving the degradation rule on its own shallow
container clone (51/441 commits) is exactly the evidence-first bar, and
the 7d-over-48h grace call was correctly grounded in the live #317/#345
parks. What it missed: its card promises "park-green, NO auto-merge —
enabler arm state verified at close and disarmed if armed", but #355
merged at 02:02:13Z by github-actions[bot], ~10 minutes after open — the
post-flip disarm lost the race to the enabler arming on the flip push +
green CI. Night 9's review already flagged this exact class on Night 8
(#349); it has now recurred with a disarm attempt added, which shows
disarm-after-flip is not a viable parking mechanism at all. Concrete
improvement: park intent must be expressed BEFORE any green CI exists —
either don't flip the card, or label `do-not-automerge` pre-flip (the
kit-law-gate-parking order: disarm+verify BEFORE labeling) — and cards
should state the landing mode as a mechanism prediction ("enabler will
arm and merge on green"), never as an intent the server can override.
This session follows its own advice: flip-and-let-merge is the declared
landing mode; no post-flip disarm will be attempted.
