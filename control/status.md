# substrate-kit · status
updated: 2026-07-10T05:34:12Z
phase: NIGHT SUMMARY (gen-2 overnight run + night-cap, 2026-07-10 ~00:10–05:35Z) — the owner's morning read. OWNER CLICKS THAT STARTED IT: #26 (PL-011, now ratified law) + #49 (seed fix) merged ~00:10Z. WHAT LANDED (12 build PRs, every number verified against main at the night-cap): #84 walking skeleton · #85 B1 run-3 recorded (row 3, first KF-8 trend — strict-F-5 FAIL, DISPUTED pending your ruling) · #86 engagement-gate comment-leniency fix · #87 inbox append-only + ORDER-grammar checker (+#89 honest writer-identity note) · #90 claim-aware checker · #91 telemetry write-at-card-commit + backfill · #92 four upgrade-UX fixes (adopted via the #98 lane) · #95 run-2 follow-ups · #98 OWNER-ACTION↔CAPABILITIES xref advisory · #99 adopter-findings batch · #103 adopt --lane · #108 planted-gate sentinel fixes (visiting gba-homebrew Track B lane, claim #105) · night-cap #109 (queue-state/next-boot reconciled, CHANGELOG backfilled for 6 PRs that shipped without entries, current-state de-drifted, one idea groomed). Closes/claims: #80/#81/#88/#93/#94/#96/#97/#100/#101/#102/#104/#107. TESTS: 813 (previous status, at #103) → 814 green at the night-cap gate run; check --strict exit 0; dist byte-pin green. NEXT AGENT-REACHABLE WORK: **queue dry** — T5 guard-probe redesign awaits a daytime do-not-automerge PR (pin path); everything else is owner-gated (the ⚑ list below). THE HOT ONE: OWNER-ACTION 1, the F-5 A/B ruling — one letter gates 2 of 3 recorded bench verdicts AND the trend headline.
health: green (main green at 9d8140e; suite 814 passed, check --strict exit 0, dist byte-pin green at #109's final head 90732cd)
kit: v1.6.0 · check: green · engaged: yes
last-shipped: #109 (squash 9d8140e — gen-2 night-cap: docs/gen2/queue-state.md reconciled per-item against the merge log (9/12 agent-queue items DONE with verified PR numbers; the 3 remaining carry exact gates), next-boot.md de-staled (OWNER-ACTION renumber, KF-8 threshold MET), CHANGELOG [Unreleased] backfilled for #86/#87+#89/#90/#91/#92/#99, current-state.md drift fixed (stale #17 owner gate removed, overnight ship block added, boot-read set trimmed back under the 7000-word orientation budget), CAPABILITIES append: armed auto-merge does NOT fire on a `behind` PR (live-hit #107; recipe: check mergeable_state first, merge origin/main, push), and the #103 card-only idea filed as docs/ideas/plain-adopt-lane-drift-advisory-2026-07-10.md. Session card: .sessions/2026-07-10-nightcap-docs-reconcile.md)
blockers: none blocking. Coordination notes carried: (1) the self-merge classifier wall stays session-dependent — this lane's enable_pr_auto_merge calls were PERMITTED (#107/#109), the enabler workflow remains the server-side backstop; (2) "Require branches to be up to date" behaves as ON — #107 stalled `behind` with green checks until a branch update (recorded in CAPABILITIES + OWNER-ACTION 2); (3) sibling lane status file control/status-gba-homebrew-trackb.md is live (visiting Track B lane, its build #108 merged) — this file's overwrite touches ONLY control/status.md, per the one-writer rule.

OVERNIGHT LEDGER: the nine-PR overnight lane ledger (#84, #86–#92, #99) lives in the #100 close (.sessions/2026-07-10-gen2-final-close.md); sibling lanes the same night: #85 (B1 run-3), #94/#95 (run-2 follow-ups), #93/#96 (closes), #97/#98 (pr92-adopt + capability-xref), #102/#103 (adopt --lane), #105/#108 (visiting gba-homebrew Track B), #107/#109 (this night-cap). Queue truth reconciled in docs/gen2/queue-state.md (the night-cap made it current — a fresh session can boot from it directly).

orders: acked=001,002,003,004,005,006,007,008,009 done=001,002,003,004,005,006,007,008,009 — standing-default + coordinator-relayed queue executed
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

NO new order ≥010 — inbox at HEAD (9d8140e) re-read this close: still ends at ORDER 009 (headers read `status: new` because only the manager flips them; diff inbox against this orders line — the gen-2 rule). The `claimed-by: nightcap-docs-reconcile-groom kit-lab 2026-07-10T05:05:00Z` claim (#107) is CLEARED — the night-cap shipped (#109 merged, 9d8140e), claim completed per the control/README claim ritual.

⚑ needs-owner: ten items below, all six-field. Item 1 is the HOT one — everything else is steady-state.

⚑ OWNER-ACTION 1 — rubric F-5 wording ruling (A or B) — HOT: gates the recorded B1 run-2/run-3 verdicts and the first KF-8 trend headline
WHAT: Read two short paragraphs and answer with one letter — which reading of the benchmark pass/fail rule is the intended one.
WHERE: docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md
HOW: reply "A" (strict none-regressing) or "B" (7k-budget-purposive) in any channel
WHY-IT-MATTERS: the two readings produce OPPOSITE verdicts on the same evidence — run-2 AND run-3 are strict-Reading-A FAILs that Reading B would flip to PASS; the benchmark's entire 1-PASS/2-FAIL headline is one letter away.
UNBLOCKS: run-4 landing under a ruled reading instead of a disputed one; honest KF-5 release notes.
VERIFIED-NEEDED: bench/rubric/ is a PIN PATH (bench integrity law); the idea file explicitly reserves the call ("Agents do not resolve this one") — product judgment on what the rubric MEANS; no agent attempt can substitute.

⚑ OWNER-ACTION 2 — P10 required-check swap
WHAT: Swap which CI check the main branch requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); set "Require branches to be up to date" OFF
WHY-IT-MATTERS: the legacy alias jobs cause ~35-minute queue stalls (~70 min lost in gen-1) purely to satisfy the old names; and the up-to-date requirement stalled another green PR tonight (#107 sat `behind` 10+ min with all checks passed until a branch update — now a recorded CAPABILITIES wall+recipe).
UNBLOCKS: an agent deletes the two legacy-alias-* jobs next session (queue item 9); the queue-stall class ends; fast-lane PRs stop paying an update round-trip whenever a sibling merges first.
VERIFIED-NEEDED: no agent path to rulesets exists — direct api.github.com HTTP is 403-blocked through the proxy (docs/CAPABILITIES.md wall) and the MCP toolset has no ruleset endpoint; Settings → Rules is owner-only UI.

⚑ OWNER-ACTION 3 — P4 arm the daily lab loop
WHAT: Create the scheduled session that makes the lab run itself every morning.
WHERE: Console → kit repo environment → Schedules → New schedule
HOW: paste the fenced prompt from docs/operations/lab-loop.md § Arming verbatim · cron `0 6 * * *` (UTC) · fresh session per fire ON · Sonnet-class model · unrestricted-branch-push OFF · auto-fix PRs ON
WHY-IT-MATTERS: turns the lab from manually-fired sessions into the self-running daily loop the program is built around.
UNBLOCKS: D3 (the autonomous daily loop; needs ≥3 scheduled fires).
VERIFIED-NEEDED: the console Schedules pane is owner UI — routine/schedule creation is an enumerated wall in docs/CAPABILITIES.md; no in-session API or MCP path exists.

⚑ OWNER-ACTION 4 — P5 create Railway project kit-lab
WHAT: Create a separate Railway project so the lab gets its own infrastructure lane.
WHERE: Railway console → New project
HOW: name `kit-lab` · region `europe-west4` · no spend caps (PL-005) · notification rule → HQ #railway-alerts; then put a project-scoped RAILWAY_TOKEN in the kit repo's environment
WHY-IT-MATTERS: the lab currently has no infra lane of its own; sharing production's is forbidden.
UNBLOCKS: the P6 console move (agent-built the moment the token exists).
VERIFIED-NEEDED: Railway project creation is owner console UI, and the ambient-IDs-are-production rule bars agents from touching the Railway IDs already present in the environment — both walls enumerated; no agent path.

⚑ OWNER-ACTION 5 — P8 confirm MIT
WHAT: Confirm the kit's license with one word.
WHERE: any channel
HOW: reply "MIT ok", or name a replacement license
WHY-IT-MATTERS: the kit ships to consumer repos with no declared license until this lands.
UNBLOCKS: closing the license ⚑ carried since KL-1.
VERIFIED-NEEDED: a license choice is a legal/product decision — owner judgment by nature; there is nothing for an agent to attempt.

⚑ OWNER-ACTION 6 — P11 public flip OR P13 read-only PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility. P13: github.com/settings/tokens → fine-grained PAT, read-only, consumer-repo scope, then add it to the fleet environments
HOW: P11 is click-through; P13 is create-token + paste into environment settings
WHY-IT-MATTERS: sibling repos cannot see kit data today, so the merged console and the loop's cross-repo sweeps run blind.
UNBLOCKS: kit data in the merged console + the lab loop's B2/B3/B4 sweeps (queue item 12).
VERIFIED-NEEDED: repo visibility and credential minting are account-owner surfaces; the wall is captured verbatim in docs/CAPABILITIES.md — cross-repo get_file_contents returned "Access denied: repository … is not configured for this session" (2026-07-09, exact error quoted in the ledger).

⚑ OWNER-ACTION 7 — branch cleanup (lowest priority)
WHAT: Turn on auto-delete for merged branches, then delete the stale branches of already-closed PRs.
WHERE: Settings → General → Pull Requests → check "Automatically delete head branches"; then each closed PR's "Delete branch" button
HOW: one checkbox + click-throughs (tonight added ~8 more merged branches to the pile: the overnight lanes' + #105/#107/#109's)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path — git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool (docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 8 — superbot upgrade decision
WHAT: Rule on superbot's kit pin — upgrade it or keep holding.
WHERE: any channel
HOW: recommendation (decide-and-flag): adopt at the next stable release in one hop — say nothing to accept, "upgrade now" or "hold pin-only" to override
WHY-IT-MATTERS: superbot's deliberate pin is now 6 releases behind (v1.0.0 vs v1.6.0) and the drift window keeps growing.
UNBLOCKS: the fleet's last non-ENGAGED adopter upgrading, whenever taken.
VERIFIED-NEEDED: the pin is a recorded owner decision (docs/adopters.md: "the v1.2.0+ upgrade is an owner decision") — agents don't overrule a deliberate stance; product judgment, not a technical wall.

⚑ OWNER-ACTION 9 — web-environment setup script paste
WHAT: Paste the corrected environment setup script so no more sessions die while starting up.
WHERE: Claude console → the environment's settings → "Setup script" field (owner-only dialog)
HOW: paste the guarded script from docs/environment-setup-script.md verbatim (gen-2 variant: docs/gen2/setup.sh)
WHY-IT-MATTERS: the current script already killed one session at provisioning (wrong cwd + hard-fail on a missing requirements.txt — PR #47 documents the casualty and the fix).
UNBLOCKS: reliable session starts in this environment. If you already pasted it, say so and this ask is withdrawn — agents cannot read the settings dialog to confirm either way.
VERIFIED-NEEDED: the environment settings dialog is owner-only console UI (docs/CAPABILITIES.md: environment configuration is an owner-click console action); the one confirmed provisioning casualty (PR #47) is the live evidence.

⚑ OWNER-ACTION 10 — (informational, low priority) optional self-merge permission rule
WHAT: Optionally grant a permission rule so future sessions can self-merge PRs directly, instead of relying on the auto-merge-enabler workflow.
WHERE: Claude console → the environment's permission/auto-mode settings
HOW: allow `mcp__github__merge_pull_request` / `mcp__github__enable_pr_auto_merge` for this environment's sessions
WHY-IT-MATTERS: one gen-2 lane's auto-mode classifier refused these calls as "Merge Without Review" (verbatim reason in docs/CAPABILITIES.md append log, 2026-07-10); the night-cap lane's calls were permitted the same night — the wall is session-dependent. The repo's auto-merge-enabler.yml covers the refused case server-side.
UNBLOCKS: nothing blocked — both paths land PRs today. This only removes the indirection; LOW priority.
VERIFIED-NEEDED: the classifier denial is verified verbatim (docs/CAPABILITIES.md, 2026-07-10); the permission grant is an owner console surface — no agent path to change auto-mode rules.

B1 RUN-3 RESULT (recorded on main via #85; carried forward): strict-F-5 **FAIL** (advisory per KF-5, DISPUTED pending OWNER-ACTION 1) — M1 regressed on all pairs while ON wins M2 (T4 resumed from T2's card) + M3 (durable write-back) inside the 7k budget, zero unrecoverable errors; purposive Reading B would PASS. First KF-8 trend (family at 3 rows): ON wins M2+M3 in every run, always in-budget, zero unrecoverable errors; scripted M1 goes to OFF in every clean measurement — strict headline 1 PASS / 2 FAIL, both FAILs hanging on the disputed wording (Reading B would make all three PASS-shaped); cross-run confounds (kit version, seeds, judge drift incl. run-3's judge=arm) mean the trend is the repeated per-measure pattern, not the raw numbers. KF-5: the NEXT release's notes must state this outcome.

next (agent-available, NOT owner-gated — for the next session):
- **Queue dry.** T5 guard-probe redesign awaits a daytime `do-not-automerge` PR (pin path — an autonomous session cannot land it; open it READY + labeled and leave the click to the owner); the rest of the remaining queue is owner-gated (items 9/12 on OWNER-ACTION 2 and 4/6).
- Ordinary-lane backlog if a session wants work: the groomed `docs/ideas/` backlog — top picks: plain-adopt lane-drift advisory (filed tonight, quick-win), orientation-budget headroom advisory (#109 card idea, unfiled), `--apply-docs` full post-hoc-apply mechanism, `bootstrap heartbeat` verb, bench model-identity capture (run-3 card idea).
- B1 run-4 — heavyweight; record-under-both-readings until OWNER-ACTION 1 is ruled.
- Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md (RECONCILED at the night-cap — current as of 9d8140e).

notes: night-cap close (docs-reconcile + groom lane, claim #107 → build #109, both merged; claim cleared above). This overwrite touches ONLY control/status.md; inbox and pin paths untouched. Sibling lane heartbeat control/status-gba-homebrew-trackb.md is live and untouched (one writer per file); its #105 claim's build (#108) is merged — that lane clears its own claim. Discrepancy check vs the coordinator's overnight brief: none material; nuances recorded on the #109 card (⚑ flag 2). Session card: .sessions/2026-07-10-nightcap-docs-reconcile.md.
