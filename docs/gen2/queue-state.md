# Gen-1 → gen-2 queue state — the whole program on one page (2026-07-09, wind-down)

> **Status:** `owner-guidance` — the roadmap/queue snapshot committed at the
> gen-1 wind-down (kit-lab lane, wind-down phase 2, PR #74). A gen-2 session
> treats this as the handoff truth for WHAT is done / in flight / next; the
> living ledger (`docs/current-state.md`) and live GitHub win over it as time
> passes. Mined from `control/status.md` (the 20:11Z fleet-wrap overwrite,
> PR #75, which carries the wind-down claim untouched),
> `docs/current-state.md`, the ⚑ OWNER-ACTION list, and the docs/retro
> continuation sections.

## DONE (evidence in parentheses — do not re-audit)

- **Bands KL-0 … KL-8 complete** — engine, release discipline, governance
  home, telemetry, lab loop + friction verb, auto-draft handoff + bench tree,
  ideas/B4 convention, engagement gate, control/ protocol band
  (`docs/current-state.md` § Stability baseline, band-by-band with PRs).
- **Inbox ORDERS 001–009 all acked AND done**
  (`control/status.md` `orders:` line; inbox headers still read `status: new`
  because only the manager flips them — diff the inbox against status, the
  gen-2 rule).
- **7 releases cut in one day**: v1.0.0 (2026-07-09 03:58Z) → v1.1.0 → v1.2.0
  → v1.3.0 → v1.4.0 → v1.5.0 → v1.6.0 (CHANGELOG.md; each published via the
  `release.yml` `workflow_dispatch` path — the only agent-runnable release
  route; v1.6.0 verified live: tag + 3 assets + sha256 match, #69 card).
- **Test suite 722 green** at wind-down (`python3 -m pytest tests/ -q`,
  re-verified by this session).
- **Benchmark family at 2 rows** (`bench/results/cold-start/index.json`):
  run01 **PASS** (M1 unmeasurable, scorer-tainted; judge claude-opus-4-8),
  run02 **FAIL** (strict F-5, advisory per KF-5, disputed wording — owner
  ruling pending; same judge). No trend claim — KF-8 needs ≥3 rows.
- **v1.6.0 fleet rollout COMPLETE** (parallel fleet-wrap session, PR #75,
  merged 20:17Z while this pack was being written): superbot-next v1.6.0
  ENGAGED (superbot-next#96) · websites v1.6.0 ENGAGED (websites#45) ·
  superbot v1.0.0 deliberate pin-only · superbot-games two-lane (version
  not relayed) · kit-lab HEAD consumer #0 (`docs/adopters.md`). Four
  upgrade-UX ideas filed from the rollout's field findings
  (`docs/ideas/upgrade-*-2026-07-09.md`).
- **Both gen-1 incidents guarded**: kit#22 label-race (guards #23 fresh-label
  re-read + #24 disarm workflow + `--label-gate`) and superbot-next#44
  card-gate slip (guard: the consumer's own dist upgrade). Map:
  `docs/operations/auto-merge-guards.md`.
- **Retro bands shipped**: ORDER 005 twin pair (canonical + `-kitlab-coordinator`,
  PRs #50/#51), ORDER 006 CAPABILITIES band (#63), ORDER 007 claim convention
  (#69), ORDER 008 OWNER-ACTION band (#68).
- **Gen-1 wind-down phase 1 (orient + claim)**: wind-down claimed on main via
  fast-lane PR #72 (`control/status.md` phase line, 19:55:47Z).
- **Sibling lane's succession pack**: the SuperBot-rebuild coordinator lane
  shipped its wind-down pack under `docs/succession/*-superbot-coordinator.md`
  + `docs/retro/wind-down-review-2026-07-09-superbot-coordinator.md` (PR #73).

## IN FLIGHT (at this commit)

- **PR #74 — this wind-down deliverables PR** (kit-lab lane, phase 2):
  capstone review + the gen-2 pack in `docs/gen2/`.
- **PR #26 — PL-011 "adoption is not done until ENGAGED"** (program law):
  open, READY, `do-not-automerge` BY DESIGN (§8.3: law rides its own
  owner-review PR; merge = ratification). All 3 checks SUCCESS on head
  `f65816b` (re-verified 2026-07-09 ~20:05Z). Terminal state = **owner
  one-click** (⚑ OWNER-ACTION 1 in `control/status.md`).
- **PR #49 — make_seed yield-keyword fix + prepare seed-suite smoke**
  (pin path `bench/seeds/`): open, READY, `do-not-automerge` BY LAW
  (`check_bench_integrity.py` rule 1 — the lab never merges its own change to
  the oracle). All 3 checks SUCCESS on head `65ba406` (re-verified same
  read). Terminal state = **owner one-click**; merging it **unblocks B1
  run-3** (⚑ OWNER-ACTION 2).
  - Both PRs are `behind` main (bases `eb540d9` / `de77b6c`). Do NOT
    update-branch/rebase them — a push could invalidate the green CI, and
    API pushes may not re-trigger workflows. "Require branches to be up to
    date" should be OFF (P10 review), so they remain one-click merges as-is.
- **Wind-down phase 3** — the `control/status.md` overwrite to
  "wind-down complete" (a separate session owns that file's next write).

## NEXT — the queue, in rough order

**Owner one-clicks (the 11 ⚑ OWNER-ACTION items, all six-field structured in
`control/status.md`):** 1 merge #26 · 2 merge #49 · 3 rubric F-5 A/B ruling
(`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md` — should land
before run-3 is judged) · 4 P10 required-check swap (legacy "Kit test suite"
+ "Cold-adoption smoke (adopt + check --strict)" → `kit-quality`) · 5 P4 arm
the daily lab loop (`docs/operations/lab-loop.md` § Arming; the loop is built
and unarmed — D3 waits on this) · 6 P5 Railway project `kit-lab` · 7 P8 MIT
confirm · 8 P11 public flip OR P13 read-only PAT · 9 branch cleanup (~25
stale) · 10 superbot upgrade decision (pin now 6 releases behind) · 11
web-environment setup script paste (`docs/environment-setup-script.md`;
gen-2 variant: `docs/gen2/setup.sh`).

**Agent queue (no owner needed):**

1. **Gen-2 boot** — a fresh gen-2 session starts from
   [`docs/gen2/next-boot.md`](next-boot.md) (walking skeleton first).
2. **B1 run-3** the moment #49 merges (fires under the ruled F-5 reading if
   item 3 lands first; otherwise strict-with-caveat like run-2). Family
   reaches the KF-8 ≥3-row threshold.
3. **Run-2 ordinary-lane follow-ups** (idea files carry guard recipes):
   `run_ab.py prepare` engagement-arc scripting · `render --live` CLAUDE.md
   gap · `_adopt_sessions_readme` Model-line checker false-red.
4. **T5 guard-probe redesign**
   (`docs/ideas/t5-headless-guard-surface-2026-07-09.md` — two runs of
   "guard probe n/a headless" evidence; pin path, so the change rides a
   `do-not-automerge` PR).
5. **Engagement-checker comment-leniency fix + inbox append-only checker**
   (friction issue #36 reports 1–2).
6. **Telemetry write-at-card-commit + backfill** (the undercount: 10
   harvested rows vs 21+ eligible cards; #50-lane idea).
7. **Claim-aware checker** (duplicate-claim + stale-claim advisory — the #69
   card's session idea; the convention is doc-contract-only today).
8. **OWNER-ACTION ↔ CAPABILITIES cross-reference advisory** (#68 card idea).
9. **Post-P10: delete the two `legacy-alias-*` jobs from `ci.yml`.**
10. **Upgrade-UX fixes from the v1.6.0 rollout** *(the consumer-upgrades
    item completed mid-wind-down — PR #75)*: the four filed ideas
    (`--apply-docs` single-shot window · rollback-loses-hash-records ·
    idempotent-archive report line, third field report · release.json
    placement checklist line), all ordinary-lane with guard recipes.
    superbot stays owner-gated (item 10); superbot-games sets
    `heartbeat_files` two-lane at its adopt. Manager relay item: websites'
    inbox ORDER 005 is genuinely unexecuted (needs a scoped websites
    session — #75 status notes).
11. **`adopt --lane`** (lane-aware adopt — self-review G1's fix for
    double-adoption; idea filed).
12. **Post-P5/P11-or-P13**: P6 console move + kit lane real data + the loop's
    B2/B3/B4 sweeps.
