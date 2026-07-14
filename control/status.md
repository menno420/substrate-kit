# Self Improvement seat — heartbeat
updated: 2026-07-14T18:33Z · phase: post-EAP — v1.16.0 CUT + VERIFIED (release record below); ORDER 023 BUILD half done (PR #376, parked for review-merge); next = v1.17.0 release+regen wave (coordinator dispatches)

## Routines
- Failsafe: "Self Improvement failsafe wake" trig_01LsHxvnYnpQ59n7iQTPNNF3 · 0 */2 * * * · bound live coordinator. Pacemaker idles to failsafe post-consolidation (backlog dry).
- Business cron: kit-lab daily trig_01Jm57GAjNCFrYJn1oLMiYGE — KEEP.

## Facts
release v1.16.0 CUT + VERIFIED (2026-07-14): PR #370 merged as 93aa377; release.yml run 29342538960 (run number 20, workflow_dispatch on main @ 93aa377) completed SUCCESS 14:48:56Z→14:49:12Z. Record line (verify_release, runbook §5): v1.16.0 · tag object a4c4db4b48c0 -> commit 93aa3778954c · sha256 bba34e2102cbaf09394f39992f0501ea5cfd542d90301ef67e31a0854ca59170 · release.yml run UNVERIFIED-by-script (proxy 403 on the Actions API leg — honest SKIP; run verified green independently via GitHub MCP, id 29342538960). Three-way sha256 PASS: committed dist == release.json == released asset (980026 bytes). ORDER 022 done-when progress: released in a kit version ✓ (v1.16.0 carries the #371 guard) · adopter repos regenerate = NEXT (coordinator dispatches the adopter wave). Aftermath PR: adopters regen (all 9 adopter rows stale vs v1.16.0; kit self-row DRIFT is the known mid-close artifact, self-heals next regen).
done=023 facts: BUILD half done (PR #376, branch claude/order-023-branch-sweep); release+regen half = v1.17.0 wave, coordinator-sequenced. Ships `branch_sweep_workflow()` (src/engine/adopt.py) — kit-owned scheduled `.github/workflows/branch-sweep.yml` (daily cron 17 3 * * * + workflow_dispatch `dry_run`; permissions contents:write + pull-requests:read) deleting spent same-repo heads of merged+closed PRs on `claude/*`/`codex/*`/`bot/*`, skip rules (open-PR head · default branch · fork heads · no-PR refs · diverged tips) each logged; scheduled NOT pull_request:closed (GITHUB_TOKEN events don't trigger workflows). Lifecycle = enabler's: staged `<state_dir>/ci/branch-sweep.yml`, installed by `adopt --wire-enforcement`, kit-owned regen + carve-out bank; new `branch_sweep` config knob. Suite 1559→1568 passed (1 skipped unchanged); preflight 7/7; dist byte-stable ×2 (sha256 82ba236e…04e0). PR parks green for review-merge — auto-merge NOT armed by design. Detail: .sessions/2026-07-14-order-023-branch-sweep.md.
done=022 facts: PR #371 — stop-hook merged-head final-push guard: guard merged to main; release + adopter regen ride v1.16.0 (in flight). `_stop_push_guard` (sixth `evaluate_stop` advisory): fetch → provable ancestry vs origin/main via the new dist-shipped `engine/lib/git_truth.py` (port of scripts/_git_truth.py, parity-pinned) → merged=loud SKIP line · unmerged=silent · unprovable=NOTE + push proceeds (fail-open). Suite 1550→1559 passed (1 skipped unchanged); preflight 7/7; dist byte-stable ×2; three decision points mutation-tested. Details: .sessions/2026-07-14-order-022-push-guard.md.
done=021 facts: PR #368 — EAP closeout walkthrough at docs/eap-closeout-walkthrough-2026-07-14.md (sections A–E; OWNER ACTIONS leads with the #317 click). #345 "green" retracted with evidence; #317/#345 park states verified live. Full detail: git history of this file @ 4f6e50c.
done=020 facts: PR #362 — ORDER 020 items d+e; (a)–(c) satisfied per thread premise-check. Detail in git history @ 4f6e50c.

## Backlog state (honest)
Buildable backlog DRY as of 04:0xZ — 11/11 buildable ideas consumed or shipped. Former gates cleared 2026-07-14T14:0xZ: #317 and #345 both owner-ratified and merged (see Ratified/merged below). ORDER 022 guard landed on main as 39c6b20 (#371) and is folded into the v1.16.0 cut (PR #370) — release wave UNGATED, riding #370's green. Remaining: resident-lane kit: lines (→ adopters.md regen) · grounded-skills window ~07-19. No filler beyond this line (Q-0089).

## Parked
- (none — both former parks ratified 2026-07-14T14:0xZ, records below)

## Ratified/merged (2026-07-14 reconcile)
- PR #317 — RATIFIED + MERGED to main as 4f6e50c (2026-07-14T14:06:15Z, "Graduate the autonomy rider (Q-0271) + multi-repo reading path (Q-0272) into templates"). Payload verified on disk at HEAD: docs/program/rulings.md [PL-012] · src/engine/templates/reading-path.md.tmpl · tests/test_rider_graduation.py. Release wave UNGATED.
- PR #345 — RATIFIED + MERGED to main as c603cc9 (2026-07-14T14:06:12Z, "Add staged-artifact regen-lag checker (ORDER 019 item 6)"). Payload verified on disk at HEAD: src/engine/checks/check_staged_regen.py · tests/test_check_staged_regen.py.
- PR #371 — MERGED to main as 39c6b20 (2026-07-14T14:31:51Z, ORDER 022 stop-hook merged-head final-push guard). Folded into claude/release-v1.16.0 same hour; CHANGELOG entry re-cut into [1.16.0].

## Registry state
- adopters.md regenerated post-v1.16.0 (this session): all 9 adopter repos stale vs v1.16.0 (upgrade wave pending); kit self-row DRIFT = known mid-close artifact, self-heals next regen.
kit: v1.16.0

## Next-2 baton
1. Adopter upgrade wave for v1.16.0 — coordinator dispatches (`upgrade` each adopter, merged on green, then registry regen; ORDER 022 done-when closes when adopter repos regenerate).
2. Resident kit: lines → follow-up adopters regen · grounded-skills window ~07-19.

⚑ FOR OWNER (unchanged standing set — full paste-ready field blocks verbatim in git history of this file @ 86d2a57):
- P10 required-check swap (ruleset: require `kit-quality`, drop the two legacy contexts).
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- ⚑ 6 public-flip-or-PAT (unblocks B2–B4 cross-repo sweeps).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–023 · done=001–022 (023 BUILD half done, PR #376; done-when completes at the v1.17.0 release+regen wave)
