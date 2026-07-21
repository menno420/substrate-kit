# Self Improvement seat — heartbeat
updated: 2026-07-21T11:07:21Z
phase: v1.20.2 RELEASED (false-wall-checker clearing/exemption fix). Adopter re-vendoring wave complete: websites already merged; trading-strategy + superbot-next re-vendored (blocked only on genuine resident/governance lines); venture-lab blocked on the classifier-walled `upgrade` verb (escalated to fm owner-queue).
health: green
kit: v1.20.2 · check: green · engaged: yes
last-shipped: v1.20.2 (tag → commit 4712ebf; release run 29819484154; dist sha256 48ecd47…9ece6) via PRs #558, #559, #560, #561 (all merged). Passed a 4-round independent adversarial review.
blockers: none agent-side. Remaining wave items are genuine resident/governance content (residents' to fix) + the owner-gated `upgrade`-verb wall (⚑ escalated to fm).

## v1.20.2 — false-wall checker fix (RELEASED)
Fix to `check_no_false_walls` clearing/exemption logic (closes the weak-OR-strong cross-line reattachment class):
- **Cross-line bridge now gated on the wall phrase being QUOTED** — a repudiation on the previous line only bridges onto a wall on the current line when that wall phrase is quoted; bare cross-line reattachment no longer clears a genuine wall.
- **Clause-split on bare conjunctions** — clauses are split so a repudiation of one capability no longer clears a wall on a different conjunction-joined clause.
- **Generated-render path-gated exemption** — the generated-render exemption is scoped by path rather than matching everywhere.
- **False-wall exemptions ride the reason-required `apply_allowlist` seam** — every exemption now carries a reason through the allowlist path.
- Shipped across PRs #558 → #561 (all merged); tag v1.20.2 = commit 4712ebf; release run 29819484154; dist sha256 48ecd47…9ece6. Passed a 4-round independent adversarial review.

## ⚑ This completion-pass — coordinator decision, FLAGGED (reversible)
The wave PIVOTED from correcting adopter false-wall WORDING to fixing the checker itself, then re-vendoring. Rationale: per Q-0120 a red firing against correct evidence is the checker's bug, not the evidence's — so the durable fix is the checker, not per-adopter wording edits. Reversible: the owner or any resident may revert any adopter wording change independently.

## v1.20.2 re-vendoring wave — adopter distribution status
Re-vendored to v1.20.2 where applicable; remaining reds trace to genuine resident/governance content or the owner-gated `upgrade` wall — NOT checker false-positives.

| adopter | PR | state | notes |
|---|---|---|---|
| websites | #452 | MERGED | already landed; dropped from this pass |
| trading-strategy | #160 | re-vendored (commit f1c5284) | blocked on 3 GENUINE governance/resident lines: current-state.md:389 + CONSTITUTION.md:166 (owner governance) · review-queue.md:8 (resident live-queue note). NOT checker FPs. |
| superbot-next | #602 | re-vendored (commit 2755fdb) | blocked; all 4 CI reds trace to the same `check --strict` on current-state.md:97 (genuine wall) + :114 (two-line-quote FP-red). No independent product failure; resident fixes both → greens. |
| venture-lab | #282 | NOT re-vendored | kit `upgrade` verb is classifier-walled venture-lab-specifically (escalated to fm owner-queue). Needs a non-walled venue / owner permission rule, then reword-3 + allowlist-4 greens it. |

## Known limitation (pointer)
A legitimate repudiation whose wall quote SPANS a line break now FP-reds (safe direction — over-flags, never under-flags a real wall). Future-hardening idea logged: detect a quote opening on the wall line and closing on the next.

## Registry / docs
- Version truth is the generated registry + each repo's committed tree, never this `kit:` line (self-reports lag by design). The adopters.md rows reflect each adopter's main-branch tree (an open/blocked upgrade PR is not yet in the tree).

## Routine / trigger state (no writes this wake)
- ARMED (active failsafe, F-1): `trig_01194PdaWChtHGNKASURxdLx` "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session — the dead-man bridge. LEFT UNTOUCHED this wake.
- No routines armed/deleted; no trigger APIs called. ORDER 024 bars re-arming routines pending the per-seat reboot go.

## Baton (honest next-slice judgment)
The checker-fix wave is drained through v1.20.2. Honest next slice: WATCH the two re-vendored adopter PRs (trading-strategy #160, superbot-next #602) — their remaining reds are resident/governance lines the hub cannot fix without pushing to resident-owned content (barred by Q-0261.3). If they stay dormant, ESCALATE to the hub venue (fleet-manager) so the owner sees the stalled adoption. The venture-lab `upgrade`-verb wall is already owner-gated at the fm owner-queue.

## ⚑ FOR OWNER (standing set)

⚑ FOR OWNER — venture-lab `upgrade`-verb classifier wall (escalated to fm owner-queue)
  WHAT:   The kit `upgrade` verb is classifier-walled venture-lab-specifically, so venture-lab #282 could NOT be re-vendored to v1.20.2 this pass.
  WHERE:  fleet-manager owner-queue (escalated) — venture-lab lane.
  HOW:    run the re-vendor from a non-walled venue, OR add an owner permission rule that clears the verb for venture-lab; then reword-3 + allowlist-4 greens it.
  WHY:    the wall is venue/classifier-specific, not a kit defect — the same verb succeeds in the other adopter lanes.
  UNBLOCKS: venture-lab v1.20.2 re-vendor.
  RISK: ↩️ reversible. RECOMMENDATION: re-run from a non-walled venue.

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
  WHAT: superbot adopts substrate-kit as a PIN ONLY (substrate.config pin 1.0.0; no vendored dist, no `.substrate/` state) — so the dist-vendoring upgrade is genuinely N/A there; it was correctly skipped in this wave.
  WHERE: superbot/substrate.config.json (or equivalent pin), pin `1.0.0`.
  HOW: (A) bump the nominal pin to `1.20.2` for a truthful version label even though no dist is vendored; (B) leave pin-only and document superbot as intentionally non-vendoring (adoption = pin-nominal only).
  WHY: the pin currently reads 1.0.0 while the fleet is on 1.20.2 — a reader can't tell "deliberately pin-only" from "stale". A one-line decision removes the ambiguity.
  UNBLOCKS: honest fleet version truth for superbot.
  RISK: ↩️ reversible either way. RECOMMENDATION: **B — document pin-only** (superbot genuinely vendors no dist; a bumped pin with no dist would itself mislead). Answer: A (bump pin) / B (document pin-only).

Standing (full paste-ready blocks verbatim in git history of this file):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).

orders: acked=001-024 done=001-024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024); its work is DONE (PR #340). The inbox `status:` field is manager-owned — an order reading `status: new` while this file's `done=` covers it is DONE-and-awaiting-manager-flip, not open.
