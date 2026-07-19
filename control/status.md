# Self Improvement seat — heartbeat
updated: 2026-07-19T12:21:57Z · phase: R11 SHIPPED (recipe applies-when: structural-signature tag + advisory check_recipe_applies_when, PR #506); R1..R11 consumed, baton retargeted → R12 (check_folded_gate remediation snippet).

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and flipped `new→done` manager-side only after the manager reads this report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound = 024) — its WORK is complete (both cfgdiff writeups on main, linked from bench/README.md, merged via PR #340).

## This wake — R11: recipe applies-when: structural-signature tag
Built R11 from the night-run groom (docs/planning/2026-07-19-night-run-idea-groom.md, R11 entry). Gave graduated recipes a machine-readable `applies-when:` structural signature so a FUTURE discovery check can nudge an adopter that grows a matching seam toward the relevant recipe (discovery, not enforcement). Three parts: (1) added a `> **applies-when:** \`content:raw.githubusercontent.com, path:*.json\`` badge to the one existing recipe (docs/recipes/pinned-feed-contract.md); (2) documented the field's grammar (comma-separated `path:<glob>` / `content:<marker>` tokens) in docs/recipes/README.md; (3) shipped an ADVISORY-only `src/engine/checks/check_recipe_applies_when.py` that flags any graduation with a missing/empty/malformed tag — wired on the `posture="advisory"` seam (mirroring R7), NOT a STRICT_SUBCHECK, dist rebuilt byte-pin clean. Files: check_recipe_applies_when.py, cli.py, build_bootstrap.py, dist/bootstrap.py (rebuilt), docs/recipes/{pinned-feed-contract.md,README.md}, tests/test_check_recipe_applies_when.py (8 tests). Full suite 1881 passed / 1 skipped; `check --strict` exit 0; the advisory is silent on the kit's own (now-tagged) recipe. PR #506 OPEN + BORN-RED until this card flip; flips complete as the last step, then auto-merges (armed, squash) on green. No routines armed; the failsafe dead-man bridge remains armed under the coordinator session (F-1 below).
- R11 decide-and-flag: shipped the tag as a blockquote BADGE line (reusing the Status-badge regex style), NOT top-of-file `--- … ---` YAML — the kit engine is deliberately PyYAML-free and this avoids introducing its first frontmatter parser; the groom doc's "frontmatter tag" wording is honored by a machine-readable header field. The adopter-nudge check is deferred to a later rung (needs a 2nd recipe with a signature first, per the recipe's own escalation rule). Also self-caught + fixed an invalid-escape backtick sequence introduced in the checker's docstring/messages (now compiles clean under -W error).
- R11 note: redirected here after a sibling claimed R10 (PR #505, MERGED 12:12:54Z, the `--freeze` self-citing reproduce block); I took R11, the next unclaimed rung.

## Recently shipped (terminal MERGED / merging)
- **#506 (this wake) — R11 recipe applies-when: structural-signature tag + advisory** (`src/engine/checks/check_recipe_applies_when.py` + `src/engine/cli.py` + `src/build_bootstrap.py` + `docs/recipes/{pinned-feed-contract.md,README.md}` + `tests/test_check_recipe_applies_when.py` + rebuilt `dist/bootstrap.py`): merging on green after this flip.
- **#505 — R10 harness --freeze self-citing reproduce block** (`scripts/measure_grounded_skills.py` + `tests/test_measure_grounded_skills.py`): MERGED 2026-07-19T12:12:54Z.
- **#501 — R9 measure_grounded_skills --commit-results PATH** (`scripts/measure_grounded_skills.py` + `tests/test_measure_grounded_skills.py`): MERGED.
- **#500 — R8 fast-lane prefix symmetry runtime check --strict sub-check** (`src/engine/checks/check_fastlane_symmetry.py` + `src/engine/cli.py` + `src/engine/guards.py` + `tests/` + rebuilt `dist/bootstrap.py`): MERGED 2026-07-19T11:23:21Z (sibling session; claim retired via #502).
- **#498 — R7 append-log ⇄ Walls-correction disagreement advisory** (`src/engine/checks/check_wall_ledger_agreement.py` + `src/engine/cli.py` + `src/build_bootstrap.py` + `tests/test_check_wall_ledger_agreement.py` + rebuilt `dist/bootstrap.py`): MERGED.
- **#497 — R6 check --explain-wall/--why** (`src/engine/checks/check_no_false_walls.py` + `src/engine/cli.py` + `tests/test_explain_wall.py` + rebuilt `dist/bootstrap.py`): MERGED.
- **#495 — R5 capability stale-wall advisory** (`src/engine/checks/check_stale_walls.py` + `tests/test_check_stale_walls.py` + rebuilt `dist/bootstrap.py`): MERGED.
- **#493 — R4 HOOK_CENSUS second fourth-surface vector** (`src/engine/guards.py` + `tests/test_guard_surface_census.py` + rebuilt `dist/bootstrap.py`): MERGED.
- **#492 — R3 shallow-clone REFUSE marker** (`scripts/measure_grounded_skills.py` + `tests/test_measure_grounded_skills.py`): MERGED.
- **#490 — R2 `/scope-backlog-item` skill** (`src/engine/skills/skills.py` + `tests/test_skills.py` + rebuilt `dist/bootstrap.py`): MERGED.
- **#488 — R1 cut_release self-row non-DRIFT** (`scripts/cut_release.py` + `tests/test_cut_release.py`): MERGED.
- **#487 — night-run idea groom + heartbeat refresh**: swept ~25 night session-card `💡` ideas + docs/ideas/, ranked into the groom doc (R1–R12), refreshed this heartbeat.

## Night run — merged #455–#486 (all terminal MERGED)
- Guard stack: claims-only fast-lane guard on both surfaces (#455/#457) + guard-parity meta-test (#459); no-false-walls guard fleet-wide (#444–#450); declarative guard-manifest (#463); guard-parity 3rd surface (#466); B-1 guard-surface census (#470).
- v1.19.0 RELEASED + verified (tag v1.19.0, run 29656601475 success, sha256 three-way PASS).
- GSW measurement COMPLETE: GSW-1..3 harness run + before/after report (#476), GSW-4 latency pass (#477), GSW-5 opt-in --api-latency mode (#479); report docs/reports/2026-07-19-grounded-skills-measurement.md.
- B-2 self-row registry-stamp automation (#472); B-3 fast-lane prefix symmetry lint (#474).
- Recipes #480 backlog-recipes planning arc; pinned-feed-contract doctrine graduated (#482); folded-gate diff-aware advisory sub-check (#484); folded-gate host ports + readiness cell routed to fm outbox (#486).

## PR state
All seat-session PRs terminal MERGED through #505 (R10, sibling). IN-FLIGHT: `claude/r11-recipe-applies-when` (R11, PR #506) — recipe `applies-when:` badge + docs/recipes/README schema + advisory `check_recipe_applies_when` + rebuilt dist; born-red hold until this session card flips complete, then auto-merges (armed, squash) on green. Post-merge cleanup: a `claim/*` fast-lane PR retires the merged R11 claim (`claude-r11-recipe-applies-when.md`).

## Backlog — groomed (R1..R11 consumed, R12 next)
The buildable-now backlog is groomed + ranked in `docs/planning/2026-07-19-night-run-idea-groom.md`. R1 (#488), R2 (#490), R3 (#492), R4 (#493), R5 (#495), R6 (#497), R7 (#498), R8 (#500), R9 (#501), R10 (#505), and R11 (#506) are now shipped. Top remaining buildable-now slices:
- **R12 (M) — check_folded_gate remediation snippet:** extend the #484 advisory to also emit the exact diff-aware card-derivation block to port, so a host fixes the fold in one paste; recurs across hosts (superbot-next `gate`, websites `quality.yml`). (from folded-gate-check card)
- **R13 (S/M) — exit-affecting PL-004 task-class gate on the born-red card:** fold the segment-3 task-class check (∈ the 9 PL-004 classes) into the born-red session-gate that already grades the PR's OWN added card, so an off-PL-004 `📊 Model:` task-class on the PR's own card reds at CI — enforce-don't-exhort, scoped to the one card the PR adds (the fleet-wide window's advisory posture stays). (from the groom doc R13 entry)
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
- `/scope-backlog-item` skill (R2, #490) makes the standing "when no exec work is left, plan" order turnkey: chase origin → fuller picture → classify + sized recipe/⚑ → retarget the Next-2 baton; indexed in docs/SKILLS.md via the registry.
- `measure_grounded_skills.py --json` (R3, #492) refuses to publish on a shallow clone — REFUSE marker + exit 2 — turning the prose trap into an enforced refuse-to-publish; markdown/stdout still soft-nulls shallow rows.
- `HOOK_CENSUS` (R4, #493) in `src/engine/guards.py` pins the fourth guard surface — all four Claude Code lifecycle hooks (3 advisory + 1 orientation) censused + kind-classified, bidirectional set-equality vs `cli._HOOK_EVENTS`/`cli._HOOK_GUARD_KINDS` in `tests/test_guard_surface_census.py`; a hook added/removed without a census entry reds the kit's own suite. Kit-only pytest meta-test (like `WORKFLOW_JOB_CENSUS`), not a STRICT_SUBCHECK.
- `check_stale_walls.py` (R5, #495) surfaces any dated `wall` row in `docs/CAPABILITIES.md` older than `cadence.staleness_days` (default 14) as an ADVISORY-only `check` finding — the enforcement analogue of the DISCOVERY RULE's staleness step, warn-only and never exit-affecting; wired on the `posture="advisory"` seam (NOT `_extra_check_findings`), not a STRICT_SUBCHECK. Deliberately skips `wall` rows with no parseable date (seeded as a follow-up idea).
- `check --explain-wall <phrase>` / `--why` (R6, #497) is a CLI lookup over the false-wall `match_blocklist`: it prints the matched rule + its per-rule `WALL_CORRECTIONS` ground-truth correction + a pointer to the `docs/CAPABILITIES.md` dated-append-row form; benign phrases report "no false-wall rule matched"; always exits 0 (a lookup, not a gate — touches neither `_extra_check_findings` nor `STRICT_SUBCHECKS`). All 19 blocklist rules carry a correction. The checker's own Finding message is left unchanged (minimal blast radius).
- `check_wall_ledger_agreement.py` (R7, #498) fires an ADVISORY-only `check` finding when a `## Walls` *correction* row and the newest same-capability `## Append log` entry in `docs/CAPABILITIES.md` disagree on a capability's status (seeded family: merge/arm/flip) — the enforcing readout for the ledger self-contradiction that persisted a full day; wired on the `posture="advisory"` seam, never exit-affecting, NOT a STRICT_SUBCHECK. Seeded `_FAMILIES` covers merge/arm/flip only; auto-deriving families from the ledger's own titles is a seeded follow-on idea.
- `check_fastlane_symmetry.py` (R8, #500) fires an ADVISORY-only `check` finding when a host's ci.yml claims-only fast-lane guard cards a prefix its `auto-merge-enabler.yml` never arms (enabler⇄guard drift) — the runtime promotion of the B-3 kit-only meta-test's enabler⇄guard leg, so ADOPTERS catch their own drift, not just kit CI. Wired on the `posture="advisory"` seam, never exit-affecting, NOT a STRICT_SUBCHECK. **Decide-and-flag:** the R8 recipe named `_extra_check_findings` + `STRICT_SUBCHECKS` (exit-affecting), but that reintroduces the tested fleet-bomb the enabler⇄config sibling `check_automerge_preflight` deliberately avoids (`test_drift_never_reds_strict_check`: "a required-check red here would be a fleet bomb during version skew"), so R8 rides the advisory seam scoped to the complementary enabler⇄guard surface. R7-surfaced PL-004 task-class gate gap registered as groom idea R13 (not built this slice).
- `measure_grounded_skills.py --commit-results PATH` (R9, #501) writes the raw `--json` results payload to a caller-named PATH (creating the parent dir) so a measure→verify→publish chain persists a durable results.json across ephemeral-container splits; shares `--json`'s shallow-clone REFUSE gate (a committed-but-zeroed artifact can't ship) and adds no git side-effect (the chain does the `git add`). Standalone `scripts/` file — not in MODULE_ORDER, dist untouched.
- `measure_grounded_skills.py --freeze` (R10, #505) makes a `--json`/`--commit-results` run self-citing: it emits `sha256(blob)` over the exact output bytes, the exact paste-ready reproduce command, and a byte count into a `<output>.freeze` sidecar next to each artifact (plus a stderr citation block), so a committed results.json is tamper-evident and reproducible (`sha256sum <output>` verifies it). Runs inside the R3 shallow-clone REFUSE guard; errors without a JSON sink; sidecar-not-payload so there is no self-referential hash. Standalone `scripts/` file — not in MODULE_ORDER, dist untouched.
- `check_recipe_applies_when.py` (R11, #506) is an ADVISORY-only `check` finding: every `docs/recipes/` graduation (except README.md) must carry a well-formed `> **applies-when:** \`<signature>\`` badge — a comma-separated list of `path:<glob>` / `content:<marker>` structural-signature tokens — so a FUTURE discovery check can match an adopter's seam to a recipe (discovery, not enforcement). Wired on the `posture="advisory"` seam, never exit-affecting, NOT a STRICT_SUBCHECK; the one existing recipe (pinned-feed-contract.md) carries the tag so the advisory is silent. Badge-line form (not YAML) keeps the engine PyYAML-free.
- Registry (docs/adopters.md): CURRENT per currency --check (12 repos); adopter rows read stale until each repo's own upgrade wave (owner-gated).
- adopters-version-lag + adopters-stale + adopters-self-row-stale advisories cover the staleness axes.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. **R12 — check_folded_gate remediation snippet (M).** Buildable now; recipe in the groom doc (R12 entry): extend the #484 advisory to also emit the exact diff-aware card-derivation block to port, so a host fixes the fold in one paste; recurs across hosts (superbot-next `gate`, websites `quality.yml`).
2. **R13 — exit-affecting PL-004 task-class gate on the born-red card (S/M).** Buildable now; recipe in the groom doc (R13 entry): fold the segment-3 task-class check (∈ the 9 PL-004 classes) into the born-red session-gate that already grades the PR's OWN added card, so an off-PL-004 `📊 Model:` task-class on the PR's own card reds at CI — enforce-don't-exhort, scoped to the one card the PR adds (the fleet-wide window's advisory posture stays).
**Baton: R11 (recipe applies-when: tag + advisory) SHIPPED via PR #506 — baton retargeted to R12 (check_folded_gate remediation snippet); full ranked list R12–R13 in docs/planning/2026-07-19-night-run-idea-groom.md.**

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
