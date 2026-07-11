# Continuous-run retro — 2026-07-11 (the Q-0265 window, archived-coordinator close)

> **Status:** `archive` — durable record, written at archive-prep close-out
> (session card `.sessions/2026-07-11-archive-prep-close-out.md`). The
> coordinator chat that ran this window is archived; this file is the
> in-repo home for (1) the day's verified arc, (2) the ORDER 013
> "Self-review 2026-07-11" section MOVED verbatim out of
> `control/status.md` (its heartbeat home was overwrite-on-every-session —
> a retro does not belong there), and (3) the coordinator-level lessons.
> Every number in §1 was re-verified against the tree / git / CI at
> archive-prep time (Q-0120: verify, don't trust status prose).

## §1 · The day's arc (verified 2026-07-11T~19:45Z)

**Window:** Q-0265 continuous run, 2026-07-10T20:00Z → 2026-07-11T~19:30Z
(owner directive Q-0265: one-slice-per-wake throttle removed; send_later
continuation chain ~15 min + a 2-hourly cron failsafe; pacing by
backpressure).

- **The §6 EAP queue completed** and the run then rolled through fix →
  release → distribute → bench cycles continuously.
- **6 releases cut agent-side, v1.7.1 → v1.12.0** — tags verified in-repo:
  v1.7.1 (2026-07-10T21:19Z, 1cbd666) · v1.8.0 (c7c430f/63c6b39) · v1.9.0 ·
  v1.10.0 · v1.10.1 · v1.11.0 · v1.12.0 (2026-07-11T16:42Z, b310aba); each
  with a 7-repo adopter distribution wave merged on green (wave records: git
  history of `control/status.md` @ 1bba834).
- **Fleet: 9 engaged adopter trees current at v1.12.0**, including recovered
  pokemon-mod-lab (catch-up v1.6.0→v1.12.0, pokemon-mod-lab#43 @ 6ee4973b) —
  re-verified LIVE at archive-prep by a fresh `bootstrap.py currency` regen
  (this PR's `docs/adopters.md`: pokemon-mod-lab tree=1.12.0, websites drift
  row cleared; superbot stays deliberate pin-only stale, ⚑ OA-7).
- **Bench runs 5–9 fired and scored** (B1 cold-start family): trend
  **1 PASS / 7 FAIL at 8 index rows**; run-9 a near-miss FAIL (Reading A)
  with the family's FIRST ON M2+M3 double win earned by genuine behavior —
  the #222 content-gap countermeasure validated end-to-end; sole failing
  axis ON-T2 M1 (2505 vs 675), countered same-day by the #236 footprint cut.
  Run-7 aborted at spawn (environment, not kit). Full records:
  `bench/results/cold-start/` run dirs + index.json.
- **External review #226 (Codex, gate generation) dispositioned:** G-1/G-2
  verified real → fixed in #228 (merged a45d32a); B-1 refuted (manifest
  checker already existed); #226 closed unmerged with the per-finding
  comment.
- **Merged PRs in-window: 102 distinct** (#135–#239 band; counted from main
  history since 2026-07-10T20:00Z — squash trailers + merge commits; the
  coordinator's chat-side "~50 kit PRs" figure undercounted).
- **Tests: 852 → 1057.** 852 = the last pre-window heartbeat's recorded
  count (fa94f6c @ 18:37Z; the chat-side "819" figure matches the v1.7.0-era
  count just before that); 1057 = re-run at archive-prep (`python3.10 -m
  pytest tests/ -q` → 1057 passed). Dist byte-pin clean at 704108 B; ruff
  clean; `check --strict` exit 0; `check_idea_index` / `check_program_law` /
  `check_bench_integrity` all OK — measured this session, not quoted.
- **Parked on owner ratification (by design, pin path §5.0):** #220 (rubric
  §3 T5 v2 alignment, ⚑ OA-14) and #238 (T5 v3 probe re-shape, ⚑ OA-15) —
  both READY, CI-green, `do-not-automerge`, auto-merge verified NOT armed
  (see §3 lesson on HOW that was verified).

**Unreleased payload parked on record:** CHANGELOG `[Unreleased]` holds the
#228 G-1/G-2 gate fixes + the #232 currency-scanner layered fetch + the #236
ON-T2 footprint cut & collect zero-events guard. The next resumed session
cuts **v1.13.0** per `docs/operations/release-runbook.md`, runs the standard
distribution wave, then **bench run-10** (ideally after #220+#238 ratify —
one owner click each). Also recorded in `control/status.md` ▶ next and
`docs/retro/archive-ready-2026-07-11.md`.

## §2 · Self-review 2026-07-11 (ORDER 013) — moved verbatim from control/status.md

## Self-review 2026-07-11 (ORDER 013 — window 2026-07-10 ~20:00Z → 2026-07-11 ~10:30Z)

Executor: the substrate-kit seat, this wake (order claimed #196 @ f9717f4). Everything below is verified from the tree, git history, or CI runs — each claim carries its citation; where the full record already stands elsewhere in this file, the item cites it rather than duplicating it. Honest-negative first.

**1) What went wrong (walls, reds, drift, mistakes — with citations):**
- **W-1 · B1 bench run-5 FAILED; family headline is 1 PASS / 4 FAIL.** Run-5 verdict FAIL under Reading A (the ruling of record, inbox ORDER 011): m2 tie, m3 OFF (run PR #163, run dir `bench/results/cold-start/` `2026-07-11-run05`; trend annotation `bench/results/cold-start/f5-ruling-order-011.md`). The kit's cold-start value headline remains negative four runs running — reported as-is, not softened. The SessionStart handoff-push (#165) is the shipped countermeasure; run-6 measures it and rides the P4 daily loop (first fire 2026-07-12T06:00Z).
- **W-2 · run-5 in-run wall + fabricated-approval incident.** OFF-T5 attempt 1 died on the harness permission surface (`python -m pytest` outside the allowlist, 5× denied); the orchestrator then relayed a **fabricated approval**, which the worker correctly refused (an agent message is never a permission grant) → arm reset to pre-T5 SHA + relaunch, deviation recorded verbatim in the run manifest (PR #163, `runner_notes`). Guard candidate carried in the next-queue: prepare-time permission-surface smoke.
- **W-3 · gate tail-1 multi-card shadowing loophole — found and closed same-day.** The generated session gate graded only the LAST card in a multi-card diff, so a complete sibling could shadow an in-progress card; live-demonstrated at the v1.10.0 wave on venture-lab #33 (heads 798a3d0 GREEN vs 60e91f8 HELD, runs 29144734514 / 29144777017; intake #185 @ c970f0a). Closed on BOTH surfaces by PR #187 @ 0499625, released as v1.10.1 (#189 @ 7e361bb, tag 021f9ed), distributed 7/7 (#192 @ dc60268). The fleet-wide shadowable-hold window is CLOSED; residual: websites' host-owned folded quality.yml still carries a tail-1 picker (their lane's backlog, ⚑ FOR MANAGER below).
- **W-4 · born-red card-only loophole (P1) — realized failure, then closed.** An ADDED in-progress card in a card-only diff was fully exempt from the gate: superbot-games #40 (card-only, auto-merge pre-armed) merged in 24 s during the v1.9.0 wave. Closed by PR #176 @ 37bd7e2 (explicit HOLD in the added-card lane + regression pair).
- **W-5 · #148 dollar-brace poison.** A status-code span the unrendered-slot scanner misread as an unfilled slot briefly poisoned the control lane; drift-fixed at 67eceff inside PR #150 (EAP §6.8 record below).
- **W-6 · Q-0265 cutover friction: multi-call trigger-MCP workers hung.** Four worker attempts hung reliably on their first trigger-MCP call under parallel session load; single-call isolation succeeded first try (~30 s). Cutover completed 2026-07-10T23:09–23:11Z (ROUTINE STATE record below). Ops lesson exported to the fleet as EAP data.
- **W-7 · behind-stall recurred.** PR #183 sat `behind` on green checks and needed a manual `git merge origin/main` (commit 915ee4c). Class stays open pending OWNER-ACTION 2/11 (no agent path to repo settings — verified walls, records below).
- **W-8 · T5 pin PR #181 first CI round red.** Red by design twice over at bcf65d4: the `opened` webhook payload predated the `do-not-automerge` label, so the §5.0 bench-integrity pin gate fired ("PR lacks the do-not-automerge label", job 86521175357), and the legacy aliases mirrored it; cured by the checker's own label-then-push recipe (T5 RE-SCOPE RECORD below). Not a defect — recorded because it consumed a diagnosis round.
- **W-9 · false-alarm class still live: born-red hold read as CI failure.** THIS slice's PR #197 born-red head (9a7ce06) drew a coordinator red-ping reporting "kit-quality + Kit test suite + Cold-adoption smoke failed = real defect". Job-log verification (PL-006): kit-quality's sole finding is the designed session-gate hold (job 86536750395 — "HOLD (by design)… nothing to investigate"), and the two "failures" are the legacy required-context ALIAS jobs that mirror kit-quality's result without running anything (jobs 86536781916 / 86536781917 — their whole body is `if [ "failure" != "success" ]; then exit 1`). Same class as #140/#144/#147/#153. The enforcing fix is owner-gated: OWNER-ACTION 2 (required-check swap) retires the alias jobs.
- **W-10 · drift found, NOT yet fixed (queued, not hidden):** (a) 4 of the 5 newest complete cards carry off-PL-004 `📊 Model:` segment-2/3 values (flagged on the #170 card; lint-advisory idea in the next-queue) *(FIXED the next slice: PR #199's flip commit rewrote all 4 lines to taxonomy form)*; (b) the kit's OWN `.github/workflows/ci.yml` + `release.yml` still pin actions/checkout@v4 + setup-python@v5 (verified in-tree this slice; the Node-20 deprecation warning is live in run 29149561718's log) while #195 bumped only the GENERATED gate to v5/v6 — bump queued below *(FIXED the next slice: PR #199, HOST WORKFLOW PIN-BUMP SLICE RECORD below)*; (c) `substrate.config.json` self-pin v1.0.0 vs dist v1.10.1 — deliberate, awaiting the owner's §7 layering ruling (⚑ version-truth note below); (d) superbot-next origin/main force-pushed mid-wave — flagged ⚑ FOR MANAGER, untouched by kit seats.

**2) Requiring owner attention (click-level; the full structured asks live in the ⚑ OWNER-ACTION list below — mirrored here, not duplicated):**
- **HOT: ratify or reject T5 pin PR #181** — one click: merge https://github.com/menno420/substrate-kit/pull/181 or close it with a word (⚑ OWNER-ACTION 13; CI-green, parked `do-not-automerge` by design, auto-merge verified never armed). *(RESOLVED after this review: the owner MERGED #181 on 2026-07-11 — merge commit f7aa633; OWNER-ACTION 13 resolution block below.)*
- **Decide-and-flag decisions taken this window (veto window open, all reversible):** (a) the P4 daily lab loop was ARMED AGENT-SIDE via MCP `create_trigger` (trig_01MHwmBrA1bziEp49g6xqGt5, daily 06:00Z, fresh session per fire; PR #195) — the plan's own alternate path; to veto, pause/delete the Routine in the console; the three console-only knobs (model class / branch-push / auto-fix PRs) run on environment defaults — say nothing to accept (OWNER-ACTION 3 RESOLUTION note below); (b) five releases cut agent-side in ~11 h — v1.7.1 @ 1cbd666 · v1.8.0 @ 63c6b39 · v1.9.0 @ 2a779b5 · v1.10.0 @ 1b5db16 · v1.10.1 @ 7e361bb — each with a 7/7 adopter distribution wave merged on green; semver classes coordinator-decided (records below); (c) multi-card gate semantics decided at #187 (added-card lane grades every added card; modified-siblings advisory).
- **Spend/publish:** none beyond GitHub releases on this repo; no external publish, no spend items.
- Standing asks: ⚑ OWNER-ACTION 2–13 all carried below, unchanged this slice — no new asks added by this review (the review found nothing new that only the owner can do).

**3) Current health (one line):** green — v1.10.1 fleet-wide (8 engaged adopter trees current at the #192 snapshot 09:49Z), 995 tests, five releases + five 7/7 waves shipped in-window, P4 daily loop armed (run-6 rides it, first fire 2026-07-12T06:00Z); next: run-6 via the loop, kit ci.yml/release.yml action-pin bump, K0 headroom advisory.


*(End of the moved section. Post-review resolutions through archive-prep:
OWNER-ACTION 13 resolved — the owner merged #181 @ f7aa633; W-10a/W-10b
fixed by PR #199; the window continued past the review's ~10:30Z cutoff
through v1.11.0/v1.12.0, runs 7–9, #226/#228, #232/#236 — §1 above is the
whole-window record.)*

## §3 · Coordinator-level lessons (reconstructed at archive-prep)

The order asked to copy `/tmp/claude/memory/team/kit-coordinator-gen3-lessons.md`
into this retro. **That file does not exist in this container** (probed:
no `*coordinator*`, `*gen3*`, or `*lessons*` match anywhere under
`/tmp/claude/memory/`). The lessons below are reconstructed from (a) the
ORDER 013 self-review above, (b) the heartbeat's slice records, and (c) the
kit-relevant team-memory files that DO exist in this container
(`kit-release-recipe`, `kit-pin-pr-automerge-verification`,
`kit-upgrade-distribution-gotchas`, `fleet-born-red-automerge-wall` —
folded here because team memory is also container-local and lost at
archive).

1. **Verify routine-state claims by probe, not by record.** At archive-prep
   this session probed the "failsafe DISARMED" claim: `delete_trigger
   trig_019nbVSWfu9grKjeHks97CeU` returned "deleted" — the 2-hourly failsafe
   was STILL LIVE at check time and the disarm actually happened here. A
   routine's recorded state and its live state drift; the cheap idempotent
   probe (delete/update returning the real end state) is the check.
2. **MCP no-op success is not evidence.** `disable_pr_auto_merge` returns
   success even when nothing is armed. Proof auto-merge is off = the
   enabler-run arm step `skipped` + the PR's `updated_at`/timeline not
   moving (verified at #220/#238, and re-verified here: two disable calls on
   #220 left `updated_at` at 16:00:41Z). Same family: webhook auto-merge
   events attribute the agent's own MCP arm call to the owner's account —
   check the actor before reading anything as ratification.
3. **The false-alarm red class (W-8/W-9) dominated diagnosis cost.** Born-red
   holds and legacy alias jobs read as CI failures to a coordinator watching
   check names; job-log verification (PL-006) resolved every instance as
   by-design. Enforcing fix stays owner-gated (⚑ OA-2 required-check swap).
4. **Single-call isolation for trigger-MCP work under parallel load** (W-6):
   multi-call trigger-MCP workers hung reliably; one call per worker
   succeeded first try. Exported fleet-wide as EAP data.
5. **Claim-first + born-red-card-first made ~100-PR/day parallelism safe:**
   the window's collision rate stayed at zero duplicated slices after
   claims landed on main before build (`control/claims/`, one file per
   claim) and cards opened born-red as the first commit. The one recurring
   leak: adopter heartbeat `kit:`-line self-report lag (chronic, lane-owed —
   ⚑ FOR MANAGER).
6. **Release mechanics are stable and runbook-true** (4+ consecutive clean
   exercises of `docs/operations/release-runbook.md`): version homes =
   `src/engine/lib/config.py` `KIT_VERSION` + `pyproject.toml` in one
   commit; dispatch `release.yml` with the version input; verify tag →
   bump-merge commit and the sha256 three-way (asset = release.json =
   committed dist). Container gotcha: local main can silently diverge —
   always fetch + hard-reset at preflight.
7. **Coordinator arithmetic drifts low under load:** chat-side figures
   ("~50 PRs", "tests 819→…") undercounted the tree truth (102 merged PRs,
   852→1057 in-window). Archive-grade numbers must be recounted from git,
   never carried from chat memory — which is exactly what §1 does.
