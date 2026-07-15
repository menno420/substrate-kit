# 2026-07-15 · retro-index-checker

> **Status:** `complete`

- **📊 Model:** Claude Fable 5 · medium · feature build
- Scope: ship the captured idea `docs/ideas/retro-docs-reachability-checker-2026-07-10.md`
  — a small kit-quality checker (`scripts/check_retro_index.py`) asserting every
  `docs/retro/*.md` is linked from `docs/retro/README.md` and every relative
  `.md` link in that README resolves (the PR #76 unindexed-addendum class,
  reconciled only at gen-2 boot #78) — wired into preflight + ci.yml, plus the
  idea's lifecycle move.
- ⚑ Self-initiated: work-ladder rung 4 — no inbox ORDER above 024 (heartbeat
  reports done=001–024), adopter kit-lines unchanged vs the 04:37Z registry at
  the ~11:3xZ read-only spot-check (next/mineverse v1.16.0, websites/games
  v1.15.0 — no currency slice due), claims dir held README only, zero open PRs
  at the 11:3xZ scan (no backpressure).

## Record

- Boot: hard-synced to origin/main 0d79ac5 (#387). Born-red card + claim =
  first commit 5859781; PR #388 opened READY immediately after.
- Shipped (2e19246): `scripts/check_retro_index.py` (index-consistency +
  link-integrity legs, mirroring `check_idea_index.py`'s enforcement item 4;
  `../`-relative README links resolve against `docs/retro/` — the real corpus
  points at `../succession/` and `../gen2/`), `tests/test_check_retro_index.py`
  (9 tests incl. the live-repo dogfood pass), the `retro-index` preflight leg,
  the lane-conditioned ci.yml kit-quality step, and the parity-pin updates
  (`PINNED_LEGS`, `HEAVY_STEP_NAMES` — the latter caught by the pre-existing
  `test_every_heavy_step_is_lane_conditioned` count pin on the first full run,
  exactly as designed). Repo-level tooling only: no engine change, dist
  byte-pin untouched.
- Lifecycle: idea flipped promoted/shipped (frontmatter PR #388, anticipated
  in-PR merged_date per the leg-6 grace convention); README entry moved
  Backlog → Shipped; CHANGELOG `[Unreleased]` note added.
- Verify: `python3 scripts/preflight.py` → 8/8 legs green (pytest 1594 passed,
  1 skipped; ruff; dist-byte-pin; idea-index; retro-index; changelog-structure;
  program-law; bench-integrity).

## Enders

- 💡 Session idea: **generalize directory-index reachability to a config-listed
  set of docs dirs** — `check_retro_index` and `check_idea_index` now carry the
  same reachability leg twice; a single generic checker over every
  `docs/<dir>/` that owns a README index (docs/operations/ has one today)
  would also surface that `docs/reports/` has **no README index at all** — the
  same invisibility class one level up (its files are reachable only via
  bench/README.md side-links). Dedup: no existing docs/ideas/ entry covers
  cross-directory index generalization; the shipped retro idea scoped itself
  to docs/retro explicitly.
- ⟲ Previous-session review (2026-07-15-engage-slot-coverage): a clean
  tests-only slice — precise citations (bc4d09a/af64390), honest "pinned ORDER
  kept for byte-reproducibility" scoping, and it fixed README-vs-frontmatter
  drift on sight. Improvement it surfaces: its heartbeat parked the model-line
  advisory sweep (4 off-taxonomy older cards) as "candidates for a later sweep
  slice" in prose only — backlog that lives solely on a heartbeat line is
  invisible to the idea conveyor; parkings meant for later work should get a
  docs/ideas/ stub (or ride an existing one) so grooming can find them.
