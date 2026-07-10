# Gen-1 → gen-2 queue state — the whole program on one page (2026-07-09, wind-down)

> **Status:** `owner-guidance` — the roadmap/queue snapshot committed at the
> gen-1 wind-down (kit-lab lane, wind-down phase 2, PR #74). A gen-2 session
> treats this as the handoff truth for WHAT is done / in flight / next; the
> living ledger (`docs/current-state.md`) and live GitHub win over it as time
> passes. Mined from `control/status.md` (the 20:11Z fleet-wrap overwrite,
> PR #75, which carries the wind-down claim untouched),
> `docs/current-state.md`, the ⚑ OWNER-ACTION list, and the docs/retro
> continuation sections.
>
> **RECONCILED 2026-07-10 (gen-2 night-cap, PR #109)** — every ✅/PR number
> below verified against `git log` on main at HEAD 704a537. The overnight
> gen-2 run (2026-07-10, ~00:30–05:00Z) closed most of the agent queue; the
> per-item annotations are the record. Earlier gen-2 sessions deliberately
> left this file untouched (the #95-card convention: closures land on
> status.md/current-state.md); this night-cap pass is the one batched
> reconcile so the next boot reads current queue truth here directly.
>
> **RE-RECONCILED 2026-07-10 (gen-2, follow-on pass)** — main now at HEAD
> `266807e`. **PR #106** (the FULL upgrade-apply-docs post-hoc mechanism)
> landed AFTER the #109 night-cap pass — it sat ~1h green-behind and landed
> via a branch-update at `855a8e4` — so agent-queue item 10's "full
> post-hoc-apply mechanism idea stays `open`" line was stale and is corrected
> below. Also landed after #109 (control-lane housekeeping, no queue impact):
> #107 (claim night-cap groom) · #109 (this file's night-cap reconcile) ·
> #110 (night-summary close, claim cleared, queue dry).

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

## IN FLIGHT (at this commit) — all RESOLVED by 2026-07-10 (night-cap reconcile)

- ✅ **PR #74 — the wind-down deliverables PR** — MERGED 2026-07-09
  (capstone review + this `docs/gen2/` pack).
- ✅ **PR #26 — PL-011 "adoption is not done until ENGAGED"** — **owner
  one-clicked ~2026-07-10T00:08–00:12Z**, merge commit `706190f` on main.
  PL-011 is ratified law.
- ✅ **PR #49 — make_seed yield-keyword fix + prepare seed-suite smoke** —
  **owner one-clicked the same window**, merge commit `6d6046b` on main.
  Its merge unblocked B1 run-3, which fired the same night (PR #85).
  - The do-not-automerge handling rule stands for any FUTURE pin-path /
    law PR: READY, CI green, never rebase/update-branch it, terminal
    state is the owner's click.
- ✅ **Wind-down phase 3** — done 2026-07-09 (PR #77 flipped
  `control/status.md` to gen-1 WIND-DOWN COMPLETE).

## NEXT — the queue, in rough order

**Owner one-clicks** *(wind-down list of 11; items 1–2 RESOLVED by the
owner's 2026-07-10 clicks — `control/status.md` renumbered the remaining
nine to OWNER-ACTION 1–10 in the #88 refresh, each six-field structured
there; that file is the live list, this is the crosswalk):*
1 merge #26 — ✅ DONE (commit `706190f`) · 2 merge #49 — ✅ DONE (commit
`6d6046b`) · 3 rubric F-5 A/B ruling — **OPEN, HOT** (now OWNER-ACTION 1;
gates the recorded run-2/run-3 verdicts + the first KF-8 trend headline;
`docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md`) · 4 P10
required-check swap — OPEN (now OWNER-ACTION 2) · 5 P4 arm the daily lab
loop — OPEN (OWNER-ACTION 3) · 6 P5 Railway `kit-lab` — OPEN
(OWNER-ACTION 4) · 7 P8 MIT confirm — OPEN (OWNER-ACTION 5) · 8 P11
public flip OR P13 read-only PAT — OPEN (OWNER-ACTION 6) · 9 branch
cleanup — OPEN (OWNER-ACTION 7) · 10 superbot upgrade decision — OPEN
(OWNER-ACTION 8) · 11 setup script paste — OPEN (OWNER-ACTION 9).

**Agent queue (no owner needed)** — *night-cap reconcile 2026-07-10: 9 of
12 items DONE, each verified against the merge log; the three that remain
carry their exact gate:*

1. ✅ **Gen-2 boot** — DONE 2026-07-10 (walking skeleton proven, PR #84
   boot-log breadcrumb + the #80/#81 fast-lane markers).
2. ✅ **B1 run-3** — DONE (PR #85, run `2026-07-10-run03`, seed 710301):
   strict-F-5 **FAIL** (advisory per KF-5, DISPUTED pending the F-5
   ruling; Reading B would PASS) — family at 3 rows, first KF-8 trend
   stated. Claim #80.
3. ✅ **Run-2 ordinary-lane follow-ups** — DONE (PR #95; claim #94): all
   three gaps (prepare engagement-arc · `render --live` CLAUDE.md ·
   Model-line byte-forms).
4. **T5 guard-probe redesign** — **REMAINS. Gate: pin path**
   (`bench/tasks/`), so the change MUST ride a `do-not-automerge` PR the
   owner one-clicks — an overnight/autonomous session cannot land it;
   needs a daytime PR left open for the owner
   (`docs/ideas/t5-headless-guard-surface-2026-07-09.md`).
5. ✅ **Engagement-checker comment-leniency fix + inbox append-only
   checker** — DONE (PRs #86 + #87; plus #89's honest-note rider on
   writer identity — issue #36 reports 1–2 all closed).
6. ✅ **Telemetry write-at-card-commit + backfill** — DONE (PR #91).
7. ✅ **Claim-aware checker** — DONE (PR #90, `check_claims` duplicate +
   stale-claim advisory).
8. ✅ **OWNER-ACTION ↔ CAPABILITIES cross-reference advisory** — DONE
   (PR #98, `check_capability_xref`; same PR adopted the stranded #92;
   claim #97).
9. **Post-P10: delete the two `legacy-alias-*` jobs from `ci.yml`** —
   **REMAINS. Gate: owner-gated on the P10 required-check swap**
   (OWNER-ACTION 2 in `control/status.md`); deleting the jobs before the
   ruleset swap would leave the required contexts permanently "expected"
   and block every merge.
10. ✅ **Upgrade-UX fixes from the v1.6.0 rollout** — DONE (PR #92, merged
    via the #98-lane adoption after its authoring session lost the race
    to arm auto-merge): all four ideas. The 4th (`--apply-docs`
    single-shot window) shipped in #92 as the interim-hint slice; its
    **full post-hoc-apply mechanism landed in PR #106** — a same-version
    `--apply-docs` now recovers template improvements from the banked
    pre-upgrade dist (no rollback needed), idea file `outcome: shipped`.
    superbot itself stays owner-gated (OWNER-ACTION 8).
11. ✅ **`adopt --lane`** — DONE (PR #103; claim #102): lane-aware adopt,
    the G1 double-adoption fix; 9 new tests.
12. **Post-P5/P11-or-P13: P6 console move + kit lane real data + the
    loop's B2/B3/B4 sweeps** — **REMAINS. Gate: owner-gated on
    OWNER-ACTION 4 (P5 Railway project) and OWNER-ACTION 6 (P11 public
    flip or P13 read-only PAT)**; nothing an agent can start until a
    token/visibility exists.

*Also landed the same night, outside this queue:* #99 (adopter findings —
owner-action token alignment + fast-CI arm-race doc + parallel-worker
worktree recipe) · the session-close/status ledger PRs #88/#93/#96/#100/
#101/#104 · and post-run, the visiting gba-homebrew Track B lane's
gate-template sentinel fixes (claim #105, build #108 — no-card PRs and
born-red ADDED cards now gate advisory via explicit absent sentinels).
