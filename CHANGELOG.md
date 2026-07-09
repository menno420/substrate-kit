# Changelog

All notable changes to substrate-kit are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning is [semver](https://semver.org/) keyed to the kit's four consumer
contracts (founding plan §4.1): **MAJOR** = breaking change to the planted-doc
contract, state schema, config schema, or CLI surface; **MINOR** = new
capability (new checker, new command, new template); **PATCH** = fixes.

Each release publishes a GitHub Release for tag `vX.Y.Z` with three assets:
`bootstrap.py` (the pinned single-file distribution), `bootstrap.py.sha256`,
and `release.json` (the machine-readable upgrade contract). The release
workflow refuses to publish a version that has no section in this file.

## [Unreleased]

### Added

- **The program governance home** (band KL-2, plan §8): `docs/program/` with
  the canonical `[PL-NNN]` rulings register (PL-001…PL-009,
  provenance-required) plus program copies of the collaboration model and the
  decision-authority model; `docs/house-style.md` (§3.4/D-7 — the kit's
  opinionated defaults, declared not configurable).
- `scripts/check_program_law.py` in the `kit-quality` gate: PL-register
  grammar, monotonic IDs, provenance-required on every block, and the
  no-ruling-bodies-in-planted-pointers assertion.
- **Templates** (MINOR — new planted content): `CONSTITUTION.md.tmpl` and
  `collaboration-model.md.tmpl` gain a "Program law" pointer section citing
  the register by PL-ID (consumers cite, never copy).

## [1.0.0] - 2026-07-09

First release of substrate-kit as its own repository — the portable,
self-improving agent-memory substrate extracted from its origin repo, adopted
by real consumers, and now nameable, pinnable, verifiable, and upgradeable.

### Added

- **The kit itself**, stable at first release (the "1.0.0 because two real
  consumers depend on a stable adopt contract" ruling, plan KF-1):
  - `dist/bootstrap.py` — single-file, stdlib-only distribution; byte-pinned
    to `src/engine/` by CI. The primary vendoring form.
  - One-step `adopt`: derives provisional interview slots from the host tree,
    plants the workflow docs (constitution, contracts, ledgers, session
    scaffolding — skip-if-exists, never clobbering), banners unrendered docs,
    vendors the bootstrap, and stages the `.claude/` packs (skills, personas,
    hooks, CI examples) under `.substrate/` for deliberate install.
  - `adopt --wire-enforcement`: the live Stop-hook nag plus a CI locked door
    (`check --strict --require-session-log`) that holds a merge red until the
    session journal is written.
  - The staged onboarding interview (`ask` / `answer` / `confirm` /
    `render --live`), integration modes (`observe` / `guided` / `active`),
    task stances, and mode-paced graduation.
  - The memory loop: reflections buffer + mining, episodic index, triggers,
    self-maintenance report + compaction, KPI footer, review seam.
  - The checker suite behind `check --strict`: docs hygiene (badge / link /
    reachability), session-log markers, namespace shadowing, seam authority,
    orientation word budget, decision-ledger grammar + stamp discipline.
  - The context-economy engine (shadow-first maturity ladder) and the
    context-pack generator.
- **Release discipline** (this release's own work, plan §4):
  - `KIT_VERSION` constant; `--version` CLI flag; version stamped into the
    dist header; `Config.kit_version` field recorded at adopt/upgrade so both
    the file and the install self-identify.
  - `adopt` records a sha256 per planted doc in `.substrate/state.json`
    (re-recorded by `render --live`) — the hash-based "consumer-untouched"
    test the upgrade path's doc-diff report is built on.
  - `.github/workflows/release.yml`: pushing a `v*` tag builds the dist
    fresh, verifies byte-equality and the version stamp, and publishes the
    GitHub Release with the three assets — refusing when this file has no
    section for the version.
  - `LICENSE` file (MIT).
- **`upgrade` CLI verb** (plan §4.3): archives the running dist to
  `.substrate/backup/bootstrap-<version>.py` first (as does `adopt`, so the
  archive exists from v1.0.0 onward), verifies sha256 against `release.json`
  when present, replaces the vendored file, regenerates staged artifacts,
  emits a hash-based planted-doc diff report (`.substrate/upgrade-report.md`),
  applies template improvements only to consumer-untouched docs and only
  under `--apply-docs`, backs up state before migration, and supports
  `upgrade --rollback`.

### Changed

- `reconciliation_prs` default 20 → 30 (stale drift vs the origin repo's
  live cadence; plan §3.4).

### Removed

- `_ENGINE_MANIFEST` dropped from the dist build (plan §3.4): the
  `init --unpack` it served never shipped, and it doubled every consumer's
  vendored file for nothing.

[1.0.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.0.0
