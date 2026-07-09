# Session 2026-07-09 — KL-1 release train → v1.0.0

> **Status:** `complete` *(the whole KL-1 train: PR A = #8/f4609ea, PR B = #9,
> PR C = the close-out + two gate-hole guards this file rides in — tag `v1.0.0`
> pushed on PR C's merge commit; Release verified on the releases page.)*

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

## PR B (#9) — what shipped

- `src/engine/upgrade.py` + CLI verb `upgrade [--apply-docs] [--rollback]
  [--release-json PATH]` (dist regenerated; upgrade.py joins MODULE_ORDER):
  - **Self-verification** vs release.json (sha256 + version; refuse exit 2;
    honest skip note when absent).
  - **Archive-first (§4.3)**: old vendored dist → `.substrate/backup/
    bootstrap-<old-version>.py`, state.json → `.substrate/backup/state.json`,
    `last-upgrade.json` marker — all before any overwrite.
  - **Hash-based planted-doc diff report** → `.substrate/upgrade-report.md`
    (classes: unchanged / template-improved / consumer-edited / diverged; old
    templates via `ast.literal_eval` of the archived dist's `_TEMPLATES` —
    never executed; diverged docs get the template@old→new delta rendered
    through the current slot context).
  - **`--apply-docs` covenant**: only consumer-untouched docs; pre-hash
    installs classify all-diverged.
  - Staged regeneration (idempotent adopt pass) → state migration (post-backup)
    → `kit_version` re-recorded → report.
  - **`--rollback`** restores banked state + archived dist + config kit_version.
- Tests 465 → 481; live end-to-end in a scratch repo (adopt → upgrade with and
  without release.json → sha-mismatch refusal → rollback) all green.
- `docs/current-state.md`: KL-1 marked done kit-side, D2's consumer-pin half +
  KL-2 as next actions, P10 section updated with the #7 incident.

## v1.0.0 — the tag + Release

Annotated tag `v1.0.0` pushed on #9's squash-merge commit; `release.yml`
published the GitHub Release with `bootstrap.py` + `bootstrap.py.sha256` +
`release.json` (notes = the CHANGELOG 1.0.0 section). ⚑ **P11 rides this
moment** (owner: flip the repo public, or veto → read-only-PAT fallback).

## ⚑ Flags

1. ⚑ **LICENSE = MIT under "Menno van Hattum"** (owner item P8 — recorded default
   applied; veto = replace the file + note the change in CHANGELOG).
2. ⚑ **PR #7 (this session's born-red card) merged INSTANTLY, red** — 24 s after
   open, by github-actions[bot]. Root cause, fully reconstructed from job logs
   (my first "vacuous contexts" hypothesis was WRONG — corrected per source-wins):
   kit-quality on #7 **failed exactly as designed** (session gate red on the
   born-red card, in 15 s — this suite is that fast), but the ruleset's two
   required contexts are the LEGACY names, reported by the temporary alias jobs —
   and a bare `needs: kit-quality` alias is **skipped** when kit-quality fails,
   and **GitHub treats a skipped check run as SATISFYING a required status
   check**. So both required contexts read satisfied on a red build and armed
   auto-merge merged instantly. Two guards shipped: (PR A) the enabler counts +
   prints required *contexts* (which is how the legacy-contexts truth surfaced);
   (PR C) the alias jobs run `if: always()` and **fail hard** when kit-quality
   is not a success — a skipped-alias can no longer green a required context.
   👤 P10 remains: require `kit-quality` itself, then delete the aliases.
2b. ⚑ **PR #9 auto-merged before its close-out commit** — the reopened shared
   card kept its 💡/⟲ markers from PR A, and the kit's session gate checked
   marker *presence* only, so born-red read as green; the enabler (which fires
   on mergeable MCP-created PRs — verified live) armed, CI passed in ~40 s, and
   the PR landed without the final card flip. **Guard shipped (PR C, engine):**
   `check_session_log` now treats a Status badge still saying
   `in-progress`/`wip`/`hold` as INCOMPLETE — the status *value* is part of
   completeness, kit-wide, so every consumer inherits real born-red. The
   orphaned close-out landed as PR C.
3. ⚑ Self-initiated: refuse-to-release guards in `release.yml` go beyond the plan
   letter (KIT_VERSION/tag equality + dist header stamp, alongside the specified
   CHANGELOG-section refusal) — cheap enforcement of the three-way version sync.
4. ⚑ Self-initiated: `release.json` gains optional per-release metadata via an
   HTML comment in the CHANGELOG section (defaults: breaking=false,
   state_migration=false, min_upgrade_from=1.0.0) — the §4.1 schema fields need a
   source of truth per release and the CHANGELOG is the one already-enforced home.
5. ⚑ **v1.0.0 cut this session** (plan KF-1/D-2: first release is 1.0.0, decided,
   never-wait). Published releases are never deleted — a bad one is superseded
   (§6.4).
6. ⚑ Deviation from the session brief: PRs were merged **by hand via MCP after
   verifying CI green** rather than trusting the enabler — the #7 instant-merge
   proved arming unsafe until P10 is confirmed; `current-state.md` ▶ Review
   rhythm now says so.

## PR C — what shipped

- `.github/workflows/ci.yml`: legacy-alias jobs `if: always()` + hard-fail on a
  non-success kit-quality (closes the skipped-satisfies-required hole, flag 2).
- `src/engine/checks/check_session_log.py`: `status_in_progress` +
  `check_log` reports "a completed Status (badge still says in-progress)" —
  born-red now checks the status VALUE (flag 2b); dist regenerated; tests
  481 → 483.
- The PR B close-out that #9's early merge orphaned (this card's completion +
  `docs/current-state.md`), cherry-picked in.

## KPIs / verification

- `python3.10 -m pytest tests/ -q` → **483 passed** (442 → 465 PR A → 481 PR B →
  483 PR C).
- `python3.10 -m ruff check src/engine/` → clean (both PRs).
- `python3.10 src/build_bootstrap.py` → byte-equal to committed dist at each push.
- `python3.10 dist/bootstrap.py --version` → `substrate-kit 1.0.0`.
- Cold scratch: `adopt` → `check --strict` green; `kit_version` recorded;
  `.substrate/backup/bootstrap-1.0.0.py` banked at adopt.
- Live upgrade drive (scratch): verify-pass with matching release.json; REFUSED
  (exit 2) on sha mismatch; report written; rollback restored state + dist.
- `src/build_release_json.py --version 1.0.0 --verify-only` → green (the tag's
  refuse-to-release guard, dry-run before tagging).

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
