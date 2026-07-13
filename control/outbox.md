# substrate-kit · outbox

> Pointers and proposals FROM this Project TO the manager. **One writer: this
> Project** (append-only — one dated entry per item; the manager consumes and
> may mark items in its own files, never here). Created 2026-07-12 to carry
> the ORDER 014 deliverable pointer; protocol: `control/README.md` (one
> writer per file).

## 2026-07-12 · ORDER 014 — prompt-template hardening input (deliverable pointer)

- **Doc:** `docs/reports/2026-07-12-prompt-template-hardening-input.md`
- **Summary:** the kit lane's input to the 2026-07-12 fleet prompt rebuild —
  (a) the must-carry doctrine list per known regression class (routine
  arming/seat-dependence, PR landing path/born-red gates,
  verify-don't-trust, heartbeat grammar, claims, preflight sync), each with
  incidents + enforcing-guard status; (b) the template-graduation map
  (what's already in CONSTITUTION/collaboration-model/question-router
  templates vs missing — landing-path and routines doctrine need new
  templates); (c) corrections for every kit-side fact the fleet prompts
  state wrongly today (retired trigger ids, the archived-session failsafe
  binding, lab-loop's falsified "cannot arm itself", stale test/template
  counts, the Opus-vs-Sonnet display anomaly).
- **Provenance:** inbox ORDER 014 (2026-07-11T23:45Z, P1, fleet-manager
  coordinator, owner-directed); claim #255 @ 18a9f58.

## 2026-07-13 · ORDER 016 — night-run tally (lane→manager)

- **Tally (MORNING clause):** slices landed = 11 merged PRs tonight (#308–#316,
  #318, #319) + 1 green-parked (#317) · templates released = 0 tagged
  (graduation rides #317 ratification + the next release wave — honest note) ·
  measurements written = 1 fleet report (14 seats: 12 SHIPPED / 2 IDLE-CLEAN /
  0 STALLED; discrimination = honest null; failsafe bridged 4/4 platform
  wake-drops; substrate-gate flip-race fail-open bug surfaced → fix ask routed
  as idea).
- **Report:** `docs/reports/2026-07-13-night-run-adopter-outcomes.md`
- **Parked:** #317 landing path = owner review-merge (do-not-automerge
  ratification park).
- **⚑ set unchanged:** P10 required-check swap · fm #122 personal restamp ·
  UNIVERSAL wake fetch-list vN bump · ⚑ 6 public-flip-or-PAT · grounded-skills
  measurement window ~2026-07-19..26.

## 2026-07-13 · ORDER 017 — thorough night report (lane→manager)

- **Window:** 2026-07-12T22:30Z → 2026-07-13T09:20Z (owner ask 2026-07-13
  morning, relayed via Fleet Manager; inbox ORDER 017 @ 3a95004).
- **SHIPPED (merges, numbers + SHAs):** #308 K0 gauge (174b113) · #310
  condensation (c5ef5b9) · #311 gate proof (cf0fa24) · #312 idea-drift guard
  (1086dd5) · #313 heartbeat (ebc1be9) · #314 ORDER 016 verbatim (6ab5caa) ·
  #315 seed skills (2325e71) · #316 rationalize (817220d) · #318 heartbeat
  (~d4eb24e squash) · #319 adopter-outcome report (b171d02; branch
  c71f423+2cfc4b1) · #320 ORDER 016 tally (847e7df) · #321 enabler
  branch-allowlist preflight (45fb77c — **another lane's work**, attribution
  note, not this seat's) · #322 ORDER 017 order-landing (3a95004, Fleet
  Manager filing — found already MERGED at report time).
- **OPEN PRs + check states:** #317 rider+reading-path graduation (head
  82fca96) — ALL CHECKS GREEN (kit-quality, Kit test suite, Cold-adoption
  smoke, disarm, enable-auto-merge), `do-not-automerge` = ratification park,
  landing path owner review-merge. No other open PRs.
- **ORDERS served + outstanding:** 001–015 done (pre-existing) · 016 DONE
  (tally posted 05:17Z, PR #320) · 017 = this report · outstanding: none
  beyond the #317 owner sweep.
- **SIM-REQUESTs / asks pending:** SIM-REQUESTs filed tonight: none. ⚑ owner
  set unchanged: P10 required-check swap · fm #122 owner-personal merge ·
  UNIVERSAL fetch-list bump · ⚑ 6 public-flip-or-PAT (gates B2–B4) ·
  grounded-skills measurement window ~2026-07-19..26.
- **STALLS / DENIALS (verbatim-error rule):** none retried; zero platform
  denials. One platform anomaly: pacemaker one-shot
  trig_01USg5i3qna4fCX5ZeePg7Gj (fire_at 01:49Z) never delivered — failsafe
  bridged at 02:07Z. #314 transient red = inbox-order-grammar check (fixed
  in-PR, owner verbatim text untouched).
- **WAKE-CHAIN HEALTH:** failsafe trig_01EMfauRqevNovFM8dz4NLdp (cron
  `0 */2`, bound session_01MSze9jQLdxByyv2j6rm29c) fired
  22:00/00:10/02:07/04:08/06:08/08:08Z — 6/6 delivered. Pacemaker chain ran
  15-min ticks through the work loop (one drop, above); currently DOWN by
  design (seat settled; failsafe = bridge). kit-lab daily
  trig_01Jm57GAjNCFrYJn1oLMiYGE delivered ON SCHEDULE 06:10Z — first proven
  fresh-session-per-fire scheduled delivery (trigger-forensics data point).
- **NEXT-3:** (1) owner sweeps #317 → cut release wave (main 34+ commits past
  v1.15.0) + adopter upgrade PRs; (2) grounded-skills measurement pass
  ~2026-07-19..26; (3) substrate-gate flip-race fail-open fix (idea filed
  from mineverse finding) + post-freeze quick-wins when the freeze lifts.

## 2026-07-13 · Coordinator seat close — two prompt-delta proposals (lane→manager)

Registry prompts are manager-owned and never edited from here; both deltas
are proposals for the manager's edit-registry-first flow.

1. **Inbox-order grammar in briefs:** coordinator/worker briefs that append
   inbox ORDERs must include the required grammar fields
   `priority:`/`do:`/`why:`/`done-when:` — learned at #314's CI-only red on
   the diff-aware inbox-order-grammar gate (local strict passes without
   `--inbox-base`, so the miss only surfaces in CI).
2. **Sequence-numbered pacemaker ticks:** pacemaker tick messages should
   carry sequence numbers plus a heartbeat last-tick line, so a platform
   drop surfaces at the next wake by gap-detection instead of forensics.
   Evidence: the 01:49Z tombstone-less drop
   (trig_01USg5i3qna4fCX5ZeePg7Gj — absent from all 1203 `list_triggers`
   records at the 10:40Z audit; failsafe bridged 02:07Z).
