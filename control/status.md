# Self Improvement seat — heartbeat
updated: 2026-07-18T21:09:08Z · phase: fourth-surface guard shipped — B-1 guard-surface CENSUS (`src/engine/guards.py::WORKFLOW_JOB_CENSUS`, 6 jobs across all 4 workflow files) + `tests/test_guard_surface_census.py` now pin the SET of enforcing guard surfaces, not just each surface's steps; a new gating workflow job can no longer ship un-pinned (PR #470, born-red); baton: B-2 CI self-row registry-stamp automation, then B-3; grounded-skills window opens 2026-07-19

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake — B-1 fourth-surface guard (workflow-job census)

Executed the B-1 groomed slice: a guard-surface CENSUS that pins the SET of enforcing guard surfaces, closing the "a FOURTH enforcing surface ships unpinned" vector. The three existing surfaces were each parity-pinned at step/sub-check granularity (ci.yml `kit-quality` steps ⇄ `REGISTRY`; adopter `substrate-gate` steps ⇄ `MIRRORS`; `check --strict` sub-checks ⇄ `STRICT_SUBCHECKS`) — but nothing pinned the set itself, so a new gating **workflow job** could ship with no parity assertion. Added `src/engine/guards.py::WORKFLOW_JOB_CENSUS` — one entry per real job read from ground truth across all 4 workflow files (6 jobs: `ci.yml::kit-quality` GATE_PINNED · `ci.yml::legacy-alias-test` / `legacy-alias-smoke` ALIAS · `auto-merge-enabler.yml::enable-auto-merge` / `auto-merge-disarm.yml::disarm` / `release.yml::release` AUTOMATION), each with a >15-char reason — plus `CENSUS_*` kind constants, `PINNING_MECHANISMS` (the three registries enumerated), an `EXPECTED_CENSUS_GATES=1` floor, and accessors. Added `tests/test_guard_surface_census.py` (8 tests): bidirectional set-equality between the live workflow `jobs:` keys and the census (stdlib parser, no yaml/subprocess), gate-pin resolution, out-of-scope reason quality, known-kinds, gate floor, pinning-mechanism completeness, copy-accessor. Rebuilt `dist/bootstrap.py` (byte-pin green). Also conformed the two PL-004 model-line advisories on the guard-manifest card (`effort high`→`high`, `kit engine refactor`→`mechanical refactor`). Evidence: full suite 1776 passed / 1 skipped; new census+parity 15/15; `check --strict` red only on this wake's born-red card hold; dist byte-clean on fresh rebuild. PR #470 OPEN + BORN-RED (session-card in-progress hold); flips complete as the last step. No new routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).

