# Self Improvement seat — heartbeat
updated: 2026-07-18T18:11:22Z · phase: guard-parity meta-test PR #459 IN FLIGHT (kit-vs-adopter guard drift detector); baton: grounded-skills window opens 2026-07-19

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake — guard-parity meta-test

Built the guard-parity meta-test (baton #2 from the PR #457 wake): a stdlib-only kit test that fails CI when an enforcing `kit-quality` guard in `.github/workflows/ci.yml` has no mirrored counterpart in the GENERATED adopter CI (`src/engine/adopt.py` `live_ci_workflow()`), unless allowlisted as kit-only with a reason. Converts the kit-vs-adopter guard-drift class from a hand-queued baton (the #455/#457 gap) into an automatic red-CI signal. PR #459 is OPEN and BORN-RED (session card in-progress hold); owner reviews before the card flips complete + merge. No new routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).

## PR state

All seat-session PRs terminal MERGED: #438–#443, #445, #451, #452, #455, #457 (the adopter-propagation half of the claims-only guard). Sibling lanes merged: #444, #446–#450, #453.

IN-FLIGHT: `claude/guard-parity-meta-test` (PR #459) — adds `tests/test_guard_parity.py` (kit-vs-adopter guard-drift detector). Test-only, no `src/engine` edit → `dist/bootstrap.py` UNMODIFIED (no rebuild). Full suite 1765 pass / 1 skip. Landing path: **owner-reviewed** — the born-red card holds `kit-quality` red until the card flips complete. control/claims/ carries this session's own claim file (`claude-guard-parity-meta-test.md`, deleted at close).

## Recently shipped (neutral pointer)

- v1.19.0 version bump merged to main via PR #461; GitHub Release publishing via release.yml workflow_dispatch (verify_release + adopters regen in aftermath). The Release artifact is published post-merge, not yet at write time.
- PR #457 (prior wake): propagated the claims-only fast-lane guard into the generated adopter CI (`src/engine/adopt.py` `live_ci_workflow()`), mirroring the kit's own `ci.yml` guard from PR #455 — so adopter repos get the same #451 fast-lane-race protection. Docs: `docs/operations/auto-merge-guards.md` row 7.
- PR #455 (prior session): the kit-CI half — a red `kit-quality` step rejecting a `claude/*` work PR whose ENTIRE diff is only `control/claims/**`, while leaving `claim/*` standalone-claim PRs green.

## Backlog — HONEST readout (carried)

Buildable, non-gated backlog remains **thin**. This wake shipped the guard-parity meta-test queued as baton #2 by the PR #457 wake; no new order exists (none >024 at inbox@HEAD). Remaining rungs owner-gated / date-parked:
- Owner veto pass over the 23-proposal menu (docs/planning/2026-07-16-overnight-veto-menu.md) — baton #1 (owner).
- Grounded-skills measurement window opens 2026-07-19 (docs/operations/grounded-skills-measurement.md; owner silence accepts) — not yet (today is 2026-07-18).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period.
- v1.18.0 adopter wave: awaits owner authorization (⚑ below).
Seat idles on the 2h failsafe trigger between now and the earliest gated date.

## Routine / trigger state — corrected at the 2026-07-18 coordinator cutover

- CLOSED — 8 spent send_later pacemakers, deleted + verified absent:
  trig_01DSh245ykS6on7WJSyKKQVF · trig_01YSUJ5DAdJEqRrmjN1Lyqpz · trig_01EDx9xMNKeZJrKbeRDkPkPS · trig_01XehM57jw86FT171dT6bc45 · trig_01TwthJQVz8XcvBb3X5wqJsE · trig_019q5TcJj3fPQ4MooUYJpsFW · trig_01WyizzoLMAWg7HmooXQzVzX · trig_013zy1tRdjdYpRQZndRpdrBa
- ARMED (active failsafe, F-1): trig_01194PdaWChtHGNKASURxdLx "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session. This is the current dead-man bridge.
- DELETED at the 2026-07-18 coordinator cutover: trig_01BcfHTVwmwogjDycfmWBtt7 (the prior "Self Improvement failsafe wake", cron `21 */2 * * *`) — superseded by trig_01194PdaWChtHGNKASURxdLx above; do not expect to find or rebind it.
- Business cron: NO trigger named kit-lab exists in this account's trigger list (verified same pagination). The 06:00Z kit-lab daily runs owner-side; the successor should not expect to find or rebind it here.

## State

kit: v1.19.0
- **No-false-walls guard now enforced fleet-wide** (campaign #444–#450): the false "agents cannot merge" doctrine was removed from templates / rendered docs / the session-close skill, then re-defended by `tools/check_no_false_walls.py` (kit CI, full lane) + `src/engine/checks/check_no_false_walls.py` (runs in every adopter's `check --strict`). Sits under CHANGELOG `[Unreleased]` — folds into the next release.
- **Claims-only fast-lane guard now on BOTH surfaces**: kit's own `ci.yml` (PR #455) + generated adopter CI via `live_ci_workflow()` (PR #457). The two guard stacks were hand-kept in agreement; the guard-parity meta-test (`tests/test_guard_parity.py`, PR #459 in flight) now fails CI on kit-vs-adopter guard drift, replacing the hand-check with a red-CI signal (`docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md`).
- Registry (docs/adopters.md): CURRENT per `currency --check` (12 repos); the superbot-games row DRIFT is adopter-side self-report lag (owner-gated, no kit-only fix — folded into the v1.18.0 wave ask). Every adopter row reads stale until its own v1.18.0 upgrade wave.
- `adopters-version-lag` (#441) + `adopters-stale` (calendar-age) advisories cover both staleness axes.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); protocol docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. Grounded-skills measurement window opens 2026-07-19 — the first successor wake on/after that date should evaluate it (docs/operations/grounded-skills-measurement.md).
2. Guard-manifest idea (from PR #459's card) — a declarative manifest that BOTH `adopt.py`'s CI generator (`live_ci_workflow()`) AND the guard-parity meta-test (`tests/test_guard_parity.py`, PR #459) read as the single source of truth for the guard list, so adding a guard means editing one manifest instead of three places. Groom it down its lifecycle (file a `docs/ideas/*.md` entry → plan) as the next-highest-value rung from the thin backlog.

## ⚑ FOR OWNER (standing set carried forward)

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2318 entries paginated to exhaustion 2026-07-17; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
  WHERE:  docs/operations/lab-loop.md asserts it "stays armed across every cutover"; the registry has nothing to keep. The doc documents NO deliberate disarm — the loop is owner-armed-only (👤 P4, console Schedule) and cannot arm itself.
  HOW:    (A) RECREATE — owner arms a daily `0 6 * * *` UTC Schedule in the Claude Code console pointed at the kit-lab loop; (B) RETIRE — remove the "stays armed" line from lab-loop.md and mark the loop dormant-by-design pending reboot.
  WHY:    doctrine and reality contradict; a rebooted seat reads "armed" and trusts a loop that never runs. ORDER 024 also bars the seat from re-arming routines pending the per-seat reboot go, so it will not create the cron unilaterally.
  UNBLOCKS: honest lab-loop doctrine — either daily owner business resumes (A) or the false "armed" claim is removed (B).
  VERIFY: (A) the Schedule shows in the console trigger list and a 06:00Z run lands; (B) `grep -n "stays armed" docs/operations/lab-loop.md` returns nothing.
  RISK ↩️ reversible either way. RECOMMENDATION: **A — recreate** (lab-loop.md frames it as genuine daily owner business; retiring silently drops it over a transient cutover gap; re-arming is one console action gated on the reboot go). Answer: A (recreate) / B (retire).

⚑ v1.19.0 adopter-wave authorization
WHAT: authorize the v1.19.0 adopter-upgrade wave. (v1.19.0 now supersedes v1.18.0 as the wave target — v1.18.0 was never distributed.)
WHERE: the executing seat session, one live owner turn.
HOW: say 'run the v1.19.0 adopter wave'.
WHY: the seat session's permission classifier denied adopter-repo writes dispatched on coordinator relay alone (denial record verbatim: PR #420 body § "Denial routing"); owner provenance in the executing session is the unblock.
UNBLOCKS: ~15 adopter currency PRs to v1.19.0.
VERIFY: wave report with per-adopter PR list.
RISK: ↩️ reversible, distribution-only diffs.
  NOTE (superbot-games, carried from 2026-07-18 rung-2 re-verify): its DRIFT row is 1 genuine self-report lag + 2 consuming-lane false-positives. The wave clears the genuine half when superbot-games re-renders + re-stamps its own control/status.md v1.15.0→v1.19.0. The two consuming lanes (control/status-mining.md / control/status-exploration.md, v1.7.1 adoption-prose) will NOT clear on a version bump — their `kit:` lines are historical prose, not current claims; either reword them adopter-side, or (kit-side, NOT recommended) prune their tokens from docs/fleet-repos.txt at the cost of lane observability.

⚑ CAPABILITIES denial-record entry (parked)
WHAT: approve appending the 2026-07-16 adopter-wave denial finding to docs/CAPABILITIES.md in summarized form (finding + date + pointer to the PR #420 body for the verbatim record).
WHERE: the executing seat session, one live owner turn.
HOW: say 'record the adopter-wave denial in CAPABILITIES, summarized'.
WHY: the CAPABILITIES discovery rule wants attempted walls appended same-session; the seat parked the append pending owner direction on form/placement.
UNBLOCKS: the can/cannot ledger stays complete for the successor.
VERIFY: a dated docs/CAPABILITIES.md entry pointing at PR #420.
RISK: ↩️ reversible, docs-only.

⚑ P10 required-check swap
WHAT: Swap which CI check main requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks.
HOW: in the ruleset panel, remove the two legacy-alias check names, add `kit-quality`.
WHY: the two legacy-alias jobs are permanently-absent required checks that stall every PR's merge until the enabler/lander path clears them; kit-quality is the real check.
UNBLOCKS: deleting the two legacy-alias jobs; ends the queue-stall class.
VERIFY: next kit PR shows kit-quality as the only required check; agent then removes the alias jobs.
RISK: ↩️ reversible — re-add the old required checks in the same ruleset panel.

⚑ public-flip-or-PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility · P13: github.com/settings/tokens → fine-grained read-only PAT scoped to this repo, then add it to the fleet environments.
HOW: P11 is click-through; P13 is create-token + paste into environment settings.
WHY: sibling repos cannot read kit data today, so cross-repo sweeps and the merged console run blind.
UNBLOCKS: B2–B4 cross-repo sweeps + kit data in the merged console.
VERIFY: a sibling-seat session fetches a kit file read-only without "Access denied: repository … is not configured for this session".
RISK: ⚠️ P11 effectively irreversible (history exposed once public) · ↩️ P13 reversible — revoke anytime.

Standing (full paste-ready blocks verbatim in git history of this file @ 86d2a57):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

## 💡 Session idea (Q-0089)

**Guard-parity meta-test — kit-vs-adopter guard drift detector.** Add a kit test (or a kit-quality lint step) that asserts every *enforcing* guard step in `.github/workflows/ci.yml`'s `kit-quality` job has a mirrored counterpart in `src/engine/adopt.py` `live_ci_workflow()` — or an explicit `kit-only-by-design` allowlist entry. This session (PR #457) existed only because the claims-only guard shipped to the kit's own CI (PR #455) but not to the generated adopter CI, and nothing detected that drift until a human queued it as a baton. A parity check catches kit-vs-adopter guard drift automatically. Distinct from the added-vs-modified lane-parity meta-test in docs/planning/2026-07-16-overnight-veto-menu.md (two *lanes* of one surface); this asserts two *surfaces* share a guard set. Durable file: docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md. Small, test-only, reversible; not built this wake.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 claims-only-fastlane-guard wake (PR #455): genuine credit — it correctly added the enforcing guard to the kit's OWN `ci.yml` (`kit-quality` step "Claims-only fast-lane guard"), pinned it with a textual test, and documented it as guard-stack row 7 — closing the #451 card-less-merge race for the kit's own repo. Reasonable split, small miss: it scoped adopter propagation OUT as a follow-up baton item rather than shipping the kit-own gate and the generated adopter gate in one pass — a defensible "kit-own first, generated second" ordering, but it meant adopters ran without the guard for a window (which this PR #457 closed). System improvement it surfaces: the guard-parity meta-test above (💡) — a checker that keeps the kit-own and adopter-generated guard stacks from silently drifting, converting the "propagate it later" gap from a hand-queued baton into an automatic red-CI signal.

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
