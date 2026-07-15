# 2026-07-15 · template-sync-advisory

> **Status:** `complete`

- **📊 Model:** Fable (Claude 5 family) · medium · feature build
- Scope: baton item 2 — build the template↔local-copy sync-advisory checker
  (docs/ideas/template-local-copy-sync-advisory-2026-07-15.md): a new
  advisory-only `check` leg comparing `## ` heading SETS between each
  `ADOPT_PLAN` template and the kit's own rendered local copy, firing
  `template-local-heading-drift` when a doctrine section exists on only one
  side. Engine change → dist byte-pin regen. One PR (#399).

About to (opening declaration, retained): write
`src/engine/checks/check_template_sync.py` (fence-aware heading scan,
`${slot}`-pattern matching so rendered headings never false-positive,
`[[fill:]]` skip, live-traffic destinations excluded), wire it into
`cmd_check`'s full lane next to the staged-regen advisory, add fixture
tests (template-only section fires; identical heading sets with divergent
prose stay silent), regenerate dist, flip the idea's lifecycle.

## Record

- Boot: hard-synced to origin/main 0959833 (#398); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line; the "ORDER 025" text at
  ~line 210 verified as the fm relay inside ORDER 019, not a new order);
  control/claims/ held README only; zero open PRs at the ~16:5xZ scan;
  `currency --check` exit 0 from repo root (registry current, 12 repos) —
  no regen slice due, so the baton-named checker build was the slice.
  Born-red card + claim (written by the `bootstrap claim` verb — dogfood)
  = first commit 1645d0f; PR #399 opened READY immediately after.
- Design step that earned its keep: before writing the checker, ran a
  15-line survey of every ADOPT_PLAN pair on the live kit tree. It found
  (a) the live-traffic noise problem the groomed recipe hadn't priced in —
  control/inbox.md alone carries 25 live `## ORDER` headings, control/
  status.md, current-state, decisions, and question-router all accumulate
  headings BY DESIGN — which became the documented `LIVE_TRAFFIC_DESTS`
  skip; and (b) the `${slot}` heading class (`Rails specific to
  ${project_name}`) which became the slot-pattern matcher. Both firewalls
  were measured needs, not speculation.
- Shipped (56206fb): `check_template_sync` (self-gates on
  `src/engine/templates/` presence — only the kit's own tree scans, so
  adopters pay nothing; anchors on ADOPT_PLAN + `_adopt_dest`, never a
  second hand-list), wired into `cmd_check`'s full lane with the standard
  advisory emit + guard-fires block; builder module-list entry (the cli
  wiring alone compiled into dist but the module body silently didn't —
  the dist grep caught it before any test could); 12 fixture tests
  pinning the idea's own fixture spec, the firewalls, the self-gate, and
  the never-exit-affecting contract; idea flipped promoted/shipped_pr 399,
  README row Backlog → Shipped (window closes 2026-08-14); CHANGELOG
  `[Unreleased]` Added entry.
- First live run: 4 REAL drift pairs surfaced on the kit tree
  (collaboration-model, CAPABILITIES, control/README, ideas README —
  details on the heartbeat), recorded as next-wake baton item 1 rather
  than scope-crept into this slice.
- Verify (at 56206fb): `python3 scripts/preflight.py` → 8/8 legs green
  (pytest 1620 passed, 1 skipped — +12 new tests; dist-byte-pin; ruff;
  idea-index; retro-index; changelog-structure; program-law;
  bench-integrity). `dist/bootstrap.py check --strict` → designed born-red
  HOLD only (this card, pre-flip) + known staged-regen-lag ×3 + the new
  template-sync ×4 (advisory, never exit-affecting). Guard-fires telemetry
  deltas committed with the work and the heartbeat.

## Session enders

- 💡 Session idea: **route advisory findings through the allowlist.**
  `apply_allowlist` runs only over the strict `doc_findings` loop; every
  advisory family (claims, staged-regen, model-line, now template-sync)
  bypasses it — so a DELIBERATE divergence has no reasoned-suppression
  path and nags forever. Live case born this wake: docs/ideas/README.md's
  local-only 'Historical / pointer stubs' + 'Shipped (survive window
  open)' sections are correct local extensions, and the new advisory will
  re-warn on every full check until someone either syncs the template (
  wrong — they're index sections, not doctrine) or mutes the pair. Cheap
  fix: run advisories through the same reason-carrying allowlist before
  emit (verdict recorded in guard-fires, exactly like suppressed strict
  findings) so "acknowledged, deliberate, here's why" is a first-class
  state. Dedup-grep docs/ideas/ (`allowlist.*advisor|advisory.*allowlist`,
  plus the allowlist mentions in engagement-native-consumer-state and
  enabler-install-preflight — both different scopes): no existing capture.
- ⟲ Previous-session review (2026-07-15-groom-sync-advisory, PR #398): the
  groom did exactly what a groom should — anchors (`ADOPT_PLAN`, the
  scan-style precedent), a fixture spec this wake's tests implemented
  nearly verbatim, and evidence pre-attached, which made this build slice
  start at full speed. The gap it surfaces: the groomed recipe said "per
  ADOPT_PLAN pair whose destination exists in the kit's own tree" without
  pricing the live-traffic pairs — a recipe-stage dry-run (the same
  15-line survey this wake ran in one minute) would have found the
  25-heading inbox noise at groom time and shipped the skip-list in the
  recipe. Improvement: when grooming a checker-shaped idea, run the
  cheapest possible live scan of the proposed surface and record its
  measured hit profile in the idea file — a recipe with numbers beats a
  recipe with anchors alone.