**Prior wake (PR #466):** pinned the THIRD enforcing surface — the `check --strict` sub-checks — via `guards.STRICT_SUBCHECKS` (7 entries) + a bidirectional parity test against the live `cli._extra_check_findings` source. Merged 2026-07-18.
**Prior wake (PR #469):** produced the grounded-skills window run plan (`docs/planning/2026-07-19-grounded-skills-window-run.md`) + a buildable-now backlog groom; planning-only, no engine code.

## PR state

All seat-session PRs terminal MERGED: #438–#443, #445, #451, #452, #455, #457, #459, #463 (guard-manifest single-source, merged 2026-07-18), #464 (its claim removal), #465 (guard-parity kit-side verified — codegen baton retired as a verification-covered null, merged 2026-07-18). Sibling lanes merged: #444, #446–#450, #453.

IN-FLIGHT: `claude/guard-surface-census` (PR #470) — B-1: pins the SET of enforcing guard surfaces via `src/engine/guards.py::WORKFLOW_JOB_CENSUS` (6 jobs across all 4 workflow files) + `tests/test_guard_surface_census.py` (8 tests, bidirectional set-equality against the live workflow `jobs:` keys). `src/engine/` edit + `dist/bootstrap.py` rebuild (byte-pin green); full suite 1776 passed / 1 skipped, `check --strict` red only on the born-red card hold. Landing path: **born-red session-card hold** — `kit-quality` stays red until `.sessions/2026-07-18-guard-surface-census.md` flips complete. (PR #466, the THIRD-surface pin, MERGED 2026-07-18.)

## Recently shipped (neutral pointer)

- PR #465 (prior wake): confirmed the rung-2 ci.yml⇄manifest codegen baton is already closed by the bidirectional exact-match in `tests/test_guard_parity.py` (proven by mutation both ways); retired the baton as a verification-covered null with a durable in-code trace; drift-fixed the stale `release-v1-19-0` claim + the Backlog v1.18.0→v1.19.0 line. Merged 2026-07-18.
- PR #463 (prior wake): single-sourced the kit↔adopter guard mapping into `src/engine/guards.py`, read by both `adopt.live_ci_workflow()` (adopter-CI generator) and `tests/test_guard_parity.py` (parity meta-test) — the parity test no longer carries its own hand-kept `REGISTRY`. Merged 2026-07-18; claim removed in #464.
- v1.19.0 RELEASED + verified — tag v1.19.0, run 29656601475 success, sha256 three-way PASS, https://github.com/menno420/substrate-kit/releases/tag/v1.19.0
- PR #459: the guard-parity meta-test (`tests/test_guard_parity.py`) — fails CI on kit-vs-adopter guard drift.
- PR #457 / #455: propagated the claims-only fast-lane guard into the generated adopter CI, and the kit-CI half.

## Backlog — HONEST readout (carried)

Buildable, non-gated backlog is now **dry**. This wake executed the third-guard-surface baton (PR #466 — see This wake); with all three enforcing guard surfaces now parity-pinned, the guard-parity thread has no further buildable rung. No new order exists (none >024 at inbox@HEAD). Remaining rungs are owner-gated or date-parked:
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
- **Claims-only fast-lane guard now on BOTH surfaces**: kit's own `ci.yml` (PR #455) + generated adopter CI via `live_ci_workflow()` (PR #457). The two guard stacks were hand-kept in agreement; the guard-parity meta-test (`tests/test_guard_parity.py`, PR #459 in flight) now fails CI on kit-vs-adopter guard drift, replacing the hand-check with a red-CI signal (`docs/ideas/guard-parity-kit-vs-adopter-2026-07-18.md`).
- Registry (docs/adopters.md): CURRENT per `currency --check` (12 repos); the superbot-games row DRIFT is adopter-side self-report lag (owner-gated, no kit-only fix — folded into the v1.18.0 wave ask). Every adopter row reads stale until its own v1.18.0 upgrade wave.
- `adopters-version-lag` (#441) + `adopters-stale` (calendar-age) advisories cover both staleness axes.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); protocol docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. **Grounded-skills measurement window — opens 2026-07-19** (target 2026-07-19..26; owner silence accepts). A turnkey, self-authorizing run plan now exists: `docs/planning/2026-07-19-grounded-skills-window-run.md` — pick **GSW-1** (run the harness) → **GSW-2** (spot-check + interpret) → **GSW-3** (publish the `audit` report). Mind the three traps: shallow-clone zeroes M4 (re-clone full), the harness is PL-008 UNVERIFIED (spot-check ≥3 numbers), and the report must be linked from `docs/operations/README.md` (docs-gate reachability).
2. **Groomed buildable-now slices** — if a wake needs work before 2026-07-19 or in parallel; all contained, reversible, test-only or advisory. **B-1 guard-surface census meta-test is DONE (PR #470, this wake).** Remaining: **B-2** CI self-row registry-stamp automation (next) · **B-3** fast-lane head-prefix ⇄ enabler branch_patterns symmetry lint. Full groom (needs-planning / owner-gated / dead classification) in the same planning file, Part B. Beyond these the backlog is owner-gated or needs-planning — an honest "nothing buildable beyond these" holds.

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

**Guard-surface census — a meta-test/doc that enumerates ALL enforcing guard surfaces and asserts each carries a parity pin.** With PR #466 the third surface (`check --strict` sub-checks) is now pinned; the three surfaces — ci.yml `kit-quality` steps, the generated adopter `substrate-gate` job, and `check --strict` sub-checks — are each guarded independently, but nothing prevents a FOURTH enforcing surface (a new git-hook, a new workflow job) from shipping with NO parity assertion. A single census that lists every enforcing surface and fails until each has a registry + parity test would make "add an enforcing surface without pinning it" impossible. Small, test-only, reversible. Dedup-grep docs/ideas/ + docs/roadmap.md for "census"/"guard.surface"/"parity" before adding a file; if a near-dup exists, note it instead.

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 guard-parity kit-side wake (PR #465): genuine credit — it retired the ci.yml⇄manifest codegen baton as a *verification-covered null* rather than building a 388-line generated workflow for zero added safety, and left a durable in-code trace so the null is not re-chased. That is the right call: honest null over busywork. System improvement it surfaces: all three guard surfaces now re-implement bespoke source-slicing parsers inside `tests/test_guard_parity.py` (each greps a different live source region to recover its guard set), and a future 4th surface would re-implement the parser again — a shared source-set-extractor helper would let the parser logic be written and tested once, then reused per surface.

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
