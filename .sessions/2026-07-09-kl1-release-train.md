# Session 2026-07-09 — KL-1 release train → v1.0.0

> **Status:** `in-progress` *(PR B of the train underway: the `upgrade` verb per
> §4.3 — archive-first, hash-based planted-doc diff report, `--apply-docs` on
> untouched docs only, state backup + `--rollback`. PR A merged as #8/f4609ea.
> Flips `complete` with the full session close-out, then tag `v1.0.0`.)*

**The train (founding plan §4 + §10 KL-1 row, one session, 2 PRs + tag):**

- **PR A (this PR):** `KIT_VERSION` + `Config.kit_version` dataclass field +
  `--version` flag + dist header stamp + adopt-time recording (kit_version into
  config **and** state; sha256 per planted doc into state) + adopt archives the
  running dist to `.substrate/backup/bootstrap-<version>.py` (§4.3 ordering
  constraint) + `CHANGELOG.md` + `LICENSE` (MIT) + `release.yml` +
  `reconciliation_prs` 20→30 + `_ENGINE_MANIFEST` dropped + the strengthened
  auto-merge-enabler guard (see friction below).
- **PR B:** `upgrade` CLI verb per §4.3 (hash-based planted-doc diff report,
  `--apply-docs`, state backup + `--rollback`).
- **Then:** tag `v1.0.0` on the final merge commit; `release.yml` publishes the
  Release (bootstrap.py + bootstrap.py.sha256 + release.json).

## PR A — what shipped

- `src/engine/lib/config.py`: `KIT_VERSION = "1.0.0"` (the one home; semver keyed
  to the planted/state/config/CLI contracts); `Config.kit_version` as a declared
  dataclass field (`from_dict` drops unknown keys — the §4.1 warning);
  `reconciliation_prs` default 20→30 (§3.4 drift fix).
- `src/engine/cli.py`: `--version` (prints `substrate-kit 1.0.0`); `render --live`
  re-records planted-doc hashes on every rewrite.
- `src/engine/adopt.py`: planted-doc sha256 recording (`planted_doc_hashes` in
  state; kept/consumer-owned files never claimed), `doc_is_untouched` (the §4.3
  hash test), `archive_dist` + adopt-time dist banking, kit_version recorded into
  config + state at adopt.
- `src/build_bootstrap.py`: version stamped into the dist's first header line;
  `_ENGINE_MANIFEST` embedding dropped (§3.4 — `init --unpack` never shipped).
- `src/build_release_json.py` + `.github/workflows/release.yml`: `v*` tag →
  refuse-to-release guards (KIT_VERSION/tag match, dist stamp, CHANGELOG section
  present) → fresh-dist byte-equality → sha256 → Release with the three assets;
  notes body = the CHANGELOG section.
- `CHANGELOG.md` (keep-a-changelog; the 1.0.0 section describes the whole kit at
  first release), `LICENSE` (MIT), `pyproject.toml` 0.1.0→1.0.0 (test-pinned to
  KIT_VERSION), kit's own `substrate.config.json` gains `kit_version` + cadence 30.
- Tests: 442 → 465 (version field round-trip, hash recording, adopt archiving,
  dist stamp, release-asset builder + refusal paths, render-live re-record).

## ⚑ Flags

1. ⚑ **LICENSE = MIT under "Menno van Hattum"** (owner item P8 — recorded default
   applied; veto = replace the file + note the change in CHANGELOG).
2. ⚑ **PR #7 (this session's born-red card) merged INSTANTLY** — 24 s after open,
   by github-actions[bot], with CI still running: the auto-merge-enabler's
   refuse-to-arm guard passed because a `required_status_checks` **rule** exists
   on main, but its required **contexts** are effectively vacuous, so armed
   auto-merge had nothing to wait for (KL-0 PR #4 class, one level deeper). The
   born-red card landed alone on main (main CI red until this PR merges —
   self-healing). **Guard strengthened in this PR**: counts required
   *contexts* (not rules), prints them, refuses at 0. 👤 P10 remains: make
   `kit-quality` a required status check on main.
3. ⚑ Self-initiated: refuse-to-release guards in `release.yml` go beyond the plan
   letter (KIT_VERSION/tag equality + dist header stamp, alongside the specified
   CHANGELOG-section refusal) — cheap enforcement of the three-way version sync.
4. ⚑ Self-initiated: `release.json` gains optional per-release metadata via an
   HTML comment in the CHANGELOG section (defaults: breaking=false,
   state_migration=false, min_upgrade_from=1.0.0) — the §4.1 schema fields need a
   source of truth per release and the CHANGELOG is the one already-enforced home.

## 💡 Session idea

Ship a `bench/`-era **"release rehearsal" checker**: a kit-quality step that runs
`build_release_json.py --verify-only` against the *current* KIT_VERSION on every
PR (not just at tag time), so version-bump PRs that forget the CHANGELOG section
or the dist restamp go red at the PR, not at the tag — moving the KL-1 refusal
from release-time (where a red run needs a re-tag dance) to merge-time (where it
is one more commit). Added to this PR as a plain test
(`test_verify_is_green_for_the_current_version`), which is the same guarantee
with zero CI cost — the idea is recorded here in case the check ever needs to
leave the test suite.

## ⟲ Previous-session review

The kl1-ci-delta session (#6) was strong: the single `kit-quality` context design
was exactly right, the legacy-alias bridge un-stuck an owner-landed ruleset
mid-flight, and its session card's friction entries carried code anchors — this
session used its `auto-merge-enabler` port unchanged. One genuine miss, proven
live today: its refuse-to-arm guard tested the wrong level (rule-count, not
context-count), so the very footgun it was built against fired again as PR #7's
instant merge. Workflow improvement: when converting a friction into a guard,
write the guard against the *observable failure condition* ("auto-merge merged
with nothing to wait for" → assert non-empty wait set), not against the nearest
config artifact ("a rule exists") — the artifact can exist in a state that still
reproduces the failure.
