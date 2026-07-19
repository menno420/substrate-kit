# Self Improvement seat — heartbeat
updated: 2026-07-19T01:01:04Z · phase: GSW-4 shipped this wake — the optional GitHub-API PR open→merge latency pass (`scripts/measure_pr_latency.py` + 12 pure tests) landed in PR #477, adding report §7 + the frozen latency JSON (`docs/reports/data/2026-07-19-grounded-skills-latency.json`, linked from `docs/operations/README.md`) to the grounded-skills report; GSW-1..4 are now ALL complete (the grounded-skills window run is fully done). Headline: fleet median open→merge latency 3.5→4.5 min (before n=1630 / after n=1768) — flat, confound-heavy, descriptive-only; all 12 roster repos returned data, zero nulls. 1808 pytest pass / 1 skipped. PR #477 born-red (session-card in-progress hold); flips complete as the last step.

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake — GSW-4 open→merge latency pass

Shipped GSW-4, the optional GitHub-API PR open→merge latency pass (the #247 §2 method the harness deliberately does not fake from git data). From-scratch `scripts/measure_pr_latency.py` (pure bucketing/percentile/aggregation logic separated from an isolated direct-egress GitHub-API fetch) + `tests/test_measure_pr_latency.py` (12 pure tests). Added report §7 (metric, reproduce command, two flagged method decisions, per-repo + fleet tables, descriptive-only interpretation) and a §4 note recording that the optional latency pass WAS run (previously an unrecorded, undeferred gap). Froze the data as `docs/reports/data/2026-07-19-grounded-skills-latency.json` (sha256 `c0fb65ba…8ebf59d`); marked GSW-4 SHIPPED in `docs/planning/2026-07-19-grounded-skills-window-run.md`; kept the `docs/operations/README.md` reachability link. Evidence: 1808 pytest pass / 1 skipped; all 12 roster repos returned data, zero nulls. PR #477 OPEN + BORN-RED (session-card in-progress hold); flips complete as the last step. No new routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).

**Prior wake (PR #476):** GSW-1..3 — the frozen harness `scripts/measure_grounded_skills.py --clone` ran once over full/non-shallow clones of the 12-repo roster, 4/4 spot-checks MATCH, before/after report published at `docs/reports/2026-07-19-grounded-skills-measurement.md` (frozen M1–M4 data `docs/reports/data/2026-07-19-grounded-skills-results.json`, linked from `docs/operations/README.md`). Merged 2026-07-19.
**Prior wake (PR #472):** B-2 — self-row registry-stamp automation (`adopters-self-row-stale` born-red gate + network-free `local_self_scan`/`restamp_self_row` wired into `scripts/cut_release.py`). Merged 2026-07-18.

## PR state

All seat-session PRs terminal MERGED through #476: #438–#443, #445, #451, #452, #455, #457, #459, #463, #464, #465, #466, #470, #471, #472 (B-2), #474 (B-3), #476 (GSW-1..3). Sibling lanes merged: #444, #446–#450, #453.

IN-FLIGHT: `claude/gsw-4-pr-latency` (PR #477) — GSW-4 open→merge latency pass. Adds `scripts/measure_pr_latency.py` + `tests/test_measure_pr_latency.py` (12 pure tests), report §7 + §4 note, frozen `docs/reports/data/2026-07-19-grounded-skills-latency.json`, GSW-4 marked SHIPPED in the planning doc. Full suite 1808 passed / 1 skipped. Landing path: **born-red session-card hold** — `kit-quality` stays red until `.sessions/2026-07-19-gsw-4-pr-latency.md` flips complete.

## Recently shipped (neutral pointer)

- PR #476 (prior wake): GSW-1..3 grounded-skills measurement — harness ran over full/non-shallow clones of the 12-repo roster (M4 valid), 4/4 PL-008 spot-checks MATCH, before/after report published + frozen M1–M4 data + reachability link. Merged 2026-07-19.
- PR #474 (prior wake): B-3 fast-lane head-prefix ⇄ enabler branch_patterns symmetry lint (advisory). Merged 2026-07-18.
- PR #472 (prior wake): B-2 self-row registry-stamp automation — `adopters-self-row-stale` born-red gate + network-free self-restamp wired into `scripts/cut_release.py`. Merged 2026-07-18.
- PR #470 (prior wake): B-1 guard-surface census — `src/engine/guards.py::WORKFLOW_JOB_CENSUS` (6 jobs) + `tests/test_guard_surface_census.py` pin the SET of enforcing guard surfaces. Merged 2026-07-18.
- v1.19.0 RELEASED + verified — tag v1.19.0, run 29656601475 success, sha256 three-way PASS, https://github.com/menno420/substrate-kit/releases/tag/v1.19.0

## Backlog — HONEST readout (carried)

**Buildable non-gated backlog is DRY.** GSW-1..4 + B-1/B-2/B-3 are all consumed. The remaining Part-B work is either **owner-gated** or **needs-planning** — no turnkey slice remains:
- Owner-gated: the 5 ⚑ FOR OWNER blocks below; the v1.19.0 adopter wave; the 23-proposal veto menu (`docs/planning/2026-07-16-overnight-veto-menu.md`).
- Needs-planning (no turnkey recipe): folded-gate-diff-aware-card · pinned-feed-contract · t5-headless-guard · control-board-kit-readiness-cell.
The next wake with owner-gated items cleared should scope one needs-planning item. This "buildable non-gated backlog dry; remaining work owner-gated or needs-planning" state is the honest, expected readout — not a stall. The seat idles on the 2h failsafe trigger between wakes.

## Routine / trigger state — corrected at the 2026-07-18 coordinator cutover

- CLOSED — 8 spent send_later pacemakers, deleted + verified absent:
  trig_01DSh245ykS6on7WJSyKKQVF · trig_01YSUJ5DAdJEqRrmjN1Lyqpz · trig_01EDx9xMNKeZJrKbeRDkPkPS · trig_01XehM57jw86FT171dT6bc45 · trig_01TwthJQVz8XcvBb3X5wqJsE · trig_019q5TcJj3fPQ4MooUYJpsFW · trig_01WyizzoLMAWg7HmooXQzVzX · trig_013zy1tRdjdYpRQZndRpdrBa
- ARMED (active failsafe, F-1): trig_01194PdaWChtHGNKASURxdLx "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session. This is the current dead-man bridge.
- DELETED at the 2026-07-18 coordinator cutover: trig_01BcfHTVwmwogjDycfmWBtt7 (the prior "Self Improvement failsafe wake", cron `21 */2 * * *`) — superseded by trig_01194PdaWChtHGNKASURxdLx above; do not expect to find or rebind it.
- Business cron: NO trigger named kit-lab exists in this account's trigger list (verified same pagination). The 06:00Z kit-lab daily runs owner-side; the successor should not expect to find or rebind it here.

## State

kit: v1.19.0
- **No-false-walls guard now enforced fleet-wide** (campaign #444–#450): the false "agents cannot merge" doctrine was removed from templates / rendered docs / the session-close skill, then re-defended by `tools/check_no_false_walls.py` (kit CI, full lane) + `src/engine/checks/check_no_false_walls.py` (runs in every adopter's `check --strict`). Sits under CHANGELOG `[Unreleased]` — folds into the next release.
- **Claims-only fast-lane guard now on BOTH surfaces**: kit's own `ci.yml` (PR #455) + generated adopter CI via `live_ci_workflow()` (PR #457). The guard-parity meta-test (`tests/test_guard_parity.py`, PR #459) fails CI on kit-vs-adopter guard drift.
- Registry (docs/adopters.md): CURRENT per `currency --check` (12 repos); the superbot-games row DRIFT is adopter-side self-report lag (owner-gated, no kit-only fix — folded into the v1.19.0 wave ask). Every adopter row reads stale until its own upgrade wave.
- `adopters-version-lag` (#441) + `adopters-stale` (calendar-age) advisories cover both staleness axes; `adopters-self-row-stale` (#472) reds CI when the kit's own self-row lags its version home.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); protocol docs/operations/grounded-skills-measurement.md; window RUN + published (GSW-1..4, PRs #476/#477).
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. **GSW-1..4 · grounded-skills window run — DONE.** GSW-1..3 (harness ran, 4/4 spot-checks MATCH, M1–M4 report published — PR #476) → GSW-4 (optional GitHub-API open→merge latency pass, report §7 + frozen latency JSON — PR #477, this wake). The grounded-skills window run is fully complete; all traps cleared (non-shallow clones, PL-008 spot-checks, reachability links, frozen+sha256-cited data).
2. **Next Part-B item is owner-gated or needs-planning** per `docs/planning/2026-07-19-grounded-skills-window-run.md` Part B — no turnkey slice remains. The next wake with owner-gated items cleared should scope one needs-planning item (folded-gate-diff-aware-card · pinned-feed-contract · t5-headless-guard · control-board-kit-readiness-cell).

**Baton: buildable non-gated backlog dry; everything remaining is owner-gated or needs-planning.** The seat idles on the 2h failsafe trigger between wakes.

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
- Grounded-skills measurement window ~2026-07-19..26 — CLOSED (measurement published 2026-07-19, PRs #476/#477).

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
