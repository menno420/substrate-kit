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

## [1.7.0] - 2026-07-10

New-capability release (MINOR) folding the kit-lab enforcement + adopter-findings
queue shipped since v1.6.0: the order-bus append-only + ORDER-grammar enforcer
(#87), the claim-aware checker that gives the ORDER 007 convention teeth (#90),
the OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (#98), lane-aware
`adopt --lane <name>` for shared multi-Project repos (#103), the upgrade-UX and
`--apply-docs`/post-hoc-apply mechanisms, telemetry backfill at card-commit
(#91), the engagement-gate comment-leniency fix (#86), and a batch of
adopter-found substrate-gate template fixes (#95/#99, gba-homebrew field
reports). No planted-doc, state schema, config schema, or CLI contract breaks —
every new checker is advisory-only or additive, existing installs inherit all of
it on `upgrade`.

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory statement for a MINOR):** B1 cold-start
run-3 was recorded this cycle (`2026-07-10-run03`, seed 710301 northride, kit
v1.6.0 ENGAGED arm) — VERDICT: **FAIL under the strict F-5 letter** (M1 to OFF on
all three pairs 2004/2521/721 vs 562/967/509) while ON wins M2 (resume-and-ship)
+ M3 (durable write-back), max ON footprint 2,521 ≪ 7k budget, zero
unrecoverable errors; disputed pending the F-5 wording ruling (Reading B would
PASS). KF-8's 3-run threshold is now met: across all three runs ON wins M2+M3
every run and stays in-budget, strict-M1 headline 1 PASS / 2 FAIL — caveated on
the open ruling and the version/seed/judge confounds (run-3: judge = arm model,
claude-fable-5 everywhere, spawn-harness model overrides ignored). Full detail in
the `### Added` B1 run-3 entry below.

### Added

- **`adopt --lane <name>` — lane-aware adoption for SHARED multi-Project
  repos** (kit-lab queue item 11, the self-review G1 double-adoption fix):
  the seeded heartbeat plants as `control/status-<name>.md` instead of the
  singular `control/status.md` and is declared in `substrate.config.json` →
  `heartbeat_files` (replacing the untouched default when no Project owns
  the singular file; appending — never dropping a sibling lane — otherwise),
  while `control/inbox.md` and `control/README.md` stay single and
  skip-if-exists. A second Project joining an adopted repo now runs one
  command instead of hand-creating its heartbeat, hand-editing
  `heartbeat_files`, and risking a second full adopt. Lane names are
  validated (letters/digits/hyphen/underscore) before any write; the
  multi-Project section of the planted `control/README.md` documents the
  one-command shape.
- **OWNER-ACTION ↔ CAPABILITIES cross-reference advisory**
  (`check_capability_xref`, kit-lab queue item 8 — the #68 card idea):
  `check` now cross-references every wall-shaped ⚑ OWNER-ACTION ask
  (VERIFIED-NEEDED citing a 403 / access-denied / owner-only surface)
  against the planted `docs/CAPABILITIES.md` ledger and warns, advisory-only
  (never exit-affecting, the `check_claims` posture):
  `owner-ask-wall-unrecorded` when the cited wall is nowhere in the ledger
  (append it — THE DISCOVERY RULE step 4), and
  `owner-ask-capability-resolved` when the ledger records the surface only
  as verified-working (the wall may have fallen — re-verify or withdraw the
  ask). Judgment-shaped asks (license/product rulings) are out of scope;
  matching is coarse distinctive-token overlap by design. Rides both CI
  lanes; every owner-ask becomes a capability-ledger contribution for free.
- **B1 cold-start run 3 recorded (KF-8 threshold met — first legal trend
  statement)**: row 3 appended to `bench/results/cold-start/index.json` +
  committed run dir (`2026-07-10-run03`, seed 710301 northride, kit v1.6.0
  ENGAGED arm). Judge verdict verbatim: **FAIL under the strict F-5 letter**
  (M1 to OFF on all pairs 2004/2521/721 vs 562/967/509) while ON wins M2
  (T4 resumed from T2's card and shipped its queued fix) + M3 (durable
  write-back), max ON footprint 2,521 ≪ 7k budget, zero unrecoverable
  errors; disputed pending the F-5 wording ruling (Reading B would PASS).
  Trend across 3 runs: ON wins M2+M3 in every run, in-budget always; M1 to
  OFF in every clean measurement (strict headline 1 PASS / 2 FAIL) —
  caveated on the open ruling + version/seed/judge confounds (run-3
  deviation: judge = arm model, claude-fable-5 everywhere, spawn-harness
  model overrides ignored). Per KF-5 the next release's notes must state
  this outcome.
- **`control/inbox.md` append-only + ORDER-grammar enforcement**
  (`check_inbox_append`, kit PR #87 — friction issue #36 report 2): the
  order bus's append-only law was convention-only (any session could
  rewrite or erase ORDERs on a green control-only PR — #34 merged 19 s
  after open with nothing checking). `check --inbox-base <file>` now
  verifies an inbox change is PURE-APPEND vs the merge-base (the base
  file's bytes are a prefix of the new file) and that the appended text
  follows the ORDER-block grammar; CI extracts the merge-base blob and
  hands the path in (the engine never shells out, §3.2), running on BOTH
  lanes. Writer IDENTITY stays deliberately unenforced — on a
  single-account program it is not enforceable in-repo, recorded honestly
  in `control/README.md` (kit PR #89) rather than pretended at.
- **Claim-aware checker** (`check_claims`, kit PR #90 — queue item 7, the
  #69 card idea): the ORDER 007 order-claim convention shipped doc-only,
  enforced by nothing. `check` now scans every configured heartbeat's
  `orders:` line for `claimed-by:` annotations and flags, advisory-only
  (never exit-affecting): `claims-duplicate` — two DISTINCT heartbeat
  files claim the same order id (the realized #50/#51 twin-execution
  race; the tiebreak stays a human call) — and `claims-stale` — a live
  claim for an id already in some lane's `done=`, or older than the
  convention's ~24h abandonment horizon.
- **SuperBot-coordinator lane wind-down succession pack** (docs-only,
  suffixed per the multi-lane rule): `docs/succession/` (new, with README
  index) carrying the gen-2 next-boot guide (read order, queue state,
  walking-skeleton check, known walls with exact error text), the Custom
  Instructions rewrite proposal, the environment spec (setup script
  re-verified exit-0 in no-repo and with-repo cases), and gen-2 blueprint
  feedback; plus the wind-down retro addendum
  `docs/retro/wind-down-review-2026-07-09-superbot-coordinator.md`
  (whole-life summary, exact-error friction ledger, first-person close)
  and the lane heartbeat flipped to wind-down-complete.

### Fixed

- **Engagement gate comment-leniency** (`check_engagement`, kit PR #86 —
  friction issue #36 report 1): `_enforcement_wired` substring-matched
  `check --strict` across whole workflow files, so a workflow whose only
  mention sat inside a `#` comment falsely cleared the gate — a repo
  looked ENGAGED with a dead door. `#`-prefixed comment content is now
  stripped per line before the needle test (still forgiving of
  hand-rolled gates, immune to comments); a known-bad fixture must red as
  `enforcement-unwired`, a genuinely-wired workflow still passes.
- **Telemetry undercount — model-usage rows now written at card-commit**
  (`reconcile_model_usage`, kit PR #91 — queue item 6): the PL-004 feed
  recorded 10 rows against 42 eligible cards because the harvest ran only
  at `session-close` and only over the newest card by mtime — any card
  committed while a newer one existed was silently dropped.
  `session-close` now also sweeps EVERY complete card carrying a valid
  `📊 Model:` line and appends the missing rows — idempotent (dedupe by
  session slug), append-only, fail-open; the backfill landed the ~3-of-4
  dropped sessions in the same PR.
- **Four upgrade-UX fixes from the v1.6.0 fleet rollout** (kit PR #92 —
  queue item 10; stranded READY+green when its authoring session lost the
  auto-merge arm race, adopted and merged by the #98 lane): the
  idempotent `archive_dist` early-return now prints `archived: <rel>
  (already banked)` instead of silence; `classify_planted_docs`
  self-heals doc-hash records lost to `--rollback` + re-run (a doc that
  byte-matches the new template render is provably kit-form); the
  `ADOPTER_CHECKLIST` names `release.json` beside `bootstrap.py.new` and
  the silent-skip consequence when absent; and the `--apply-docs` hint
  names the real `--rollback` + re-run recovery instead of a no-op
  "re-run" (interim slice — the full post-hoc apply mechanism idea stays
  open).
- **Adopter-findings batch** (kit PR #99, venture-lab field reports): the
  `owner-action-fields` checker now also accepts the WHY /
  VERIFIED-WHEN shorthand alongside the canonical WHY-IT-MATTERS /
  VERIFIED-NEEDED tokens (backward-compatible — an accepted alternate
  only withholds the advisory nag; tests pin checker↔template token
  agreement); plus two wall+recipe appends to `docs/CAPABILITIES.md` (and
  `docs/operations/auto-merge-guards.md` § Operational notes): the
  fast-CI auto-merge arm race (sub-~10 s CI flips `pending`→`clean`
  before `enable_pr_auto_merge` binds — fall back to REST merge-on-green
  or a deliberate pending window) and the parallel file-mutating
  subagents race in a shared clone (isolated worktree per writer OR
  serialize; never `git add -A` from a shared checkout).
- **Planted substrate-gate template: no-card and born-red-heartbeat PRs no
  longer red on an unrelated card** (`live_ci_workflow()` in
  `src/engine/adopt.py` — two adopter-found defects, both hit and fixed live
  on menno420/gba-homebrew and validated across its PRs #3–#14):
  - A PR whose diff names **no session card** now passes an explicitly named,
    nonexistent sentinel (`--session-log <sessions_dir>/__no-card-in-diff__.md`)
    **without** `--require-session-log` — advisory per the engine contract.
    The previous behaviour (omitting the argument) was believed fail-open but
    was not: on a fresh CI checkout the newest-by-mtime fallback latched onto
    the mid-session in-progress card and redded every unrelated PR
    (gba-homebrew PR #3).
  - A card **ADDED** by the PR (a born-red heartbeat — first-commit
    conventions require an in-progress card at birth) gates advisory via the
    absent sentinel (`__born-red-card-added__.md`), since under `--strict` the
    locked door reds ANY existing-but-incomplete card and a heartbeat could
    never merge green (gba-homebrew PR #2 merged red on exactly this). A card
    **MODIFIED** by the PR (every close-out flips one) keeps the full
    `--require-session-log` locked-door gate, so a close-out that forgot to
    flip `complete` still reds.
- **Run-2 ordinary-lane follow-ups (kit PR #95)** — the three engine/harness
  gaps the B1 record sessions filed as idea files:
  - `bench/run_ab.py prepare` no longer fails by design on ON arms: it walks
    the KL-7 RED→ENGAGED→GREEN arc itself (deterministic seed-derived
    interview answers, `render --live`, staged-gate install, first session
    card, seed heartbeat), asserts `check --strict` exit 0, and writes
    `manifest.json` on the failure path too (`smoke_failed` marker) so an
    aborted prepare leaves evidence.
  - `render --live` now covers `.claude/CLAUDE.md` (and every other
    engagement-gate-scoped planted file): the render set is the gate's own
    `scan_relpaths()`, so the two surfaces can never again disagree about
    whose job a planted file is and the KL-7 checklist completes by its own
    named commands.
  - Session-marker misses name the expected byte-form: the planted
    `.sessions/README.md` renders ``label (`needle`)`` pairs (a cold session
    can learn the `📊 Model:` form from inside the repo) and the session-log
    checker reports ``Model line (expected `📊 Model:`)`` instead of a bare
    label that contradicts the visible card. (Distinct from the
    `parse_model_line` harvest-shadowing fix in PR #40.)

## [1.6.0] - 2026-07-09

New-capability release (MINOR) covering two coordination-protocol bands
(inbox ORDERs 007 + 008, both from the 2026-07-09 fleet retro synthesis /
owner directive; ORDER 008's band merged in PR #68, ORDER 007's in this
cut's PR):

- **Owner-action quality band (ORDER 008):** agents' ⚑ needs-owner asks
  were too often unnecessary (assumed walls nobody hit) or unactionable by
  a non-technical owner. Every ask now carries six REQUIRED OWNER-ACTION
  fields — WHAT / WHERE / HOW / WHY-IT-MATTERS / UNBLOCKS /
  VERIFIED-NEEDED (attempted, or the exact wall; assumption-based asks
  banned) — with an advisory `check` warning and a session-close hygiene
  step behind it.
- **Order-claiming convention (ORDER 007):** the root-cause fix for the
  realized #50/#51 twin-execution failure (two sessions both saw an order
  still `new` and executed it twice). An executing session now claims
  FIRST — `claimed-by:` on its own status orders line, landed on main
  before any build work — re-reads inbox + sibling statuses after the
  claim merges, and stale claims (~24h, no activity) expire so a dead
  lane never deadlocks an order.

No planted-doc, state schema, config schema, or CLI contract breaks (the
new checker is advisory-only and can never red a gate; template changes
are additive; existing installs inherit both bands on `upgrade`).

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory statement for a MINOR):** no fresh
firing this release — both bands are templates + docs + an advisory-only
checker and touch no scored surface; the standing run of record remains B1
run-2 (`2026-07-09-run02`, VERDICT: FAIL under strict F-5,
advisory-to-pass) as stated in v1.4.0/v1.5.0. Run-3 stays gated behind the
#49 seed fix (owner-gated, one click) and the F-5 wording ruling.

### Added

- **Owner-action quality band** (ORDER 008, PR #68):
  - `check_owner_actions.py` — advisory-only checker (never
    exit-affecting, both CI lanes incl. `--status-only`): one
    `owner-action-fields` finding per configured heartbeat file whose
    `⚑ needs-owner` value is non-`none` while the file lacks any of the
    six field labels; guard-fire telemetry recorded; multi-lane via
    `heartbeat_files`; fail-open on unreadable files.
  - `control-README.md.tmpl` § "⚑ needs-owner — the OWNER-ACTION item
    format": the six REQUIRED fields, the
    try-it-yourself-or-cite-the-exact-wall bar, stale-ask expiry,
    fewer-clearer-asks doctrine (self-hosted `control/README.md` matches).
  - Doctrine wiring: `CONSTITUTION.md.tmpl` autonomy rail "Owner
    attention is the scarcest resource"; `collaboration-model.md.tmpl`
    § "Routing work to the owner"; `session-close` skill step 3
    "Owner asks" (steps renumbered).
- **Order-claiming convention** (ORDER 007, this PR):
  - `control-README.md.tmpl` § "Claiming an order — one executor per
    order": claim FIRST on your own status orders line
    (`claimed-by: <ids> <lane-or-session> <ISO8601>`, landed on main
    before build), re-read inbox + sibling statuses post-merge (tiebreak:
    earliest merged claim), ~24h no-activity claim expiry; the
    per-session ritual bullet and the status-format `orders:` line now
    reference the claim (self-hosted `control/README.md` matches).
    One-writer-per-file is preserved — a lane only ever claims on its
    own status file.

### Changed

- Suite 707 → 722 (owner-action checker suite + skill/adopt wiring +
  claim-convention plant assertions).

### Notes

- ORDER 007's other half — disposing of duplicate-execution PR #50 — was
  verified already terminal (merged 2026-07-09T17:40:03Z as the
  lane-suffixed salvage, before the order was appended); a disposition
  comment on #50 records the audit trail.

## [1.5.0] - 2026-07-09

New-capability release (MINOR): the **capability-manifest band** (inbox
ORDER 006, owner directive 2026-07-09 — sessions repeatedly stall on
imagined walls and forget provisioned capabilities, burning owner attention
as hand reminders). Adopted repos now get a planted `docs/CAPABILITIES.md` —
the verified ledger of what sessions can/cannot do plus THE DISCOVERY RULE
(check file → check env → attempt once + capture the exact error → append
same session) — wired into the orientation reading order and nudged at
session close. No planted-doc, state schema, config schema, or CLI contract
breaks (one additive ADOPT_PLAN entry; existing installs inherit the doc on
`upgrade`, skip-if-exists as always).

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory statement for a MINOR):** no fresh
firing this release — the band is templates + docs wiring and touches no
scored surface; the standing run of record remains B1 run-2
(`2026-07-09-run02`, VERDICT: FAIL under strict F-5, advisory-to-pass) as
stated in v1.4.0. Run-3 is deliberately gated behind the #49 seed fix
(owner-gated, one click) and the F-5 wording ruling.

### Added

- **`CAPABILITIES.md.tmpl`** (ORDER 006): new content template planted at
  `docs/CAPABILITIES.md` on adopt — seed content: the media→ffmpeg-frames→
  read recipe, printenv-before-assuming-no-credentials, and the fleet's
  verified walls (tag/release/branch-delete 403s with the
  workflow_dispatch release workaround, env/routine/Project creation =
  owner clicks, the self-merge classifier line incl. the
  coordinator-vs-child asymmetry, the GraphQL quota), plus THE DISCOVERY
  RULE and an append log.
- **Orientation wiring** (ORDER 006): `CLAUDE.md.tmpl`,
  `CONSTITUTION.md.tmpl` (a "Capabilities are discovered, never assumed"
  working-agreement bullet), and `AGENT_ORIENTATION.md.tmpl` (start-of-
  session list + planted-doc set) all route every session through
  `docs/CAPABILITIES.md` at start.
- **Session-close capability nudge** (ORDER 006): the `session-close`
  skill's procedure gains step 2 — "did you discover a new capability or
  hit a wall this session? append it."
- **Self-hosted `docs/CAPABILITIES.md`** in this repo, seeded with the
  fleet findings plus a same-day live one: cross-repo reads are
  allowlisted per session (`menno420/fleet-manager` returned "not
  configured for this session" — which is also why the master-copy sync is
  documented as manager-relayed rather than performed directly).

- **SuperBot-coordinator lane wake-up review** (suffixed per the owner's
  multi-lane rule; a different Project than kit-lab, filed here because the
  gen-1 retro protocol lives in `docs/retro/`):
  `docs/retro/project-review-2026-07-09-superbot-coordinator.md` (the
  SuperBot-rebuild true state + full coordinator-fleet agent audit +
  efficiency verdict + ⚑ owner actions + continuation) and
  `docs/retro/self-review-2026-07-09-superbot-coordinator.md` (every
  `docs/retro/QUESTIONS.md` ID answered from the coordinator lane's
  vantage), plus the lane heartbeat
  `control/status-superbot-coordinator.md` (not yet in `heartbeat_files`
  by design — kit-lab owns the config; decide-and-flag).
- **Kit-lab-coordinator-lane retro companions** (ORDER 005, twin execution):
  `docs/retro/self-review-2026-07-09-kitlab-coordinator.md` +
  `docs/retro/project-review-2026-07-09-kitlab-coordinator.md` — the
  parallel coordinator-spawned lane's independent answers + the
  session-side agent audit (35-session fact ledger, model split, stall
  census) cross-checked against the repo with discrepancies named (incl.
  the telemetry harvest gap: 11 post-KL-3 cards' Model lines never
  harvested). Docs-only.
- **Gen-1 retro self-review + project review** (inbox ORDER 005):
  `docs/retro/self-review-2026-07-09.md` — every `docs/retro/QUESTIONS.md`
  question answered by ID with PR/commit/file evidence — and
  `docs/retro/project-review-2026-07-09.md` — true current state, the full
  agent audit (every session, with stall/death causes classified), the
  honest efficiency verdict, ⚑ owner actions, and the continuation plan.

## [1.4.0] - 2026-07-09

New-capability release (MINOR): **configurable heartbeat paths** for
multi-Project repos (inbox ORDER 004, rider to v1.3.0's adopter-visibility
band — relayed from a real adopter finding: superbot-games is a SHARED repo
with per-lane heartbeats, and the status checker hardcoded
`control/status.md`, misfiring on that shape). The validated heartbeat set
is now `substrate.config.json` → `heartbeat_files` (default
`["control/status.md"]`), the per-lane pattern is documented in the planted
`control/README.md` contract, and superbot-games is registered as the
two-lane adopter. No planted-doc, state schema, config schema, or CLI
contract breaks (the config key is additive; unset configs behave exactly
as before).

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory run for a MINOR):** B1 run-2
(`2026-07-09-run02`, fired since v1.3.0 on the #40-fixed scorer) is the run
of record — **VERDICT: FAIL** under the strict F-5 "none regressing" clause
(judge claude-opus-4-8, independent; M1 regressed ON 1706/2272/531 vs OFF
556/1481/511) while ON wins M2 + M3 inside the 7k budget with zero
unrecoverable errors. Advisory-to-pass per KF-5's letter — a release that
regresses the A/B says so in its own changelog (founding plan §4). No trend
claim (family at 2 rows; KF-8 needs ≥3); the F-5 wording decision is
⚑ owner-pending (`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`).

### Added

- **Configurable heartbeat paths** (ORDER 004): new `substrate.config.json`
  key `heartbeat_files` (list of repo-relative status files; default
  `["control/status.md"]`; empty/unset falls back to the default so a
  misconfiguration can never silently disable the gate).
  `check_status_current` validates every listed file independently —
  per-lane `status-missing` / `status-no-heartbeat` gate findings and
  per-lane `status-stale` advisories, each naming its own file — and both
  `cli.py` consumers (`cmd_check`, incl. the `--status-only` control fast
  lane, and `cmd_adopt`'s engagement checklist) plus the Stop-hook
  overwrite reminder read the configured list (the hook clears on ANY
  fresh lane, since it cannot know which lane a session belongs to).
- **Per-lane multi-Project pattern in the planted contract**
  (`control-README.md.tmpl` + the kit's own `control/README.md`): one
  status file per lane (`control/status-<lane>.md`), single manager-owned
  `inbox.md`, lanes declared via `heartbeat_files` — the one-writer rule
  scales by splitting the heartbeat, never by sharing it.
- **`docs/adopters.md`: superbot-games registered as the two-lane adopter**
  (per-lane heartbeats `control/status-mining.md` +
  `control/status-exploration.md`; kit_version/engaged pending the first
  relayed per-lane `kit:` line).
- **B1 run-2 recorded** (`2026-07-09-run02`, PR #44): second cold-start
  row appended (append-only) + raw run dir committed at
  `bench/results/cold-start/2026-07-09-run02/`. Judge claude-opus-4-8
  (independent): **VERDICT FAIL** under the strict F-5 "none regressing"
  clause — the first clean M1 measurement on the #40-fixed scorer
  regressed (ON 1706/2272/531 vs OFF 556/1481/511) — while ON wins M2
  (handoff actually used) + M3 (durable write-back) inside the 7k budget
  with zero unrecoverable errors; advisory per KF-5, no trend claim
  (family at 2 rows, KF-8 needs ≥3). Run-2 follow-up ideas filed
  (rubric F-5 wording owner brief · make_seed yield-keyword bug ·
  prepare engagement arc · render CLAUDE.md gap · T5 idea updated with
  the last-card gate gap); fixes deliberately not in the recording PR.

## [1.3.0] - 2026-07-09

New-capability release (MINOR): the substrate-coordinator visibility band
(inbox ORDER 003, rider to v1.2.0's coordination protocol) — every adopter
self-reports its kit state in its own heartbeat, kit-lab keeps the fleet
adopter registry, and every release's notes automatically carry the adopter
upgrade checklist — plus the fleet-review fast-lane hardening and the run-2
harness fixes shipped since v1.2.0. Zero new access anywhere (KF-2-clean:
the kit never writes adopter repos; the manager relays orders). No
planted-doc, state schema, config schema, or CLI contract breaks.

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory run for a MINOR):** the standing B1
cold-start baseline `2026-07-09-run01` — **VERDICT: PASS** (judge
claude-opus-4-8, independent; row 1 of
`bench/results/cold-start/index.json`) — remains the run of record. No fresh
firing this MINOR: run-2 is the next queued lane, deliberately sequenced
*after* this release so it fires on the fixed scorer (both run-1 M1 scorer
taints were fixed + regression-tested in #40); advisory-to-pass per KF-5's
own letter; no trend claim (KF-8 needs ≥3 paired runs).

### Added

- **The `kit:` heartbeat self-report line** (ORDER 003 item 1): the planted
  `control/status.md` seed now carries
  `kit: v<X.Y.Z> · check: green|red · engaged: yes|no`, rendered with the
  REAL running kit version at adopt — `build_context` injects the
  engine-computed `kit_version` key (`ENGINE_CONTEXT_KEYS`, exempt from the
  template/bank coherence guard) on every render path — and the planted
  `control/README.md` contract documents the line's format + update duty
  (keep the version current in the same session as every upgrade). Every
  adopter self-reports kit state in its heartbeat; the coordinator needs
  zero new access.
- **`docs/adopters.md` — the fleet adopter registry** (ORDER 003 item 2):
  repo · kit_version · engaged · last-seen, sole writer kit-lab, seeded
  from the 2026-07-09 fleet-review facts (superbot-next + websites ENGAGED
  on v1.2.0, superbot deliberate v1.0.0 pin-only, trading-strategy + game
  repos planned). Fed by relayed `kit:` heartbeats, never by writing
  adopter repos (KF-2).
- **Adopter upgrade checklist in every release's notes** (ORDER 003
  item 3): `src/build_release_json.py` appends the version-stamped
  checklist (run `upgrade` → `check --strict` green → engagement green →
  update your `kit:` status line) to `notes.md` automatically — the
  appender lives in the asset builder, so a release author cannot forget
  it (enforce, don't exhort).
- **`check --status-only` — the fast lane's scoped gate** (MINOR, new CLI
  capability): runs ONLY the `control/` status heartbeat checker
  (`check_status_current`); the allowlist and guard-fire telemetry apply
  exactly as in a full run, and the session-log seam is never touched
  (heartbeat PRs carry no card by design, so the lane cannot deadlock).
  Stdlib-only, so a CI lane can run it on the system `python3` without
  `setup-python`.

### Fixed

- **The CI control fast lane is no longer checker-free** (fleet adoption
  review 2026-07-09, finding 1 — med): the lane skipped
  `check_status_current` on exactly the PRs that write control files, so
  a heartbeat-deleting control-only PR rode the lane GREEN while
  `check --strict` on the same tree exits 1 (`status-no-heartbeat`) —
  deferring the red onto the NEXT unrelated full-suite PR, the same
  "bomb" shape the checker's docstring rules out for time-staleness,
  reintroduced for content-validity. Both the kit's own `ci.yml` and the
  planted `substrate-gate.yml` now run `check --strict --status-only` as
  a fast-lane step (only when `control_only == 'true'`). Reproduced
  before/after on a v1.2.0 fixture; pinned by
  `tests/test_ci_control_lane.py` + `tests/test_adopt.py`; scoping
  behavior pinned by three `tests/test_cli_gate.py` cases.
- **`bench/score_m1.py` run-1 artifact fixes** (#40, run-2 harness prep):
  read-only fd redirects (`2>/dev/null`, `2>&1`, …) no longer count as
  mutations, and a mutating tool_use whose paired tool_result is an error
  is cancelled (failed Edits don't stop the M1 count) — all three run-1
  M1 taints reproduce as regression tests; recorded run-1 results
  untouched (append-only law).
- **`parse_model_line` last-valid-line fix** (#40, found live in
  websites#31): a prose line that merely mentions the `📊 Model:` marker
  can no longer shadow the genuine line into a false "no line" advisory —
  the harvest keeps the last line that parses validly.

## [1.2.0] - 2026-07-09

New-capability release (MINOR): the fleet coordination protocol becomes a
kit capability — every adopted repo gets the `control/` git-as-message-bus
(manager inbox + project status heartbeat + the planted contract), the
heartbeat is enforced by a new dist-shipped checker, and coordination
writes ride a CI fast lane that can never jam a required context. No
planted-doc, state schema, config schema, or CLI contract breaks.

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory run for a MINOR):** the standing B1
cold-start baseline `2026-07-09-run01` — **VERDICT: PASS** (judge
claude-opus-4-8, independent; row 1 of
`bench/results/cold-start/index.json`, recorded earlier the same day for
the v1.1.0 cycle) — is the run of record for this release: no fresh firing
was made because run-2 is deliberately gated behind the filed harness
fixes (`docs/ideas/score-m1-mutation-artifacts-2026-07-09.md` et al. — a
same-day re-fire would reproduce the known-tainted M1 pairs), KF-5 is
advisory-to-pass and never release-blocking, and no trend claim is made
(KF-8 requires ≥3 paired runs). Nothing in this release touches the
benchmarked handoff surface.

### Added

- **The `control/` fleet-coordination scaffold** (band KL-8, inbox ORDER
  002; canonical spec: superbot
  `docs/planning/fleet-coordination-protocol-2026-07-09.md` §2 — MINOR,
  new templates): `adopt` now plants the git-as-message-bus protocol in
  every host — a generalized `control/README.md` contract (roles, the
  one-writer-per-file rule, both file formats, and the two 2026-07-09 CI
  lessons: prefer an in-job fast lane over `paths-ignore`, and
  API-authored PRs may carry zero check runs — the manager's canonical
  inbox write is a direct Contents-API commit to the default branch) plus
  seeded-skeleton `control/inbox.md` (manager-written orders) and
  `control/status.md` (the project-written heartbeat — honestly
  heartbeat-less until the first real overwrite). Skip-if-exists,
  hash-recorded, `${project_name}`-rendered like every plant.
- **`check_status_current` — the status-freshness checker** (engine-side,
  ships in the dist — MINOR, new checker): a missing or heartbeat-less
  `control/status.md` rides the strict finding loop RED
  (`status-missing` / `status-no-heartbeat` — the spec's "graduates to
  the born-red post-adopt gate", printed on the adopt checklist alongside
  the KL-7 engagement findings); wall-clock staleness (`status-stale`,
  > 72h) is **advisory-only** — surfaced and telemetry-recorded but never
  exit-affecting, so a required CI check can never red on time alone.
  The Stop hook gains a fifth advisory: `control/status.md` not
  overwritten this session (file mtime vs the KL-5 session anchor).
  Input-gated: a host without `control/` sees nothing.
- **The CI control fast lane**: a control-only diff (`control/**` and
  nothing else — a heartbeat, an inbox append) short-circuits the heavy
  suite GREEN **in-job** in both the kit's own `ci.yml` and the planted
  `substrate-gate.yml` — deliberately never `paths-ignore`, because a
  REQUIRED context that never reports stays pending forever and jams
  heartbeat auto-merge; the session gate is among the skipped steps
  (coordination writes need no session card). Pinned by
  `tests/test_ci_control_lane.py`; the cold-adopt smoke now walks the
  extended arc (RED on the seed status → GREEN after the first real
  heartbeat).

### Fixed

- **Dist-completeness guard**: an engine module missing from
  `build_bootstrap.MODULE_ORDER` builds a dist whose `cmd_check` crashes
  with a `NameError` at runtime while the byte-pin stays green (the fresh
  build is equally incomplete) — hit live when `check_status_current.py`
  first shipped. `test_module_order_covers_every_engine_module` now pins
  `MODULE_ORDER` == the on-disk `src/engine/` module set.

## [1.1.0] - 2026-07-09

New-capability release (MINOR): everything the kit-lab run built since
v1.0.0 — program law, telemetry, the friction loop, the auto-drafted
handoff + benchmark harness, and the post-adopt ENGAGEMENT gate that fixes
the "adopted but never onboarded" fleet finding. No planted-doc, state
schema, config schema, or CLI contract breaks.

<!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

**Benchmark outcome (KF-5 — mandatory run for a MINOR):** B1 cold-start
run `2026-07-09-run01` — **VERDICT: PASS** (judge claude-opus-4-8,
independent): ON wins M2 (resumed from a genuinely-used handoff) and M3
(durable write-back). No regressions established. M1 unmeasurable this run
(all 3 pairs scorer-tainted — artifacts of the scorer, not the kit; run-2
harness fixes are filed in `docs/ideas/`); the T5 guard probe was n/a
(headless arms never engaged the hook layer). Row 1 of
`bench/results/cold-start/index.json`.

### Added

- **The `bench/` tree — the pinned benchmark harness** (band KL-5, plan
  §5.0/§5.1 — MINOR, new capability; first rubric version **owner-blessed**
  on the `do-not-automerge` PR that authored it): the B1 cold-start judge
  rubric + the B2 allocation rubric; fixed task texts T1–T5 (T5 = the new
  break-a-rule guard probe, D-17, run with `--wire-enforcement` arms); the
  seed-corpus generator (`bench/seeds/make_seed.py` — fresh surface names
  per run, same shape, one seeded untested bug); `bench/score_m1.py`
  (scripted words-before-first-mutation over event-JSONL transcripts);
  `bench/run_ab.py` (`prepare` builds identical arms + adopts ON + the §5.1
  smoke step · `collect` files artifacts + scores M1 immediately ·
  `record` appends schema-checked, run_id-deduped rows); append-only
  `bench/results/{cold-start,allocation,guards,ideas,friction}/index.json`;
  and `scripts/check_bench_integrity.py` in the kit-quality gate — pin-path
  changes (`bench/rubric|tasks|seeds`) must ride a `do-not-automerge` PR,
  and `bench/results/` history is immutable (index appends allowed,
  edits/deletes never). B1's first firing follows the rubric's owner
  blessing — never run or graded by the session that authored it.

- **Auto-drafted session handoff** (band KL-5, plan §10 — MINOR, new
  capability; the ruled prerequisite for B1's first firing): `session-close`
  and the Stop hook now **draft** the session card's close-out from evidence
  instead of exhorting the agent to write one (the twice-measured Phase-2.5
  failure: discipline-dependent write-back does not happen). Evidence — all
  pure stdlib, no subprocess: a **session-start anchor** (timestamp + git
  HEAD/branch parsed from `.git`, worktree-aware) recorded by the
  SessionStart hook / `session-start`; an mtime scan of files touched since
  the anchor, classified code/tests/docs/sessions; HEAD movement; the
  derived `verify_command` slot (carried as a run-and-record slot — the
  engine never fakes results). A missing card gets a drafted skeleton
  (`Status: drafted`); an in-progress card missing close-out markers gets
  the drafted section (+ needle-carrying stand-ins for exactly the missing
  markers) appended; completed cards are never touched. New on-demand
  `draft` verb runs the same seam. The session-log checker gains the
  **drafted-vs-completed distinction**: unresolved `[[fill:]]` slots and the
  `drafted` status token hold the born-red gate with a distinct finding, and
  a drafted `📊 Model:` stand-in line is never harvested into the
  PL-004 feed. Everything fail-open: drafting can never crash a hook or
  session-close.

- **The B4 ideas-frontmatter convention + `check_idea_index.py`** (band
  KL-6, plan §5.4 — MINOR, new checker; convention and checker ship in the
  same PR): every `docs/ideas/` entry opens with a flat YAML-subset
  frontmatter block `{state, origin, shipped_pr, shipped_repo, merged_date,
  outcome}` — the machine-readable "ideas that ship and survive" record the
  B4 sweep scores. `scripts/check_idea_index.py` (stdlib, kit-quality gate)
  enforces the grammar, the outcome-consistency rules (ship outcomes require
  the ship fields; `survived` requires the 30-day D-15 window), the
  `-YYYY-MM-DD.md` cohort-key filename, and README-backlog index consistency
  (every file linked, every link resolving). Existing entries migrated; the
  planted `ideas-README` template documents the convention for consumers
  (dist regenerated + byte-pinned). `telemetry/*.jsonl` gains a
  `merge=union` gitattribute so parallel sessions' append-only rows never
  conflict.

- **Explicit + diff-aware session-gate card selection** (groomed-ideas-1 —
  MINOR, new CLI surface): `check --session-log <file>` gates on the named
  card instead of the newest-by-mtime guess, which a fresh CI checkout
  silently degrades (every mtime flattens to checkout time); a missing named
  file counts as an absent log, never a silent fallback. The kit's own
  `ci.yml` and the planted `substrate-gate.yml` (`adopt --wire-enforcement`)
  now derive the card from what the PR/push diff touches and pass it
  explicitly — the git-mtime-restore CI shim is deleted kit-side and never
  travels to consumers. No argument → mtime selection unchanged (fail-open,
  backward-compatible). Companion conventions in the same PR: the reflection
  miner only harvests 💡/⚑ lines *led* by the marker (mid-prose
  cross-references were mined as junk lessons), and session cards carry
  **guard recipes** (function + file + test anchors) for deferred
  friction→guard entries (both `.sessions/README`s).

- **The `friction` verb + outbox** (band KL-4, plan §9.1 — MINOR, new CLI
  capability): `friction export` collects the install's ⚑ friction records
  (reflection buffer + a full session-log scan, deduplicated — D-14), wraps
  them in the wire envelope `{schema: 1, repo, project_id, kit_version,
  reports[reflection-records]}`, writes it to
  `<state_dir>/friction-outbox/` (atomic, serial-numbered), and prints the
  issue-ready title + body; `friction list` / `friction show <name>` drive
  the drain. The engine (stdlib-only, credential-free) never files the
  issue — the session/agent files it on the kit repo with the `friction`
  label and deletes the drained file; `session-close` advises on pending
  envelopes (best-effort, fail-open).
- **The lab-loop routine doc** (`docs/operations/lab-loop.md`, plan §6):
  definition table + the paste-ready 9-part prompt (daily cron `0 6 * * *`
  UTC, fresh session per fire, Sonnet-class default / Opus escalation per
  D-11, the scope fence, the `Run type: routine · lab` token, kill
  switches) + the exact 👤 P4 arming steps. Git is the prompt's source of
  truth; console copies are re-pasted on change.

- **Telemetry substrate** (band KL-3, plan §5.2/§5.3 — MINOR, new
  capability): guard-fire JSONL writers at the two local choke points
  (`check`'s finding loop, `hook`'s dispatch) appending §5.3 records to
  `<state_dir>/guard-fires.jsonl` — fail-open by contract, written only into
  an existing install; the `ci` surface + `did_not_run` rows stay derived by
  readers from the Checks API, never written in CI.
- **Reasons-required allowlist** (`<state_dir>/check-exceptions.yml`):
  entries `{path, kind, reason (REQUIRED), triaged, by, verdict?}` suppress
  exact path+kind finding matches; a reason-less entry is refused and
  reported as its own finding; a suppression records the guard fire with the
  entry's verdict (`accepted_risk` default / `false_positive`) + reason —
  creating the entry IS the verdict event. The session-log gate is never
  allowlistable.
- **The `📊 Model:` run-report line + harvest**: `session-close` parses
  `- **📊 Model:** <model> · <effort> · <task-class>[ · <tokens_out>]` from
  the session card into `telemetry/model-usage.jsonl` (the PL-004 record:
  `{session, date, model, effort, task_class, tokens_out, outcome}` —
  `tokens_out` null-tolerated per KF-9, `outcome` an all-null object until
  the lab sweep backfills it; one row per session slug).
- **Session-marker needle**: `📊 Model:` joins the default
  `session_markers` for new adopts; `upgrade` adds it to an existing
  install's config and reports it — a consumer's gate only tightens when it
  upgrades, never mid-version.
- `telemetry/allocation-ladder.md` + `telemetry/README.md` seeded in the kit
  repo (the program-wide PL-004 ladder with the KF-8 numbers; feed schemas).
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
- **The 9th task class `feature build`** (program-law amendment PL-010 —
  MINOR): `TASK_CLASSES` gains `feature build` for new-capability building,
  ending the nearest-neighbor mislabeling of B2 allocation rows (friction
  issue #15 report 3; KL-2/KL-3/KL-4 all had to shoehorn feature work).
  `docs/program/rulings.md` [PL-010] amends PL-004's taxonomy; the
  allocation ladder gains an **observe-first** row (no seeded tier —
  PL-005: B2 data seeds it); existing dataset rows are never rewritten.
- **The post-adopt ENGAGEMENT gate** (band KL-7, D-0006 — MINOR, new
  checker; the fleet-review §4 fix): `check` now scans an adopted host and
  holds `--strict` **RED** until the last mile is walked — no planted doc
  under the UNRENDERED banner or carrying leftover `${...}` slots, a CI
  workflow running `check --strict`, and an engaged session loop
  (`session_count ≥ 1` or a real session card). Four finding kinds
  (`unrendered-banner` · `unrendered-slot` · `enforcement-unwired` ·
  `session-loop-idle`), planted-docs scope only (template sources are never
  scanned), adoption-evidence-gated so a bare tree lints as before. `adopt`
  now **stages the live `substrate-gate.yml`** under `<state_dir>/ci/` on
  every run (kit stages, host installs) and ends by printing the gate's
  findings as the engagement checklist — a default adopt can no longer LOOK
  onboarded while being neither rendered nor enforcing. The cold-adoption
  smoke + tests pin the full RED→ENGAGED→GREEN arc.

- **B1's first cold-start row recorded** (run `2026-07-09-run01` — the
  KF-5 benchmark-ran condition for the next MINOR): judge claude-opus-4-8
  (independent), **VERDICT: PASS** — ON wins M2 (resumed from a
  genuinely-used handoff) + M3 (durable write-back); M1 unmeasurable this
  run (all 3 pairs scorer-tainted); T5 guard probe n/a (headless arms never
  engaged the hook layer). Row 1 of `bench/results/cold-start/index.json`
  + the committed raw run dir (`bench/results/cold-start/2026-07-09-run01/`);
  the three harness follow-ups filed under `docs/ideas/` for run-2 fixes.

### Fixed

- **auto-merge-enabler label race** (found live on the bench-tree PR #17):
  an MCP-created PR gets its `do-not-automerge` label in a second call
  right after create, so the enabler's payload-snapshot label check could
  arm auto-merge on a PR that must never auto-merge. The enabler now waits
  a grace beat and re-reads the labels FRESH from the API just before
  arming, refusing when the label is present.
- **`upgrade` from-version truth** (superbot-next#46): the vendored dist's
  header now outranks a disagreeing `config.kit_version` pin when naming
  `from_version` — a pin recorded BEFORE the first real upgrade (the D2
  order) misreported the report/`last-upgrade.json` (pin said 1.0.0, the
  archive honestly said `bootstrap-unknown.py`) and a rollback would have
  restored the wrong pin. The hand-copied-new-dist case (header equals the
  running `KIT_VERSION`) still trusts the pin; rollback now restores the
  unrecorded sentinel `""` (never the literal `"unknown"`).
- **`upgrade` input self-cleanup** (superbot-next#46): a completed upgrade
  now removes the consumed `bootstrap.py.new` + the `release.json` next to
  it instead of stranding them at the repo root; `--keep-inputs` opts out;
  cleanup is fail-open and only ever touches the files the flow itself
  consumed.

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

[1.7.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.7.0
[1.6.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.6.0
[1.5.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.5.0
[1.4.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.4.0
[1.3.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.3.0
[1.2.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.2.0
[1.1.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.1.0
[1.0.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.0.0
