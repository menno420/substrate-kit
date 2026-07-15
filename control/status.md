# Self Improvement seat — heartbeat
updated: 2026-07-15T15:55Z · phase: EAP EXTENSION ACTIVE (EAP through 2026-07-21; inbox consumed 001–024; routines coordinator-managed)

## This wake (2026-07-15 · work slice · claude/order-claim-collision-completion · PR #397)
- Baton item 2 completed (no inbox ORDER above 024 at sync HEAD 311841d; control/claims/ held README only at the ~15:5xZ scan; zero open PRs at open; `currency --check` exit 0 — no regen slice due): the cross-branch ORDER-collision idea (docs/ideas/order-claim-cross-branch-collision-2026-07-14.md). Finding: the mechanism already shipped in PR #365 (2026-07-14 — claim `--order` segment + `claims-order-collision` advisory + verb refusal) but three doc segments never landed; this slice landed them: (1) idea lifecycle flip (frontmatter was still `captured`/`shipped_pr: null` — drift fixed on sight) + README index row Backlog → Shipped; (2) local control/claims/README.md synced to the shipped template (the `--order NNN` paragraph + the `claims-order-collision` advisory row were missing — a live instance of the template↔local-copy lag class); (3) lab-loop prompt STEP 2 CLAIM-BEFORE-BUILD line (the idea's part 3 boot-time visibility). Docs-only, no engine change, no dist delta beyond the byte-pin regen check.
- Note for the merger/owner: docs/operations/lab-loop.md's fenced prompt changed — per that file's change discipline the console Schedule copy needs a re-paste after merge (git is the prompt's source of truth).
- Verify (at fa118d7): `python3 scripts/preflight.py` → 8/8 legs green (pytest 1608 passed 1 skipped; dist-byte-pin; ruff; idea-index; retro-index; changelog-structure; program-law; bench-integrity). `dist/bootstrap.py check --strict` → designed born-red HOLD only (this wake's card, pre-flip) + known staged-regen-lag ×3; guard-fires telemetry deltas committed per the checker instruction.

## Routine state (observed facts — trigger inventory carried from the 2026-07-15 ~04:4xZ read-only list_triggers pass; this wake armed no triggers)
- This session armed no triggers and ran no new trigger inventory. Routines are coordinator-managed this wake.
- Carried observation (04:4xZ pass): "Self Improvement failsafe wake" trig_01CUfSZo9Uky9DdpoqpZPcfT — cron `0 */2 * * *`, enabled=true, created 2026-07-15T04:38:07Z via meta_mcp, bound to a coordinator session (persistent_session_id session_01SFVAo5bPD41RMx9TzGxnPY) — plus one pending one-shot pacemaker (run_once_at 2026-07-15T04:55:00Z, same session binding). Not created by this seat's sessions.
- ⚑ FOR OWNER REVIEW: ORDER 024 (control/inbox.md @ 58b3f80) states "do NOT re-arm routines yet; wait for the owner's per-seat go (the v3.6 reboot prompt IS that go)". The observed failsafe above post-dates that order. This heartbeat records the discrepancy neutrally for the owner's review/veto; it does not adjudicate it. Prior heartbeat (git history @ 58b3f80) had recorded all seat routines verified DOWN; kit-lab daily loop re-arm recipe remains docs/operations/lab-loop.md.

## State
- kit: v1.17.0
- v1.17.0 distributed 9/9 engaged adopters; registry (docs/adopters.md, generated 13:14:20Z at #391) current — the 15:4xZ `currency --check` live run confirmed exit 0 (12 repos, rows-only compare, zero delta); DRIFT rows unchanged (superbot-next, superbot-games, superbot-mineverse self-report lag + kit's tree-internal pin row).
- Wake currency scan is turnkey (#392): `python3 dist/bootstrap.py currency --check` — exit 0 registry current / exit 1 regen slice due (changed rows printed). Use it instead of hand-fetching adopter `kit:` lines.
- Cross-branch ORDER-collision guard fully closed (#365 mechanism + #397 doc segments): work claims carry `--order NNN`, `check_claims` emits `claims-order-collision`, the claim verb refuses cross-branch duplicates, and the lab-loop prompt now claims-before-build; console re-paste of the lab-loop fenced prompt pending post-merge.
- Plain-adopt lane-drift advisory (#396): `adopt` without `--lane` into a lane-shaped repo (non-default `heartbeat_files`) now nudges `adopt --lane <name>` as the first report line — advisory, never a refusal; adopters inherit on next upgrade/regen wave.
- Delegated-tally doctrine (#395): coordinator-written heartbeats are marked, member repos carry a live-tally pointer, sweeps classify by PR record + coordinator status — `control/README.md` § "Delegated tally" (template: control-README.md.tmpl; adopters inherit on next upgrade/regen wave).
- Model-line effort taxonomy (#394): `unrecorded` is the sanctioned terminal value for retro-repaired cards whose authors never self-reported effort — advisory-silent, harvested verbatim; live sessions still report `low|medium|high` (.sessions/README.md teaches the reservation).
- Grounded-skills measurement: harness MERGED (#386, main @ c5380dc) — turnkey: `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton
1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md (turnkey since #386 merged; PR #247 methodology; owner silence accepts); publish the findings report under docs/reports/ and link it from the operations index.
2. Groom the template↔local-copy sync advisory (💡 from the #395 card, card-only today) into docs/ideas/ — fresh evidence this wake: PR #397 hand-fixed a live instance (control/claims/README.md lagged the shipped control-claims-README.md.tmpl by a whole feature paragraph); a checker comparing planted local copies against their templates would have caught it mechanically. Alternative buildable idea if grooming feels thin: the engagement native-consumer state (docs/ideas/engagement-native-consumer-state-2026-07-12.md, post-freeze quick-win).

## ⚑ FOR OWNER (standing set carried forward — NO new asks this wake)

⚑ P10 required-check swap
WHAT: Swap which CI check main requires, from the two legacy names to the current one.
WHERE: repo Settings → Rules → the `main` ruleset → required status checks.
HOW: remove "Kit test suite" and "Cold-adoption smoke (adopt + check --strict)"; add `kit-quality` (source: GitHub Actions); set "Require branches to be up to date" OFF.
WHY: the legacy alias jobs exist purely to satisfy the old required names; the up-to-date requirement stalls green PRs `behind`.
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

orders: acked=001–024 · done=001–024
