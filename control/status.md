# substrate-kit · status
updated: 2026-07-10T21:02:00Z
phase: v1.7.1-payload slice EXECUTED (coordinator-assigned, not an inbox order) — three distribution-wave findings fixed kit-side, CHANGELOG framed as the v1.7.1 payload, NO tag cut (deliberately the next slice). (1) SPURIOUS BACKUP FIX: `bootstrap upgrade` banked `.substrate/backup/bootstrap-<NEW>.py` — a copy of the new dist — next to the correct old-dist archive (field-reproduced on fleet-manager #35, superbot-games #22, trading-strategy #38; harmless, `last-upgrade.json` named the right archive, but wrong). Root cause: `run_upgrade` step 6 → `adopt()` step 0c re-archived the vendored file AFTER the step-5 replace. Fix: `adopt(archive_running=...)` (default True — standalone adopt unchanged), upgrade passes False; regression test pins EXACTLY ONE banked `bootstrap-*.py`, old version's name + bytes. (2) GATE CARVE-OUT PROTECTION (superbot-games #16 class — its ONLY pytest job was hand-added inside the kit-owned gate; a plain regen would have silently deleted the repo's whole test gate): the kit-owned `substrate-gate.yml` regen now outlines live-vs-expected (`gate_carveouts()`, stdlib line-based), reports host-added jobs/steps as explicit `carve-out:` lines + a dedicated ⚠️ section in `.substrate/upgrade-report.md`, and banks the FULL pre-regen copy content-hash-named under `.substrate/backup/substrate-gate.pre-regen-<sha8>.yml` — detection is best-effort BY DESIGN but the bank makes a parse miss under-report, never lose content; adopter relocation rule documented in the release-notes ADOPTER_CHECKLIST (negative finding: docs/ has NO dedicated upgrade-recipe doc — the checklist in `src/build_release_json.py` is the operative recipe, founding plan §4.3 is historical). (3) INBOX-BASE WIRING — NEGATIVE FINDING CONFIRMED then fixed: the post-#130 generated gate did NOT wire `--inbox-base` (the flag existed only in cli.py + the checker; only the kit's own ci.yml ran the inbox gate) — inbox pure-append enforcement was LATENT on EVERY adopter. The generated gate now carries the inbox append-only step (both lanes, self-skips when the inbox is untouched, merge-base blob git-extracted in bash, stdlib python3); adopters inherit it on their next upgrade via the kit-owned regen. Carried context: §6.3 currency checker (#133 @ ff3b752), §6.1 kit-owned gate (#130 @ b221c87), ORDER 011 F-5 Reading A (#128), v1.7.0 RELEASED (tag @ 93c7bdb).
health: green — verified this session (2026-07-10, PR #137 final head dc5391d): `python3 -m pytest tests/ -q` → **858 passed** (852 on main → +6 new: exactly-one-archive regression, upgrade carve-out surfacing, pristine-regen-clean, inbox-base wiring pin, gate_carveouts unit coverage, adopt-regen bank+report); `python3 dist/bootstrap.py check --strict` → exit 0; `python3 -m ruff check src/engine/` clean; dist rebuilt, byte-pin clean. CI run **29123213759** — https://github.com/menno420/substrate-kit/actions/runs/29123213759 — green end-to-end (kit-quality + both legacy aliases + enable-auto-merge).
kit: v1.7.0 released · KIT_VERSION 1.7.0 · tag v1.7.0 live · check: green · engaged: yes (v1.7.1 payload staged in CHANGELOG [Unreleased]; tag deliberately NOT cut — next slice)

ROUTINE STATE:
— DELETED old trigger trig_01FnqnAQjLU2T8d16iHwWQ2h ("kit-lab gen2 hourly wake", cron "0 * * * *", bound to retired session_01Gb1Dq9vgeNkTyBPvvPqTrj); delete_trigger returned "deleted trigger trig_01FnqnAQjLU2T8d16iHwWQ2h"; confirmed absent in follow-up list_triggers.
— CREATED trigger trig_016EfUawz6KxEYqUM6f1BqDw "substrate-kit 2-hourly standing wake", cron "0 */2 * * *", created 2026-07-10T15:53:36Z via meta_mcp, enabled=true, persist_session=true, bound to coordinator session_01YMJrUDpcarFsqPZ2BeeiVB, first fire ~2026-07-10T16:01:56Z; stored wake prompt matched the coordinator's spec character-for-character; existence verified via list_triggers.
(The 14:17Z heartbeat's "ARMED and RECURRING" record described the OLD hourly trigger, verified before the cutover — both records are true in sequence; the 2-hourly trigger above is the live one. The stale ARMED pointer in docs/gen2/next-boot.md § 0 carries a superseded-note as of PR #128.)

last-shipped: v1.7.1-payload lane — claim fast-lane PR #136 (squash **7e600c6**: `claimed-by: v1.7.1-payload kit-v171-lane 2026-07-10T20:47Z` on the orders line, landed on main BEFORE build work per the ORDER 007 ritual), then session PR #137 (squash **17fddff** on origin/main, verified via git log; born-red card `.sessions/2026-07-10-v171-payload.md` as the first commit, PR opened + auto-merge self-armed within minutes of session start; content: `adopt(archive_running=...)` + upgrade passes False + `gate_carveouts()`/`_workflow_outline()` + carve-out bank/report wiring in adopt step 6b and `upgrade_report_text(..., carveouts)` + the inbox append-only step in `live_ci_workflow()` + ADOPTER_CHECKLIST carve-out rule + 6 tests (858 total) + CHANGELOG [Unreleased] Fixed×2/Added×1 + dist rebuilt byte-pin clean). Mid-flight red at first head 8fe425b was the born-red session-gate hold + the two legacy aliases mirroring it BY DESIGN (verified in the run-29122693626 job log: sole kit-quality finding was this card's incomplete markers); the card flip cleared it — final head green, run 29123213759. Before that: EAP §6.3 lane #132/#133 (currency checker), §6.1 lane #129/#130 (kit-owned gate), ORDER 011 lane #127/#128 (F-5 Reading-A ruling), v1.7.0 release (tag @ 93c7bdb).

blockers: none blocking. Coordination notes carried: (1) self-merge classifier wall stays session-dependent; `auto-merge-enabler.yml` + self-armed `enable_pr_auto_merge` are the working paths (this lane's #127/#128 arms were PERMITTED). (2) "Require branches to be up to date" behaves as ON — a green PR can stall `behind` until a branch update (recipe in docs/CAPABILITIES.md). (3) Sibling lane heartbeats control/status-gba-homebrew-trackb.md + control/status-superbot-coordinator.md untouched — one writer per file.

B1 FAMILY VERDICTS (post-ruling, the un-caveated record): run 1 **PASS** · run 2 **FAIL** · run 3 **FAIL** · run 4 **FAIL** — headline **1 PASS / 3 FAIL** (Reading A, the ruling of record via ORDER 011; run-4 failed under both readings so it was ruling-independent). No dual-reading caveat travels with these verdicts anymore; future rows are scored under Reading A only. Full annotation: `bench/results/cold-start/f5-ruling-order-011.md`; full run-4 numbers: the #116 row + `.sessions/2026-07-10-b1-run-4.md`; lane PR ledger through the gen-2 waves: the 14:17Z heartbeat (git history of this file, #125).

orders: acked=001,002,003,004,005,006,007,008,009,010,011 done=001,002,003,004,005,006,007,008,009,010,011 claimed-by: release-v1.7.1 kit-release-lane 2026-07-10T21:11Z (coordinator slice, not an inbox order: cut release v1.7.1 — version bump + CHANGELOG [1.7.1] cut + dist re-pin, release.yml workflow_dispatch, adopters currency regen, status close-out) — the whole dispatched queue is executed (ORDER 011 acked+done per the 16:17Z heartbeat: claim #127 → build #128, citing ORDER 011 · 2026-07-10T15:33Z · P0 · owner delegation Q-0262.1). The v1.7.1-payload claim annotation (kit-v171-lane, 2026-07-10T20:47Z, landed via #136 @ 7e600c6) is CLEARED by this overwrite — the claimed work is PR #137 (squash 17fddff, CI run 29123213759) + this record. No open claim. Inbox tail (observed-at 2026-07-10T20:45Z preflight, HEAD f0e6c85; unchanged at this overwrite): the highest ORDER is 011 and it is done — NO new orders (012+) in the inbox at this close; derive the tail by diffing control/inbox.md against this line at read time (headers stay `status: new` because only the manager flips them). control/inbox.md untouched this close.
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

ORDER 010 RECORD (hourly wake routine — carried; the trigger it records is now RETIRED by the cutover above):
- Mechanism: MCP tool `create_trigger` on the `claude-code-remote` MCP server — a tool call, not a console/UI path.
- Args: name "kit-lab gen2 hourly wake" · cron_expression "0 * * * *" · result trigger trig_01FnqnAQjLU2T8d16iHwWQ2h · created 2026-07-10T01:56:06Z · bound to the then-coordinator session_01Gb1Dq9vgeNkTyBPvvPqTrj · ~14 consecutive hourly fires observed 02:02Z→14:08Z, zero misses (verified via `list_triggers` at 13:52Z + 14:09Z, #124/#125 record).
- 2026-07-10T~15:53Z: that trigger was DELETED and replaced by the 2-hourly standing wake — see ROUTINE STATE above. The ORDER 010 substance (this Project arms its own clock, agent-side, via create_trigger) remains satisfied by the successor trigger.

⚑ needs-owner: eleven open items (items 2–12, carried verbatim — ordinals kept stable so cross-references hold; item 1, the F-5 ruling, was RESOLVED by ORDER 011 and its resolved-record block is now retired per the expire-stale-asks hygiene — the durable record lives in `bench/results/cold-start/f5-ruling-order-011.md` + the 18:40Z heartbeat in this file's git history). The steady-state list follows.

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

⚑ version-truth deference (flagged for the owner's §7 layering ruling, decide-and-flag): generated `docs/adopters.md` is now the SINGLE home for the fleet's kit-version spread; other homes (hand-kept registries, release-json narratives, status-prose version claims) should DEFER to it pending the owner's §7 ruling. Concretely open under that ruling: the kit repo's own `substrate.config.json` pin (v1.0.0, self-adopt-era) vs its dist (v1.7.0) — surfaced as the registry's one DRIFT row, deliberately NOT hand-fixed this slice because what consumer-#0's pin *means* is the §7 question.

next (agent-available, NOT owner-gated — for the next session; queue owner = the coordinator, who may reorder — this list is the lane's best knowledge, not a lock):
- **Next coordinator slice (queued, UNCLAIMED — claim before building): release v1.7.1 + light distribution wave** — the [Unreleased] payload (#137: spurious-backup fix + gate carve-out protection + inbox-base gate wiring) is staged and byte-pin clean; cut the release per the release.yml workflow_dispatch path, then the light wave. THEN: program review §6.4 — one claims template + check_claims unified (spec: menno420/superbot docs/eap/eap-program-review-2026-07-10.md §6 item 4; §6.2 — generated repo roster — is manager-owned, not a kit lane).
- **B1 run-5 — UNBLOCKED by the F-5 ruling** (Reading A of record; the run itself was NOT part of the ORDER 011 slice). Fire per bench/README.md when a runner session picks it up; scored under Reading A only, no more dual-scoring.
- **§6.1 follow-on (rides the v1.7.1 distribution wave):** adopter repos with an installed substrate-gate.yml (gba-homebrew's hand-fixed copy included) receive the kit-owned regeneration on their next `bootstrap upgrade` — now WITH carve-out protection (#137): host additions are reported + banked, never silently dropped; the regenerated gate also wires the previously-latent `--inbox-base` enforcement.
- **T5 guard-probe redesign** — pin path, awaits a daytime `do-not-automerge` PR; re-scope against `docs/ideas/t5-headless-guard-surface-2026-07-09.md` first (run-4 partially resolved its premise).
- **legacy-alias job delete** (queue item 9) — unblocked only AFTER OWNER-ACTION 2's required-check swap.
- **B2/B3/B4 cross-repo sweeps** (queue item 12) — blocked on OWNER-ACTION 6 (read access).
- **SessionStart handoff-push idea** (run-4's 💡, top buildable per docs/gen2/next-boot.md § 0) + the ordinary-lane backlog in docs/ideas/.
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md.

notes: v1.7.1-payload close. Session shape: preflight (HEAD f0e6c85, no ORDER 012+ in the inbox), claim-first (#136 @ 7e600c6, fast lane, on main before build), born-red card + PR open FIRST (#137 armed at open, ~2 min after claim), build (Items 1–3 + CHANGELOG + 6 tests + dist rebuild), card flips complete as the deliberate last content commit (branch updated onto main first — the up-to-date requirement), this heartbeat as the close. Honest findings for the coordinator: (1) NEGATIVE FINDING (headline): the generated gate template never wired `--inbox-base` — inbox pure-append enforcement was latent on every adopter since the control band shipped; only the kit's own ci.yml enforced it. Fixed in #137; reaches adopters on the v1.7.1 upgrade wave. (2) NEGATIVE FINDING: docs/ carries no dedicated upgrade-recipe doc — the operative adopter recipe is ADOPTER_CHECKLIST in `src/build_release_json.py` (ships in every release's notes; now carries the carve-out relocation rule); founding plan §4.3 is historical. (3) The upgrade no longer banks the NEW dist at all (decided-and-flagged): the next upgrade's archive-first step banks it before any overwrite, so nothing is lost; the standalone-adopt bank still covers re-adopt flows. (4) Carve-out regen still OVERWRITES the gate (kit-owned by design) — it never auto-writes a new live workflow file (would breach the never-installs-CI-silently doctrine); relocation is a one-line adopter action from the banked copy. (5) Local `.substrate/guard-fires.jsonl` telemetry appends from this session's check runs were deliberately NOT committed (control-only heartbeat diff). Sibling heartbeats untouched; inbox untouched; bench pin paths untouched; K0 orientation budget untouched (no boot-doc words added; check --strict green).
