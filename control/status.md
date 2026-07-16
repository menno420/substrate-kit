# Self Improvement seat — heartbeat
updated: 2026-07-16T16:16:39Z · phase: 1 work PR in flight (#432 staged-regen render; #430 registry refresh merged at HEAD)

## This wake (2026-07-16 close-out slice) — SEAT-CLOSING HEARTBEAT

- Wake source: coordinator-dispatched close-out slice; control-only diff (status heartbeat), card-less fast lane.
- **PR ledger: #414–#429 ALL MERGED on green; #430 now OPEN** (#429 merged at HEAD d007294 — the no-badge grammar graduation into check_log + shared `_status_grammar_findings` helper landed; #430 opened this wake on top of it).
- **#430 MERGED at HEAD (registry refresh).** **#432 OPEN — re-render staged .substrate/ tree (architect.md, reviewer.md, claude/CLAUDE.md) to clear 3 staged-regen-lag advisories · auto-merge armed SQUASH 2026-07-16T16:13:43Z · born-red, self-lands on green at card flip.** The staged tree carried unrendered `${slot}` tokens for interview slots filled since #381; the kit's own render path (`agents --build` + scoped `adopt` keeping only `.substrate/claude/CLAUDE.md`) fills them — net diff exactly 3 files, `check --strict` staged-regen-lag advisories → 0. Registry-refresh detail below reflects #430 as merged.
- Merged this calendar day: #414 S3 · #415 · #416 S4 · #417 · #418 v1.18.0 bump · #419 close-out · #420 KL-5 residue generalization · #421 · #422 status-badge value-parse fix · #423 · #424 archive S2 evidence-hint coverage + adopt-planted surface settled empty · #425 claim prune · #426 valueless-badge grammar finding + residue coverage pin. Release v1.18.0 out (run 29466068874, sha256 three-way PASS — full record @ 13a0b44 history).
- Denial records live in PR bodies, not here: adopter-wave classifier denial verbatim in the **PR #420 body** (§ "Denial routing"). This heartbeat carries pointers + asks only.

## Backlog — HONEST readout (carried)

**Buildable backlog DRY beyond date-parked / owner-gated items.** This session took the one open contained rung — the adopters.md registry refresh (#430). Everything remaining is DATE-PARKED or OWNER-GATED, not buildable now:
- Grounded-skills measurement window opens ~2026-07-19 (run ~07-19..26 per docs/operations/grounded-skills-measurement.md; owner silence accepts).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period — `session-card-slot-residue` + archive advisories proving quiet on genuine cards/notes across a few sessions.
- v1.18.0 adopter wave: awaits owner authorization (⚑ below; denial record in PR #420 body).
Seat idles on the 2h failsafe trigger between now and the earliest of those dates.

Neutral findings verified this session (facts, not new work): ORDER 048 autonomy doctrine already graduated as [PL-012] (verified — no new graduation needed); the lowercase `docs/capabilities.md` pointer is already fixed + test-guarded; no new CAPABILITIES denial was hit this session (no git-stash / auto-mode block occurred — the earlier-queued entry premise was not reproduced).

## Routine / trigger state — COORDINATOR-REPORTED via session relay

Routine facts below are COORDINATOR-REPORTED via session relay (coordinator's own paginated list_triggers snapshot 2026-07-16T14:16:39Z); this stateless seat did not independently re-verify the trigger registry — recorded with provenance for cutover audit, not as this seat's verified state.

- **failsafe `Self Improvement failsafe wake`** (coordinator-reported) — trigger `trig_01Mw9yn9r21Bi5q19v7QcqjN`, cron `0 */2 * * *`, reported ARMED + bound to the coordinator session, next fire reported 2026-07-16T16:01:36Z.
- **pacemaker send_later** (coordinator-reported) — `trig_017ANi5hZQmyFM5tdjHeaHGv` → coordinator, reported firing 14:21Z.
- **prior/stale twin** (coordinator-reported) — `trig_01AHRsGDBmbSDAc8AkjU2zJN` (prior seat session `session_01TEnyj8QTuxfywgYwWP75Am`, reported last fired 12:11Z; reported to have spawned a ghost wake session 14:09Z, stood down) — record as **deleted (coordinator-reported, server-confirmed; not re-verified by this seat)**.

## State

kit: v1.18.0
- Session gate judges the badge VALUE, not line prose (#422), and a present-but-valueless badge is a grammar finding, never a release (#426 MERGED) — the value-grammar family closed.
- KL-5 residue program: every named drafted-fill surface covered or settled (#420 cards · #424 archive S2 hints + adopt-planted settled empty) AND mechanically pinned (#426 coverage pin — unguarded future surfaces fail the suite). Remaining deliberate step: PL-008 graduation of the advisories once proven quiet across sessions.
- Registry (docs/adopters.md): regenerated at v1.18.0 (#419); every adopter row reads stale until its own upgrade wave (parked — see ⚑ ask; denial record in PR #420 body).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); turnkey `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. **SHIPPED this session** — staged-regen render (#432): re-render the staged `.substrate/` tree (architect.md, reviewer.md, claude/CLAUDE.md) so interview slots filled since #381 render, clearing the 3 staged-regen-lag advisories; self-lands on green at card flip. (Prior slice #430 adopters.md registry refresh — merged at HEAD.)
2. Date-parked / owner-gated (unchanged): grounded-skills window ~2026-07-19..26; KL-5/PL-008 graduation awaits the advisory quiet period; v1.18.0 adopter wave awaits owner authorization.

## ⚑ FOR OWNER (standing set carried forward + one new ask)

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2021 entries paginated to exhaustion 2026-07-15; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
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

⚑ **Kit self-pin version-truth ruling (§7)** — the kit's own adopters.md row shows a permanent cosmetic tree-internal DRIFT.
- WHAT: rule how the kit's OWN substrate.config.json pin should read so `currency` stops emitting a permanent tree-internal DRIFT row on substrate-kit itself.
- WHERE: substrate.config.json `kit_version: 1.0.0` vs tree dist/bootstrap.py v1.18.0; emitted by src/engine/currency.py drifts(); surfaces on every docs/adopters.md regen.
- HOW (A/B): **A (recommended)** — bump the kit's own pin to track its release (pin == KIT_VERSION, bumped at each release cut) ↩️ reversible; B — teach currency.drifts() the source repo's own pin is N/A (a floor, never DRIFT) and suppress/annotate that one row ↩️ reversible.
- WHY: it is the only permanent false-DRIFT in the registry; it muddies every currency scan and the registry-truth signal.
- UNBLOCKS: a clean self-row on adopters.md; clears the 2026-07-11 "§7 version-truth" retro park.
- VERIFY: after the ruling, `dist/bootstrap.py currency` shows substrate-kit `current` with no tree-internal drift line.
- RISK: ✅ (both options contained + reversible; no adopter writes).

Standing (full paste-ready blocks verbatim in git history of this file @ 86d2a57):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–024 · done=001–024
