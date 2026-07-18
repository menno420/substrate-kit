# Session · 2026-07-18 · kit-release-v1.19.0

> **Status:** `complete`

Intent: cut the substrate-kit **v1.19.0** release — the born-red version-bump
PR that stamps the three version homes to 1.19.0, transforms CHANGELOG
`[Unreleased]` → `[1.19.0] - 2026-07-18`, and rebuilds the pinned
`dist/bootstrap.py`. Publish (tag + GitHub Release via `release.yml`
`workflow_dispatch`) is a later step, NOT this PR.

- **📊 Model:** Opus 4.8 · high · feature build (release cut)
- ⚑ Self-initiated: cut substrate-kit v1.19.0 (minor bump — folds in the #455/#457/#459 guard stack; #457 is adopter-facing generated-CI, arguing the minor). Per the standing MANDATE / decide-and-flag grant.

About to: cut substrate-kit v1.19.0 — reconcile CHANGELOG `[Unreleased]`
completeness against the merges since v1.18.0 (fold in #455/#457/#459 +
the already-listed #444–#450 / #426 / #424 / #420–#422 / #414), run
`scripts/cut_release.py 1.19.0 --write` (three version homes +
CHANGELOG transform), regenerate `dist/bootstrap.py` via
`src/build_bootstrap.py`, verify locally per the release runbook, and open
the born-red bump PR. This card holds the PR red until a deliberate final
flip (which this session does NOT perform — the PR is left born-red per
the owner's instruction).

Scope: `CHANGELOG.md` · `src/engine/lib/config.py` · `pyproject.toml` ·
`substrate.config.json` · `dist/bootstrap.py` · this card ·
`control/claims/release-v1-19-0.md`.

## 💡 Session idea (Q-0089)

**Declarative guard-manifest — one source of truth for the kit guard list.** Add a
single declarative manifest file that lists every enforcing kit CI guard, and have
BOTH `src/engine/adopt.py`'s adopter-CI generator (`live_ci_workflow()`) AND the
guard-parity meta-test (`tests/test_guard_parity.py`, PR #459) read it — so adding
a guard means editing one manifest instead of three places (the kit `ci.yml` step,
the generated adopter step, and the parity test's `REGISTRY`). Why it's worth
having: PR #459's meta-test *detects* kit↔adopter guard drift but the mapping is
still hand-maintained across those surfaces; a declarative manifest removes the
drift at the root rather than merely red-flagging it. (Not filed in `docs/ideas/`
yet — the guard-parity meta-test card floated it only as a one-liner 💡; this cut
promotes it to the next baton, and it's worth a `docs/ideas/*.md` entry when
groomed.)

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 guard-parity-meta-test wake (PR #459): genuine credit — it
shipped a stdlib-only meta-test with a maintained three-way `REGISTRY`
(SETUP/MIRRORS/KIT_ONLY) plus an anchor floor (5 MIRRORS + 10 KIT_ONLY) so the
registry can't be gutted to a vacuously-green empty pass, and it cross-checked
18 named steps ⇄ 18 keys by hand — a thorough, defensible close of the #457 drift
class. Small miss: the `REGISTRY` it maintains is itself a third hand-kept copy of
the guard list (alongside `ci.yml` and `live_ci_workflow()`), so the meta-test
trades one drift surface for another — the residual risk it names but doesn't
close. System improvement it surfaces: the declarative guard-manifest above (💡) —
collapsing all three surfaces onto one source of truth is the structural fix the
parity test's own design points at.
