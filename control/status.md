# substrate-kit · status
updated: 2026-07-09T20:11:00Z
phase: fleet rollout v1.6.0 COMPLETE — both active adopters ENGAGED on v1.6.0 (superbot-next#96 merged 9761db4: check --strict exit 0, 1124 tests green; websites#45 merged ab0995d: check --strict exit 0, 125 tests green; registry rows updated in docs/adopters.md); inbox drained (001–009 done); agent queue = the four upgrade-UX fixes filed from the rollout's field findings (docs/ideas/upgrade-*-2026-07-09.md, all ordinary-lane with guard recipes) then B1 run-3 (owner-blocked: #49 + F-5 ruling); owner queue unchanged (the 11 OWNER-ACTION items below). Carried claim stands untouched: gen-1 WIND-DOWN CLAIMED by kitlab-winddown-phase1 2026-07-09T19:55:47Z per the ORDER 007 claim-first ritual — this fleet-wrap heartbeat records rollout facts only and does not affect that claim. Prior state stands: ORDERS 007+008 DONE, v1.6.0 LIVE (release verified: tag + 3 assets, sha256 match), order-claiming convention planted, #50 verified terminal
health: green
kit: v1.6.0 · check: green · engaged: yes
last-shipped: #69 — ORDER 007 order-claiming convention + v1.6.0 cut (control-README.md.tmpl + local copy: "Claiming an order" 4-step ritual, claimed-by: orders-line annotation, claim expiry; CHANGELOG covers both bands, KF-5: no scored surface touched, run-2 stays run of record; suite 722); #68 — ORDER 008 owner-action quality band (OWNER-ACTION six REQUIRED fields incl. VERIFIED-NEEDED attempted-or-exact-wall; advisory checker check_owner_actions.py, never exit-affecting, both lanes; CONSTITUTION/collaboration doctrine; session-close "Owner asks" step; suite 707→721); #67 — ORDER 007+008 claim
blockers: none agent-side. Owner-gated: PR #26 (PL-011) + PR #49 (pin-path seed fix) — both one-click merges
orders: acked=001,002,003,004,005,006,007,008,009 done=001,002,003,004,005,006,007,008,009 claimed-by: gen1-wind-down kitlab-winddown-phase1 2026-07-09T19:55:47Z
PING-ACK ORDER 009 · discovered 2026-07-09T18:07:30Z · via mid-session inbox check (the ORDER 006 session re-read origin/main while babysitting build PR #63's merge and saw the #61/#64 inbox appends; ack landed on main 18:12Z via #65, before resuming, per the order)
⚑ needs-owner: 11 items, all in OWNER-ACTION form below (mirrors docs/retro/project-review-2026-07-09-kitlab-coordinator.md §e; ORDER 008 six-field standard). Dropped as stale this pass: the fleet-review #35 §5 carries — 3 cross-repo asks (superbot-next required-check, websites rules glance, cite-never-copy ruling) live in their home repos' heartbeats where the attempt/wall evidence is, and PL-010 (#22) ratify/veto is answered (docs/program/rulings.md records PL-010 status: decided; the standing veto right needs no list entry)

⚑ OWNER-ACTION 1 — merge PR #26 (PL-011 ratification)
WHAT: One click merges the PR that makes "an adoption is only done when it is actually working (ENGAGED)" official program law.
WHERE: <https://github.com/menno420/substrate-kit/pull/26> → "Merge pull request"
HOW: click only (veto = comment on the thread instead; a session then reverts the register note)
WHY-IT-MATTERS: without it, a repo can "adopt" the kit on paper and silently never work — both fresh adopters were found stranded exactly this way.
UNBLOCKS: PL-011 becoming citable program law fleet-wide.
VERIFIED-NEEDED: attempted twice — the auto-mode permission classifier refuses owner-gated merges on relayed consent (the #17 merge was DENIED until the owner typed "merge 17" live in-session; a later worker-spawn including "merge #26" was denied the same way — review §b audit row 23). Only a live owner click clears this class.

⚑ OWNER-ACTION 2 — merge PR #49 (benchmark seed fix)
WHAT: One click merges the fix for the bug that makes the benchmark's project generator produce broken code for some seeds.
WHERE: <https://github.com/menno420/substrate-kit/pull/49> → "Merge pull request"
HOW: click only (CI green, card complete; carries do-not-automerge by law, not by doubt)
WHY-IT-MATTERS: the benchmark — the only measurement of whether the kit actually helps — cannot run its third trial until this lands.
UNBLOCKS: B1 run-3 fires as soon as it merges; the result family reaches the KF-8 ≥3-row trend threshold.
VERIFIED-NEEDED: bench/seeds/ is a PIN PATH — the bench integrity law (check_bench_integrity.py rule 1: the lab never merges its own change to the oracle) forbids self-merge; the PR carries do-not-automerge from creation under that law.

⚑ OWNER-ACTION 3 — rubric F-5 wording ruling (A or B)
WHAT: Read two short paragraphs and answer with one letter — which reading of the benchmark pass/fail rule is the intended one.
WHERE: docs/ideas/rubric-f5-none-regressing-wording-2026-07-09.md
HOW: reply "A" (strict none-regressing) or "B" (7k-budget-purposive) in any channel
WHY-IT-MATTERS: the two readings produce OPPOSITE verdicts on the same run-2 evidence — the benchmark's headline result is currently disputed.
UNBLOCKS: run-3's verdict landing under a ruled reading instead of a disputed one.
VERIFIED-NEEDED: bench/rubric/ is a PIN PATH (same integrity law as item 2), and the idea file explicitly reserves the call ("Agents do not resolve this one") — it is product judgment on what the rubric MEANS; no agent attempt can substitute.

⚑ OWNER-ACTION 4 — P10 required-check swap
WHAT: Swap which CI check the main branch requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); leave "Require branches to be up to date" OFF
WHY-IT-MATTERS: the legacy alias jobs cause ~35-minute queue stalls (~70 min lost in gen-1) purely to satisfy the old names.
UNBLOCKS: an agent deletes the two legacy-alias-* jobs next session; the queue-stall class ends.
VERIFIED-NEEDED: no agent path to rulesets exists — direct api.github.com HTTP is 403-blocked through the proxy (docs/CAPABILITIES.md wall) and the MCP toolset has no ruleset endpoint; Settings → Rules is owner-only UI.

⚑ OWNER-ACTION 5 — P4 arm the daily lab loop
WHAT: Create the scheduled session that makes the lab run itself every morning.
WHERE: Console → kit repo environment → Schedules → New schedule
HOW: paste the fenced prompt from docs/operations/lab-loop.md § Arming verbatim · cron `0 6 * * *` (UTC) · fresh session per fire ON · Sonnet-class model · unrestricted-branch-push OFF · auto-fix PRs ON
WHY-IT-MATTERS: turns the lab from manually-fired sessions into the self-running daily loop the program is built around.
UNBLOCKS: D3 (the autonomous daily loop; needs ≥3 scheduled fires).
VERIFIED-NEEDED: the console Schedules pane is owner UI — routine/schedule creation is an enumerated wall in docs/CAPABILITIES.md ("owner-click actions in the console — queue them under ⚑ needs-owner"); no in-session API or MCP path exists.

⚑ OWNER-ACTION 6 — P5 create Railway project kit-lab
WHAT: Create a separate Railway project so the lab gets its own infrastructure lane.
WHERE: Railway console → New project
HOW: name `kit-lab` · region `europe-west4` · no spend caps (PL-005) · notification rule → HQ #railway-alerts; then put a project-scoped RAILWAY_TOKEN in the kit repo's environment
WHY-IT-MATTERS: the lab currently has no infra lane of its own; sharing production's is forbidden.
UNBLOCKS: the P6 console move (agent-built the moment the token exists).
VERIFIED-NEEDED: Railway project creation is owner console UI, and the ambient-IDs-are-production rule bars agents from touching the Railway IDs already present in the environment — both walls enumerated; no agent path.

⚑ OWNER-ACTION 7 — P8 confirm MIT
WHAT: Confirm the kit's license with one word.
WHERE: any channel
HOW: reply "MIT ok", or name a replacement license
WHY-IT-MATTERS: the kit ships to consumer repos with no declared license until this lands.
UNBLOCKS: closing the license ⚑ carried since KL-1.
VERIFIED-NEEDED: a license choice is a legal/product decision — owner judgment by nature; there is nothing for an agent to attempt.

⚑ OWNER-ACTION 8 — P11 public flip OR P13 read-only PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility. P13: github.com/settings/tokens → fine-grained PAT, read-only, consumer-repo scope, then add it to the fleet environments
HOW: P11 is click-through; P13 is create-token + paste into environment settings
WHY-IT-MATTERS: sibling repos cannot see kit data today, so the merged console and the loop's cross-repo sweeps run blind.
UNBLOCKS: kit data in the merged console + the lab loop's B2/B3/B4 sweeps.
VERIFIED-NEEDED: repo visibility and credential minting are account-owner surfaces; the wall is captured verbatim in docs/CAPABILITIES.md — cross-repo get_file_contents returned "Access denied: repository … is not configured for this session" (2026-07-09, exact error quoted in the ledger).

⚑ OWNER-ACTION 9 — branch cleanup (lowest priority)
WHAT: Turn on auto-delete for merged branches, then delete the ~25 stale branches of already-closed PRs.
WHERE: Settings → General → Pull Requests → check "Automatically delete head branches"; then each closed PR's "Delete branch" button (full branch list: review §e item 9)
HOW: one checkbox + click-throughs; KEEP the open PRs' branches (#26 claude/pl011-adoption-engaged, #49 claude/seed-fix-yield-keyword-2026-07-09)
WHY-IT-MATTERS: pure hygiene — ends the clutter class permanently; nothing functional waits on it.
UNBLOCKS: nothing functional; the checkbox prevents recurrence forever.
VERIFIED-NEEDED: branch deletion is 403 on EVERY agent path — git push :branch 403, REST 403, GraphQL deleteRef disabled, no MCP tool (review §b audit row 21; docs/CAPABILITIES.md "Branch deletion" wall). A full session attempted it and deleted zero.

⚑ OWNER-ACTION 10 — superbot upgrade decision
WHAT: Rule on superbot's kit pin — upgrade it or keep holding.
WHERE: any channel
HOW: recommendation (decide-and-flag): adopt at the next stable release in one hop — say nothing to accept, "upgrade now" or "hold pin-only" to override
WHY-IT-MATTERS: superbot's deliberate pin is now 6 releases behind (v1.0.0 vs v1.6.0) and the drift window keeps growing.
UNBLOCKS: the fleet's last non-ENGAGED adopter upgrading, whenever taken.
VERIFIED-NEEDED: the pin is a recorded owner decision (docs/adopters.md: "the v1.2.0+ upgrade is an owner decision") — agents don't overrule a deliberate stance; product judgment, not a technical wall.

⚑ OWNER-ACTION 11 — web-environment setup script paste
WHAT: Paste the corrected environment setup script so no more sessions die while starting up.
WHERE: Claude console → the environment's settings → "Setup script" field (owner-only dialog)
HOW: paste the guarded script from docs/environment-setup-script.md verbatim
WHY-IT-MATTERS: the current script already killed one session at provisioning (wrong cwd + hard-fail on a missing requirements.txt — PR #47 documents the casualty and the fix).
UNBLOCKS: reliable session starts in this environment. If you already pasted it, say so and this ask is withdrawn — agents cannot read the settings dialog to confirm either way.
VERIFIED-NEEDED: the environment settings dialog is owner-only console UI (docs/CAPABILITIES.md: environment configuration is an owner-click console action); the one confirmed provisioning casualty (PR #47) is the live evidence.

notes: ORDER 007+008 deviations (decide-and-flag, detailed in .sessions/2026-07-09-order007.md + -order008.md): (a) ONE v1.6.0 release covers both bands (both done-whens say "in a release"; the ORDER 004 ship-with-next-release precedent) — 008 built first as P1 via #68 without a bump, 007's #69 carried the cut; (b) the new owner-action checker is ADVISORY-only by design (a gate would pre-redden every adopter's free-text heartbeat on upgrade; migration by nag + close ritual per the order's "warning"); (c) DONE this session (control-only fast-lane PR): the ⚑ list is now fully OWNER-ACTION-structured — all 11 items carry the six fields, the self-advisory is cleared, and 4 stale carries were expired with cited reasons (see the ⚑ intro line); the click-by-click detail stays mirrored in review §e. (d) claim convention is doc-contract-only this release — a claim-aware checker (duplicate-claim + stale-claim advisory) is filed as the #69 card's session idea. Manager: v1.6.0's notes carry the adopter upgrade checklist; adopters inherit both bands on upgrade — BOTH active adopters have now walked it (superbot-next#96, websites#45). Manager relay item: websites' inbox ORDER 005 is genuinely unexecuted (/queue 404s live; websites#44 shipped only the P0 ping-ack for their ORDER 006) — needs a scoped websites session. Continuation without owner: claim-aware checker idea; OWNER-ACTION↔CAPABILITIES cross-reference idea (#68 card); B1 run-3 after #49; run-2 ordinary-lane follow-ups; T5 probe redesign; engagement-checker comment-leniency fix + inbox append-only checker (issue #36); telemetry write-at-card-commit + backfill (guard-fire rows from this session's local runs deliberately uncommitted, the #54 pattern). The coordinator keeps executing.
