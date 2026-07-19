# Self Improvement seat — heartbeat
updated: 2026-07-19T08:08:25Z · phase: IDLE — R1 SHIPPED (cut_release self-row non-DRIFT, PR #488); buildable-now backlog still REFILLED (docs/planning/2026-07-19-night-run-idea-groom.md, R1–R12); baton retargeted → R2 (`/scope-backlog-item` skill).

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and flipped `new→done` manager-side only after the manager reads this report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound = 024) — its WORK is complete (both cfgdiff writeups on main, linked from bench/README.md, merged via PR #340).

## This wake — R1: cut_release dist-before-self-restamp fix
Built R1 from the night-run groom (docs/planning/2026-07-19-night-run-idea-groom.md). Root cause: `scripts/cut_release.py` stamped the bump self-row from `local_self_scan`, which reads `config_pin` from the just-bumped `substrate.config.json` (= target) but `tree_version` from `dist/bootstrap.py`'s still-OLD header (the dist rebuild is a manual FOLLOWUP step) — rendering tree(old) != pin(target), a false tree-internal DRIFT committed into the version-bump PR (kit #472 regression). Fix: stamp the self-row from the release's tree truth (target); every mergeable PR carries `dist == target` by the byte-pin (`test_committed_bootstrap_is_current`), so the committed self-row is honest. Added a pinning test tied to the real `currency.drifts()`/`verdict()`. Full suite 1822 passed. PR #488 OPEN + BORN-RED until this card flip; flips complete as the last step. No routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).

## Recently shipped (terminal MERGED / merging)
- **#488 (this wake) — R1 cut_release self-row non-DRIFT** (`scripts/cut_release.py` + `tests/test_cut_release.py`): merging on green after this flip.
- **#487 — night-run idea groom + heartbeat refresh**: swept ~25 night session-card `💡` ideas + docs/ideas/, ranked into the groom doc (R1–R12), refreshed this heartbeat.

## Night run — merged #455–#486 (all terminal MERGED)
- Guard stack: claims-only fast-lane guard on both surfaces (#455/#457) + guard-parity meta-test (#459); no-false-walls guard fleet-wide (#444–#450); declarative guard-manifest (#463); guard-parity 3rd surface (#466); B-1 guard-surface census (#470).
- v1.19.0 RELEASED + verified (tag v1.19.0, run 29656601475 success, sha256 three-way PASS).
- GSW measurement COMPLETE: GSW-1..3 harness run + before/after report (#476), GSW-4 latency pass (#477), GSW-5 opt-in --api-latency mode (#479); report docs/reports/2026-07-19-grounded-skills-measurement.md.
- B-2 self-row registry-stamp automation (#472); B-3 fast-lane prefix symmetry lint (#474).
- Recipes #480 backlog-recipes planning arc; pinned-feed-contract doctrine graduated (#482); folded-gate diff-aware advisory sub-check (#484); folded-gate host ports + readiness cell routed to fm outbox (#486).

## PR state
All seat-session PRs terminal MERGED through #487. IN-FLIGHT: `claude/cut-release-dist-before-restamp` (R1, PR #488) — one-file fix + pinning test; born-red hold until the session card flips complete, then auto-merges on green.

## Backlog — REFILLED (R1 consumed, R2 next)
The buildable-now backlog is groomed + ranked in `docs/planning/2026-07-19-night-run-idea-groom.md`. R1 is now shipped (#488). Top remaining buildable-now slices:
- **R2 (S) — `/scope-backlog-item` skill:** scaffold the planning-recipe arc as a `docs/SKILLS.md` skill, making the standing "when no exec work is left, plan" order turnkey. (from #480 card)
- R3–R12: shallow-clone REFUSE marker · HOOK_CENSUS · stale-wall advisory · check --explain-wall · append-log⇄Walls disagreement lint · fast-lane symmetry runtime advisory · harness --commit-results · harness --freeze self-cite · recipes applies-when tag · check_folded_gate remediation snippet (see the groom doc).
Cross-repo / owner-gated (not kit-landable): folded-gate host ports (superbot-next `gate`, websites `quality.yml`, routed via fm #486); v1.19.0 adopter wave; the 23-proposal veto menu.

## Held decision
**v1.20.0 cut DEFERRED** pending adopter-wave authorization — the next release carries the #482 pinned-feed template rider + the #484 folded-gate checker to adopters; cutting before the wave is authorized ships doctrine no adopter consumes. Unblocks on the ⚑ v1.19.0 adopter-wave authorization below.

## Routine / trigger state (no writes this wake)
- ARMED (active failsafe, F-1): `trig_01194PdaWChtHGNKASURxdLx` "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session — the current dead-man bridge.
- No new routines armed; no trigger APIs called this wake.
- Business cron: no kit-lab-named trigger in the account list; the 06:00Z kit-lab daily runs owner-side (see the ⚑ kit-lab block).

## State
kit: v1.19.0
- No-false-walls guard enforced fleet-wide (kit ci.yml + every adopter's check --strict); folds into the next release.
- Claims-only fast-lane guard on both surfaces + guard-parity meta-test fails CI on kit↔adopter guard drift.
- cut_release now stamps the bump self-row from the release target (R1, #488) — committed adopters.md self-row is non-DRIFT for the mergeable state; the FOLLOWUP dist rebuild is still a manual step guarded by the byte-pin.
- Registry (docs/adopters.md): CURRENT per currency --check (12 repos); adopter rows read stale until each repo's own upgrade wave (owner-gated).
- adopters-version-lag + adopters-stale + adopters-self-row-stale advisories cover the staleness axes.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. **R2 — `/scope-backlog-item` skill (S).** Buildable now; add the skill + index it in docs/SKILLS.md, scaffolding the planning-recipe arc turnkey. Recipe in the groom doc.
2. **R3 — shallow-clone REFUSE marker (S).** Buildable now; next slice in the groom doc's ranked list.
**Baton: R1 (cut_release dist-order fix) SHIPPED (#488) — baton retargeted to R2 (`/scope-backlog-item` skill); full ranked list R2–R12 in docs/planning/2026-07-19-night-run-idea-groom.md.**

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

P10 required-check swap — DONE/moot: ruleset "main-branch-protection" (id 18694708) already requires kit-quality as the sole check; no owner action.

⚑ public-flip-or-PAT (pick one)
WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
WHERE: P11: Settings → General → Danger Zone → Change visibility · P13: github.com/settings/tokens → fine-grained read-only PAT scoped to this repo, then add it to the fleet environments.
HOW: P11 is click-through; P13 is create-token + paste into environment settings.
WHY: sibling repos cannot read kit data today, so cross-repo sweeps and the merged console run blind.
UNBLOCKS: B2–B4 cross-repo sweeps + kit data in the merged console.
VERIFY: a sibling-seat session fetches a kit file read-only without "Access denied: repository … is not configured for this session".
RISK: ⚠️ P11 effectively irreversible (history exposed once public) · ↩️ P13 reversible — revoke anytime.

⚑ t5-headless-guard fix (owner-gated: pin-path + cross-tree kit-lab)
WHAT: fix the T5 bench probe so it produces a real in-session guard fire in the ON arm. Recommend shape 2 (check-driven guards) — needs no hook-honoring harness rebuild and the enforcement surface exists headless.
WHERE: kit-lab repo, `bench/tasks/T5.md` (PIN PATH) + `bench/README.md` / `run_ab.py`; optional engine sliver `src/engine/checks/` (substrate-kit) for the last-card freshness anchor — verify it is not already covered by #19's `--require-session-log`.
HOW: shape 2 — the arm's protocol runs `check --strict` inside the session flow (or a wrapper fails the task on red) so the guard's fire/obey/repair arc is observable without the hook layer.
WHY: without it, T5 scores all guard items n/a — the ON arm demonstrates nothing over the unguarded baseline; the guard-probe purpose of T5 is unmet.
UNBLOCKS: a T5 run that scores guard fire/obey/repair met/not-met instead of n/a; closes judge report §5.5 item 2.
VERIFY: a T5 run produces ≥1 real in-session guard fire (or a recorded deliberate violation) in the ON arm.
RISK: ⚠️ pin-path change → must land via a `do-not-automerge` owner-review PR in kit-lab; not landable from substrate-kit. Detail home: docs/planning/2026-07-19-needs-planning-recipes.md §4.

Standing (full paste-ready blocks verbatim in git history of this file):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- Grounded-skills measurement window — CLOSED (measurement published 2026-07-19, PRs #476/#477).

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
