# Self Improvement seat — heartbeat
updated: 2026-07-19T00:28:53Z · phase: grounded-skills window GSW-1..3 ran this wake — the frozen harness `scripts/measure_grounded_skills.py --clone` ran once over full/non-shallow clones of the 12-repo roster (M4 `shallow:false` on every repo), and 4/4 spot-checks MATCH against git/source ground truth. The before/after report is published at `docs/reports/2026-07-19-grounded-skills-measurement.md` (frozen raw data `docs/reports/data/2026-07-19-grounded-skills-results.json`, linked from `docs/operations/README.md`), PR #476 (born-red, auto-merge armed). GSW-1..3 all DONE; baton advances to GSW-4 (optional API-latency pass) or the next Part-B backlog item per `docs/planning/2026-07-19-grounded-skills-window-run.md`. 1796 pytest pass, dist byte-pin clean

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake — B-2 self-row registry-stamp automation

Executed the B-2 groomed slice: automate the substrate-kit **self-row** registry stamp so the version-bump PR itself carries the correct self-row, removing the manual aftermath hop. Two halves. (1) A self-row-scoped **born-red gate** `adopters-self-row-stale` in `src/engine/checks/check_adopters_current.py` reds CI when the substrate-kit self-row in `docs/adopters.md` goes stale versus the local kit version home — the self-row can no longer silently lag its own kit. (2) A **network-free self-restamp** — `local_self_scan` + `restamp_self_row` in `src/engine/currency.py` — wired into `scripts/cut_release.py`, so the release-bump PR stamps the correct self-row inline instead of leaving it for a manual aftermath edit. Evidence: full suite 1786 passed, dist byte-pin clean on fresh rebuild, independent review returned SHIP; `check --strict` red only on this wake's born-red card hold. PR #472 OPEN + BORN-RED (session-card in-progress hold); flips complete as the last step. No new routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).

