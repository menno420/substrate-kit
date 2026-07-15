# 2026-07-15 · model-line-unrecorded-marker

> **Status:** `complete`

- **📊 Model:** fable-5 · medium · feature build
- Scope: baton item 2 — sanction `unrecorded` as the terminal,
  advisory-silent effort value in `check_model_line` (idea
  docs/ideas/model-line-unrecorded-effort-marker-2026-07-15.md), silencing
  the two standing PR #390 retro-backfill nags honestly. Engine carve-out +
  `.sessions/README.md` teaching line + 3 tests + dist byte-pin regen +
  idea lifecycle flip + CHANGELOG entry, one PR (#394).
- ⚑ Fix-on-sight rider (not baton-named): retro-repaired the #393
  merge-verification-probe card's shape-malformed Model line using the
  just-shipped marker (details in Record) — contained, reversible,
  the mechanism's first live use.

About to (opening declaration, retained): build baton item 2 — sanction
`unrecorded` as a terminal, advisory-silent effort value in
`check_model_line`, so the two standing `model-line-effort` nags from the
PR #390 retro-backfill go silent HONESTLY (harvest still records verbatim;
live off-taxonomy values still nag). Scope: engine check + one
`.sessions/README.md` teaching line + tests + dist byte-pin regen + idea
lifecycle flip, one PR.

## Record

- Boot: hard-synced to origin/main e372601 (#393); inbox tops at ORDER 024
  (all acked+done per the heartbeat orders line); control/claims/ held
  README only; zero open PRs at the ~14:1xZ scan. Born-red card + claim
  (`bootstrap claim` rendered — first attempt refused for backticks in
  --scope, re-rendered plain; round-trip verified) = first commit 586cc8a;
  PR #394 opened READY immediately after.
- Shipped (2c0ba8d): `MODEL_EFFORT_UNRECORDED = "unrecorded"` in
  `src/engine/checks/check_model_line.py` — the effort advisory's
  membership test becomes `effort not in MODEL_EFFORT_VALUES and effort !=
  MODEL_EFFORT_UNRECORDED`; `MODEL_EFFORT_VALUES` stays `(low, medium,
  high)` (any other off-taxonomy value still nags with the taught values),
  and the telemetry harvest records `unrecorded` verbatim — test-pinned
  (`test_harvest_records_unrecorded_verbatim`). The checker source supports
  no live-vs-retro distinction (a card is a card), so the literal value is
  sanctioned everywhere and the reservation is taught in docs, exactly the
  idea's sketch. Same commit: the `.sessions/README.md` effort-segment
  line (live sessions report a real tier; `unrecorded` reserved for
  retroactive repair; never on your own live card), 3 tests
  (`unrecorded` silent · silences ONLY the effort advisory, exact-id/class
  still fire on the same line · harvest verbatim), dist regen
  (`python3 src/build_bootstrap.py`, byte-pin green), idea frontmatter
  promoted/shipped PR #394 + README Backlog → Shipped row, CHANGELOG
  [Unreleased] ### Changed entry.
- Fix-on-sight rider (7e71513): post-build `check --strict` surfaced a NEW
  `model-line-shape` on .sessions/2026-07-15-merge-verification-probe.md
  (#393, merged after the last heartbeat's advisory inventory) — the
  foreign probe session merged its Model segment into the Run-type line, so
  the harvest recorded NOTHING from it. Split to the taught form:
  `sonnet-5 · unrecorded · docs-only` (author's model self-report kept ·
  author never reported a tier, no invented telemetry · factual class for
  an inert probe doc). First live use of the marker this PR ships. Same
  commit: guard-fires telemetry delta, committed per checker instruction.
- Verify (at 7e71513): `python3 scripts/preflight.py` → 8/8 legs green —
  `1604 passed, 1 skipped in 48.66s` (pytest, 3 new tests); ruff `All
  checks passed!`; dist-byte-pin; idea-index (`check_idea_index: OK` —
  lifecycle flip indexed); retro-index; changelog-structure; program-law;
  bench-integrity. `dist/bootstrap.py check --strict` → exit 0; designed
  born-red HOLD only (this card, pre-flip) + known staged-regen-lag ×3.
  The two standing `unrecorded` model-line-effort nags are GONE and zero
  model-line payload advisories remain on the tree.
- Heartbeat (ff2d379): control/status.md overwritten wholesale — this wake
  recorded; ⚑ blocks carried byte-identical (diff-verified: no ⚑/WHAT/
  orders lines in the diff); `kit:` line plain; orders line unchanged
  (acked=001–024 · done=001–024); next-2 baton refreshed (1: grounded-
  skills window ~07-19..26 · 2: heartbeat delegated-tally guidance,
  docs/ideas/heartbeat-delegated-tally-guidance-2026-07-13.md).
- This flip commit also deletes the claim
  (control/claims/claude-model-line-unrecorded-marker.md), per convention.

## Enders

- 💡 Session idea: **model-line lint: name the sanctioned terminal marker
  in the `model-line-shape` / `model-line-effort` fix path.** The #393
  probe card showed the live repair flow: an agent hits the advisory on a
  FOREIGN card and must decide what to put in the effort slot — the
  finding's `_FIX_PATH` quotes the taught byte-form but never mentions
  `unrecorded`, so the repairer's honest option is only discoverable via
  `.sessions/README.md`. One clause in `_FIX_PATH` ("not the author and no
  self-reported tier? use `unrecorded`") puts the anti-fabrication rail in
  the exact moment of temptation. Dedup: grepped docs/ideas/ —
  model-line-unrecorded-effort-marker (this PR) sanctions the value but its
  sketch never touches the finding message; nothing else covers it.
- ⟲ Previous-session review (2026-07-15-merge-verification-probe, PR #393):
  as a cross-repo dispatch it did its one job — the probe doc landed,
  auto-merge-on-green was empirically confirmed, and it honestly declared
  its enders not-applicable instead of filling them with ceremony. But its
  Model line squeezed two markers onto one line (`sonnet-5 · **Run
  type:**...`), which the payload lint immediately flagged and the harvest
  silently dropped — this session had to retro-repair it (7e71513).
  Concrete improvement: shipped as this card's 💡 above — put the
  `unrecorded` guidance into the lint's own fix-path message so a foreign
  or dispatched session composing/repairing a card sees the taught form
  AND the honest fallback in the same sentence.

## 📤 Run report

- **Did:** sanctioned `unrecorded` as the advisory-silent terminal effort
  value in `check_model_line` + docs line + tests + dist regen + idea
  lifecycle flip; retro-repaired the #393 card's malformed Model line
  (fix-on-sight, flagged) · **Outcome:** shipped, PR #394
- **Shipped:** src/engine/checks/check_model_line.py ·
  tests/test_check_model_line.py · .sessions/README.md · dist/bootstrap.py
  (regen) · docs/ideas/model-line-unrecorded-effort-marker-2026-07-15.md +
  docs/ideas/README.md (lifecycle) · CHANGELOG.md ·
  .sessions/2026-07-15-merge-verification-probe.md (repair) · this card
- **Run type:** work-loop slice (coordinator-dispatched, baton item 2)
