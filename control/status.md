# substrate-kit · status
updated: 2026-07-10T04:57:30Z
phase: gen-2 active — queue item 11 (`adopt --lane`, lane-aware adoption for SHARED repos) shipped via the claim ritual (#102 claim → #103 build); this close clears the claim
health: green (main green; full suite 813 passed, check --strict exit 0, dist byte-pin green at #103's final head cc304ae; squash b42c07d now main HEAD)
kit: v1.6.0 · check: green · engaged: yes
last-shipped: #103 (squash SHA b42c07d — queue item 11: `adopt --lane <name>`, the self-review G1 double-adoption fix, the scaffold half of the enforce-don't-exhort arc whose checker half shipped v1.4.0/ORDER 004. With `--lane` the seeded heartbeat plants as `control/status-<lane>.md` (never the singular file) and is declared in `substrate.config.json` → `heartbeat_files` — replacing the untouched default when no Project owns `control/status.md`, appending (never dropping a sibling lane) otherwise; empty list expands to the default first; `inbox.md`/`README.md` stay single and skip-if-exists; lane names validated (`[A-Za-z0-9][A-Za-z0-9_-]*`) BEFORE any write, refusal exit 2; planted-doc provenance hash recorded under the lane relpath; the planted control/README's multi-Project section now documents the one-command shape. 9 new tests (813 total); CHANGELOG [Unreleased] ### Added entry (MINOR); dist regenerated + byte-pinned. Field-verified end-to-end via the real dist CLI in a scratch repo: fresh lane adopt → `['control/status-mining.md']`, second lane joins → both listed + shared bus `kept:`, `--lane ../evil` → REFUSED exit 2. Session chain this lane: #102 (claim, control fast lane, merged in ~19 s) → #103 (build, born-red card → complete), both merged. Session card: .sessions/2026-07-10-adopt-lane.md.

OVERNIGHT LEDGER: the nine-PR overnight lane ledger (#84, #86–#92, #99) lives in the #100 close (.sessions/2026-07-10-gen2-final-close.md); sibling lanes the same night: #85 (B1 run-3), #94/#95 (run-2 follow-ups), #93/#96 (closes), #97/#98 (pr92-adopt + capability-xref), #102/#103 (this lane — adopt --lane).

blockers: none blocking. The agent self-merge-call classifier wall (mcp__github__merge_pull_request / enable_pr_auto_merge refused as "Merge Without Review") remains session-dependent — THIS lane's MCP enable_pr_auto_merge calls were PERMITTED tonight too (#102/#103), consistent with the #97/#98 lane; the repo's auto-merge-enabler.yml covers the refused case server-side (recipe in docs/CAPABILITIES.md append log, 2026-07-10). Carried coordination note for the claims band: the #100 close earlier tonight overwrote this file while a sibling's `claimed-by:` was still live and dropped the annotation — harmless that time (scopes never overlapped) but exactly the status-collision class the claim ritual exists to surface; closes should carry sibling lanes' live claims forward (this close checked: no sibling claim live at overwrite time — open PRs zero, orders line carried only this lane's now-cleared claim).

orders: acked=001,002,003,004,005,006,007,008,009 done=001,002,003,004,005,006,007,008,009 — standing-default + coordinator-relayed queue executed
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (ack landed on main 18:12Z via #65, before resuming, per the order)

NO new order ≥010 — inbox at HEAD (b42c07d) re-read this close: still ends at ORDER 009 (headers read `status: new` because only the manager flips them; diff inbox against this orders line — the gen-2 rule). The `claimed-by: queue-item-11-adopt-lane kit-lab-gen2 2026-07-10T04:40:47Z` claim (#102) is CLEARED — queue item 11 is done (#103 merged, b42c07d), claim completed per the control/README claim ritual.

⚑ needs-owner: OWNER-ACTION 1 (merge #26) and OWNER-ACTION 2 (merge #49) from an earlier status were RESOLVED and WITHDRAWN — both owner-ratified and still merged on main (#26 = commit 706190f; #49 = commit 6d6046b; both merged_by menno420, re-verified in the merge log this close). The remaining still-open owner actions carry forward below (numbering as in the #88-refresh renumbering); item 1 is the HOT one.

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
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); leave "Require branches to be up to date" OFF
WHY-IT-MATTERS: the legacy alias jobs cause ~35-minute queue stalls (~70 min lost in gen-1) purely to satisfy the old names.
UNBLOCKS: an agent deletes the two legacy-alias-* jobs next session; the queue-stall class ends.
VERIFIED-NEEDED: no agent path to rulesets exists — direct api.github.com HTTP is 403-blocked through the proxy (docs/CAPABILITIES.md wall) and the MCP toolset has no ruleset endpoint; Settings → Rules is owner-only UI. (Observed 2026-07-10: PRs went `behind` and needed a branch update before merging — "Require branches to be up to date" currently behaves as ON; the swap is a good moment to confirm that toggle too.)

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
UNBLOCKS: kit data in the merged console + the lab loop's B2/B3/B4 sweeps.
VERIFIED-NEEDED: repo visibility and credential minting are account-owner surfaces; the wall is captured verbatim in docs/CAPABILITIES.md — cross-repo get_file_contents returned "Access denied: repository … is not configured for this session" (2026-07-09, exact error quoted in the ledger).

⚑ OWNER-ACTION 7 — branch cleanup (lowest priority)
WHAT: Turn on auto-delete for merged branches, then delete the stale branches of already-closed PRs.
WHERE: Settings → General → Pull Requests → check "Automatically delete head branches"; then each closed PR's "Delete branch" button
HOW: one checkbox + click-throughs (the #26 and #49 branches can also be deleted — both PRs merged; the #94/#95 branches and this close's branch `claude/gen2-final-close-2026-07-10` add to the pile)
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
WHY-IT-MATTERS: one gen-2 lane's auto-mode classifier refused these calls as "Merge Without Review" (verbatim reason in docs/CAPABILITIES.md append log, 2026-07-10); the run-3 lane's calls were permitted the same night — the wall is session-dependent. The repo's auto-merge-enabler.yml covers the refused case server-side.
UNBLOCKS: nothing blocked — both paths land PRs today. This only removes the indirection; LOW priority.
VERIFIED-NEEDED: the classifier denial is verified verbatim (docs/CAPABILITIES.md, 2026-07-10); the permission grant is an owner console surface — no agent path to change auto-mode rules.

B1 RUN-3 RESULT (recorded on main via sibling lane #85; carried forward, NOT re-run this lane): strict-F-5 **FAIL** (advisory per KF-5, DISPUTED pending OWNER-ACTION 1) — M1 regressed on all pairs while ON wins M2 (T4 resumed from T2's card) + M3 (durable write-back) inside the 7k budget, zero unrecoverable errors; purposive Reading B would PASS. First KF-8 trend (family at 3 rows): the kit's cold-start benefit is consistent in KIND — ON wins M2+M3 in every run, always inside the 7k budget, zero unrecoverable errors — while scripted M1 goes to OFF in every clean measurement (runs 2–3), making the strict-F-5 headline 1 PASS / 2 FAIL. Both FAILs hang on the disputed "none regressing" wording (Reading B would make all three runs PASS-shaped); cross-run confounds (kit v1.0.0→v1.3.0→v1.6.0, fresh seeds, judge drift incl. run-3's judge=arm) mean the trend is the repeated per-measure pattern, not the raw numbers. KF-5: the NEXT release's notes must state this outcome.

next (agent-available, NOT owner-gated — for the next session):
- B1 run-4 / any run-3 re-run — heavyweight; its HEADLINE verdict is owner-gated on the F-5 ruling (OWNER-ACTION 1), so record-under-both-readings until ruled.
- bench model-identity capture — collect harvests arm_model from transcripts, record warns on judge==arm (the run-3 deviation class); idea lives in the B1 run-3 card.
- upgrade-apply-docs post-hoc-apply full mechanism — #92 shipped only the interim hint slice of the 4th upgrade-UX fix; the full mechanism idea is left `open`.
- remaining queue-state items not yet done: regeneration-lag checker (#39); T5 guard-probe redesign (pin-path `do-not-automerge` PR — owner-gated, an overnight session can't land it); post-P10 legacy-alias job deletion (owner-gated on OWNER-ACTION 2); the two overnight idea seeds from #79. `adopt --lane` is DONE (#103, this close); the OWNER-ACTION ↔ CAPABILITIES cross-reference advisory is DONE (#98). Fresh idea seeds from tonight's cards, unfiled: plain-adopt lane-drift advisory (#103 card — a plain adopt into a lane-shaped repo should nudge `--lane`); CAPABILITIES append-log format advisory (#98 card). Boot from docs/gen2/next-boot.md; queue truth in docs/gen2/queue-state.md (reconcile against the DONE items above — queue-state predates tonight).

notes: kit-lab gen-2 session close (adopt-lane lane). Claim ritual run end-to-end for the fourth time tonight: claim #102 (control fast lane, merged ~19 s) → build #103 (born-red card first commit, squash b42c07d — `adopt --lane` scaffold + 9 tests, 813 total green, check --strict exit 0, dist byte-pin regenerated + verified on final head cc304ae) → claim cleared here. The multi-Project convention is now end-to-end machine-shaped: checker (v1.4.0/ORDER 004) + scaffold (#103) — a second Project joining a SHARED repo is one command, closing the G1 double-adoption gap. The kit's own control/README.md documents the command (mirrored from the template, ORDER 003/004 precedent). This close write touches ONLY control/status.md; control/inbox.md and all pin paths untouched; no src/ change in this PR so dist needs no regen. Session card: .sessions/2026-07-10-adopt-lane.md.