**Prior wake (PR #470):** B-1 — pinned the SET of enforcing guard surfaces via `src/engine/guards.py::WORKFLOW_JOB_CENSUS` (6 jobs across all 4 workflow files) + `tests/test_guard_surface_census.py` (8 tests, bidirectional set-equality against the live workflow `jobs:` keys). Merged 2026-07-18 (claim removed in #471).
**Prior wake (PR #466):** pinned the THIRD enforcing surface — the `check --strict` sub-checks — via `guards.STRICT_SUBCHECKS` (7 entries) + a bidirectional parity test against the live `cli._extra_check_findings` source. Merged 2026-07-18.

## PR state

All seat-session PRs terminal MERGED: #438–#443, #445, #451, #452, #455, #457, #459, #463 (guard-manifest single-source), #464 (its claim removal), #465 (guard-parity kit-side verified), #466 (third-surface pin), #470 (B-1 guard-surface census, merged 2026-07-18), #471 (its claim removal). Sibling lanes merged: #444, #446–#450, #453.

IN-FLIGHT: `claude/self-row-registry-stamp` (PR #472) — B-2: self-row registry-stamp automation. Adds the self-row-scoped born-red gate `adopters-self-row-stale` (`src/engine/checks/check_adopters_current.py`) + the network-free `local_self_scan`/`restamp_self_row` (`src/engine/currency.py`) wired into `scripts/cut_release.py`. `src/engine/` edit + `dist/bootstrap.py` rebuild (byte-pin green); full suite 1786 passed, independent review SHIP, `check --strict` red only on the born-red card hold. Landing path: **born-red session-card hold** — `kit-quality` stays red until `.sessions/2026-07-18-self-row-registry-stamp.md` flips complete.

## Recently shipped (neutral pointer)

- PR #470 (prior wake): B-1 guard-surface census — `src/engine/guards.py::WORKFLOW_JOB_CENSUS` (6 jobs) + `tests/test_guard_surface_census.py` pin the SET of enforcing guard surfaces (bidirectional set-equality against the live workflow `jobs:` keys), closing the "a FOURTH enforcing surface ships unpinned" vector. Merged 2026-07-18.
- PR #465 (prior wake): retired the ci.yml⇄manifest codegen baton as a *verification-covered null* (proven by bidirectional mutation in `tests/test_guard_parity.py`); left a durable in-code trace. Merged 2026-07-18.
- PR #463 (prior wake): single-sourced the kit↔adopter guard mapping into `src/engine/guards.py`, read by both `adopt.live_ci_workflow()` and `tests/test_guard_parity.py`. Merged 2026-07-18; claim removed in #464.
- v1.19.0 RELEASED + verified — tag v1.19.0, run 29656601475 success, sha256 three-way PASS, https://github.com/menno420/substrate-kit/releases/tag/v1.19.0
- PR #459: the guard-parity meta-test (`tests/test_guard_parity.py`) — fails CI on kit-vs-adopter guard drift.

## Backlog — HONEST readout (carried)

With B-1 (PR #470) and B-2 (PR #472) both DONE, the buildable, non-gated backlog holds one remaining groomed slice: **B-3** fast-lane head-prefix ⇄ enabler branch_patterns symmetry lint (S, advisory). Beyond B-3 the backlog is owner-gated or date-parked:
- Owner veto pass over the 23-proposal menu (docs/planning/2026-07-16-overnight-veto-menu.md) — baton #1 (owner).
- Grounded-skills measurement window opens 2026-07-19 (docs/operations/grounded-skills-measurement.md; owner silence accepts) — not yet (today is 2026-07-18).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period.
- v1.19.0 adopter wave: awaits owner authorization (⚑ below). (v1.19.0 supersedes v1.18.0 — v1.18.0 was never distributed.)
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
- **Claims-only fast-lane guard now on BOTH surfaces**: kit's own `ci.yml` (PR #455) + generated adopter CI via `live_ci_workflow()` (PR #457). The guard-parity meta-test (`tests/test_guard_parity.py`, PR #459) fails CI on kit-vs-adopter guard drift.
- Registry (docs/adopters.md): CURRENT per `currency --check` (12 repos); the superbot-games row DRIFT is adopter-side self-report lag (owner-gated, no kit-only fix — folded into the v1.19.0 wave ask). Every adopter row reads stale until its own upgrade wave.
- `adopters-version-lag` (#441) + `adopters-stale` (calendar-age) advisories cover both staleness axes; `adopters-self-row-stale` (#472, this wake) reds CI when the kit's own self-row lags its version home.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); protocol docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. **GSW-1..3 · grounded-skills measurement — DONE** (this wake, 2026-07-19; PR #476, born-red). GSW-1 (harness ran over full/non-shallow clones of the 12-repo roster) → GSW-2 (4/4 spot-checks MATCH) → GSW-3 (`audit` report published at `docs/reports/2026-07-19-grounded-skills-measurement.md`, frozen results.json at `docs/reports/data/`, linked from `docs/operations/README.md`, window ⚑ closed). All three traps cleared: clones verified non-shallow (M4 valid), the PL-008-unverified harness was spot-checked, and the report is reachability-linked.
2. **GSW-4 (optional API-latency pass) OR the next Part-B backlog item** per `docs/planning/2026-07-19-grounded-skills-window-run.md` Part B (needs-planning / owner-gated / dead classification). B-1 (PR #470), B-2 (PR #472), B-3 (PR #474) all DONE.

**Baton to GSW-4 / next Part-B item; buildable non-gated backlog otherwise thin — everything beyond is owner-gated or date-parked.** The seat idles on the 2h failsafe trigger between wakes.

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
- Grounded-skills measurement window ~2026-07-19..26 — CLOSED (measurement published 2026-07-19, PR #476).

## 💡 Session idea (Q-0089)

**Rebuild dist BEFORE the self-restamp in the release flow (or render a "pending-rebuild" marker in the self-row tree cell).** B-2's `restamp_self_row` bumps the self-row's config-pin cell but leaves the tree cell (dist header version) lagging until the aftermath dist rebuild, so a release-bump PR momentarily commits a `docs/adopters.md` whose own self-row shows a DRIFT verdict against the kit itself. A follow-up could reorder the release flow to rebuild dist first (or write a `pending-rebuild` marker into the tree cell) so the bump PR always commits a clean, non-self-drifting self-row. Small, contained, reversible. Dedup-checked: no `restamp`/`self-row`/`tree cell` idea exists under docs/ideas/ (the two grep hits — README.md line 269 and heartbeat-verb-2026-07-09.md — are the unrelated CLI restamp verb PR #346 and the restamp-lane contract, not this self-row tree-cell lag).

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 B-1 guard-surface-census wake (PR #470): genuine credit — it read all six workflow jobs from ground truth and asserted **bidirectional** set-equality against the live `jobs:` keys, so a new, removed, OR renamed job now reds CI (the rename case is covered, not a gap). What it could improve: the census pins the NAME set but trusts the **hand-declared KIND** (GATE_PINNED / ALIAS / AUTOMATION) — the tests check reason length and kind-membership, not whether a job classified AUTOMATION actually cannot red a PR, so a job's kind could silently drift from declared (AUTOMATION) to actual (gating) without the census noticing. System improvement it surfaces: cross-check each census kind against a ground-truth signal (is the job in the `main` ruleset's required checks? does it run pytest/`check`?) so KIND can't drift undetected from what the workflow actually does.

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
