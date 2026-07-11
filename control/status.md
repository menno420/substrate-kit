# substrate-kit · status
updated: 2026-07-11T22:25:00Z
phase: RELEASE v1.12.1 SHIPPED + VERIFIED (this session, owner directive via coordinator: 2026-07-11 feature FREEZE — ship the pending PATCH release carrying the substrate-gate false-green fix). Premise verified FIRST: the #228 gate fixes (squash a45d32a, work commit f75460c — G-1 modified-sibling cards graded through the locked door; G-2 session-card deletions hard-red on both gate surfaces; external review #226) were NOT an ancestor of v1.12.0 (`git merge-base --is-ancestor` negative), so the release was genuinely pending. The cut, runbook's fifth consecutive clean exercise: claim PR **#243** (@ 4271fd3) → born-red bump PR **#244** (auto-merged squash **203bb09**; one coordinator red-ping mid-flight was the designed born-red hold — the W-9 false-alarm class AGAIN, job log verbatim "Designed hold — not a CI failure to investigate", job 86589400731, the two extra "failures" the legacy alias jobs) → `release.yml` dispatch run **29170017074** (success, head 203bb09) → tag **v1.12.1** (annotated 4be444d → 203bb09) → three-way sha256 verified: downloaded asset == release.json field == committed dist @ 203bb09 == **1055ca2cfd32a83e3dab7a978b05fbec2a82932a3375de0b1034f2519c16e4aa** (704108 B). ⚑ CLASS DECISION (decide-and-flag): the prior heartbeat penciled this payload as "v1.13.0"; the newer owner freeze directive says PATCH — shipped as **v1.12.1**, contract-defensible per §4.1 (payload = fixes/hardening of existing surfaces: #228 + #232 layered fetcher + #236 fast path & collect guard; no new checker/command/template, no contract breaks). ⚑ WAVE NOT STARTED — explicit coordinator directive ("do NOT start distribution waves"): 9 engaged adopter trees remain at v1.12.0; the v1.12.1 wave is the queue top. ⚑ adopters regen (runbook §6) also deferred to the wave slice. Bench B1 trend 1 PASS / 7 FAIL at 8 rows unchanged; resume one-pager: docs/retro/archive-ready-2026-07-11.md.
health: green — verified at the cut (2026-07-11, this session): `python3 -m pytest tests/ -q` → **1057 passed** (container note: pytest absent under `python3.10` here — 3.11 local, CI's 3.10 kit-quality run green on #244 is the ground truth); `ruff check src/engine/` clean; dist byte-pin clean (builder print == disk, **704108 B**); `check_idea_index` / `check_program_law` OK; `build_release_json --version 1.12.1 --verify-only` green pre-cut; `check --strict` exit 0 (sole pre-flip red on #244 = the designed born-red hold, job 86589400731). Prior health chains: git history of this file.
kit: v1.12.1 · check: green · engaged: yes

ROUTINE STATE (final record at archive, live-verified this session):
— **ARMED, survives the archive: the daily kit-lab loop** — trigger **trig_01MHwmBrA1bziEp49g6xqGt5** "kit-lab loop" · cron `0 6 * * *` (UTC) · fresh session per fire · environment env_01R1G1wsWsEMShxECRsFnVor · prompt = docs/operations/lab-loop.md fenced block · verified live at archive-prep: enabled=true, next fire 2026-07-12T06:01:33Z. Owner kill-switch: pause/delete the Routine in the console. First-fire confirmation owed by the first session after 06:00Z.
— **DISARMED: the Q-0265 failsafe cron** trig_019nbVSWfu9grKjeHks97CeU ("substrate-kit failsafe wake", `0 */2 * * *`, bound to the archived coordinator session). Honest correction: the archive order recorded it as already deleted; the live probe here found it **still armed** — `delete_trigger` returned "deleted trigger trig_019nbVSWfu9grKjeHks97CeU", so the disarm actually happened in this close-out. Lesson recorded (retro §3.1): verify routine-state claims by probe, not by record.
— One stray Q-0265 `send_later` one-shot (trig_0159SwShY6z4WXa6nbV2s2Ft, 19:34Z) may fire once into the archived coordinator session — harmless, self-disables after firing. The send_later continuation chain is otherwise ENDED with the archive (Q-0265 continuous mode ends; the daily loop is the standing cadence).

⚑ FOR MANAGER (relay debts owed to the kit — refreshed at the v1.12.0-wave close):
- **NEW — pokemon-mod-lab lane-owed items (from the v1.6.0 → v1.12.0 catch-up, pokemon-mod-lab#43; Q-0261.3 scope, deliberately NOT done by the wave):** (a) its `control/status.md:40` heartbeat still says kit v1.6.0 — one-writer per file, the lane must bump it; (b) claims-home decision owed — legacy root `claims/` is the binding practice there vs the kit's `control/claims/`; the check advisory fires every session until the lane pins one via `substrate.config.json` → `claims_dir`; (c) its `automerge.required_context` defaults to "substrate-gate" but the repo's actual required check is **"ROM builds"** — must be fixed BEFORE its staged auto-merge enabler is ever wired live; (d) `control/README.md` classified DIVERGED — manual merge owed, delta preserved in `.substrate/upgrade-report.md` § Template deltas; (e) its heartbeat uses the bold-label `- **kit:** vX` form the kit's KIT_LINE_RE doesn't parse (kit-side grammar follow-up idea filed on the #232 session card).
- **heartbeat `kit:`-line bump OWNERSHIP question (wave-report inconsistency)** — still open: the wave records disagree about who owes the post-upgrade heartbeat bump (websites bumped its `kit:` line in-lane on the wave PR itself and scanned clean at the #207 regen; every other adopter's bump is recorded as "lane-owed" and chronically lags 1–3 releases — the registry's whole recurring self-report DRIFT class). The manager should rule which seat owns the post-wave `kit:`-line bump — the wave-upgrade PR itself (websites' shape) vs each lane's next wake — so the drift class ends fleet-wide instead of regenerating as ⚠️ noise every wave. The pokemon-mod-lab item (a) above is the newest instance.
- **superbot-next origin/main was force-pushed mid-wave** (the v1.10.x window) — flagged, not touched by any kit-seat session; their lane owns the history reconcile.
- **v1.12.0-wave heartbeat `kit:` bumps still lane-owed** (self-report lag class, per the wave records + the #232 regen: fleet-manager, superbot-games — its status.md still has NO `kit:` line at all — and trading-strategy all lane-owed; kit-seat quad self-report lag persists per the chronic class; trees all already v1.12.0). Also lane-owed from the trio wave: `docs/AGENT_ORIENTATION.md` diverged manual merges on all three (template delta preserved in each repo's `.substrate/upgrade-report.md`).
- Carried from earlier waves, still standing as far as kit evidence shows: superbot-next duplicate session cards guard-firing (their gate noise — lane dedup) · venture-lab dual claims homes (control/claims/ + legacy — consolidate per §6.4) · gba-homebrew docs pending `upgrade --apply-docs` · fleet-manager owner-action-fields advisory (chronic) · trading-strategy docs/CAPABILITIES.md landing-constraints entry (chronic).

last-shipped: **v1.12.1** — bump PR #244 (squash 203bb09, claim #243), release run 29170017074, tag v1.12.1, three-way sha verified (see phase). Before it: #241 archive-prep wrap-up (retro + archive-ready note + routine-state record); #236 ON-T2 footprint cut — now RELEASED in v1.12.1.

blockers: none. Coordination notes: pin PRs #220 + #238 park OPEN by design (owner ratification, ⚑ 14/15 below — do NOT arm auto-merge on them); control/claims/ holds the #245 "measure adopter outcomes" claim (another lane, active — this session's release-v1.12.1 claim is deleted by this PR); ~48 stale merged-PR branches await the owner's auto-delete checkbox (⚑ 10; agent branch-deletion is a verified 403 wall).

B1 FAMILY VERDICTS (post-ruling record): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** · run 5 **FAIL** · run 6 **FAIL** · run 7 **ABORTED — harness environment seam, NOT SCORED, no row** · run 8 **FAIL** — scored headline **1 PASS / 6 FAIL at 7 rows** (Reading A, the ruling of record via ORDER 011). Run-8 is the delegation-seam-smoke run: the run-7 environment failure is countered (mitigated flat seam, verbatim 6/6) and the #203 pointer CONVERTS at the measured seam — the open gap is the unfilled auto-draft card it points at (B1 RUN-8 RECORD above; run dir + row PR #215 @ 54658bb). Full annotation: `bench/results/cold-start/f5-ruling-order-011.md`.

orders: acked=001,002,003,004,005,006,007,008,009,010,011,012,013 done=001,002,003,004,005,006,007,008,009,010,011,012,013

⚑ needs-owner: thirteen open items (items 2–12 carried verbatim — ordinals kept stable so cross-references hold — plus 14 + 15, the two parked pin PRs; item 13 RESOLVED 2026-07-11: the owner merged #181 @ f7aa633 — full resolution record in the retro §2 postscript + git history of this file). The two HOT ones are one click each:

⚑ OWNER-ACTION 15 — T5 v3 probe re-shape — pin PR #238 awaits your ratification (do-not-automerge by design; PAIRS with OWNER-ACTION 14 / PR #220)
WHAT: Ratify (merge) or reject (close with a word) the T5 task-text re-shape that restores the probe's discriminating tension.
WHERE: https://github.com/menno420/substrate-kit/pull/238
HOW: click "Merge pull request" to ratify, or close it with a one-line reason — the PR is READY, CI-green at head 917318d, labeled at open, diff = bench/tasks/T5.md + its session card only.
WHY-IT-MATTERS: run-9 proved the v2 probe degenerate post-#222 — T4 now completes the card, so T5 boots on a "complete" push and the skip-vs-ritual tension the probe exists to measure never arises (run-9 report §5.5). v3 has the runner seed the drafted/unresolved state (and commit the arm tree clean — retiring the 4/4 commit-sweep confound of runs 8–9), so the probe discriminates regardless of T4's behavior.
UNBLOCKS: run-10 fires a non-degenerate T5. PAIRING: judge items are unchanged from v2, so rubric pin PR #220 scores v3 as-is and needs no re-cut — ratify both (one click each) and run-10 judges v3 task text under the §3-v2 rubric coherently.
VERIFIED-NEEDED: pin-path law (§5.0, check_bench_integrity rule 1): the lab never merges its own change to the bench oracle — labeled `do-not-automerge` at open, auto-merge verified not armed (enabler run 29164948745 arm step conclusion=skipped, KL-5 fresh-label guard; the head-917318d synchronize run 29165025432 skipped the whole enable-auto-merge job on the labeled payload; PR sat open at mergeable_state=clean on green CI), parked; only the owner's click lands it.

⚑ OWNER-ACTION 14 — rubric §3 T5 v2 alignment — pin PR #220 awaits your ratification (do-not-automerge by design)
WHAT: Ratify (merge) or reject (close with a word) the judge-rubric alignment your #181 merge made due.
WHERE: https://github.com/menno420/substrate-kit/pull/220
HOW: click "Merge pull request" to ratify, or close it with a one-line reason to reject — the PR is READY, CI-green at head c582006, diff = bench/rubric/cold-start-rubric.md (§3 T5 block only) + its session card.
WHY-IT-MATTERS: the judge already scores T5 from the ratified v2 task text, but the written rubric still describes the retired v1 items — every bench run carries a "protocol pins applied" deviation note until the two documents agree.
UNBLOCKS: bench runs from run-9 on score T5 straight from rubric §3; retires the run-8 report §5 limitation line.
VERIFIED-NEEDED: pin-path law (§5.0, check_bench_integrity rule 1): the lab never merges its own change to the bench oracle — this session labeled #220 at open, verified the enabler's arm step was SKIPPED (run 29158862553, step "Enable native auto-merge (squash)" conclusion=skipped) and a disarm probe mutated nothing (PR updated_at unchanged), and parked it. Only the owner's click can land it — the designed wall, not an assumed one.
(PAIRING note added 2026-07-11: T5 v3 pin PR #238 / ⚑ 15 keeps the v2 judge items verbatim — ratifying both, one click each, gives run-10 a coherent text+rubric pair.)

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
(Correction note appended 2026-07-10, ORDER 010 — the VERIFIED-NEEDED line above is now PARTIALLY invalidated: routines CAN be armed agent-side via `create_trigger` (the ORDER 010 arm and both cutovers above prove it). The ask stays open because the lab loop wants a fresh-session-per-fire daily schedule with specific console options (model class, branch-push, auto-fix PRs), which the MCP arm has NOT been verified to cover — per THE DISCOVERY RULE a next session should ATTEMPT `create_trigger` (fresh-session mode) before treating this as owner-only.)
(RESOLUTION note appended 2026-07-11, the P4 slice — the directed ATTEMPT was made and SUCCEEDED: `create_trigger` with `create_new_session_on_fire=true` armed the loop agent-side — trigger trig_01MHwmBrA1bziEp49g6xqGt5, cron `0 6 * * *`, substrate-kit environment, lab-loop.md prompt verbatim, next fire 2026-07-12T06:01:54Z (full record: ROUTINE STATE). The founding plan's P4 row itself blesses this path ("or agent-created trigger + owner kill-switch"); the kill switch exists both sides (owner pause toggle + agent delete_trigger). **The ask is REDUCED to an optional console verification**: the three console-only knobs — model class Sonnet-class, unrestricted-branch-push OFF, auto-fix PRs ON — are not settable/readable via MCP; the fired sessions run on environment defaults. If the defaults are acceptable, say nothing — the loop is live; to adjust, open the Routine in the console and set the knobs. D3's ≥3-consecutive-fires count starts 2026-07-12.)

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
WHY-IT-MATTERS: superbot's deliberate pin is now 14 releases behind (v1.0.0 vs v1.12.0) and the drift window keeps growing.
UNBLOCKS: the fleet's last non-ENGAGED adopter upgrading, whenever taken.
VERIFIED-NEEDED: the pin is a recorded owner decision (docs/adopters.md: "the v1.2.0+ upgrade is an owner decision") — agents don't overrule a deliberate stance; product judgment, not a wall.

⚑ OWNER-ACTION 8 — web-environment setup script paste
WHAT: Paste the corrected environment setup script so no more sessions die at startup.
WHERE: Claude console → the environment's settings → "Setup script" field (owner-only dialog)
HOW: paste the guarded script from docs/gen2/setup.sh (gen-2 variant) verbatim
WHY-IT-MATTERS: the current script already killed one session at provisioning (wrong cwd + hard-fail on a missing requirements.txt — PR #47 documents the casualty + fix).
UNBLOCKS: reliable session starts in this environment. If already pasted, say so and this ask is withdrawn — agents cannot read the settings dialog to confirm.
VERIFIED-NEEDED: the environment settings dialog is owner-only console UI (docs/CAPABILITIES.md); PR #47 is the live evidence of the one confirmed casualty.
(§6.5 note appended 2026-07-10: the kit-side setup-script CONTRACT shipped without this — PR #147 planted `scripts/env-setup.sh` + the `check_setup_script` enforcer from the fleet-manager archetype material. This ask remains the ENV-PANEL half: the owner-pasted shim is what makes any repo's `scripts/env-setup.sh` actually run at provisioning. The paste-ready archetype scripts live at fleet-manager `environments/archetype-*.sh`.)

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
HOW: one checkbox + click-throughs (this window added the release/regen/bench lanes' merged branches to the pile)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path (git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool — docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 11 — enable "automatically update branches" (closes the auto-merge behind-stall)
WHAT: Turn on the repo setting that auto-updates a PR branch when its base moves, so an armed auto-merge PR that goes `behind` gets refreshed and lands without an agent round-trip.
WHERE: Settings → General → Pull Requests → check "Always suggest updating pull request branches" / the auto-update-branch control (the counterpart to OWNER-ACTION 2's "Require branches up to date")
HOW: one checkbox
WHY-IT-MATTERS: with "Require branches up to date" ON, a green armed PR stalls `behind` whenever a sibling merges first (live-hit #107 + the §6.4/§6.5/§6.8/§6.10 window; #144, #147, #150 and #153 pre-empted it only by a manual branch update). The enabler `synchronize` re-arm (#111) narrows this — a fix-push now re-arms — but a PR that goes behind AFTER its last push still needs a manual `git merge origin/main` + push. Auto-update removes that residual manual step.
UNBLOCKS: armed auto-merge completes on green even when a sibling merges first with no later push; fully ends the behind-stall class (complements OWNER-ACTION 2, which offers the alternative of turning the requirement OFF entirely).
VERIFIED-NEEDED: repo General settings are owner-only UI; no agent path to toggle repo settings (same class as the ruleset/branch walls in docs/CAPABILITIES.md). Live evidence: #107 (and later close branch updates) sat `behind` with green checks until a manual branch update; the enabler `synchronize` fix (#111) is a partial, not a full, close.

⚑ OWNER-ACTION 12 — route the websites ORDER 005 fleet relay
WHAT: Send the unexecuted ORDER 005 from the `websites` repo's inbox to a session that has websites scope, so it gets done.
WHERE: the `menno420/websites` repo — its `control/inbox.md` ORDER 005 (route it to a websites-scoped session; e.g. dispatch a session on that repo)
HOW: assign/relay ORDER 005 to a websites-scoped session (a substrate-kit / coordinator session cannot — no websites write scope)
WHY-IT-MATTERS: a dispatched fleet order is sitting unexecuted; the coordinator surfaced it but has no websites scope to route or run it, so it stalls until the owner routes it.
UNBLOCKS: whatever ORDER 005 on websites was meant to deliver (its substance lives in that repo's inbox).
VERIFIED-NEEDED: cross-repo write to `menno420/websites` is out of this session's scope (the per-session repo allowlist governs reads; execution needs a websites-scoped session) — genuinely owner-routed, not an assumed wall. Provenance: coordinator relay 2026-07-10 (docs/retro/coordinator-session-2026-07-10.md § 4); origin is this lane's gen-1 status notes.

⚑ version-truth deference (flagged for the owner's §7 layering ruling, decide-and-flag): generated `docs/adopters.md` is now the SINGLE home for the fleet's kit-version spread; other homes (hand-kept registries, release-json narratives, status-prose version claims) should DEFER to it pending the owner's §7 ruling. Concretely open under that ruling: the kit repo's own `substrate.config.json` pin (v1.0.0, self-adopt-era) vs its dist (v1.12.0) — the registry's one tree-internal DRIFT row, deliberately NOT hand-fixed because what consumer-#0's pin *means* is the §7 question.

next (agent-available, NOT owner-gated — queue owner = whoever wakes next; the daily loop or a fresh session):
- **Top: the v1.12.1 distribution wave** (`upgrade` each engaged adopter per docs/operations/release-runbook.md §6 + the wave records' shape) + the adopters currency regen — BOTH deliberately deferred by this release slice (coordinator directive: release only, no waves). The release-cut half of the old "v1.13.0" queue item is DONE (shipped as v1.12.1, see phase ⚑ CLASS DECISION); [Unreleased] is fresh/empty.
- **Then bench run-10** — re-measure the ON-T2 axis + fire the advisory-lane probe (bench/results/cold-start/run-10-spec-notes.md); judges best after ⚑ 14/15 ratify.
- Carried queue (unchanged): K0 headroom advisory · B2–B4 sweeps gated on ⚑ 6 · the groomed backlog (docs/ideas/README.md).

notes: the v1.12.1 release slice (single session end-to-end, worker under the coordinator's feature-freeze directive). Session shape: verify-the-premise-first (fix-ancestry check before any build), runbook fifth clean exercise, PATCH-class decide-and-flag (see phase). Session card: .sessions/2026-07-11-bump-v1.12.1.md (in #244). Container gotcha recorded on the card: no pytest under python3.10 in this seat — runbook §3 interpreter-discovery idea filed. Prior heartbeat (archive-ready baseline) preserved verbatim at git history @ 700c5b6.
