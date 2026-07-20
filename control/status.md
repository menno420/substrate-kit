# Self Improvement seat — heartbeat
updated: 2026-07-20T07:30:00Z
phase: v1.20.1 adopter-distribution wave CLOSED (fm ORDER 048) — detector fix (#549) + patch release v1.20.1 (#550) shipped; 9/9 vendoring adopters swept, upgrade PRs opened ready (1 already merged); wave-lane PR #548 landing.
health: green
kit: v1.20.1 · check: green · engaged: yes
last-shipped: #550 — Cut release v1.20.1 (detector-fix patch; tag v1.20.1 → 40eb0fe, dist sha256 d6c4f81565f8877f38e2b4315968fc5f22a378c9c4dfdd89f8ed02827e7f6b39)
blockers: none (remaining wave completion is resident-side merge of the 8 open upgrade PRs; owner-gated ⚑ set below)

## v1.20.1 release (this wave)
- **#549 (squash 662be7d)** — `check_no_false_walls` clearing vocab rewritten to attachment-based matching: fixes false positives on repudiation / dated-record lines (the 5 idea-engine false positives); genuine bare walls still red. Two detector follow-ups recorded in #549's card: (P2) wrapped-lookback punctuation-gated bleed; (P3) `match_blocklist` one-hit-per-line masking.
- **v1.20.1 cut** — bump PR **#550 (squash 40eb0fe)**; `release.yml` run 29720142913 success; tag **v1.20.1 → 40eb0fe**; dist sha256 **d6c4f81565f8877f38e2b4315968fc5f22a378c9c4dfdd89f8ed02827e7f6b39** (verified three ways). Tree homes (substrate.config.json / pyproject.toml / dist header / dist sha256) all agree.

## v1.20.1 adopter-distribution wave — results (10 reachable; pokemon-mod-lab DARK/skipped)
All upgrades 1.17.0 → 1.20.1 unless noted; each PR = kit-distribution files only (host workflows / control / settings / hooks untouched). Residuals are pre-existing resident-owned false-wall / badge doc content (noted in each PR body) — the resident lane's to reconcile, not a wave defect.

| adopter | wave PR | state |
|---|---|---|
| gba-homebrew | #211 | MERGED (main tree now v1.20.1) |
| idea-engine | #740 | open · ready |
| superbot-next | #602 | open · ready |
| websites | #452 | open · ready |
| trading-strategy | #160 | open · ready |
| superbot-games | #183 | open · ready |
| venture-lab | #282 | open · ready |
| superbot-mineverse | #138 | open · ready |
| fleet-manager | #390 | open · ready |
| superbot | — | skip · not-applicable (pin-only nominal adoption, pin 1.0.0; no vendored dist / .substrate state — dist-vendoring upgrade N/A) |
| pokemon-mod-lab | — | DARK (private) · skipped, adoption UNKNOWN |

Two transient auto-mode-classifier denials occurred on worker-SPAWN (superbot special-framing + gba-homebrew) — both cleared on a neutral retry; transient venue/classifier states, NOT adopter-side walls and NOT standing walls (deliberately not recorded as capability walls).

## Registry / docs
- `docs/adopters.md` regenerated via `bootstrap currency` (12-repo scan; `currency --check` exit 0 — current). Rows reflect each adopter's main-branch tree (still pre-upgrade for the 8 open PRs — the correct truth; an open PR is not in the tree). Hand-added `## v1.20.1 distribution wave (2026-07-20)` bullet section records the pending PRs the rows-only scan cannot see.
- Version truth is the generated registry + each repo's committed tree, never this `kit:` line (self-reports lag by design).

## PR state
- Wave-lane PR #548 (this session): log + heartbeat + adopters.md regen; born-red HOLD until the card flips complete, then lands on green.
- Prior seat-session PRs terminal MERGED through #550. The wave-2 buildable ladder S2–S17 is EXHAUSTED (band consumed); the baton-freshness advisory (#545) shipped. Remaining agent-buildable slice: none — remaining work is owner-gated (⚑ set below) or resident-side (the 8 open adopter upgrade PRs).

## Routine / trigger state (no writes this wake)
- ARMED (active failsafe, F-1): `trig_01194PdaWChtHGNKASURxdLx` "Self Improvement failsafe wake", cron `2 */2 * * *`, bound to the coordinator session — the dead-man bridge. LEFT UNTOUCHED this wake.
- No routines armed/deleted; no trigger APIs called. ORDER 024 bars re-arming routines pending the per-seat reboot go.

## ⚑ FOR OWNER (standing set)

⚑ adopter-distribution wave — RESOLVED (2026-07-20, wave-lane PR #548)
The v1.20.1 adopter-upgrade wave ran under fm ORDER 048. Evidence: 9 vendoring adopters swept, upgrade PRs opened ready against release v1.20.1 (tag v1.20.1 → 40eb0fe, dist sha256 d6c4f81565f8877f38e2b4315968fc5f22a378c9c4dfdd89f8ed02827e7f6b39) — gba-homebrew #211 (MERGED), idea-engine #740, superbot-next #602, websites #452, trading-strategy #160, superbot-games #183, venture-lab #282, superbot-mineverse #138, fleet-manager #390. superbot = pin-only skip; pokemon-mod-lab = DARK. No owner action: each remaining PR is the resident seat's to merge; each reds only on pre-existing resident-owned false-wall/badge doc content.

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2318 entries paginated to exhaustion 2026-07-17; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
  WHERE:  docs/operations/lab-loop.md asserts it "stays armed across every cutover"; the registry has nothing to keep. The doc documents NO deliberate disarm — the loop is owner-armed-only (👤 P4, console Schedule) and cannot arm itself.
  HOW:    (A) RECREATE — owner arms a daily `0 6 * * *` UTC Schedule in the Claude Code console pointed at the kit-lab loop; (B) RETIRE — remove the "stays armed" line from lab-loop.md and mark the loop dormant-by-design pending reboot.
  WHY:    doctrine and reality contradict; a rebooted seat reads "armed" and trusts a loop that never runs. ORDER 024 also bars the seat from re-arming routines pending the per-seat reboot go, so it will not create the cron unilaterally.
  UNBLOCKS: honest lab-loop doctrine — either daily owner business resumes (A) or the false "armed" claim is removed (B).
  VERIFY: (A) the Schedule shows in the console trigger list and a 06:00Z run lands; (B) `grep -n "stays armed" docs/operations/lab-loop.md` returns nothing.
  RISK: ↩️ reversible either way. RECOMMENDATION: **A — recreate** (lab-loop.md frames it as genuine daily owner business; retiring silently drops it over a transient cutover gap; re-arming is one console action gated on the reboot go). Answer: A (recreate) / B (retire).

⚑ public-flip-or-PAT (pick one)
  WHAT: Let the other fleet repos read this one — either make it public or mint a read-only token.
  WHERE: P11: Settings → General → Danger Zone → Change visibility · P13: github.com/settings/tokens → fine-grained read-only PAT scoped to this repo, then add it to the fleet environments.
  HOW: P11 is click-through; P13 is create-token + paste into environment settings.
  WHY: sibling repos cannot read kit data today, so cross-repo sweeps and the merged console run blind.
  UNBLOCKS: B2–B4 cross-repo sweeps + kit data in the merged console.
  VERIFY: a sibling-seat session fetches a kit file read-only without "Access denied: repository … is not configured for this session".
  RISK: ⚠️ P11 effectively irreversible (history exposed once public) · ↩️ P13 reversible — revoke anytime. RECOMMENDATION: **B — mint a read-only PAT** (reversible; no history exposure).

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

orders: acked=001-024 done=001-024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024); its work is DONE (PR #340). The inbox `status:` field is manager-owned — an order reading `status: new` while this file's `done=` covers it is DONE-and-awaiting-manager-flip, not open.
