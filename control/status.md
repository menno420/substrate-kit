# substrate-kit · status
updated: 2026-07-11T00:30:00Z
phase: QUEUED KIT FIXES batch SHIPPED (coordinator-assigned dev slice, not an inbox order) — all four carried fixes in one PR, each with regression tests + a CHANGELOG [Unreleased] entry (v1.8.0 payload, NO release cut). Claim fast-lane PR #155 (squash **c232804**, `control/claims/kit-fixes-batch.md` on main before build per §6.4) → born-red build PR #156 (squash **e096a41**): (1) carve-out scan EXPLICIT-WHEN-CLEAN — `_regen_kit_owned_workflow()` emits `carve-out scan: <relpath> — ran, 0 found` on clean scans and upgrade-report.md always carries a `## Carve-out scan` section (clean per-file lines / hit pointer / "no kit-owned live workflow installed, nothing to scan"; the post-hoc --apply-docs report stays silent by design — there the detector genuinely never runs); (2) already-banked backup HASH-VERIFIED — `archive_dist()` never overwrites a differing pre-existing archive: new bytes bank under `bootstrap-<version>.<sha8>.py` with a loud name-collision report, the earlier bank (a rollback source) stays byte-untouched; (3) mid-PR gate-regen born-red hold (venture-lab #14, decided-and-flagged) — the generated substrate-gate routes a card ADDED by a PR through the FULL locked door when the same diff touches the gate workflow file itself (GitHub runs the PR head's workflow, so version-stability is impossible — the cheapest enforcing invariant is "hold semantics may only TIGHTEN, never loosen, inside the PR that changes them"); (4) code-span-aware unrendered-slot scan (the #148/#150 poison) — `find_placeholders_outside_code()` strips fenced blocks + inline code spans before the slot scan (banner hold keeps full-text evidence), AND the fast-lane skip is closed as the deeper bug (decided-and-flagged): `check --strict --status-only` now runs `check_engagement_control()` (the scan scoped to control-plane planted docs), so a control-only PR can no longer smuggle a slot regression onto main.
health: green — verified this session (2026-07-11, PR #156): local `python3 -m pytest tests/ -q` → **938 passed** (was 927; +11 regression tests); `python3 -m ruff check src/engine/` clean; dist rebuilt + byte-pin clean; `python3 dist/bootstrap.py check --strict` → exit 0 after the card flip (sole pre-flip finding was the card's own born-red hold, the known #140/#144/#147/#153 class — verified in job log 86490176865 before dismissing, PL-006; the coordinator's two extra red jobs were the legacy-alias mirrors of kit-quality). CI on #156 final head ac632db: run **29132463781** — https://github.com/menno420/substrate-kit/actions/runs/29132463781 — green end-to-end (kit-quality job 86490300356).
kit: v1.7.1 · check: green · engaged: yes

ROUTINE STATE:
— DELETED old trigger trig_01FnqnAQjLU2T8d16iHwWQ2h ("kit-lab gen2 hourly wake", cron "0 * * * *", bound to retired session_01Gb1Dq9vgeNkTyBPvvPqTrj); delete_trigger returned "deleted trigger trig_01FnqnAQjLU2T8d16iHwWQ2h"; confirmed absent in follow-up list_triggers.
— Q-0265 ROUTINE CUTOVER COMPLETE (2026-07-10T23:09–23:11Z, via single-call isolation after 4 multi-call worker attempts hung on their first trigger-MCP call): CREATED failsafe trig_019nbVSWfu9grKjeHks97CeU 'substrate-kit failsafe wake', cron '0 */2 * * *', enabled=true, persist_session=true, bound session_01YMJrUDpcarFsqPZ2BeeiVB, created 2026-07-10T23:09:56Z, next fire 2026-07-11T00:08:20Z, prompt per Q-0265 template verbatim. DELETED old trigger: delete_trigger returned 'deleted trigger trig_016EfUawz6KxEYqUM6f1BqDw'. ARMED continuation chain: send_later returned fire_at 2026-07-10T23:26:00Z, trigger_id trig_01F7KpBrT3uUpzvtG5fgHjT3; chain re-arms ~15 min per wake. Ops lesson for other seats (EAP data): multi-call trigger-MCP worker sequences hung reliably under parallel session load; single-call-per-worker succeeded first try (~30s).
— OWNER DIRECTIVE Q-0265 (2026-07-10) RECORD: continuous mode adopted — the one-slice-per-wake throttle is removed; the send_later continuation chain (~15 min) is the primary loop, and the 2-hourly cron is the "substrate-kit failsafe wake"; pacing is backpressure, not time-throttle; the honesty guard is unchanged.
(The 14:17Z heartbeat's "ARMED and RECURRING" record described the OLD hourly trigger, verified before the cutover — records are true in sequence; the live failsafe is trig_019nbVSWfu9grKjeHks97CeU above. The stale ARMED pointer in docs/gen2/next-boot.md § 0 carries a superseded-note as of PR #128.)

v1.7.1 DISTRIBUTION WAVE RECORD (2026-07-10): **7/7 merged-on-green** — superbot-next #122 1ba8607 · websites #74 a057140 · gba-homebrew #27 16e64d7 · venture-lab #14 7558cb2b · fleet-manager #40 7660be58 · superbot-games #23 b134961e · trading-strategy #44 24649d76; registry regen kit #142 8b4ae72. Carve-out detector first live exercise: clean everywhere; backup fix verified live. HELD unchanged: superbot (⚑ OWNER-ACTION 7) · pokemon-mod-lab (not adopted). (v1.7.0 wave record + RELEASE v1.7.1 RECORD: git history of this file, the 21:26Z heartbeat — release run 29124338479, tag v1.7.1 @ 1cbd666, asset sha256 2aa4feddf7de7e20b00f46866826985ca8fd11f40bc51ebe261bbdef3118486d.)

EAP §6.4 RECORD (2026-07-10): claim #143 @ **2599193** (`claimed-by: eap-6.4-claims kit-dev-lane 2026-07-10T22:25Z`, on main before build) · build PR #144 @ **80898c4** (born-red card `.sessions/2026-07-10-eap-64-claims.md` first commit c1e61a4, PR open + enabler-armed at open, flip-complete cf1d627, branch updated a485a69 after the claim merge to clear the behind-stall, CI run **29128279027** green) · survey ground truth in the card: superbot `docs/owner/claims/` (measured per-file evidence) · gba-homebrew root `claims/` · websites orders-line only · kit orders-line incl. checker-invisible non-numeric slice ids — that record's own claim was the LAST of the pre-convention practice; slice claims now go in `control/claims/` (the §6.5 session's #146 was the first).

EAP §6.5 RECORD (2026-07-10): claim fast-lane PR #146 @ **2a8e2ae** (`control/claims/eap-6.5-setup-script.md`, on main before build — first claim through the new §6.4 convention; deleted by the #148 close-out) · build PR #147 @ **6f87900** (born-red card `.sessions/2026-07-10-eap-65-setup-script.md` first commit 5efd9b4, PR open + auto-merge self-armed at open via `enable_pr_auto_merge` (MCP-created PR), build e26abde, branch update d5ac39d after #146 landed to pre-empt the behind-stall, flip-complete 8c8ca9b, CI run **29129398462** green) · feasibility ground truth: fleet-manager@ced65b4 `environments/` (archetypes.md, 5 archetype scripts, setup-universal.sh) — §6.5 NOT input-blocked; OWNER-ACTION 8 (the env-panel PASTE) remains open and is orthogonal to the kit-side contract. Design decisions (decided-and-flagged, detail in the session card): plant-don't-stage; `SETUP_SCRIPT_RELPATH` is a house-style constant, not config (D-7); no missing-file nag.

EAP §6.8 RECORD (2026-07-10): claim fast-lane PR #149 @ **d72943a** (`control/claims/eap-6.8-grammar.md`, on main before build; deleted by the #151 close-out) · build PR #150 @ **fa20735** (born-red card `.sessions/2026-07-10-eap-68-grammar.md` first commit e62ff51, PR open + auto-merge self-armed at open via `enable_pr_auto_merge`, drift-fix 67eceff (the #148 dollar-brace poison — a status code span the unrendered-slot scanner read as an unfilled slot), build 4998d29, branch update f7ea22e after #149 landed to pre-empt the behind-stall, flip-complete 1a44656, CI run **29130431557** green) · writer↔enforcer agreement verdict from the new tests: **all 17 passed on first run — the taught templates and the enforcers already agreed**; the only live drift found that session was the #148 status poison (fixed) and this repo's planted `control/README.md` being an older decoration-variant of the current template (§5.3 convention-fork class — pointers added to both, full re-sync left to the template-regeneration lane).

EAP §6.10 RECORD (2026-07-10, this lane): claim fast-lane PR #152 @ **c9b632f** (`control/claims/eap-6.10-automerge-enabler.md`, on main before build; deleted by this close-out) · build PR #153 @ **4ff0721** (born-red card `.sessions/2026-07-10-eap-610-automerge-enabler.md` first commit 1ad7b89, PR open + auto-merge self-armed at open via `enable_pr_auto_merge` (MCP-created PR — both arm calls PERMITTED first try this session), coordinator red ping on the born-red head root-caused per PL-006 as the designed session-gate hold (job log 86486411915 — the #140/#144/#147 class, no defect), build 7f89e57, branch update c590fbe after #152 landed to pre-empt the behind-stall, flip-complete 9d4fde0, CI run **29131416883** green, auto-merge fired) · decided-and-flagged (detail in the session card): enabler lifecycle = the gate's EXACTLY (live only via --wire-enforcement; a live planted enabler is the more dangerous artifact class, so no looser than the gate); planted at the SAME basename adopters hand-forked so forks fall under kit ownership on upgrade; `do-not-automerge` label stays a constant, not config (program-wide vocabulary); `automerge.required_context` is informational-only by design (the refuse-to-arm guard counts contexts generically).

KIT FIXES BATCH RECORD (2026-07-11, this lane): claim fast-lane PR #155 @ **c232804** (`control/claims/kit-fixes-batch.md`, on main before build; deleted by this close-out) · build PR #156 @ **e096a41** (born-red card `.sessions/2026-07-11-kit-fixes-batch.md` first commit 9acaced, PR open + auto-merge self-armed at open via `enable_pr_auto_merge` (MCP-created PR — both arm calls PERMITTED first try this session), build faffea3, branch update 0ccd513 after #155 landed to pre-empt the behind-stall, flip-complete ac632db, CI run **29132463781** green, auto-merge fired) · per-fix one-liners: (1) clean carve-out scans now say `ran, 0 found` per file + upgrade-report.md always states scan status; (2) archive_dist hash-verifies pre-existing banks — mismatch → content-hash dedup name, never overwrite, never silent-accept; (3) generated gate holds an ADDED card to the locked door when the PR also touches the gate file (mid-PR semantics only tighten); (4) slot scan strips code spans/fences + the control fast lane now runs the control-scoped unrendered scan (`check_engagement_control`). Tests 927 → 938. **The queued-fixes list is CLEARED — nothing deferred.**

EAP §6 STATUS NOTE (as of this heartbeat): the kit-owned EAP program-review §6 queue — items 1, 3, 4, 5, 8, 10 — is **COMPLETE**; §6.2 is manager-owned and stays with the manager.

last-shipped: kit fixes batch — claim fast-lane PR #155 (squash **c232804**), build PR #156 (squash **e096a41** on origin/main, verified via git log; content per the phase line above; 938 tests green, dist byte-pin clean, CI run 29132463781). Before that: EAP §6.10 (#152/#153/#154), EAP §6.8 (#149/#150/#151), EAP §6.5 (#146/#147/#148), EAP §6.4 (#143/#144), v1.7.1 distribution wave 7/7 + registry regen #142, release v1.7.1 (#139/#140, tag @ 1cbd666).

blockers: none blocking. Coordination notes carried: (1) self-merge classifier wall stays session-dependent; this session's `enable_pr_auto_merge` calls (#155, #156) were PERMITTED first try. (2) "Require branches up to date" behaves as ON — #156 pre-empted the behind-stall with a `git merge origin/main` push after #155 landed (same play as #144/#147/#150/#153). (3) Sibling lane heartbeats control/status-gba-homebrew-trackb.md + control/status-superbot-coordinator.md untouched — one writer per file. (4) Mid-flight coordinator red pings on #156's pre-flip heads were both root-caused from job logs per PL-006 as the designed born-red session-gate hold (+ the legacy-alias mirror jobs) — no defect.

B1 FAMILY VERDICTS (post-ruling, the un-caveated record): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** — headline **1 PASS / 3 FAIL** (Reading A, the ruling of record via ORDER 011; run-4 failed under both readings so it was ruling-independent). Future rows are scored under Reading A only. Full annotation: `bench/results/cold-start/f5-ruling-order-011.md`.

orders: acked=001,002,003,004,005,006,007,008,009,010,011 done=001,002,003,004,005,006,007,008,009,010,011 — the whole dispatched queue is executed (unchanged since the #154 heartbeat). The `kit-fixes-batch` work claim (control/claims/, landed via #155 @ c232804) is CLEARED by this close-out — the claimed work is PR #156 (squash e096a41, CI run 29132463781) + this record; the claim file is deleted in this same PR. No open claim; no claim files in control/claims/. Inbox tail (observed-at 2026-07-11T00:05Z preflight on origin/main d8d9508; unchanged at this overwrite): the highest ORDER is 011 and it is done — NO new orders (012+) in the inbox; derive the tail by diffing control/inbox.md against this line at read time (headers stay `status: new` because only the manager flips them). control/inbox.md untouched this close.
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

ORDER 010 RECORD (hourly wake routine — carried; the trigger it records is RETIRED by the cutovers above):
- Mechanism: MCP tool `create_trigger` on the `claude-code-remote` MCP server — a tool call, not a console/UI path.
- Args: name "kit-lab gen2 hourly wake" · cron_expression "0 * * * *" · result trigger trig_01FnqnAQjLU2T8d16iHwWQ2h · created 2026-07-10T01:56:06Z · bound to the then-coordinator session_01Gb1Dq9vgeNkTyBPvvPqTrj · ~14 consecutive hourly fires observed 02:02Z→14:08Z, zero misses (verified via `list_triggers` at 13:52Z + 14:09Z, #124/#125 record).
- 2026-07-10T~15:53Z: that trigger was DELETED and replaced by the 2-hourly standing wake; 2026-07-10T23:09Z: THAT trigger was in turn replaced by failsafe trig_019nbVSWfu9grKjeHks97CeU + the 15-min send_later chain — see ROUTINE STATE above. The ORDER 010 substance (this Project arms its own clock, agent-side, via create_trigger) remains satisfied by the successor triggers.

⚑ needs-owner: eleven open items (items 2–12, carried verbatim — ordinals kept stable so cross-references hold). The steady-state list follows.

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
WHY-IT-MATTERS: superbot's deliberate pin is now 8 releases behind (v1.0.0 vs v1.7.1) and the drift window keeps growing.
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
HOW: one checkbox + click-throughs (this window added the §6.4/§6.5/§6.8/§6.10 lanes' merged branches to the pile)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path (git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool — docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 11 — enable "automatically update branches" (closes the auto-merge behind-stall)
WHAT: Turn on the repo setting that auto-updates a PR branch when its base moves, so an armed auto-merge PR that goes `behind` gets refreshed and lands without an agent round-trip.
WHERE: Settings → General → Pull Requests → check "Always suggest updating pull request branches" / the auto-update-branch control (the counterpart to OWNER-ACTION 2's "Require branches up to date")
HOW: one checkbox
WHY-IT-MATTERS: with "Require branches up to date" ON, a green armed PR stalls `behind` whenever a sibling merges first (live-hit #107 + again this window; #144, #147, #150 and #153 pre-empted it only by a manual branch update). The enabler `synchronize` re-arm (#111) narrows this — a fix-push now re-arms — but a PR that goes behind AFTER its last push still needs a manual `git merge origin/main` + push. Auto-update removes that residual manual step.
UNBLOCKS: armed auto-merge completes on green even when a sibling merges first with no later push; fully ends the behind-stall class (complements OWNER-ACTION 2, which offers the alternative of turning the requirement OFF entirely).
VERIFIED-NEEDED: repo General settings are owner-only UI; no agent path to toggle repo settings (same class as the ruleset/branch walls in docs/CAPABILITIES.md). Live evidence: #107 (and later close branch updates) sat `behind` with green checks until a manual branch update; the enabler `synchronize` fix (#111) is a partial, not a full, close.

⚑ OWNER-ACTION 12 — route the websites ORDER 005 fleet relay
WHAT: Send the unexecuted ORDER 005 from the `websites` repo's inbox to a session that has websites scope, so it gets done.
WHERE: the `menno420/websites` repo — its `control/inbox.md` ORDER 005 (route it to a websites-scoped session; e.g. dispatch a session on that repo)
HOW: assign/relay ORDER 005 to a websites-scoped session (a substrate-kit / coordinator session cannot — no websites write scope)
WHY-IT-MATTERS: a dispatched fleet order is sitting unexecuted; the coordinator surfaced it but has no websites scope to route or run it, so it stalls until the owner routes it.
UNBLOCKS: whatever ORDER 005 on websites was meant to deliver (its substance lives in that repo's inbox).
VERIFIED-NEEDED: cross-repo write to `menno420/websites` is out of this session's scope (the per-session repo allowlist governs reads; execution needs a websites-scoped session) — genuinely owner-routed, not an assumed wall. Provenance: coordinator relay 2026-07-10 (docs/retro/coordinator-session-2026-07-10.md § 4); origin is this lane's gen-1 status notes.

⚑ version-truth deference (flagged for the owner's §7 layering ruling, decide-and-flag): generated `docs/adopters.md` is now the SINGLE home for the fleet's kit-version spread; other homes (hand-kept registries, release-json narratives, status-prose version claims) should DEFER to it pending the owner's §7 ruling. Concretely open under that ruling: the kit repo's own `substrate.config.json` pin (v1.0.0, self-adopt-era) vs its dist (v1.7.1) — the registry's one tree-internal DRIFT row, deliberately NOT hand-fixed because what consumer-#0's pin *means* is the §7 question.

next (agent-available, NOT owner-gated — for the next session; queue owner = the coordinator, who may reorder):
- **Next coordinator slice (queued, UNCLAIMED — claim in `control/claims/` before building): release v1.8.0 + distribution wave** (payload: §6.4 claims · §6.5 setup-script · §6.8 grammar · §6.10 auto-merge enabler · the kit fixes batch #156) to the engaged adopters.
- **B1 run-5** — unblocked (Reading A of record); fire per bench/README.md when a runner session picks it up.
- **legacy-alias job delete** (queue item 9) — unblocked only AFTER OWNER-ACTION 2's required-check swap.
- **B2/B3/B4 cross-repo sweeps** (queue item 12) — blocked on OWNER-ACTION 6 (read access).
- 💡 from the #156 card: an upgrade-report ACKNOWLEDGEMENT advisory — the #137 chain is detection → banking → reporting, but nothing proves an adopter read a ⚠️ carve-out section before the enabler auto-merged the upgrade PR; a `check` advisory closing that last silent gap.
- 💡 from the #153 card: `adopt --check-repo-settings` / `doctor --repo` — with an ambient GH_TOKEN, ATTEMPT the read-only halves of the repo-settings checklist and print VERIFIED per-item state (pairs with the carried `bootstrap doctor --env` idea).
- 💡 from the #150 card: `bootstrap grammar` subcommand — print the canonical control-plane formats from `engine.grammar`'s example renderers. 💡 carried from the #144 card: auto-create/auto-delete claim files in session-start/Stop-hook.
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md.

notes: kit fixes batch close. Session shape: preflight (origin/main d8d9508, inbox tops at ORDER 011, NO 012+), claim-first (#155 fast lane, on main before build), born-red card + PR open FIRST (#156, auto-merge self-armed at open), two coordinator red pings on pre-flip heads root-caused per PL-006 from job logs (the designed session-gate hold + legacy-alias mirrors — no defect, no fix pushed for them), build (4 fixes + 11 tests + CHANGELOG ### Fixed ×4 + dist regen), card flip last → merge e096a41 → this close-out. Honest findings for the coordinator: (1) fix 2's brief said the already-banked path "accepts without verifying" — ground truth was subtler: byte-equality WAS verified on the accept path, but a MISMATCH silently OVERWROTE the earlier bank; the shipped fix targets that real failure (dedup-name, never overwrite). (2) fix 4's code-span regexes had to be renamed `_MD_*` in render.py — the dist's single-namespace flattening collided with check_session_log's private constants (caught by the namespace guard test, not by import). (3) The fast-lane control slot gate creates no new deadlock class: the only pre-render window with slotted control docs is the adopt seed, which the status checker's no-heartbeat finding already holds red on the same lane. Sibling heartbeats untouched; inbox untouched; bench pin paths untouched.
