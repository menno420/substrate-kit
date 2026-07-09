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

[1.1.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.1.0
[1.0.0]: https://github.com/menno420/substrate-kit/releases/tag/v1.0.0
