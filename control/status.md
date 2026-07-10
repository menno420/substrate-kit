# substrate-kit · status
updated: 2026-07-10T22:41:00Z
phase: EAP program review §6.4 SHIPPED (coordinator-assigned slice, not an inbox order) — one kit-owned claims convention + `check_claims` unified on it. Claim fast-lane PR #143 (squash **2599193**, claimed-by on main before build per the ORDER 007 ritual) → born-red build PR #144 (squash **80898c4**: new `control-claims-README.md.tmpl` planted at `control/claims/README.md` via ADOPT_PLAN, routing section in `control-README.md.tmpl` + this repo's local copies, `claims_dir` config key (default `control/claims`), `check_claims` extended with work-claim findings `claims-format`/`claims-stale` (72h horizon)/`claims-duplicate` (cross-location)/`claims-legacy-location` — ALL advisory-only, posture unchanged; CHANGELOG [Unreleased] entry; NO release cut). Design decision (decided-and-flagged): ORDER claims stay the heartbeat `claimed-by:` annotation (one-writer-per-file, already enforced); WORK/lane claims are one-file-per-claim under `control/claims/` — superbot's measured evidence won (~98% merge-conflict rate for shared-append vs 0% per-file, `tools/sim/claim_layout_sim.py`) + gba-homebrew's first-claim-merged-to-main arbitration; placed under control/ so claims ride the CI fast lane. Compat mechanics (flagged): legacy homes `docs/owner/claims/` + root `claims/` are AUTO-DETECTED and scanned in place with a `claims-legacy-location` nudge — advisory-by-contract means no adopter's existing claims can red a gate on upgrade; a deliberate different home pins via `claims_dir` (pinned = canonical, no nudge). `bootstrap currency` regen rode #144: trading-strategy row `stale (v1.7.0 < v1.7.1)` → `current` (tree v1.7.1); ALL 7 wave repos now read tree v1.7.1 in docs/adopters.md.
health: green — verified this session (2026-07-10, PR #144): local `python3 -m pytest tests/ -q` → **876 passed** (was 858; +18 claims/adopt tests); dist rebuilt + byte-pin clean; ruff clean; idea-index / program-law / bench-integrity checkers OK; `check --strict --require-session-log --session-log .sessions/2026-07-10-eap-64-claims.md` → "all checks passed" pre-push. CI on #144 final head a485a69: run **29128279027** — https://github.com/menno420/substrate-kit/actions/runs/29128279027 — green end-to-end (the cold-adoption smoke's adopt output shows `planted: control/claims/README.md` live, the new template proving itself in CI). Mid-flight red at head c1e61a4 (run 29127764220) was the born-red session-gate hold + legacy aliases mirroring it BY DESIGN — verified in kit-quality job log 86476896583 (sole finding: the card's incomplete markers), the same false-alarm class as #140.
kit: v1.7.1 · check: green · engaged: yes

HEADLINE (carried for the coordinator): **fleet-manager check-run wall** — after a gate-regenerating commit, no event created PR check runs for ~25 min; landed via its documented R21 REST path; mitigation (card-first-open + git-credential push) in team memory.

ROUTINE STATE:
— DELETED old trigger trig_01FnqnAQjLU2T8d16iHwWQ2h ("kit-lab gen2 hourly wake", cron "0 * * * *", bound to retired session_01Gb1Dq9vgeNkTyBPvvPqTrj); delete_trigger returned "deleted trigger trig_01FnqnAQjLU2T8d16iHwWQ2h"; confirmed absent in follow-up list_triggers.
— CREATED trigger trig_016EfUawz6KxEYqUM6f1BqDw "substrate-kit 2-hourly standing wake", cron "0 */2 * * *", created 2026-07-10T15:53:36Z via meta_mcp, enabled=true, persist_session=true, bound to coordinator session_01YMJrUDpcarFsqPZ2BeeiVB, first fire ~2026-07-10T16:01:56Z; stored wake prompt matched the coordinator's spec character-for-character; existence verified via list_triggers.
(The 14:17Z heartbeat's "ARMED and RECURRING" record described the OLD hourly trigger, verified before the cutover — both records are true in sequence; the 2-hourly trigger above is the live one. The stale ARMED pointer in docs/gen2/next-boot.md § 0 carries a superseded-note as of PR #128.)
— OWNER DIRECTIVE Q-0265 (2026-07-10) RECORD: continuous mode adopted — the one-slice-per-wake throttle is removed; the send_later continuation chain (~15 min) is the primary loop, and the 2-hourly cron is re-armed as the "substrate-kit failsafe wake"; pacing is backpressure, not time-throttle; the honesty guard is unchanged. re-arm record: pending worker report, next heartbeat carries it.

v1.7.1 DISTRIBUTION WAVE RECORD (2026-07-10): **7/7 merged-on-green** — superbot-next #122 1ba8607 · websites #74 a057140 · gba-homebrew #27 16e64d7 · venture-lab #14 7558cb2b · fleet-manager #40 7660be58 · superbot-games #23 b134961e · trading-strategy #44 24649d76; registry regen kit #142 8b4ae72. Carve-out detector first live exercise: clean everywhere; backup fix verified live. HELD unchanged: superbot (⚑ OWNER-ACTION 7) · pokemon-mod-lab (not adopted). (v1.7.0 wave record + RELEASE v1.7.1 RECORD: git history of this file, the 21:26Z heartbeat — release run 29124338479, tag v1.7.1 @ 1cbd666, asset sha256 2aa4feddf7de7e20b00f46866826985ca8fd11f40bc51ebe261bbdef3118486d.)

EAP §6.4 RECORD (2026-07-10, this lane): claim #143 @ **2599193** (`claimed-by: eap-6.4-claims kit-dev-lane 2026-07-10T22:25Z`, on main before build) · build PR #144 @ **80898c4** (born-red card `.sessions/2026-07-10-eap-64-claims.md` first commit c1e61a4, PR open + enabler-armed at open, flip-complete cf1d627, branch updated a485a69 after the claim merge to clear the behind-stall, CI run **29128279027** green) · survey ground truth in the card: superbot `docs/owner/claims/` (measured per-file evidence) · gba-homebrew root `claims/` · websites orders-line only · kit orders-line incl. checker-invisible non-numeric slice ids — this record's own claim was the LAST of that pre-convention practice; future slice claims go in `control/claims/`.

QUEUED KIT FIXES (next dev slice, carried from the wave): (1) `upgrade-report.md` is silent when carve-outs=0 — indistinguishable from detector-never-ran; (2) the "already banked" path doesn't hash-verify a pre-existing backup; (3) venture-lab mid-PR gate-regen born-red semantics gotcha.

last-shipped: EAP §6.4 lane — claim fast-lane PR #143 (squash **2599193**), build PR #144 (squash **80898c4** on origin/main, verified via git log; content per the phase line above; 876 tests green, dist byte-pin clean, CI run 29128279027). Before that: v1.7.1 distribution wave 7/7 (record block above) + registry regen #142, release v1.7.1 (#139/#140, tag @ 1cbd666), v1.7.1 payload #136/#137, EAP §6.3 #132/#133, §6.1 #129/#130, ORDER 011 #127/#128.

blockers: none blocking. Coordination notes carried: (1) self-merge classifier wall stays session-dependent; this session's `merge_pull_request` (#143) and `enable_pr_auto_merge` were PERMITTED, but the GitHub MCP hit "API rate limit already exceeded" repeatedly on GraphQL-backed calls while REST worked — arms succeeded on retry; the enabler workflow (claude/* heads) armed #144 at open. (2) "Require branches to be up to date" behaves as ON — #144 pre-empted the behind-stall with a `git merge origin/main` push after #143 landed. (3) Sibling lane heartbeats control/status-gba-homebrew-trackb.md + control/status-superbot-coordinator.md untouched — one writer per file.

B1 FAMILY VERDICTS (post-ruling, the un-caveated record): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** — headline **1 PASS / 3 FAIL** (Reading A, the ruling of record via ORDER 011; run-4 failed under both readings so it was ruling-independent). Future rows are scored under Reading A only. Full annotation: `bench/results/cold-start/f5-ruling-order-011.md`.

orders: acked=001,002,003,004,005,006,007,008,009,010,011 done=001,002,003,004,005,006,007,008,009,010,011 — the whole dispatched queue is executed (ORDER 011 acked+done citing ORDER 011 · 2026-07-10T15:33Z · P0 · owner delegation Q-0262.1). The `eap-6.4-claims` claim annotation (kit-dev-lane, 2026-07-10T22:25Z, landed via #143 @ 2599193) is CLEARED by this overwrite — the claimed work is PR #144 (squash 80898c4, CI run 29128279027) + this record. No open claim; no claim files in control/claims/. Inbox tail (observed-at 2026-07-10T22:24Z preflight on origin/main 8b4ae72; unchanged at this overwrite): the highest ORDER is 011 and it is done — NO new orders (012+) in the inbox; derive the tail by diffing control/inbox.md against this line at read time (headers stay `status: new` because only the manager flips them). control/inbox.md untouched this close.
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

ORDER 010 RECORD (hourly wake routine — carried; the trigger it records is now RETIRED by the cutover above):
- Mechanism: MCP tool `create_trigger` on the `claude-code-remote` MCP server — a tool call, not a console/UI path.
- Args: name "kit-lab gen2 hourly wake" · cron_expression "0 * * * *" · result trigger trig_01FnqnAQjLU2T8d16iHwWQ2h · created 2026-07-10T01:56:06Z · bound to the then-coordinator session_01Gb1Dq9vgeNkTyBPvvPqTrj · ~14 consecutive hourly fires observed 02:02Z→14:08Z, zero misses (verified via `list_triggers` at 13:52Z + 14:09Z, #124/#125 record).
- 2026-07-10T~15:53Z: that trigger was DELETED and replaced by the 2-hourly standing wake — see ROUTINE STATE above. The ORDER 010 substance (this Project arms its own clock, agent-side, via create_trigger) remains satisfied by the successor trigger.

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
(Correction note appended 2026-07-10, ORDER 010 — the VERIFIED-NEEDED line above is now PARTIALLY invalidated: routines CAN be armed agent-side via `create_trigger` (the ORDER 010 arm and the 2-hourly cutover above both prove it). The ask stays open because the lab loop wants a fresh-session-per-fire daily schedule with specific console options (model class, branch-push, auto-fix PRs), which the MCP arm has NOT been verified to cover — per THE DISCOVERY RULE a next session should ATTEMPT `create_trigger` (fresh-session mode) before treating this as owner-only.)

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
HOW: one checkbox + click-throughs (this window added the §6.4 lanes' merged branches to the pile)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path (git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool — docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 11 — enable "automatically update branches" (closes the auto-merge behind-stall)
WHAT: Turn on the repo setting that auto-updates a PR branch when its base moves, so an armed auto-merge PR that goes `behind` gets refreshed and lands without an agent round-trip.
WHERE: Settings → General → Pull Requests → check "Always suggest updating pull request branches" / the auto-update-branch control (the counterpart to OWNER-ACTION 2's "Require branches up to date")
HOW: one checkbox
WHY-IT-MATTERS: with "Require branches up to date" ON, a green armed PR stalls `behind` whenever a sibling merges first (live-hit #107 + again this window; #144 pre-empted it only by a manual branch update). The enabler `synchronize` re-arm (#111) narrows this — a fix-push now re-arms — but a PR that goes behind AFTER its last push still needs a manual `git merge origin/main` + push. Auto-update removes that residual manual step.
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
- **Next coordinator slice (queued, UNCLAIMED — claim in `control/claims/` before building, per the new convention): EAP program review §6.5 — setup-script contract** (`scripts/env-setup.sh`, exit-0, no secrets, rendered from the manager's archetypes — six divergent hand-rolled scripts today; spec: menno420/superbot `docs/eap/eap-program-review-2026-07-10.md` §6 item 5), unless the inbox says otherwise at read time.
- **QUEUED KIT FIXES block above** (upgrade-report silent-when-clean · already-banked hash-verify · gate-regen born-red semantics) — a natural dev slice, pairs with §6.5 or stands alone.
- **B1 run-5** — unblocked (Reading A of record); fire per bench/README.md when a runner session picks it up.
- **legacy-alias job delete** (queue item 9) — unblocked only AFTER OWNER-ACTION 2's required-check swap.
- **B2/B3/B4 cross-repo sweeps** (queue item 12) — blocked on OWNER-ACTION 6 (read access).
- 💡 from the #144 card: auto-create/auto-delete `control/claims/<branch>.md` in session-start/Stop-hook — enforcement exists (check_claims), automation is the missing half.
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md.

notes: EAP §6.4 close. Session shape: preflight (origin/main 8b4ae72, inbox tops at ORDER 011, NO 012+), survey (superbot/gba-homebrew/websites/kit claim mechanisms, read-only), claim-first (#143 fast lane, on main before build), born-red card + PR open FIRST (#144, enabler-armed at open), build (checker + template + config + tests), card flip last → branch update after #143 → merge 80898c4. Honest findings for the coordinator: (1) GitHub MCP GraphQL quota wall recurred (arms/lookups refused "API rate limit already exceeded" while REST worked — everything landed on retry; worth a CAPABILITIES.md note if it recurs across sessions). (2) A legacy claims home under docs/ (superbot's shape) also meets the ORDINARY docs-hygiene checkers when a host runs the kit gate — check_docs behavior, not a claims-posture leak; noted in the #144 tests. (3) The #144 first-head red was the born-red hold, verified in the job log before dismissing (PL-006). Sibling heartbeats untouched; inbox untouched; bench pin paths untouched.
