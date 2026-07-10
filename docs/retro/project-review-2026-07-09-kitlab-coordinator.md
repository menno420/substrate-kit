# Project review — substrate-kit gen-1 (2026-07-09) · kit-lab coordinator-lane companion

> **Status:** `audit`
>
> **Twin-execution note:** the parallel ORDER 005 lane's review merged
> first (PR #51) and holds the canonical path
> [project-review-2026-07-09.md](project-review-2026-07-09.md) — a strong
> repo-evidence-only pass whose model attribution is honestly "cannot be
> determined" wherever the repo lacks a Model line. THIS companion exists
> because it carries what only the coordinator's side had: the
> authoritative session-side fact ledger (35 sessions with per-session
> friction, the deliberate model split — fable-5 build lane · sonnet-5
> benchmark arms · opus-4-8 judges — and the human-input points), plus the
> cross-check of those facts against the repo. Read the canonical file for
> the repo-verified state; read section (b) here for the session-side
> audit and the named discrepancies.
>
>
> The owner-directed companion to the ORDER 005 self-review
> ([self-review-2026-07-09.md](self-review-2026-07-09.md)): what this
> Project is, its TRUE repo-verified state, the full agent audit
> (coordinator-session facts cross-checked against the repo, discrepancies
> named), the honest efficiency verdict, the ⚑ owner-actions list, and the
> continuation plan. Repo facts verified live on 2026-07-09 (main at
> `de77b6c`); session-side facts that the repo cannot confirm are marked
> **"per coordinator"**.

## (a) What this Project is + true current state

**What it is.** substrate-kit is the fleet's **portable agent-memory
substrate and the lab that improves it**: a stdlib-only engine
(`src/engine/`, shipped as the single-file `dist/bootstrap.py`) that any
repo adopts to get the working-agreement docs, the session loop (born-red
cards, auto-drafted handoff), the checker gate (`check --strict`), the
control/ coordination bus, telemetry, and the upgrade path — plus, in this
repo only, the **benchmark harness** (`bench/`) that measures whether the
kit actually helps, and the program-law register (`docs/program/`). The
repo is its own consumer #0 and the substrate coordinator for the fleet
(`docs/adopters.md`).

**True current state — verified against the repo, not memory:**

- **main = `de77b6c`** (#47); the full suite is **705 tests, green**
  (verified locally this session: `python3 -m pytest tests/ -q`).
- **5 releases exist, all published 2026-07-09** by github-actions via the
  `release.yml` dispatch path: v1.0.0 (03:58Z) → v1.1.0 (13:26Z) →
  v1.2.0 (14:05Z) → v1.3.0 (15:24Z) → v1.4.0 (16:57Z). Tags v1.0.0–v1.4.0
  confirmed in-repo.
- **41 merged PRs** (this file's draft said 44; reconciled against the live PR list and the #51 pass) in the #1–#48 range (#15, #36–#39 are issues; #26 open
  by design; #30 closed unmerged, superseded). Since then: **#49** (this
  session's pin-path seed fix, open + `do-not-automerge` by law), **#50**
  (this retro, in flight), **#51** (a duplicate ORDER 005 PR from a
  parallel session — see §(b) discrepancy 2).
- **Benchmark: `bench/results/cold-start/index.json` has exactly 2 rows** —
  run01 **PASS** (M1 unmeasurable, scorer-tainted) and run02 **FAIL**
  (strict F-5; first clean M1 measurement regressed while M2/M3 favor ON
  inside the 7k budget). Judge both times: `claude-opus-4-8`. Family below
  the KF-8 trend threshold (needs ≥3).
- **Control ritual:** `control/status.md` reports
  `orders: acked=001,002,003,004,005 done=001,002,003,004` — ORDER 005 is
  what this session executes. Inbox carries ORDERS 001–005 verbatim.
- **Adopters** (`docs/adopters.md`): kit-lab (consumer #0, HEAD) ·
  superbot-next v1.2.0 ENGAGED · websites v1.2.0 ENGAGED · superbot v1.0.0
  deliberate pin-only · superbot-games two-lane (version not yet relayed) ·
  trading-strategy + game repos planned.
- **Open friction issues:** #36–#39 (fleet-review filings); #15 filed and
  triaged (closed).
- **Standing incidents ledger: two** (`docs/current-state.md` §Field
  notes): the #22 label-race merge (guards since: #23 fresh-label re-read,
  #24 disarm workflow + law label gate) and superbot-next#44's card-gate
  slip (guard: the consumer's own dist upgrade).
- **Owner-gated, still pending:** P4 (lab-loop cron), P5 (Railway), P8
  (MIT confirm), P10 (required-context swap), P11-or-P13 (public flip or
  read-only PAT), PL-011 ratification (#26), the rubric F-5 wording ruling,
  and — new via #47 — the corrected web-environment setup script paste.

## (b) Agent audit — every session, cross-checked

**Model provenance (authoritative session-side, per coordinator; repo
corroboration noted):** the kit-lab coordinator session runs on
**claude-fable-5**; every spawned build/collect/record worker inherited
**claude-fable-5** unless deliberately overridden; the **12 benchmark ARM
sessions ran claude-sonnet-5** (deliberate: same model both arms per the
rubric); the **2 benchmark judges ran claude-opus-4-8** (deliberate:
stronger than the arms, independent). Repo corroboration: all 10
`telemetry/model-usage.jsonl` rows say `fable-5 · high`; every completed
session card's `📊 Model:` line says fable-5; both bench index rows record
`judge_model: claude-opus-4-8`. **The arm models are NOT independently
verifiable from the repo** (run manifests carry no model field) — sonnet-5
for arms stands as "per coordinator". ~40 workers total per coordinator;
the repo cannot count sessions that produced no artifact.

**Session-by-session** (coordinator facts 1–35, verified where the repo
can; classification (a) = our setup/pattern, (b) = platform):

| # | Session (evidence) | Verdict + friction |
|---|---|---|
| 1 | Orientation scout (no repo artifact) | clean — per coordinator |
| 2 | KL-0 (#4/#5, cards `kl0-dogfood-seed`) | clean; **incident: #4 instant-merged** — no required checks existed yet (a) |
| 3 | KL-1 CI delta (#6) | clean; discovered the owner-landed legacy-name ruleset mid-session (a) |
| 4 | KL-1 release train (#7–#11, v1.0.0) | one mid-work stop on **tag-push HTTP 403**; resumed; released via `release.yml` dispatch (b). Repo confirms: #7 card-only instant-merge, #11 carries the dispatch path, issue #15 report 2 |
| 5 | PR #17 label check (read-only) | clean |
| 6 | Consumer pins (superbot#1879, superbot-next#42) | clean — cross-repo, cited in `current-state.md` D2 |
| 7 | KL-2 governance home (#12) | clean; **shared `/home/user` checkout collision** with a parallel worker → all later workers moved to scratchpad worktrees (a, fixed same day) |
| 8 | superbot-next v1.0.0 upgrade (their #44/#46) | clean; **incident: their #44 premature merge** — old dist couldn't hold a card red (a); ledgered in `current-state.md` §Field notes |
| 9 | KL-2 riders (superbot#1881) | clean; **~30 min lost to ~25-min-stale MCP PR reads** (b) |
| 10 | superbot in-tree removal (superbot#1882) | **stalled twice** on background watchers that cannot wake a stopped agent; coordinator resumed both (a pattern + b semantics) |
| 11 | KL-3 telemetry (#13) | clean |
| 12 | KL-4 lab loop + friction (#14, issue #15) | clean |
| 13 | KL-5 (#16 + #17) | clean; **caught the enabler label race live on #17** after a coordinator webhook nudge; disarmed by hand; guard shipped inside #17 |
| 14 | KL-6 unblocked (#18 + superbot#1883) | one timer-stall (class as row 10); resumed; clean |
| 15 | Groomed ideas (#19) | clean |
| 16 | Console contract (superbot#1884 + websites#11 + kit#20) | clean; **found + fixed a live websites dict-vs-list dashboard bug** |
| 17 | Run close-out (#21) | clean |
| 18 | PL-004 discuss PR (#22) | **GOVERNANCE INCIDENT**: `do-not-automerge` PR merged mechanically — enabler armed from a stale pre-label event payload after a ~12-min runner-queue lag; the worker's disarm calls had landed pre-arm as no-ops. (a) our guard rode unmerged #17 + (b) stale-payload semantics. Contained same-hour by #23. Repo confirms: incident comment on #22, guards on main |
| 19 | Enabler hotfix (#23) | one background-poll stall; resumed; clean; repo confirms #23 merged via auto-merge as designed |
| 20 | Audit follow-ups + day report (#24) | one monitor stall; resumed; clean; **disproved the auditor's #23 API-merge suspicion** (verify-then-fix) |
| 21 | Branch-deletion attempt (#24 card ⚑) | **fully blocked**: git push --delete 403, REST 403, GraphQL deleteRef disabled, no MCP tool. Zero deletions, honest report (b) |
| 22 | P0 engagement gate (#25 + PL-011 #26) | clean; **bitten twice by our own guards** (born-red hold through a surprise #17 merge; stamp-discipline check) — guards working as designed |
| 23 | #17 merge attempt | **DENIED by the auto-mode permission classifier** (relayed owner consent insufficient); resolved when the owner typed "merge 17" in-session; branch-prep worker merged (b — arguably correct trust boundary). Same classifier class later denied a worker-spawn including merging #26 → **#26 is now an owner one-click item** |
| 24 | B1 run-1 (prep + 6 sonnet-5 cold arms + 3 collect workers + opus-4-8 judge + record #28) | clean pipeline; found 3 M1 scorer artifacts + the T5-headless limitation; **verdict PASS** (repo: index row 1, run dir) |
| 25 | Control adopt worker → follow-up (#27 + #30) | first worker **stopped correctly at contract-missing** (#27 unmerged, 0 CI runs — manager's API-authored PR triggered no CI, (b)); follow-up landed #27 + heartbeat #30 (superseded, closed); one **~35-min runner-queue stall** on the legacy alias contexts (b) |
| 26 | v1.1.0 release (#29) | one poller stall; resumed; **one flagged force-with-lease on its OWN branch** (rebase after #27); legacy-alias jobs cancelled by a queue stall needed `rerun_failed_jobs` (b) |
| 27 | ORDER 002 control band (#31/#32/#33, v1.2.0) | clean; **live-proved the control fast lane (7-second CI)** on #33 |
| 28 | Close-#30 worker | clean |
| 29 | superbot-next v1.2.0 upgrade (their #69) | clean; ENGAGED end state; no kit bugs |
| 30 | websites upgrade + de-strand (their #31) | clean; corrected the stale fleet-review premise (websites already had required CI); **found the `parse_model_line` shadowing bug** (fixed kit-side in #40) |
| 31 | Harness/telemetry fixes (#40) | clean |
| 32 | ORDER 003 (#41/#42, v1.3.0) | clean |
| 33 | B1 run-2 (prep — **found the make_seed yield-keyword bug**, seed 424242→424243 deviation in the manifest `runner_notes`; ON-arm engagement forced by our own P0 gate; 6 sonnet arms; 3 collects; opus judge; record #44) | clean pipeline; **verdict strict-F-5 FAIL** (M1 regressed on the first clean measurement; M2/M3 ON in-budget) |
| 34 | ORDER 004 (#46/#48, v1.4.0) | clean; `enable_pr_auto_merge` **rate-limited once**, retried OK (b) |
| 35 | This worker — ORDER 005 + review + seed-fix #49 | in flight; frictions logged below |

**Coordinator annex (verified where possible):** coordinator session model
claude-fable-5 (per coordinator — no repo artifact). Sibling sessions
today: "Verify kit-lab run output" (independent audit — its verdict is
cited in the day report), "Fleet kit-adoption review" (**repo-confirmed**:
kit#35 + issues #36–#39; superbot#1894 per coordinator), "Mirror fleet
spec heartbeat format" (superbot#1898 — per coordinator, other repo), one
inline read-only branch-list subagent (fable-5, ~104s, clean — per
coordinator). The coordinator cannot determine child-session models from
its side (the spawn API exposes none) — repo telemetry is the only
cross-check, and it only covers sessions that ran `session-close` here.

**Discrepancies + repo-side additions vs the coordinator facts:**

1. **PR #47 is missing from the coordinator's list** *(reconciled: the #51 review claims session `01Y5uPEhxhYUvC8qMpoDDvJ7` as one of ITS workers — #47 belongs to the twin wake-up lane, which is why the kit-lab coordinator's ledger never saw it; two coordinators, two ledgers, no shared registry)* — "Document the
   corrected Claude Code on the web environment setup script" (merged
   17:02Z, session `01Y5uPEhxhYUvC8qMpoDDvJ7`): a web session was killed
   at provisioning by the environment's setup script (wrong cwd +
   hard-fail on a missing `requirements.txt`) and a session documented the
   corrected script in `docs/environment-setup-script.md` + a pending
   owner action in `current-state.md`. The repo knows a casualty + a fix
   the session-side ledger doesn't.
2. **PR #51 — live duplicate of ORDER 005** (branch
   `claude/laughing-franklin-ey1v37`, session `01S7eRG1Zz5irp4iuaAFWNA1`,
   opened 17:11:50Z, ~90s after this session's #50): a parallel session
   started the same retro lane. Flagged on #51 in-flight; **#51 merged first (17:23Z)** and holds the canonical paths, so this lane's documents were repositioned as `-kitlab-coordinator` companions (suffixed per the owner's multi-lane rule, the #52 precedent) instead of racing the same paths;
   gen-1 friction evidence for the claim-before-commit rule (self-review
   F1.3).
3. **Telemetry undercounts the run**: `telemetry/model-usage.jsonl` has
   **10 rows** while 21+ completed session cards carry valid `📊 Model:`
   lines — every card from the enabler hotfix (#23) onward went
   unharvested (the harvest runs only inside `session-close`, which later
   sessions didn't run here). Where rows exist they corroborate the
   coordinator (all fable-5 · high); where they don't, the coordinator's
   facts are the only record — exactly the fragility this retro exists to
   surface.
4. **"8 listed merged branches" is stale**: that was the #24-era count.
   Today **25 stale head branches of closed PRs** exist (every `claude/*`,
   `manager/*`, `docs/*` branch except open #26/#49/#50/#51's) — the
   deletion blockade (row 21) plus five more sessions of merges. Exact
   list in §(e).
5. Minor: coordinator fact 24 says "record #28" under B1 run-1 — repo
   confirms, and adds that #28 also filed the three harness follow-up
   ideas the run-2 session then consumed. No contradiction, just the repo
   being more complete.
6. Everything else checked — PR numbers, verdicts, incident timelines,
   release paths, and the #30 supersede all match the repo record.

## (c) The ORDER 005 answers

Every `docs/retro/QUESTIONS.md` question answered by ID, twice and
independently: the canonical
**[self-review-2026-07-09.md](self-review-2026-07-09.md)** (#51 lane) and
this lane's
**[self-review-2026-07-09-kitlab-coordinator.md](self-review-2026-07-09-kitlab-coordinator.md)** (A1–A4 work &
correctness · B1–B4 errors & friction, including the full error table ·
C1–C4 efficiency · D1–D5 autonomy · E1–E4 protocol & environment · F1–F4
redesign payload · G1–G3 kit addendum).

## (d) Honest efficiency verdict

**Where the time actually went.** Build time was the majority and was
productive (8 bands, 5 releases, a benchmark run twice, 3 consumer
rollouts). The recoverable losses were almost entirely *waiting*:

- **2 × ~35-min runner-queue stalls** on the legacy alias required
  contexts (sessions 25/26) — root cause P10, cleared by
  `rerun_failed_jobs`;
- **~30-min MCP-staleness poll** (session 9) — the PR had merged 25
  minutes before the API said so;
- **6 stall-resume roundtrips** (sessions 10×2, 14, 19, 20, 26) — each one
  a stopped worker waiting on a watcher that cannot wake it, plus
  coordinator time to notice and resume;
- **1 rate-limit retry** (session 34) — trivial;
- incident containment (#22 → #23/#24) — real time, but it bought the
  guard stack and the honest incident ledger, so only partly "lost".

**What I'd redo, in order** (mirrors self-review C4): (1) **P10 swap on
day one** — deletes the alias jobs and both 35-min stalls before they
exist; (2) **scratchpad worktrees from the first worker** — deletes the
/home/user collision; (3) **in-turn-polling doctrine in every worker
prompt from the start** — deletes the 6 stall-resumes; (4) **control fast
lane earlier** (with ORDER 001, not 002) — heartbeats were paying
full-suite CI for half a day; (5) **needle byte-forms in the planted
README from the start** — marker retrofits at `upgrade` cost every
existing install a version lag.

## (e) ⚑ OWNER ACTIONS — exact clicks + what each unblocks

1. **Merge PR #26** (PL-011 ratification) — open
   <https://github.com/menno420/substrate-kit/pull/26>, one click on
   "Merge pull request". Merge = ratify; to veto, comment instead and a
   session reverts the register note. **Unblocks:** the adoption-is-ENGAGED
   law becoming citable program law.
2. **Merge PR #49** (make_seed yield-keyword fix + prepare seed-suite
   smoke; pin-path, CI-green, card complete) — open
   <https://github.com/menno420/substrate-kit/pull/49>, one click.
   **Unblocks: B1 run-3** (the seed generator can currently not serve seed
   424242-class draws).
3. **Rubric F-5 wording decision** — read
   `docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md` (two
   readings, A strict / B budget-purposive, one paragraph each) and answer
   "A" or "B" in any channel. **Unblocks:** run-3's verdict landing under a
   ruled reading instead of a disputed one.
4. **P10 — required-context swap**: Settings → Rules → the `main` ruleset →
   edit required status checks → **remove** "Kit test suite" and
   "Cold-adoption smoke (adopt + check --strict)", **add** `kit-quality`
   (source: GitHub Actions). Leave "Require branches to be up to date"
   OFF. **Unblocks:** deleting the two `legacy-alias-*` jobs (agent does
   it next session) and ends the alias-queue-stall class (~70 min lost
   this run).
5. **P4 — arm the lab loop**: Console → kit-repo environment → Schedules →
   New schedule → paste the fenced prompt from
   `docs/operations/lab-loop.md` § Arming verbatim → cron `0 6 * * *`
   (UTC) → fresh session per fire ON → Sonnet-class model →
   unrestricted-branch-push OFF, auto-fix PRs ON. **Unblocks:** D3 (the
   self-running daily loop; ≥3 scheduled fires).
6. **P5 — create Railway project `kit-lab`**: region `europe-west4`, no
   spend caps (PL-005), notification rule → HQ `#railway-alerts`; then put
   a project-scoped `RAILWAY_TOKEN` in the kit repo's environment.
   **Unblocks:** the P6 console move (agent-built).
7. **P8 — confirm MIT**: one word ("MIT ok") or name a replacement.
   **Unblocks:** closing the license ⚑ carried since KL-1.
8. **P11 or P13** — either flip the repo public (Settings → General →
   Danger Zone → Change visibility) **or** veto and create a read-only
   consumer-scope PAT for cross-repo reads. **Unblocks:** kit data in the
   merged console + the loop's B2/B3/B4 sweeps.
9. **Branch cleanup**: Settings → General → Pull Requests → check
   **"Automatically delete head branches"** (prevents recurrence); then
   delete the 25 stale branches of closed PRs — fastest via each closed
   PR's "Delete branch" button, or Code → Branches: `populate-kit`,
   `kit-ci`, `setup/codeowners`, `claude/kl0-dogfood-seed`,
   `claude/kl0-dogfood-seed-2`, `claude/kl1-ci-delta`,
   `claude/kl1-release-train`, `claude/kl1-upgrade-verb`,
   `claude/kl1-close-guards`, `claude/kl1-release-dispatch`,
   `claude/kl2-governance-home`, `claude/kl3-telemetry`,
   `claude/kl4-lab-loop`, `claude/kl5-auto-draft`, `claude/kl5-bench-tree`,
   `claude/kl6-unblocked`, `claude/groomed-ideas-1`,
   `claude/pinned-feed-contract-idea`, `claude/run-closeout`,
   `claude/pl004-feature-build`, `claude/enabler-race-hotfix`,
   `claude/audit-followups-2026-07-09`, `claude/p0-adopt-engage-gate`,
   `manager/control-plant`, `claude/b1-record-run01`,
   `claude/v1.1.0-release`, `claude/control-protocol-adopt`,
   `claude/kl8-control-protocol`, `claude/order002-status`,
   `manager/inbox-2026-07-09-3`, `claude/fleet-adoption-review-2026-07-09`,
   `claude/run2-harness-prep`,
   `claude/order003-adopter-visibility-2026-07-09`,
   `claude/order003-status-overwrite-2026-07-09`,
   `manager/order-004-heartbeat-paths`, `claude/b1-run2-record-2026-07-09`,
   `claude/fleet-retro-2026-07-09`,
   `claude/order004-heartbeat-paths-2026-07-09`,
   `claude/order004-status-overwrite-2026-07-09`,
   `docs/web-env-setup-script` — **keep** the branches of open PRs
   (#26 `claude/pl011-adoption-engaged`, #49
   `claude/seed-fix-yield-keyword-2026-07-09`, #51
   `claude/laughing-franklin-ey1v37`) until they resolve. (Agents cannot
   do any of this: deletion is 403-blocked in-session — audit row 21.)
   **Unblocks:** nothing functional; ends the clutter class permanently.
10. **superbot upgrade decision**: superbot's deliberate pin-only stance
    is now **4 releases behind** (v1.0.0 vs v1.4.0). Recommendation
    (decide-and-flag): stay pin-only until the F-5 ruling + run-3, then
    upgrade in one hop; say "upgrade now" to override. **Unblocks:** the
    fleet's last non-ENGAGED adopter, whenever taken.
11. **Web-environment setup script** (new, via PR #47): paste the guarded
    script from `docs/environment-setup-script.md` into the environment's
    "Setup script" field (owner-only settings dialog). **Unblocks:** no
    more sessions killed at provisioning (one confirmed casualty).

## (f) Continuation — what proceeds without the owner

The coordinator keeps executing; nothing below waits on a human:

- **B1 run-3** fires as soon as #49 merges (and lands under the ruled
  F-5 reading if the ruling arrives first — otherwise recorded under
  strict-with-caveat exactly like run-2). Family reaches the KF-8
  threshold (≥3 rows) at run-3.
- **T5 probe redesign** — `docs/ideas/t5-headless-guard-surface-2026-07-09.md`
  (two runs of "guard probe n/a headless" evidence) graduates from idea to
  a planned harness change for run-3 or run-4.
- **The daily lab loop's prompt is ready** (`docs/operations/lab-loop.md`)
  — the moment P4 is armed it runs without further setup; until then,
  manually-fired sessions cover the same duties.
- **Inbox orders** continue to be acked and executed as they arrive
  (the control ritual is proven through ORDER 005).
- Groomed follow-ups queue behind those: the engagement checker's
  comment-leniency fix (issue #36 report 1), the inbox append-only checker
  (report 2), `adopt --lane` (the #46 idea, G1's fix), and the telemetry
  write-at-card-commit convention (discrepancy 3).
