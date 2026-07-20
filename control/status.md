# Self Improvement seat — heartbeat
updated: 2026-07-20T07:45:00Z
phase: v1.20.1 shipped + adopter-distribution wave complete (fm ORDER 048). Detector follow-ups P2+P3 (#549's card) built + landing as PR #555. Wave: gba-homebrew merged; 8 adopter upgrade PRs open in resident lanes (all red only on resident-owned content); superbot pin-only (flagged).
health: green
kit: v1.20.1 · check: green (except this session's by-design born-red card HOLD) · engaged: yes
last-shipped: #549/#550 v1.20.1 patch (detector attachment-based clearing + release); #555 (P2/P3 hardenings) landing on green.
blockers: none agent-side. Remaining wave completion is resident-side merge of the 8 open upgrade PRs; owner-gated ⚑ set below.

## This session — PR #555 (P2 + P3 detector hardenings)
The two NON-BLOCKING follow-ups recorded in #549's card, both built + mutation-pinned:
- **P2 — wrapped-lookback punctuation-gated bleed.** `is_cleared`'s one-line wrapped lookback could bridge a repudiation from the previous line's trailing clause onto a wall on the current line even when that clause repudiated a DIFFERENT capability. Added a `_capability_families` gate: the lookback bridges only when the prev clause names the SAME family as the wall (or names none — a genuine continuation). Merge wall no longer cleared by a push repudiation.
- **P3 — `match_blocklist` one-hit-per-line masking.** Clearing was graded on only the first blocklist hit per line, masking a genuine wall sharing a line with a repudiated `false "…"` quote. Added `match_blocklist_all` (all matches + spans); `scan_text` grades each independently and reports the first uncleared (≤1 finding/line preserved). Clearing is now position-aware (a `false "…"` quote clears only the match its span covers).
- Engine source + `dist/bootstrap.py` rebuilt (currency green) + `tests/test_check_no_false_walls_leg.py` (mutation-pinned both directions). Full suite **2060 passed, 1 skipped**; `check --strict` clean except the born-red card HOLD.
- CI note: on PR #555 the checks named `Kit test suite` + `Cold-adoption smoke (adopt + check --strict)` are TEMPORARY legacy-context ALIAS jobs (ci.yml §362-399) that `needs: kit-quality` and conclude failure whenever kit-quality ≠ success. The real suite + cold-adopt smoke run as STEPS inside kit-quality. All three reds trace to the single born-red session-gate HOLD and clear at card flip — not independent failures.

## v1.20.1 adopter-distribution wave — LIVE state (checked 2026-07-20T07:40Z via per-PR MCP get)
All upgrades 1.17.0 → 1.20.1; each PR = kit-distribution files only (host workflows / control / settings / hooks untouched). Every red is on RESIDENT-owned content (the v1.20.1 false-wall gate catching resident-authored walls, or the repo's own product CI) — NOT kit-distribution content, and NOT a wave defect. No resident (non-agent) activity on any (all single-commit agent PRs, updated_at == created_at). Per Q-0261.3 these PRs are the resident lanes' to merge; the hub does NOT push to them.

| adopter | PR | state | CI | red-on-resident? | resident-activity? |
|---|---|---|---|---|---|
| gba-homebrew | #211 | MERGED | green | n/a | n/a |
| idea-engine | #740 | open | substrate-gate RED | yes — CAPABILITIES.md:139/:149 (dated incident, no inline date) | none |
| superbot-next | #602 | open | substrate-gate + tests/checkers/code-quality RED | yes — current-state.md:97/:114 + repo's own product CI | none |
| websites | #452 | open | quality RED | yes — resident docs false-walls (backlog.md:924, OWNER-ACTIONS.md:173/187/481, seat-digest.md:48) | none |
| trading-strategy | #160 | open | substrate-gate RED (pytest green) | yes — current-state.md:389, review-queue.md:8, CONSTITUTION.md:166 | none |
| superbot-games | #183 | open | substrate-gate + tests RED | yes — current-state.md:102, gen2…:73 + resident test pins OLD kit wording | none |
| venture-lab | #282 | open | substrate-gate RED (24 others green) | yes — 9 resident-doc false-walls (NEXT-TASKS.md:208, conventions.md:26, launch/*, operations/*) | none |
| superbot-mineverse | #138 | open | substrate-gate RED (pytest green) | yes — NEXT-TASKS.md:26, decisions.md:39 | none |
| fleet-manager | #390 | open | substrate-gate RED (freshness green) | yes — 39 resident/hub-owned false-walls across docs/ + CONSTITUTION.md:88 | none |
| superbot | — | skip | n/a | pin-only nominal adoption (pin 1.0.0; no vendored dist / .substrate) — dist-vendoring upgrade N/A; owner ⚑ below | n/a |
| pokemon-mod-lab | — | DARK (private) | unknown | adoption UNKNOWN — skipped | n/a |

## Registry / docs
- Version truth is the generated registry + each repo's committed tree, never this `kit:` line (self-reports lag by design). The adopters.md rows reflect each adopter's main-branch tree (still pre-upgrade for the 8 open PRs — an open PR is not in the tree).

## Routine / trigger state (no writes this wake)
- ARMED (active failsafe, F-1): `trig_01194PdaWChtHGNKASURxdLx` "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session — the dead-man bridge. LEFT UNTOUCHED this wake.
- No routines armed/deleted; no trigger APIs called. ORDER 024 bars re-arming routines pending the per-seat reboot go.

## Baton (honest next-slice judgment)
Agent-buildable kit slices are drained through v1.20.1 + #555. The honest next slice is: land #555 on green, then WATCH the 8 open adopter PRs — they are resident-lane merges the hub cannot make. If residents stay dormant (no merge / no resident activity across the next wake or two), ESCALATE to the hub venue (fleet-manager) so the owner sees the stalled adoption, rather than the hub silently pushing to resident-owned PRs (barred by Q-0261.3). Remaining non-resident work is owner-gated (⚑ below).

## ⚑ FOR OWNER (standing set)

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2318 entries paginated to exhaustion 2026-07-17; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
  WHERE:  docs/operations/lab-loop.md asserts it "stays armed across every cutover"; the registry has nothing to keep. The doc documents NO deliberate disarm — the loop is owner-armed-only (👤 P4, console Schedule) and cannot arm itself.
  HOW:    (A) RECREATE — owner arms a daily `0 6 * * *` UTC Schedule in the Claude Code console pointed at the kit-lab loop; (B) RETIRE — remove the "stays armed" line from lab-loop.md and mark the loop dormant-by-design pending reboot.
  WHY:    doctrine and reality contradict; a rebooted seat reads "armed" and trusts a loop that never runs. ORDER 024 also bars the seat from re-arming routines pending the per-seat reboot go, so it will not create the cron unilaterally.
  UNBLOCKS: honest lab-loop doctrine — either daily owner business resumes (A) or the false "armed" claim is removed (B).
  VERIFY: (A) the Schedule shows in the console trigger list and a 06:00Z run lands; (B) `grep -n "stays armed" docs/operations/lab-loop.md` returns nothing.
  RISK: ↩️ reversible either way. RECOMMENDATION: **A — recreate**. Answer: A (recreate) / B (retire).

⚑ FOR OWNER — public-flip-or-PAT (pick one)
  WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
  WHERE: P11: Settings → General → Danger Zone → Change visibility · P13: github.com/settings/tokens → fine-grained read-only PAT scoped to this repo, then add it to the fleet environments.
  HOW: P11 is click-through; P13 is create-token + paste into environment settings.
  WHY: sibling repos cannot read kit data today, so cross-repo sweeps and the merged console run blind.
  UNBLOCKS: B2–B4 cross-repo sweeps + kit data in the merged console.
  VERIFY: a sibling-seat session fetches a kit file read-only without "Access denied: repository … is not configured for this session".
  RISK: ⚠️ P11 effectively irreversible (history exposed once public) · ↩️ P13 reversible — revoke anytime. RECOMMENDATION: **B — mint a read-only PAT** (reversible; no history exposure).

⚑ FOR OWNER — t5-headless-guard fix (owner-review: pin-path PR #552 OPEN, awaiting owner merge)
  STATUS: PR opened, awaiting owner review — https://github.com/menno420/substrate-kit/pull/552 (do-not-automerge; green; the additive shape-2 guard-observability edit to bench/tasks/T5.md). OWNER'S LANE — the agent does NOT touch it.
  WHAT: fix the T5 bench probe so it produces a real in-session guard fire in the ON arm (shape 2 — check-driven guards; no hook-honoring harness rebuild needed).
  WHY: without it, T5 scores all guard items n/a — the ON arm demonstrates nothing over the unguarded baseline.
  VERIFY: a T5 run produces ≥1 real in-session guard fire (or a recorded deliberate violation) in the ON arm.
  RISK: ⚠️ pin-path oracle change → lands via a `do-not-automerge` owner-review PR (never auto-merged). Detail: docs/planning/2026-07-19-needs-planning-recipes.md §4.

⚑ FOR OWNER — superbot pin-bump: bump nominal pin, or leave as pin-only? (question)
  WHAT: superbot adopts substrate-kit as a PIN ONLY (substrate.config pin 1.0.0; no vendored dist, no `.substrate/` state) — so the v1.20.1 dist-vendoring upgrade is genuinely N/A there; it was correctly skipped in this wave.
  WHERE: superbot/substrate.config.json (or equivalent pin), pin `1.0.0`.
  HOW: (A) bump the nominal pin to `1.20.1` for a truthful version label even though no dist is vendored; (B) leave pin-only and document superbot as intentionally non-vendoring (adoption = pin-nominal only).
  WHY: the pin currently reads 1.0.0 while the fleet is on 1.20.1 — a reader can't tell "deliberately pin-only" from "stale". A one-line decision removes the ambiguity.
  UNBLOCKS: honest fleet version truth for superbot.
  RISK: ↩️ reversible either way. RECOMMENDATION: **B — document pin-only** (superbot genuinely vendors no dist; a bumped pin with no dist would itself mislead). Answer: A (bump pin) / B (document pin-only).

Standing (full paste-ready blocks verbatim in git history of this file):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).

orders: acked=001-024 done=001-024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024); its work is DONE (PR #340). The inbox `status:` field is manager-owned — an order reading `status: new` while this file's `done=` covers it is DONE-and-awaiting-manager-flip, not open.
