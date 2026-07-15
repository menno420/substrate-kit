# Session · 2026-07-15 · taxonomy-sync-checker

> **Status:** `complete`

Intent: baton item 1 — ship the taxonomy-surface sync checker (idea taxonomy-surface-sync-checker-2026-07-09): `scripts/check_taxonomy_sync.py` asserts set-equality between the canonical `MODEL_TASK_CLASSES` tuple (src/engine/grammar.py), the allocation-ladder table's first column, and the telemetry README class list, with tests + CI step + preflight leg.

- **📊 Model:** Claude Fable 5 · medium · feature build
- ⚑ Self-initiated: no — baton-named (control/status.md Next-2 item 1 at sync HEAD f3ab863).

## What shipped (PR #404)

- `scripts/check_taxonomy_sync.py` (stdlib, import-free, PL-008 UNVERIFIED header): regex-parses the canonical `MODEL_TASK_CLASSES` tuple from `src/engine/grammar.py` (the tuple `TASK_CLASSES` in `src/engine/loop/telemetry.py` aliases — the idea file predates that move), the `## The ladder` table's first column in `telemetry/allocation-ladder.md` (emphasis/flag glyphs stripped, the revision-log table ignored), and the `task_class ∈` bullet's `·`-list in `telemetry/README.md`; asserts set-equality both ways per surface plus the README's "the N PL-004 classes" count. Parse failure on any surface is itself a finding (`grammar-unparsed` / `ladder-unparsed` / `readme-unparsed`), never a silent pass.
- Wiring: kit-quality CI step "Taxonomy sync (PL-004 — TASK_CLASSES ⇄ ladder ⇄ telemetry README)" behind the control-fast-lane condition (.github/workflows/ci.yml), plus a `taxonomy-sync` leg in `scripts/preflight.py` (docstring leg list renumbered 6→9). Pins updated: `PINNED_LEGS` (tests/test_kit_preflight.py) and `HEAVY_STEP_NAMES` (tests/test_ci_control_lane.py).
- Tests: `tests/test_check_taxonomy_sync.py` — 15 tests: parsers (tuple order, emphasis/flag stripping, revision-log exclusion, bullet list + count), deliberately-desynced fixtures (missing ladder row, typoed row = missing+extra pair, README class drift, README count drift), parse-failure findings, and the real-repo-in-sync pin. Manual probe: an injected `docs-onIy` ladder typo reds with the missing+extra pair.
- Docs: idea flipped `promoted`/`shipped` (PR #404, window closes 2026-08-14) + README index entry moved to Shipped; CHANGELOG under `[Unreleased]` `### Added`. Repo-level guard — nothing ships in `dist/bootstrap.py` (byte-pin leg verified unchanged).
- Verify at 7767707: `scripts/preflight.py` 9/9 green (pytest 1645 passed, 1 skipped); `dist/bootstrap.py check --strict` shows only the designed born-red HOLD (this card, pre-flip), the known staged-regen-lag ×3, and the required-unverified NOTE; guard-fires telemetry delta committed with the session.

## 💡 Session idea

Class-count sweep over living prose surfaces: the PL-010 session found the taxonomy's class count hardcoded in four places, and this session's grep still finds "the 9 PL-004 classes"-shaped literals outside the checker's two surfaces (src/engine/grammar.py:423 comment; docs/ideas/model-line-payload-lint-advisory-2026-07-11.md:34). Extend `check_taxonomy_sync.py` with a repo-wide regex sweep for `\d+ PL-004 (task )?classes` over living surfaces (src/ + telemetry/ + docs/, excluding append-only historical registers — docs/program/rulings.md deliberately preserves the founding "8 task classes" wording — and docs/ideas/ time-capsules), asserting each N equals `len(MODEL_TASK_CLASSES)`: a 10th-class amendment then cannot leave a stale count anywhere agents read. Dedup: zero count-sweep hits under docs/ideas/ (grepped this session).

## ⟲ Previous-session review

The #403 session (adopt-pytest-gate-step) left the cheapest possible pickup: its baton line named the idea file, the size call ("smallest genuine backlog win"), and the shipped-boundary (#403 done), and its session idea was concrete enough to become this wake's refreshed baton item 1 verbatim — zero re-derivation spent. Miss, small: its card's "Verify at 629d8c2" line reported preflight "8/8 green" without noting that the leg count itself is a moving pin (tests/test_kit_preflight.py PINNED_LEGS), so this session's 8→9 bump had to be discovered by a red pytest leg rather than being named as the expected touchpoint for any new-checker slice. System improvement worth keeping: the idea file's guard recipe (or the baton line naming a new checker) should list the two standing pins every kit checker addition must touch — PINNED_LEGS + HEAVY_STEP_NAMES — turning a predictable first-red into a checklist line; this card's "Wiring" bullet does that for the next reader.
