# Self Improvement seat — heartbeat
updated: 2026-07-18T17:18:08Z · phase: SESSION-ENDER v3.7 — coordinator chain closed; failsafe bridge armed for successor; #451-race enabler-guard slice shipping

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake — SESSION-ENDER v3.7

Coordinator chain closed. Zero new routines armed at close. Failsafe dead-man bridge left armed for the successor (F-1 below).

## PR state

All seat-session PRs terminal MERGED: #438–#443, #445, #451, #452 (#451 was the claim-only fast-lane race artifact, completed by #452). Sibling lanes merged: #444, #446–#450, #453.

IN-FLIGHT: `claude/claims-only-fastlane-guard` (this session's PR) — the enabler-guard slice that CLOSES the #451 fast-lane race in CI: a red `kit-quality` step rejects a `claude/*` work PR whose ENTIRE diff is only `control/claims/**`, while leaving `claim/*` standalone-claim PRs green. Landing path: **lands-on-green (auto-merge armed)**. control/claims/ carries this session's own claim file (deleted at close).

## Backlog — HONEST readout (carried)

Buildable, non-gated backlog remains **thin**. This wake's work was verification + reconcile of the campaign (above); no new order exists (none >024 at inbox@HEAD) and no ripe kit-only build surfaced. Remaining rungs owner-gated / date-parked:
- Owner veto pass over the 23-proposal menu (docs/planning/2026-07-16-overnight-veto-menu.md) — baton #1.
- Grounded-skills measurement window opens ~2026-07-19 (docs/operations/grounded-skills-measurement.md; owner silence accepts) — not yet (today is 2026-07-18).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period.
- v1.18.0 adopter wave: awaits owner authorization (⚑ below).
Seat idles on the 2h failsafe trigger between now and the earliest gated date.

## Routine / trigger state — VERIFIED 2026-07-18 by exhaustive list_triggers pagination (2,492 triggers, 25 pages)

- CLOSED — 8 spent send_later pacemakers, deleted + verified absent:
  trig_01DSh245ykS6on7WJSyKKQVF · trig_01YSUJ5DAdJEqRrmjN1Lyqpz · trig_01EDx9xMNKeZJrKbeRDkPkPS · trig_01XehM57jw86FT171dT6bc45 · trig_01TwthJQVz8XcvBb3X5wqJsE · trig_019q5TcJj3fPQ4MooUYJpsFW · trig_01WyizzoLMAWg7HmooXQzVzX · trig_013zy1tRdjdYpRQZndRpdrBa
- ARMED (successor dead-man bridge, F-1): trig_01BcfHTVwmwogjDycfmWBtt7 "Self Improvement failsafe wake", cron `21 */2 * * *`, next fire 2026-07-18T16:21:00Z, bound to the coordinator session. Successor boot cutover rebinds-then-deletes.
- Business cron: NO trigger named kit-lab exists in this account's trigger list (verified same pagination). The 06:00Z kit-lab daily runs owner-side; the successor should not expect to find or rebind it here.

## State

kit: v1.18.0
- **No-false-walls guard now enforced fleet-wide** (campaign #444–#450): the false "agents cannot merge" doctrine was removed from templates / rendered docs / the session-close skill, then re-defended by `tools/check_no_false_walls.py` (kit CI, full lane) + `src/engine/checks/check_no_false_walls.py` (runs in every adopter's `check --strict`). Sits under CHANGELOG `[Unreleased]` — folds into the next release.
- Registry (docs/adopters.md): CURRENT per `currency --check` (12 repos); the superbot-games row DRIFT is adopter-side self-report lag (owner-gated, no kit-only fix — folded into the v1.18.0 wave ask). Every adopter row reads stale until its own v1.18.0 upgrade wave.
- `adopters-version-lag` (#441) + `adopters-stale` (calendar-age) advisories cover both staleness axes.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); protocol docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. Grounded-skills window opens 2026-07-19 — the first successor wake on/after that date should evaluate it.
2. Propagate the claims-only guard to ADOPTERS: the `claude/*`-claims-only reject now lives in the kit's own `ci.yml` (this session), but adopters' generated CI does not yet carry it — port it into `src/engine/adopt.py` `live_ci_workflow()`, rebuild `dist/bootstrap.py`, and pin it in `tests/test_adopt.py`. Kit-only, contained, reversible — the natural next rung. (SHIPPED this session: the kit-CI half — the #451-race enabler-guard on `claude/claims-only-fastlane-guard`.)

## ⚑ FOR OWNER (standing set carried forward)

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2318 entries paginated to exhaustion 2026-07-17; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
  WHERE:  docs/operations/lab-loop.md asserts it "stays armed across every cutover"; the registry has nothing to keep. The doc documents NO deliberate disarm — the loop is owner-armed-only (👤 P4, console Schedule) and cannot arm itself.
  HOW:    (A) RECREATE — owner arms a daily `0 6 * * *` UTC Schedule in the Claude Code console pointed at the kit-lab loop; (B) RETIRE — remove the "stays armed" line from lab-loop.md and mark the loop dormant-by-design pending reboot.
  WHY:    doctrine and reality contradict; a rebooted seat reads "armed" and trusts a loop that never runs. ORDER 024 also bars the seat from re-arming routines pending the per-seat reboot go, so it will not create the cron unilaterally.
  UNBLOCKS: honest lab-loop doctrine — either daily owner business resumes (A) or the false "armed" claim is removed (B).
  VERIFY: (A) the Schedule shows in the console trigger list and a 06:00Z run lands; (B) `grep -n "stays armed" docs/operations/lab-loop.md` returns nothing.
  RISK ↩️ reversible either way. RECOMMENDATION: **A — recreate** (lab-loop.md frames it as genuine daily owner business; retiring silently drops it over a transient cutover gap; re-arming is one console action gated on the reboot go). Answer: A (recreate) / B (retire).

⚑ v1.18.0 adopter-wave authorization
WHAT: authorize the v1.18.0 adopter-upgrade wave.
WHERE: the executing seat session, one live owner turn.
HOW: say 'run the v1.18.0 adopter wave'.
WHY: the seat session's permission classifier denied adopter-repo writes dispatched on coordinator relay alone (denial record verbatim: PR #420 body § "Denial routing"); owner provenance in the executing session is the unblock.
UNBLOCKS: ~15 adopter currency PRs to v1.18.0.
VERIFY: wave report with per-adopter PR list.
RISK: ↩️ reversible, distribution-only diffs.
  NOTE (superbot-games, carried from 2026-07-18 rung-2 re-verify): its DRIFT row is 1 genuine self-report lag + 2 consuming-lane false-positives. The wave clears the genuine half when superbot-games re-renders + re-stamps its own control/status.md v1.15.0→v1.18.0. The two consuming lanes (control/status-mining.md / control/status-exploration.md, v1.7.1 adoption-prose) will NOT clear on a version bump — their `kit:` lines are historical prose, not current claims; either reword them adopter-side, or (kit-side, NOT recommended) prune their tokens from docs/fleet-repos.txt at the cost of lane observability.

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

**Wall-freshness advisory — enforce the ">14d re-verify" doctrine on real walls.** The campaign's `check_no_false_walls` catches *false* walls; nothing yet catches *stale-but-real* ones. The protocol says walls must be quoted fresh and re-verified after 14 days, but that lives as an exhortation, not a check. Idea: a stdlib advisory that scans `docs/CAPABILITIES.md` wall entries for their dated/`LAST-VERIFIED` stamp and flags any real wall older than 14 days as due-for-re-verification (advisory, non-blocking — friction→guard, Q-0132/Q-0194). Turns "quote walls fresh" into an enforced nag so a stale 403-wall gets re-probed instead of trusted indefinitely. Distinct from `check_no_false_walls` (which asserts a wall is FALSE); this asserts a real wall is STALE. Low-priority / one-file build; not built this wake.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18T00:51Z rung-2 wake (DRIFT verdict #442 + trigger-id correction #443): genuine remark — it did the disciplined TRUTH-bar thing, catching that the failsafe trigger id carried in prior heartbeats (`trig_01Mw9yn9r21Bi5q19v7QcqjN`) was a carried-forward invention and correcting it against a live `list_triggers` audit, plus a clean document-not-act verdict on the superbot-games DRIFT. Small miss the tree exposed: it recorded a "backlog thin / no build" idle at 00:51Z, yet within hours six substantial PRs (#444–#450, the dewall campaign) landed from sibling sessions in the same lane — so the "backlog dry" readout was a per-session view, not a fleet view, and the heartbeat then lagged the tree ~9.5h until this wake reconciled it. System improvement it surfaces: a session that lands substantial work should touch the heartbeat (or the coordinator reconcile faster) so the seat ledger doesn't sit 9h behind main — the stateless-parallel cost is real, and the cheapest mitigation is exactly this kind of prompt reconcile pass.

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
