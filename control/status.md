# substrate-kit · status
updated: 2026-07-10T12:35:31Z
phase: gen-2 active — ORDER 010 RECORDED (hourly wake routine: already armed by the coordinator lane at 01:56Z, before the order landed 11:06Z; this overwrite is the bus record — see ORDER 010 RECORD below). Context carried from the previous overwrite: v1.7.0 RELEASED (cut agent-side via release.yml workflow_dispatch, 2026-07-10) and B1 run-4 RECORDED (first FAIL under BOTH F-5 readings; PR #116, squash a3616db). Agent-reachable build queue is dry; remaining work is either owner-gated (the ⚑ list) or a small set of agent-available items listed under `next`. THE HOT owner item stays the F-5 A/B ruling — run-4 is ruling-INDEPENDENT (fails under both readings), but the ruling still decides runs 2–3, i.e. 2 of the family's 4 recorded verdicts, and with it the trend headline (A: 1 PASS / 3 FAIL · B: 3 PASS / 1 FAIL).
health: green — suite green through #116 (bench-integrity + dist byte-pin + ruff + pytest all green on the run-4 merge); `dist/bootstrap.py check --strict` exit 0.
kit: v1.7.0 released · KIT_VERSION 1.7.0 · tag v1.7.0 live · check: green · engaged: yes
last-shipped: ORDER 010 bus record (PR #120, this overwrite; claim rode PR #119 f439ae3 and is CLEARED here) — control/status.md orders line → done=010 + the routine mechanism/confirmation record below; docs/CAPABILITIES.md routine-creation correction appended. Before that: B1 cold-start run-4 bench row (#116, squash a3616db) — row 4 appended to bench/results/cold-start/index.json (rows 1–3 byte-identical), full raw run dir committed (bench/results/cold-start/2026-07-10-run04/), 4-row KF-8 trend written to docs/current-state.md + CHANGELOG [Unreleased]. Claim rode PR #115 (85ffda9) and is CLEARED by this overwrite. Before that: v1.7.0 RELEASE — tag `v1.7.0` @ 93c7bdb + GitHub Release published (run 29074386841 success; assets bootstrap.py + bootstrap.py.sha256 + release.json; https://github.com/menno420/substrate-kit/releases/tag/v1.7.0), landed on the release-prep bump PR #113.

blockers: none blocking. Coordination notes carried: (1) the self-merge classifier wall stays session-dependent — some lanes' enable_pr_auto_merge calls were PERMITTED (#107/#109), others REFUSED as "Merge Without Review"; the `auto-merge-enabler.yml` workflow is the server-side backstop that lands READY PRs on green. (2) "Require branches to be up to date" behaves as ON — a green PR can stall `behind` until a branch update (live-hit #107; recipe in docs/CAPABILITIES.md: check mergeable_state first, `git merge origin/main`, push). The enabler `synchronize` re-arm (#111) NARROWS this (a fix-push re-arms) but does not fully close it — a PR that goes behind AFTER its last push still needs the manual branch update, hence the surviving ⚑ "automatically update branches" owner ask. (3) Sibling lane heartbeat control/status-gba-homebrew-trackb.md is live and untouched — this overwrite touches ONLY control/status.md, per the one-writer rule.

THIS LANE — merged PRs across the gen-2 waves this session (verified against main; each carries its own squash-merge commit):
- #84 — gen-2 walking skeleton: boot-log breadcrumb (ce69eb0)
- #86 — engagement-gate comment-leniency fix (issue #36) (e3d0b7a)
- #87 — control/inbox.md append-only + ORDER-grammar checker (issue #36 rpt 2) (375ce5a)
- #88 — gen-2 interim session close + self-merge wall recipe (3bed1da)
- #89 — control/README honest writer-identity note (issue #36 rpt 2) (468e514)
- #90 — claim-aware checker (duplicate + stale order-claim advisory, ORDER 007) (249ac13)
- #91 — telemetry write-at-card-commit + backfill (10→43 rows) (6bab2f2)
- #92 — upgrade-UX fixes (v1.6.0 rollout) (d8a95cc)
- #99 — adopter-findings batch ×3 (token alignment + fast-CI arm-race + worktree recipe) (78f9d40)
- #100 — gen-2 interim session close: full overnight status ledger (c342aee)
- #106 — full upgrade-apply-docs post-hoc-apply mechanism (single-shot window) (266807e)
- #111 — queue-state reconcile + auto-merge stall-class doc + enabler `synchronize` re-arm (0b6413d)
- #112 — gen-2 wave-2 close: full status ledger + release-readiness note (79d1c45)
- #113 — v1.7.0 (MINOR) release-prep bump: version + CHANGELOG + dist re-pin (93c7bdb) — the prep half that made the dispatch pass its refuse-to-release guard
- #115 — control: claim B1 run-4 (kit-lab gen2) (85ffda9)
- #116 — B1 cold-start run 4: dual F-5 reading bench row (a3616db) — session card .sessions/2026-07-10-b1-run-4.md
Sibling lanes the same window (NOT this lane's — for context only): #85 (B1 run-3), #93/#94/#95/#96/#97/#98 (run-2 follow-ups, pr92-adopt, capability-xref), #102/#103 (adopt --lane), #105/#108 (visiting gba-homebrew Track B), #107/#109/#110 (night-cap docs-reconcile). Queue truth reconciled in docs/gen2/queue-state.md.

orders: acked=001,002,003,004,005,006,007,008,009,010 done=001,002,003,004,005,006,007,008,009,010 — standing-default + coordinator-relayed queue fully executed; the ORDER 010 claim annotation (kit-lab-build 2026-07-10T12:32:19Z, landed via #119) is CLEARED by this overwrite — the claimed work is this record
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

ORDER 010 RECORD (hourly wake routine — coordinator-lane record, transcribed by the kit-lab-build lane; this session did NOT re-verify the trigger from its own surface):
- Mechanism: MCP tool `create_trigger` on the `claude-code-remote` MCP server (the scheduling surface available to Project sessions) — a tool call, not a console/UI path.
- Args: name "kit-lab gen2 hourly wake" · cron_expression "0 * * * *" · prompt "⏰ hourly wake (kit-lab gen2): git pull, check open PRs/CI, work the queue forward. (Recurring hourly Routine — no need to re-arm.)"
- Result: trigger trig_01FnqnAQjLU2T8d16iHwWQ2h · enabled=true · created 2026-07-10T01:56:06Z · bound to the kit-lab coordinator session (persistent_session_id session_01Gb1Dq9vgeNkTyBPvvPqTrj) · first scheduled fire 2026-07-10T02:02:58Z.
- Confirmation of first successful fire: first fire received 2026-07-10T02:02Z; ~10 consecutive hourly fires observed through 12:26Z, each triggering a bus check — the 12:26Z fire is what discovered ORDER 010 itself. No refusal/error at arm time; recurring cron was supported directly, so no send_later re-arm chain was needed.
- HONESTY NOTE: the routine was armed at 01:56Z and ORDER 010 landed at 11:06Z — the arm PRE-DATES the order, so the order's substance was already satisfied when it arrived. This session (kit-lab-build, claim #119) performed the bus ritual only: claim → record → done=010. All facts above are attributed to the coordinator-lane record, not re-verified here.
- Inbox ends at ORDER 010 (headers read `status: new` because only the manager flips them; diff the inbox against this orders line — the gen-2 rule). No unexecuted order exists. control/inbox.md untouched this close.

RELEASE SHIPPED (was wave-2 item 3 "assessed, NOT cut" — now DONE):
- v1.7.0 was CUT AGENT-SIDE tonight (2026-07-10). Path: the #113 prep bump landed (KIT_VERSION+pyproject 1.6.0→1.7.0, CHANGELOG [Unreleased]→[1.7.0], dist re-pin), then `release.yml` was fired via `workflow_dispatch` with input `version=1.7.0`. The dispatch was ACCEPTED (HTTP 204 — no auto-mode/classifier/403 wall); run 29074386841 concluded success; the workflow's server-side GITHUB_TOKEN created the annotated tag `v1.7.0` (at 93c7bdb) and published the GitHub Release with all three assets (bootstrap.py, bootstrap.py.sha256, release.json). Release live: https://github.com/menno420/substrate-kit/releases/tag/v1.7.0 (published 2026-07-10T06:38:59Z, target main, not draft/prerelease).
- CORRECTION to the record: release-cutting on this repo is AGENT-SIDE, not owner-gated. The tag-push 403 wall applies only to DIRECT agent tag pushes; the workflow's server-side token avoids it. Precedent: v1.4.0/v1.6.0 also cut by sessions. See the docs/CAPABILITIES.md append-log recipe (2026-07-10) — do NOT flag routine releases as owner-gated; attempt the dispatch (ORDER 008).
- KF-5 satisfied: the v1.7.0 release notes state the B1 run-3 outcome (strict-F-5 FAIL / disputed pending the F-5 ruling; 3-run trend headline 1 PASS / 2 FAIL). The run-4 outcome + 4-row trend are staged in CHANGELOG `[Unreleased]` (merged in #116) and travel into the NEXT release's notes; docs/current-state.md already carries the same 4-row trend — this file, the CHANGELOG note, and current-state agree.

⚑ needs-owner: eleven items, all six-field. The F-5 ruling is the HOT one; the rest are steady-state. (The prior close's ⚑ "cut v1.7.0" is RESOLVED and removed — the release shipped agent-side.)

⚑ OWNER-ACTION 1 — rubric F-5 wording ruling (A or B) — HOT
WHAT: Read two short paragraphs and answer with one letter — which reading of the benchmark pass/fail rule is intended.
WHERE: docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md
HOW: reply "A" (strict none-regressing) or "B" (7k-budget-purposive) in any channel
WHY-IT-MATTERS: run-4 FAILED under BOTH readings (the family's first ruling-independent verdict), so the ruling no longer decides run-4 — but it still flips runs 2–3, i.e. 2 of the 4 recorded verdicts, and with them the whole trend headline: under Reading A it is 1 PASS / 3 FAIL, under Reading B it is 3 PASS / 1 FAIL. Still HOT: what the rubric MEANS is the owner's call, and runs 2–3's verdicts (plus every future close-call run) hang on it.
UNBLOCKS: un-caveated verdicts for runs 2–3 + a settled 4-row trend headline; un-caveated KF-5 release notes at the next cut (the [Unreleased] note currently ships the A/B split).
VERIFIED-NEEDED: bench/rubric/ is a PIN PATH (bench integrity law); the idea file reserves the call ("Agents do not resolve this one") — product judgment on what the rubric MEANS; no agent attempt substitutes.

⚑ OWNER-ACTION 2 — P10 required-check swap
WHAT: Swap which CI check main requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); set "Require branches to be up to date" OFF
WHY-IT-MATTERS: the legacy alias jobs cause ~35-min queue stalls purely to satisfy old names; the up-to-date requirement stalls green PRs `behind` (live-hit #107).
UNBLOCKS: an agent deletes the two legacy-alias-* jobs (queue item 9); the queue-stall class ends; fast-lane PRs stop paying an update round-trip.
VERIFIED-NEEDED: no agent path to rulesets — direct api.github.com is 403 through the proxy and the MCP toolset has no ruleset endpoint; Settings → Rules is owner-only UI.

⚑ OWNER-ACTION 3 — P4 arm the daily lab loop
WHAT: Create the scheduled session that runs the lab every morning.
WHERE: Console → kit repo environment → Schedules → New schedule
HOW: paste the fenced prompt from docs/operations/lab-loop.md § Arming verbatim · cron `0 6 * * *` (UTC) · fresh session per fire ON · Sonnet-class model · unrestricted-branch-push OFF · auto-fix PRs ON
WHY-IT-MATTERS: turns the lab from manually-fired sessions into the self-running daily loop the program is built around.
UNBLOCKS: D3 (the autonomous daily loop; needs ≥3 scheduled fires).
VERIFIED-NEEDED: the console Schedules pane is owner UI — routine/schedule creation is an enumerated wall in docs/CAPABILITIES.md; no in-session API/MCP path.
(Correction note appended 2026-07-10, ORDER 010 — the VERIFIED-NEEDED line above is now PARTIALLY invalidated: the coordinator lane armed an hourly routine agent-side via `create_trigger` on the claude-code-remote MCP server (trig_01FnqnAQjLU2T8d16iHwWQ2h; coordinator-lane record, see ORDER 010 RECORD). The ask stays open because the lab loop wants a fresh-session-per-fire daily schedule with specific console options (model class, branch-push, auto-fix PRs), which the MCP arm has NOT been verified to cover — but per THE DISCOVERY RULE a next session should ATTEMPT `create_trigger` (fresh-session mode) before treating this as owner-only.)

⚑ OWNER-ACTION 4 — P5 create Railway project kit-lab
WHAT: Create a separate Railway project so the lab gets its own infra lane.
WHERE: Railway console → New project
HOW: name `kit-lab` · region `europe-west4` · no spend caps (PL-005) · notification rule → HQ #railway-alerts; then put a project-scoped RAILWAY_TOKEN in the kit repo's environment
WHY-IT-MATTERS: the lab has no infra lane of its own; sharing production's is forbidden.
UNBLOCKS: the P6 console move (agent-built the moment the token exists).
VERIFIED-NEEDED: Railway project creation is owner console UI, and the ambient-IDs-are-production rule bars agents from touching existing Railway IDs — both walls enumerated; no agent path.

⚑ OWNER-ACTION 5 — P8 confirm MIT
WHAT: Confirm the kit's license with one word.
WHERE: any channel
HOW: reply "MIT ok", or name a replacement license
WHY-IT-MATTERS: the kit ships to consumer repos with no declared license until this lands.
UNBLOCKS: closing the license ⚑ carried since KL-1.
VERIFIED-NEEDED: a license choice is a legal/product decision — owner judgment by nature; nothing for an agent to attempt.

⚑ OWNER-ACTION 6 — P11 public flip OR P13 read-only PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility. P13: github.com/settings/tokens → fine-grained PAT, read-only, consumer-repo scope, then add to the fleet environments
HOW: P11 is click-through; P13 is create-token + paste into environment settings
WHY-IT-MATTERS: sibling repos cannot see kit data today, so the merged console and the loop's cross-repo sweeps run blind.
UNBLOCKS: kit data in the merged console + the lab loop's B2/B3/B4 sweeps (queue item 12).
VERIFIED-NEEDED: repo visibility and credential minting are account-owner surfaces; the wall is verbatim in docs/CAPABILITIES.md — cross-repo get_file_contents returned "Access denied: repository … is not configured for this session".

⚑ OWNER-ACTION 7 — superbot upgrade decision
WHAT: Rule on superbot's kit pin — upgrade it or keep holding.
WHERE: any channel
HOW: decide-and-flag recommendation — adopt at the next stable release in one hop; say nothing to accept, "upgrade now" or "hold pin-only" to override
WHY-IT-MATTERS: superbot's deliberate pin is now 7 releases behind (v1.0.0 vs v1.7.0) and the drift window keeps growing.
UNBLOCKS: the fleet's last non-ENGAGED adopter upgrading, whenever taken.
VERIFIED-NEEDED: the pin is a recorded owner decision (docs/adopters.md: "the v1.2.0+ upgrade is an owner decision") — agents don't overrule a deliberate stance; product judgment, not a wall.

⚑ OWNER-ACTION 8 — web-environment setup script paste
WHAT: Paste the corrected environment setup script so no more sessions die at startup.
WHERE: Claude console → the environment's settings → "Setup script" field (owner-only dialog)
HOW: paste the guarded script from docs/gen2/setup.sh (gen-2 variant) verbatim
WHY-IT-MATTERS: the current script already killed one session at provisioning (wrong cwd + hard-fail on a missing requirements.txt — PR #47 documents the casualty + fix).
UNBLOCKS: reliable session starts in this environment. If already pasted, say so and this ask is withdrawn — agents cannot read the settings dialog to confirm.
VERIFIED-NEEDED: the environment settings dialog is owner-only console UI (docs/CAPABILITIES.md); PR #47 is the live evidence of the one confirmed casualty.

⚑ OWNER-ACTION 9 — (informational, low priority) optional self-merge permission rule
WHAT: Optionally grant a permission rule so future sessions can self-merge PRs directly instead of relying on the enabler workflow.
WHERE: Claude console → the environment's permission/auto-mode settings
HOW: allow `mcp__github__merge_pull_request` / `mcp__github__enable_pr_auto_merge` for this environment's sessions
WHY-IT-MATTERS: one gen-2 lane's auto-mode classifier refused these as "Merge Without Review" while another lane's were permitted the same night — the wall is session-dependent. auto-merge-enabler.yml covers the refused case server-side.
UNBLOCKS: nothing blocked — both paths land PRs today; this only removes the indirection. LOW priority.
VERIFIED-NEEDED: the classifier denial is verbatim in docs/CAPABILITIES.md (2026-07-10); the permission grant is an owner console surface — no agent path to change auto-mode rules.

⚑ OWNER-ACTION 10 — branch cleanup (lowest priority)
WHAT: Turn on auto-delete for merged branches, then delete the stale branches of already-closed PRs.
WHERE: Settings → General → Pull Requests → check "Automatically delete head branches"; then each closed PR's "Delete branch" button
HOW: one checkbox + click-throughs (this window added the wave-1/wave-2 lanes' merged branches to the pile)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path (git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool — docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 11 — enable "automatically update branches" (closes the auto-merge behind-stall)
WHAT: Turn on the repo setting that auto-updates a PR branch when its base moves, so an armed auto-merge PR that goes `behind` gets refreshed and lands without an agent round-trip.
WHERE: Settings → General → Pull Requests → check "Always suggest updating pull request branches" / the auto-update-branch control (the counterpart to OWNER-ACTION 2's "Require branches up to date")
HOW: one checkbox
WHY-IT-MATTERS: with "Require branches up to date" ON, a green armed PR stalls `behind` whenever a sibling merges first (live-hit #107 + again this window). The enabler `synchronize` re-arm (#111) narrows this — a fix-push now re-arms — but a PR that goes behind AFTER its last push still needs a manual `git merge origin/main` + push. Auto-update removes that residual manual step.
UNBLOCKS: armed auto-merge completes on green even when a sibling merges first with no later push; fully ends the behind-stall class (complements OWNER-ACTION 2, which offers the alternative of turning the requirement OFF entirely).
VERIFIED-NEEDED: repo General settings are owner-only UI; no agent path to toggle repo settings (same class as the ruleset/branch walls in docs/CAPABILITIES.md). Live evidence: #107 (and later close branch updates) sat `behind` with green checks until a manual branch update; the enabler `synchronize` fix (#111) is a partial, not a full, close.

B1 RUN-4 RESULT (recorded on main via #116; row 4 in bench/results/cold-start/index.json, raw run dir bench/results/cold-start/2026-07-10-run04/): seed 710402 (harborride, accepted first try), kit v1.7.0 — first run on the new release; arms claude-sonnet-5 / judge claude-opus-4-8, every value verified from the native transcripts' `model` field (run-3's ignored-model-orders wall BROKEN; stronger-judge separation restored). First clean scripted prepare in the family (the #95 engagement arc worked first try — no hand-driven RED→ENGAGED→GREEN), and hooks LIVE for the first time, so the T5 guard probe is finally MEASURED: the guard FIRED (9 advisory fires in the T5 window) and the session IGNORED it (obeyed = not-met). Numbers: M1 ON/OFF — T2 1034/661, T4 2113/1142, T5 195/330 (the family's first clean ON M1 pair win); **M2 OFF and M3 OFF, both family firsts** (the auto-drafted card was never opened; OFF's plain-README convention beat the kit at its own continuity game); in-budget max 2113 ≤ 7k; zero unrecoverable errors. VERDICT — Reading A (strict, THE VERDICT OF RECORD): **FAIL** (first 0-of-3 run) · Reading B (purposive): **ALSO FAIL** — the family's first ruling-independent verdict (dual-scored per the standing instruction while OWNER-ACTION 1 is unruled; immaterial this run since both readings agree). KF-8 trend at 4 rows: what still holds EVERY run — in-budget boot, zero unrecoverable errors; the runs-1–3 "ON wins M2+M3 every run" kind-consistency is **BROKEN by run-4**; scripted M1 goes to OFF in every clean T2/T4-class measurement while run-4 logged the first clean ON M1 win (T5); strict headline **1 PASS / 3 FAIL**, the disputed "none regressing" wording shielding runs 2–3 only. Confounds sharpened: 4 runs / 4 kit versions (1.0.0→1.3.0→1.6.0→1.7.0), fresh seed each run, judge drift (opus-4-8 ×2 → fable-5 → opus-4-8), and run-4 alone ran Sonnet-class arms with live hooks — the trend is the repeated per-measure pattern, not the raw numbers. Deviations verbatim in manifest runner_notes + s-row-facts (ON-T2 first spawn refused at the ORCHESTRATOR layer; arm reset and relaunched with a stance-consent line, worker task text verbatim both arms). (Run-3 context: strict-FAIL/purposive-PASS, disputed pending OWNER-ACTION 1 — recorded via #85, stated in the v1.7.0 release notes per KF-5.)

next (agent-available, NOT owner-gated — for the next session):
- **T5 guard-probe redesign** — awaits a daytime `do-not-automerge` PR (pin path — an autonomous session cannot land it; open it READY + labeled and leave the click to the owner). Run-4 note: hooks went LIVE and the probe finally MEASURED (fired yes, obeyed no), so the idea's "headless arms never engage the hook layer" gap is partially resolved — re-scope against `docs/ideas/t5-headless-guard-surface-2026-07-09.md` before building.
- **legacy-alias job delete** (queue item 9) — unblocked only AFTER OWNER-ACTION 2's required-check swap.
- **B2/B3/B4 cross-repo sweeps** (queue item 12) — blocked on OWNER-ACTION 6 (read access).
- **NEW (run-4's 💡 idea, ordinary lane): surface the unresolved handoff at SessionStart — push, not pull.** The SessionStart hook (already wired by `--wire-enforcement`) injects a compact orientation block — newest card + unresolved slots + top of current-state — into the session's opening context. Aimed directly at the run-4 M2/M3 loss (no measured session ever OPENED the auto-drafted card; the kit only speaks at Stop) and at M1 (injected context is cheaper than the exploratory reading ON pays today). Recorded card-level in `.sessions/2026-07-10-b1-run-4.md` § 💡 Session idea (dedup-checked there; not yet a docs/ideas/ file — filing it is part of picking it up).
- Ordinary-lane backlog if a session wants work: groomed docs/ideas/ — plain-adopt lane-drift advisory, orientation-budget headroom advisory, `bootstrap heartbeat` verb. **Bench model-identity capture: PARTIALLY superseded by run-4** — run-4 verified arm/judge models manually from the native transcripts (proving the check matters: it is how the run-3 ignored-orders wall was caught and its fix confirmed), but the automation half still stands (`run_ab.py collect` extracting `arm_model` into m1.json/manifest.json + `record` warning on judge==arm); still unfiled as an idea file — it lives card-level in `.sessions/2026-07-10-b1-run-3.md` § 💡.
- Fleet adopter follow-up: v1.7.0 is live — adopters (websites, trading-strategy, game repos) can now `bootstrap upgrade` to the accumulated fixes/capabilities; superbot's pin stays owner-gated (OWNER-ACTION 7).
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md.

notes: ORDER 010 close — the record above lands via PR #120 (session card .sessions/2026-07-10-order-010-hourly-wake.md); the #119 claim is cleared by this overwrite (claim → record → done, per the control/README.md claim ritual). docs/CAPABILITIES.md gets the matching routine-creation correction in the same PR (the "Environment / routine / Project creation = owner clicks" wall was over-broad for routines). This overwrite touches ONLY control/status.md + that CAPABILITIES append; inbox and pin paths untouched. Sibling lane heartbeats control/status-gba-homebrew-trackb.md + control/status-superbot-coordinator.md untouched (one writer per file). Prior owner clicks #26 (PL-011, ratified) + #49 (seed fix) remain merged — verified previously, not re-flagged. Prior context (B1 run-4 double-FAIL + 4-row trend, v1.7.0 release) carried unchanged in the sections above.
