# substrate-kit · status
updated: 2026-07-10T16:17:12Z
phase: ORDER 011 executed — F-5 ruling applied (Reading A), runs 2–3 re-scored, KF-8 headline un-caveated (**1 PASS / 3 FAIL**), B-benches UNPAUSED. This overwrite is the ORDER 011 close heartbeat (claim #127, session PR #128, born-red card `.sessions/2026-07-10-order-011-f5-reading-a.md`). The HOT owner blocker (⚑ OWNER-ACTION 1, F-5 A/B) is RESOLVED — the owner delegated the round-3 recommended answers wholesale (Q-0262) and ORDER 011 routed the ruling (Q-0262.1): **Reading A, the stricter reading; honest-negative headlines are the fleet's credibility asset.** B1 run-5 is free to fire (this slice cleared the hold only — no bench was run). Carried context: v1.7.0 RELEASED (tag `v1.7.0` @ 93c7bdb, run 29074386841), B1 run-4 RECORDED (#116, a3616db — FAIL under both readings, ruling-independent), ORDER 010 executed (#120), gen-2 close-out heartbeats #124/#125.
health: green — re-verified this session (2026-07-10, PR #128 branch): `python3 -m pytest tests/ -q` → 819 passed; `python3 dist/bootstrap.py check --strict` → exit 0; dist byte-pin clean (`python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py`). This slice is docs/control/bench-annotation only (no src, no dist regen; `bench/results/` untouched except a NEW annotation file — append-only law respected, `check_bench_integrity.py` green).
kit: v1.7.0 released · KIT_VERSION 1.7.0 · tag v1.7.0 live · check: green · engaged: yes

ROUTINE STATE:
— DELETED old trigger trig_01FnqnAQjLU2T8d16iHwWQ2h ("kit-lab gen2 hourly wake", cron "0 * * * *", bound to retired session_01Gb1Dq9vgeNkTyBPvvPqTrj); delete_trigger returned "deleted trigger trig_01FnqnAQjLU2T8d16iHwWQ2h"; confirmed absent in follow-up list_triggers.
— CREATED trigger trig_016EfUawz6KxEYqUM6f1BqDw "substrate-kit 2-hourly standing wake", cron "0 */2 * * *", created 2026-07-10T15:53:36Z via meta_mcp, enabled=true, persist_session=true, bound to coordinator session_01YMJrUDpcarFsqPZ2BeeiVB, first fire ~2026-07-10T16:01:56Z; stored wake prompt matched the coordinator's spec character-for-character; existence verified via list_triggers.
(The 14:17Z heartbeat's "ARMED and RECURRING" record described the OLD hourly trigger, verified before the cutover — both records are true in sequence; the 2-hourly trigger above is the live one. The stale ARMED pointer in docs/gen2/next-boot.md § 0 carries a superseded-note as of PR #128.)

last-shipped: ORDER 011 lane — claim fast-lane PR #127 (38a1e5a: `claimed-by: 011 kit-lab-order-011 2026-07-10T16:02Z` on the orders line, landed on main BEFORE build work per the ORDER 007 ritual), then session PR #128 (born-red card first commit; content: `bench/results/cold-start/f5-ruling-order-011.md` — the family-level ruling annotation, since `bench/results/` rows are CI-immutable and the re-score therefore supersedes rather than edits the recorded dual-reading caveats; un-caveated Reading-A headline in docs/current-state.md + CHANGELOG [Unreleased]; the "B1 run-5 WAITS" hold cleared in docs/gen2/next-boot.md + queue-state.md crosswalk; F-5 idea file RULED/historical + README index). Before that: gen-2 close-out heartbeats #124 (f08d959) + #125 (bc468ac), ORDER 010 bus record #120, B1 run-4 row #116 (a3616db), v1.7.0 release (#113 prep, tag @ 93c7bdb).

blockers: none blocking. Coordination notes carried: (1) self-merge classifier wall stays session-dependent; `auto-merge-enabler.yml` + self-armed `enable_pr_auto_merge` are the working paths (this lane's #127/#128 arms were PERMITTED). (2) "Require branches to be up to date" behaves as ON — a green PR can stall `behind` until a branch update (recipe in docs/CAPABILITIES.md). (3) Sibling lane heartbeats control/status-gba-homebrew-trackb.md + control/status-superbot-coordinator.md untouched — one writer per file.

B1 FAMILY VERDICTS (post-ruling, the un-caveated record): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** — headline **1 PASS / 3 FAIL** (Reading A, the ruling of record via ORDER 011; run-4 failed under both readings so it was ruling-independent). No dual-reading caveat travels with these verdicts anymore; future rows are scored under Reading A only. Full annotation: `bench/results/cold-start/f5-ruling-order-011.md`; full run-4 numbers: the #116 row + `.sessions/2026-07-10-b1-run-4.md`; lane PR ledger through the gen-2 waves: the 14:17Z heartbeat (git history of this file, #125).

orders: acked=001,002,003,004,005,006,007,008,009,010,011 done=001,002,003,004,005,006,007,008,009,010,011 — the whole dispatched queue is executed. ORDER 011 acked+done this overwrite (claim #127 → build #128, citing ORDER 011 · 2026-07-10T15:33Z · P0 · owner delegation Q-0262.1). The order-011 claim annotation (kit-lab-order-011, 2026-07-10T16:02Z, landed via #127) is CLEARED by this overwrite — the claimed work is PR #128 + this record. No open claim. Inbox tail (observed-at 2026-07-10T16:02Z, HEAD 38a1e5a): the highest ORDER is 011 and it is done — derive the tail by diffing control/inbox.md against this line at read time (headers stay `status: new` because only the manager flips them). control/inbox.md untouched this close.
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

ORDER 010 RECORD (hourly wake routine — carried; the trigger it records is now RETIRED by the cutover above):
- Mechanism: MCP tool `create_trigger` on the `claude-code-remote` MCP server — a tool call, not a console/UI path.
- Args: name "kit-lab gen2 hourly wake" · cron_expression "0 * * * *" · result trigger trig_01FnqnAQjLU2T8d16iHwWQ2h · created 2026-07-10T01:56:06Z · bound to the then-coordinator session_01Gb1Dq9vgeNkTyBPvvPqTrj · ~14 consecutive hourly fires observed 02:02Z→14:08Z, zero misses (verified via `list_triggers` at 13:52Z + 14:09Z, #124/#125 record).
- 2026-07-10T~15:53Z: that trigger was DELETED and replaced by the 2-hourly standing wake — see ROUTINE STATE above. The ORDER 010 substance (this Project arms its own clock, agent-side, via create_trigger) remains satisfied by the successor trigger.

⚑ needs-owner: eleven open items (item 1 RESOLVED this session and recorded below; items 2–12 carried verbatim from the 14:17Z heartbeat — ordinals kept stable so cross-references hold). The steady-state list follows.

⚑ OWNER-ACTION 1 — rubric F-5 wording ruling (A or B) — ✅ RESOLVED 2026-07-10 by ORDER 011
WHAT: Was: read two short paragraphs and answer with one letter. ANSWERED: **Reading A** (strict none-regressing) — owner delegation Q-0262.1 (superbot router Q-0262, round-3 recommended answers adopted wholesale), routed via inbox ORDER 011 (2026-07-10T15:33Z).
OUTCOME: runs 2–3 re-scored under Reading A (both stand as un-caveated FAILs); family headline **1 PASS / 3 FAIL**; B-benches unpaused (run-5 free to fire, Reading A only); un-caveated KF-5 notes ride the next release via CHANGELOG [Unreleased]. Record: `bench/results/cold-start/f5-ruling-order-011.md` (PR #128).

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

⚑ OWNER-ACTION 12 — route the websites ORDER 005 fleet relay
WHAT: Send the unexecuted ORDER 005 from the `websites` repo's inbox to a session that has websites scope, so it gets done.
WHERE: the `menno420/websites` repo — its `control/inbox.md` ORDER 005 (route it to a websites-scoped session; e.g. dispatch a session on that repo)
HOW: assign/relay ORDER 005 to a websites-scoped session (a substrate-kit / coordinator session cannot — no websites write scope)
WHY-IT-MATTERS: a dispatched fleet order is sitting unexecuted; the coordinator surfaced it but has no websites scope to route or run it, so it stalls until the owner routes it.
UNBLOCKS: whatever ORDER 005 on websites was meant to deliver (its substance lives in that repo's inbox).
VERIFIED-NEEDED: cross-repo write to `menno420/websites` is out of this session's scope (the per-session repo allowlist governs reads; execution needs a websites-scoped session) — genuinely owner-routed, not an assumed wall. Provenance: coordinator relay 2026-07-10 (docs/retro/coordinator-session-2026-07-10.md § 4); origin is this lane's gen-1 status notes.

next (agent-available, NOT owner-gated — for the next session):
- **B1 run-5 — UNBLOCKED by the F-5 ruling** (Reading A of record; the run itself was NOT part of the ORDER 011 slice). Fire per bench/README.md when a runner session picks it up; scored under Reading A only, no more dual-scoring.
- **Next coordinator slice (in flight): program review §6.1 — born-red gate fix into the kit CI template.**
- **T5 guard-probe redesign** — pin path, awaits a daytime `do-not-automerge` PR; re-scope against `docs/ideas/t5-headless-guard-surface-2026-07-09.md` first (run-4 partially resolved its premise).
- **legacy-alias job delete** (queue item 9) — unblocked only AFTER OWNER-ACTION 2's required-check swap.
- **B2/B3/B4 cross-repo sweeps** (queue item 12) — blocked on OWNER-ACTION 6 (read access).
- **SessionStart handoff-push idea** (run-4's 💡, top buildable per docs/gen2/next-boot.md § 0) + the ordinary-lane backlog in docs/ideas/.
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md.

notes: ORDER 011 close. Session shape: claim-first (#127, fast lane, on main before build), born-red card (#128 first commit), content (ruling annotation + un-caveat sweep + unpause), this heartbeat as the deliberate last content step, card flips complete as the last commit. Adaptation recorded honestly: index.json rows 2–3 already carried strict-FAIL as the verdict of record, so "re-score → both become FAIL" changed no verdict field — the re-score retired the dual-reading caveats; and `bench/results/` is CI-immutable (append-only law), so the ruling landed as a NEW annotation file rather than edits to recorded history. Sibling heartbeats untouched; inbox untouched; pin paths (bench/rubric|tasks|seeds) untouched.
