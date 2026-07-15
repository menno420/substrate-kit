# 2026-07-15 · adopt-lane-drift-advisory

> **Status:** `complete`

- **📊 Model:** Fable (Claude 5 family) · medium · engine+tests
- Scope: baton item 2 — the plain-adopt lane-drift advisory (idea
  docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md, the
  `adopt --lane` / #103 inverse gap). Engine change + tests, one PR (#396).

About to (opening declaration, retained): build a one-line advisory in
`adopt` when a plain (no `--lane`) adopt targets a repo whose
`heartbeat_files` is already lane-shaped (non-default), nudging
`adopt --lane <name>` instead of silently planting an undeclared singular
`control/status.md`. Advisory only, never a refusal.

## Record

- Boot: hard-synced to origin/main 3df8ac8 (#395); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line; the "ORDER 025" text at
  ~line 210 verified as the fm relay inside ORDER 019, not a new order);
  control/claims/ held README only; zero open PRs at the ~15:1xZ scan;
  `currency --check` exit 0 (registry current, 12 repos) — no regen slice
  due, so the baton-named idea was the slice. Born-red card + claim = first
  commit d0ad0f0; PR #396 opened READY immediately after.
- Shipped (514cc24): `engine.adopt.lane_drift_advisory` (lane-shaped =
  non-empty `heartbeat_files` ≠ the untouched
  `["control/status.md"]` default; empty list stays non-lane-shaped per the
  fall-back-to-default doctrine) + the (0a) advisory branch in `adopt()` —
  the nudge is the FIRST report line, planting continues unchanged. Four
  tests mirroring the #103 lane set: lane-shaped + plain adopt → advisory
  printed and files still planted; default-shaped → silent; lane adopt →
  silent; unit contract incl. the mixed superbot-games join shape. Plus
  CHANGELOG [Unreleased] ### Added entry, idea lifecycle flip (frontmatter
  promoted / shipped_pr 396 / outcome shipped + README Backlog → Shipped),
  dist byte-pin regen.
- Edit lesson (cost: one local red, fixed pre-push): the insertion point
  chosen for the new test block split an existing test's trailing assert
  (`test_planted_readme_documents_the_one_command_lane_shape` had one more
  line than the matched old_string) — the orphaned assert NameError'd on
  first run; restored to its home before commit.
- Decide-and-flag: `upgrade` re-runs `adopt(lane=None)` (its step 6,
  src/engine/upgrade.py ~1025), so lane-shaped adopters (superbot-games)
  will see the advisory line in upgrade reports too — kept BY DESIGN: it
  truthfully flags the same half-declared state at the exact moment adopt
  plants/keeps the undeclared singular seed, advisory-only, one line. The
  root fix is filed as this session's 💡 below.
- Verify (at 514cc24): `python3 scripts/preflight.py` → 8/8 legs green
  (pytest 1608 passed, 1 skipped; dist-byte-pin; ruff; idea-index;
  retro-index; changelog-structure; program-law; bench-integrity).
  `dist/bootstrap.py check --strict` → designed born-red HOLD only (this
  card, pre-flip) + known staged-regen-lag ×3. Guard-fires telemetry delta
  committed with the heartbeat (1c6026f).

## Session enders

- 💡 Session idea: **skip the stray singular seed on lane-shaped
  plants.** The advisory warns, but the underlying drift still happens:
  with `lane=None` the ADOPT_PLAN loop plants `control/status.md`
  unconditionally (skip-if-exists only), so a plain adopt — and every
  `upgrade`, which re-runs `adopt(lane=None)` — into a lane-shaped repo
  whose singular file is absent CREATES the undeclared seed the advisory
  is warning about. Root fix: when `heartbeat_files` is lane-shaped and
  does not declare `control/status.md`, skip planting it (report a
  `skipped: control/status.md — lane-shaped repo, undeclared` line) so the
  half-declared state can no longer be created by the kit itself; the
  advisory then only fires on the operator's deliberate hand-path. Dupe
  check: only docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md
  mentions the singular-seed drift, and it ships the advisory, not the
  plant skip.
- ⟲ Previous-session review (2026-07-15-heartbeat-delegated-tally): clean,
  well-scoped docs/template slice — the grammar lesson (idea frontmatter
  vocabulary: `outcome: shipped` carries the ship fact, never
  `state: shipped`) was recorded honestly with its checker citation and
  saved this session from repeating it (the flip here matched the #395
  exemplar first try). Improvement it surfaces: its 💡 (template↔local-copy
  sync advisory) was left card-only rather than filed into docs/ideas/ —
  the exact pattern that needed the 2026-07-10 night-cap groom to rescue
  THIS session's idea five days later. The card-only 💡 → docs/ideas/ file
  gap is a recurring leak; this session's baton line 2 now names "groom it
  into docs/ideas/ first" explicitly so the next wake closes it.
