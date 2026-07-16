# Self Improvement seat — heartbeat
updated: 2026-07-16T09:51:29Z · phase: SEAT CLOSING (EAP through 2026-07-21; inbox consumed 001–024; buildable backlog dry — remaining items date-parked; seat idles on the 2h failsafe bridge)

## This wake (2026-07-16 close-out slice) — SEAT-CLOSING HEARTBEAT

- Wake source: coordinator-dispatched close-out slice; control-only diff (status heartbeat), card-less fast lane.
- **PR ledger settled: #414–#426 ALL MERGED on green. Zero open seat PRs** (verified live 2026-07-16T09:47Z: open-PR list empty; #426 merged 2026-07-16T04:00:09Z — this fixes the prior heartbeat's stale "#426 OPEN" line).
- Merged this calendar day: #414 S3 · #415 · #416 S4 · #417 · #418 v1.18.0 bump · #419 close-out · #420 KL-5 residue generalization · #421 · #422 status-badge value-parse fix · #423 · #424 archive S2 evidence-hint coverage + adopt-planted surface settled empty · #425 claim prune · #426 valueless-badge grammar finding + residue coverage pin. Release v1.18.0 out (run 29466068874, sha256 three-way PASS — full record @ 13a0b44 history).
- Denial records live in PR bodies, not here: adopter-wave classifier denial verbatim in the **PR #420 body** (§ "Denial routing"). This heartbeat carries pointers + asks only.

## Backlog — HONEST readout (carried)

**Buildable backlog DRY.** #426 landed the last coordinator-judged buildable item. Everything remaining is DATE-PARKED, not buildable now:
- Grounded-skills measurement window opens ~2026-07-19 (run ~07-19..26 per docs/operations/grounded-skills-measurement.md; owner silence accepts).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period — `session-card-slot-residue` + archive advisories proving quiet on genuine cards/notes across a few sessions.
- v1.18.0 adopter wave: awaits owner authorization (⚑ below; denial record in PR #420 body).
Seat idles on the 2h failsafe trigger between now and the earliest of those dates.

## Routine / trigger state — verified via list_triggers at 2026-07-16T09:51Z (paginated to end, 21 pages)

- This seat's ONLY trigger: `Self Improvement failsafe wake` trig_01AHRsGDBmbSDAc8AkjU2zJN · cron `0 */2 * * *` · ENABLED · bound to persistent session session_01TEnyj8QTuxfywgYwWP75Am · next fire 2026-07-16T10:07Z. It is the successor's dead-man bridge; no other trigger of any kind is bound to this seat's session anywhere in the full listing.
- The three send_later one-shots the 01:52Z audit saw pending (created 01:37–01:43Z) have all since fired (`ended_reason=run_once_fired`); none was bound to this seat's session (they target other seats' persistent sessions). Zero pending send_later one-shots bound to this seat.
- Fleet-wide, one send_later remains pending at audit time (trig_01Rs2X36wg6GzKYtnhdnDt9B, fires 2026-07-16T10:12Z, bound to the Fleet Manager session) — noted for completeness; not this seat's.
- ⚑ FOR OWNER REVIEW (carried forward): ORDER 024 says "do NOT re-arm routines yet; wait for the owner's per-seat go". The enabled failsafe above (created 2026-07-16T01:09Z) post-dates that order. Recorded neutrally for owner review/veto; not adjudicated here. Kit-lab daily loop re-arm recipe: docs/operations/lab-loop.md.

## State

kit: v1.18.0
- Session gate judges the badge VALUE, not line prose (#422), and a present-but-valueless badge is a grammar finding, never a release (#426 MERGED) — the value-grammar family closed.
- KL-5 residue program: every named drafted-fill surface covered or settled (#420 cards · #424 archive S2 hints + adopt-planted settled empty) AND mechanically pinned (#426 coverage pin — unguarded future surfaces fail the suite). Remaining deliberate step: PL-008 graduation of the advisories once proven quiet across sessions.
- Registry (docs/adopters.md): regenerated at v1.18.0 (#419); every adopter row reads stale until its own upgrade wave (parked — see ⚑ ask; denial record in PR #420 body).
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); turnkey `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol pre-registered at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. Grounded-skills measurement window ~2026-07-19..26 — run per docs/operations/grounded-skills-measurement.md, publish the findings report under docs/reports/.
2. KL-5 gate graduation (deliberate, PL-008) on quiet evidence: once `session-card-slot-residue` + the archive advisories prove quiet on genuine cards/notes across a few sessions, graduate them into the merge-blocking gate lanes.

## ⚑ FOR OWNER (standing set carried forward + one new ask)

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

Standing (full paste-ready blocks verbatim in git history of this file @ 86d2a57):
- fm #122 v3.4 restamp — owner reviews/merges PERSONALLY.
- UNIVERSAL wake fetch-list vN bump (+ docs/seat-digest.md, docs/SKILLS.md).
- Grounded-skills measurement window ~2026-07-19..26 — silence accepts.

orders: acked=001–024 · done=001–024
