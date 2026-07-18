# Self Improvement seat — heartbeat
updated: 2026-07-18T00:51:54Z · phase: routine failsafe wake — rung-2 DRIFT verdict landed (#442) + failsafe trigger-id correction

> **Orders done-truth (read this first):** orders **001–024 are ALL DONE** — the `done=` line at the end of this file is the seat's completion signal. The inbox `status:` field is **manager-owned** and is flipped `new→done` manager-side only after the manager reads this status report (control/README.md:86), so an inbox order reading `status: new` while this file's `done=` covers it means **DONE-and-awaiting-manager-flip, not open**. No ORDER >024 exists in control/inbox.md at HEAD; "ORDER 025" is not a standalone bound order — it is the `>`-quoted fm relay inside ORDER 019 item 5 (highest bound order = 024). Its WORK is nonetheless COMPLETE: both cfgdiff writeups are on main (docs/reports/2026-07-09-cfgdiff-differential-testing-method.md + …-v0.1.1-release-decision.md), linked from bench/README.md, merged via PR #340 (2026-07-13). The redundant standalone ORDER-025-block append that hit the classifier wall is therefore MOOT.

## This wake (2026-07-18 · routine failsafe · rung-2 investigation + heartbeat)

- **Verified PR #441 landed:** MERGED by github-actions[bot] 2026-07-17T22:37:47Z (head SHA 87dd52a), all 4 checks green — `kit-quality` success (Actions run 29618412439). No open PRs in the repo — chain clean.
- **Rung-2 (baton + docs/adopters.md re-verify) — superbot-games DRIFT investigated; verdict = document-not-act.** The registry's superbot-games row (docs/adopters.md:31) reads tree v1.17.0 with three self-report DRIFT bullets (docs/adopters.md:44-46). Root cause is **adopter-side self-report lag, correctly detected — not a discovery bug, not a stale adopters.md value** (adopters.md is fresh generated output; header `Generated: 2026-07-17T20:34:39Z`). Breakdown:
  - `control/status.md` claims v1.15.0 vs tree v1.17.0 — a **genuine, canonically-shaped self-report** never re-stamped when the repo upgraded its dist to v1.17.0 (the release-notes "update your `kit:` line" step skipped). Real lag.
  - `control/status-mining.md` + `control/status-exploration.md` claim v1.7.1 — **historical adoption-prose** on superbot-games' two *consuming* lanes ("adopted... CONSUMES it"), which adopt-once and don't independently version; the lenient `KIT_VERSION_TOKEN_RE` parser reads the historical token as a current claim → two false-positive DRIFT rows.
  - **No clean kit-only fix.** KF-2: kit-lab has zero write access to adopter repos, and adopters.md itself says reconcile at the SOURCE, never by hand-edit. The status.md re-stamp is superbot-games' own tree → owner-gated (effectively part of the v1.18.0 adopter wave). The one kit-side lever (prune the two lane-heartbeat tokens from docs/fleet-repos.txt) is **declined** — it silences the two false-positive rows by *reducing observability* (hiding lanes that could later carry a real self-report): a cosmetic win at a truth cost. Full breakdown folded into the ⚑ v1.18.0 wave ask below.
- Housekeeping: pruned stale claim `claude-adopters-version-home-lag.md` (PR #441 terminal/merged).
- **Correction (TRUTH bar):** the failsafe trigger id carried in prior heartbeats (`trig_01Mw9yn9r21Bi5q19v7QcqjN`) does NOT exist — it was a carried-forward invention, not a live read. Coordinator's live `list_triggers` audit (2,383 triggers, 24 pages, 2026-07-18T00:5xZ) shows the only armed Self Improvement failsafe is `trig_01BcfHTVwmwogjDycfmWBtt7` (cron `21 */2 * * *`, coordinator-session-bound, next fire 02:21Z). Chain intact (net effect zero); pointer corrected below so the next wake stops re-propagating the wrong id.

## PR state (verify live before trusting — MCP PR reads lag ~25 min)

- **No open PRs** at investigation time. PR #441 MERGED 2026-07-17T22:37:47Z @ 87dd52a; #440/#439/#438 MERGED terminal; #433 CLOSED unmerged 2026-07-17T13:21Z. This wake's heartbeat PR opens control-only (fast lane, green by design).

## Backlog — HONEST readout (carried)

Buildable, non-gated backlog is **thin** (unchanged from the 2026-07-17 rung-4 wake, which consumed the strongest self-initiated rung). This wake found **no new order** (none >024 at inbox@HEAD) and **no appropriate kit-only build** on rung 2 (the superbot-games DRIFT is owner-gated adopter-side — above); rung 3 (template/gate/graduation) surfaced no concrete ripe candidate. Honest outcome: a rung-2 investigation recorded + heartbeat, no code PR. Remaining rungs owner-gated / date-parked:
- Owner veto pass over the 23-proposal menu (docs/planning/2026-07-16-overnight-veto-menu.md) — baton #1.
- Grounded-skills measurement window opens ~2026-07-19 (docs/operations/grounded-skills-measurement.md; owner silence accepts).
- KL-5 gate graduation (PL-008): awaits the advisory quiet period.
- v1.18.0 adopter wave: awaits owner authorization (⚑ below) — now carries the superbot-games DRIFT breakdown.
Seat idles on the 2h failsafe trigger between now and the earliest gated date.

## Routine / trigger state (carried pointer)

- **failsafe `Self Improvement failsafe wake`** — `trig_01BcfHTVwmwogjDycfmWBtt7`, cron `21 */2 * * *`, ENABLED, coordinator-session-bound, next fire 02:21Z (per the coordinator's live `list_triggers` audit 2026-07-18T00:5xZ — 2,383 triggers, 24 pages; supersedes the invented `trig_01Mw9yn9r21Bi5q19v7QcqjN` carried by prior heartbeats). Source = live read, not memory.
- pacemaker chain: no new one-shots armed this wake.
- kit-lab daily 06:00Z cron: ABSENT from the registry (⚑ A/B below, unchanged).

## State

kit: v1.18.0
- Registry (docs/adopters.md): last regenerated by discovery in #440; superbot-games row DRIFT re-verified this wake (adopter-side self-report lag; breakdown above) — owner-gated, no kit-only fix. Every adopter row reads stale until its own v1.18.0 upgrade wave (parked — ⚑ ask).
- `adopters-version-lag` advisory (#441) + `adopters-stale` (calendar-age) pair now covers both staleness axes.
- Session gate judges the badge VALUE not line prose (#422); no-badge + modified-lane parity landed (#428/#429); value-grammar family closed.
- Wake currency scan turnkey (#392): `python3 dist/bootstrap.py currency --check`.
- Grounded-skills measurement: harness MERGED (#386); turnkey `python3 scripts/measure_grounded_skills.py --clone --workdir <dir> --json <f> --out <f>`; protocol at docs/operations/grounded-skills-measurement.md.
- Revival boot reading: CONSTITUTION.md → control/inbox.md → this file → docs/eap-closeout-walkthrough-2026-07-14.md §E → docs/audits/eap-project-audit-2026-07-14.md.

## Next-2 baton

1. **Owner veto pass** over docs/planning/2026-07-16-overnight-veto-menu.md (23 proposals) — build the survivors once vetoed.
2. Date-parked / owner-gated (unchanged): grounded-skills window ~2026-07-19..26; KL-5/PL-008 graduation awaits the advisory quiet period; v1.18.0 adopter wave awaits owner authorization (now with superbot-games DRIFT breakdown).

## ⚑ FOR OWNER (standing set carried forward)

⚑ FOR OWNER — kit-lab daily cron: recreate or retire? (A/B)
  WHAT:   The 06:00Z 'kit-lab daily' owner-business cron is absent from the account trigger registry (coordinator-reported: ~2318 entries paginated to exhaustion 2026-07-17; no kit-named or hour-6 cron; never created or deleted — not re-verified by this stateless seat).
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
  NOTE (superbot-games, added 2026-07-18 rung-2 re-verify): its DRIFT row is 1 genuine self-report lag + 2 consuming-lane false-positives. The wave clears the genuine half when superbot-games re-renders + re-stamps its own control/status.md v1.15.0→v1.18.0. The two consuming lanes (control/status-mining.md / control/status-exploration.md, v1.7.1 adoption-prose) will NOT clear on a version bump — their `kit:` lines are historical prose, not current claims; either reword them adopter-side, or (kit-side, NOT recommended) prune their tokens from docs/fleet-repos.txt at the cost of lane observability.

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

**Consuming-lane roster annotation for multi-lane adopters.** superbot-games is the fleet's only multi-lane adopter; its two *consuming* lanes (status-mining / status-exploration, which adopt-once and don't independently version) surface historical `kit:` prose as false-positive DRIFT rows in docs/adopters.md, because the discovery parser reads any version token as a current claim. A roster annotation in docs/fleet-repos.txt (e.g. a `consumes:` marker per lane) would let discovery still SCAN those lanes (observability kept) but classify their disagreement as informational, not DRIFT — sharpening the registry the owner reads to plan a wave. Genuinely believe in it but **low-priority / one-adopter today**: worth building only if multi-lane adopters proliferate; the simpler true-fix stays adopter-side rewording. Distinct from the prev card's "kit's-own-row self-DRIFT" idea (that couples the kit's dist header to its own registry row; this classifies *adopter consuming-lane* rows). Not built.

## ⟲ Previous-session review (Q-0102)

Of the adopters-version-home-lag session (card .sessions/2026-07-17-adopters-version-home-lag.md): genuine remark — it did the disciplined thing, choosing the git-free version-value comparison over the idea's literal git-log signal once it hit the §3.2 subprocess ban, and folded the "checker constraints apply" lesson back so the next builder inherits the boundary — a clean idea→build→refined-idea link. Small miss: its 💡 idea (kit's-own-row self-DRIFT nag) and this wake's rung-2 finding both circle the SAME registry-truth surface (recorded self-report vs live tree), yet the card didn't note that the *adopter* rows (superbot-games) carry a louder version of the same drift class — so this wake re-derived the adopter-side breakdown from scratch. System improvement it surfaces: a session that ships a registry-truth guard should, in its card, name the *adjacent* registry rows still un-guarded (here: adopter self-report lag) so the successor inherits the map instead of re-investigating — folded into this heartbeat's ⚑ wave note + session idea. Beyond that, nothing to invent.

orders: acked=001–024 · done=001–024
note: "ORDER 025" is the `>`-quoted fm relay inside ORDER 019 item 5, not a standalone bound order (highest bound = 024). Its WORK is DONE — both cfgdiff writeups on main + linked from bench/README.md, merged via PR #340 (2026-07-13); the redundant standalone-block append that hit the classifier wall is MOOT.
