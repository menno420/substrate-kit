# Gen-1 retro self-review — SuperBot-rebuild coordinator lane (2026-07-09)

> **Status:** `owner-guidance` — the SuperBot-rebuild COORDINATOR lane's
> answers to [QUESTIONS.md](QUESTIONS.md), by ID. Filename suffixed
> `-superbot-coordinator` per the owner's multi-lane rule; kit-lab's own
> answers are the unsuffixed
> [self-review-2026-07-09.md](self-review-2026-07-09.md) and stand for the
> kit-specific questions. Honest over flattering; evidence is mostly
> superbot-next PRs plus the coordinator's session ledger (audited in
> [project-review-2026-07-09-superbot-coordinator.md](project-review-2026-07-09-superbot-coordinator.md),
> hereafter "the audit"); "I don't know" stated where true.

Perspective note: this lane's "work" is orchestration — spawning, steering,
recovering, and standing down sessions. Answers are given from that vantage;
where a question is really about hands-on-keyboard building, the answer says
whose keyboard it was.

## A. Work & correctness

**A1 — shipped to main vs branches/drafts.** Shipped to main by this
Project's sessions: 86 merged PRs in superbot-next (verified live at review
time — kernel S0–S15, layer-V, K10, port bands 1–7, presentation rework,
plugin contract, and the testing-band fixes #54–#85), plus substrate-kit #47
(the setup-script doc) from the setup-script-fix session. Gap between
"exists" and "shipped": the plugin example still lives at
`examples/superbot-plugin-hello` inside superbot-next instead of its own
repo — not a branch/draft gap but an owner-click gap (session tokens cannot
create repos; ⚑ owner action 2 in the audit). The coordinator itself ships
no code; its deliverable is this review pair plus the lane heartbeat.

**A2 — externally-verified claims vs self-tested.** Externally verified:
the live bot (Galaxy Bot) boots and serves commands in a real Discord test
guild — a live deploy, the strongest oracle this Project has; 465 goldens
replay against recorded old-bot behavior (recorded oracle, 0 flipped,
honest-red); the owner's 9 recorded defects were triaged against real
screen-recording evidence (superbot-next #65, #66). Self-tested only: unit
suites — and the headline finding of the whole testing phase is precisely
that they were insufficient (~15 real bugs found only live, e.g. the two
dispatch-blocking bugs in #56/#58 that every unit test missed).

**A3 — least confident, and the disproving check.** The claim "the builder
ran claude-fable-5 throughout". Directly verified for exactly one child
transcript plus one sibling session card ("Model: fable-5"); the other ~17
workers are inferred from model inheritance. Concrete check: enumerate every
builder-worker transcript via the platform's event API and grep the model
field — the coordinator could not do this cheaply mid-run. Second-least:
"~15 real bugs" — the count is honest but hand-tallied from PR
descriptions; a re-count against the testing session's band reports could
move it by one or two.

**A4 — unnecessary, duplicated, or already existing.** The duplicate ORDER
005 execution: the wake-up session built (and merged, PR #51 here) a
deliverable kit-lab was already carrying on PR #50 — pure duplication,
caused by order broadcast without lane suffixes (audit §b). The revived
zombie session also began re-doing the already-merged setup-script doc
before stand-down. Within the build itself the coordinator knows of no
duplicated band — sequential workers with progress-log handoffs prevented
overlap.

## B. Errors & friction

**B1 — every error hit.** From the ledger, with time lost and class:
1. Environment setup script exited 1 at provisioning — killed retro
   session #1 dead (~30 min incl. respawn; preventable by better setup —
   now documented, #47).
2. The same dead session self-revived ~6h later and started duplicate
   work (risk more than time; platform oddity, not preventable by us).
3. PR #35 frozen at "Expected" by misconfigured required checks (~35 min;
   preventable by setup — owner fixed the ruleset).
4. Band-3 worker externally killed mid-run (recovery ~20 min via read-only
   scout + continuation worker, zero loss; external).
5. ~100+ no-op webhook wakes (token cost only; platform).
6. ORDER-005 lane collision — PR #51 merged before the stand-down landed
   (fallout: kit-lab's #50 now dirty; preventable by instructions — the
   suffix rule wasn't in the broadcast).
7. Setup-script-fix session's ~5.5h creation-to-activity gap (cause
   unknown; platform, cannot determine).

**B2 — figured out but already documented somewhere.** The multi-lane
heartbeat pattern: the coordinator initially reasoned out per-lane status
files from first principles, then found kit-lab had already shipped exactly
this in v1.4.0 (`control/README.md`, "per-lane heartbeats"). It should have
been visible at the moment the lane was created — i.e., in the broadcast
order itself, which is redo-rule 4 in the audit.

**B3 — broke silently.** The two dispatch-blocking bugs (superbot-next
#56, #58): the kernel and all unit tests were green while the live bot
could not serve those command paths at all. Discovered only by the first
live band. Also silent: the presentation gap the owner's screen recordings
exposed (9 defects, #65/#66) — rendered output looked wrong while every
check was green. Both discoveries argue for redo-rule 3 (live-boot right
after K10).

**B4 — ambiguous/missing instruction line.** Missing, not ambiguous: the
broadcast ORDER 005 text carried no lane-suffix clause, and the per-session
ritual line "execute any order whose status is `new`" (control/README.md)
gives two lanes in one repo identical marching orders with no claim step —
quoted lesson, and the exact hole kit-lab's own #51-card idea (an order
claim signal) proposes to close. Also missing: nothing in the coordinator's
instructions said what to do when a stand-down message races an auto-merge —
it improvised (corrective FYI, no revert).

## C. Efficiency

**C1 — time split.** Coordinator-lane estimate (no per-minute log was
kept — this is labelled estimate, from session timestamps): orientation/
reading ~15%, building ~55% (builders/testers doing the work), verifying
~15% (live bands, replay), CI/merge mechanics ~5%, blocked/waiting ~10%
(owner-gated clicks: intents, repo creation, rulings). Biggest single sink:
the blocked/waiting slice — every entry in it was an owner-only platform
click.

**C2 — context rebuilt that should have been durable.** The fleet picture
itself: who owns which order, which lanes exist, which PRs are in flight —
re-derived by recon workers several times today. The durable form now
exists (per-lane `control/status-*.md` heartbeats plus this audit); it
should have existed from the first multi-lane moment.

**C3 — most/least value per minute.** Most: live band testing — every band
produced real bugs unit tests missed (~15 across 5 bands; #56–#85). Least:
webhook wake triage — 100+ wakes, zero actions taken.

**C4 — redo speed and the ordering change.** Perhaps 20–25% faster
end-to-end, almost all from the audit's redo ordering: setup script fixed
first (no dead/zombie sessions), replay adapter before port bands, and the
big one — **first live boot right after K10** instead of after all seven
bands, which moves the day's two most expensive bugs a day earlier.

## D. Autonomy & owner input

**D1 — every stop for owner input.** (1) Privileged Discord intents —
truly owner-only (external account control). (2) Plugin repo creation —
NOT owner-only in nature; unblockable by a repo-creation scope on session
tokens. (3) Kernel-drift corpus ruling (flag 13) — truly owner-only
(product taste). (4) Required-checks ruleset fix — unblockable by
ruleset read/write on own repos. (5) Test-guild hygiene + throwaway member
— owner-only (guild admin). Named grants: see D4.

**D2 — routed up but should have been decide-and-flag.** The lane
heartbeat file: the coordinator hesitated over whether creating
`control/status-superbot-coordinator.md` in a repo whose config kit-lab
owns needed permission. It doesn't — the v1.4.0 per-lane pattern makes the
lane the sole writer of its own file; this review ships it decide-and-flag
(the config `heartbeat_files` addition stays with kit-lab).

**D3 — took while unsure allowed.** Standing down another owner-created
session (the zombie, and today the wake-up session). No written rule says a
coordinator may order an owner-spawned session to stop. The rule that would
make it unambiguous: "the lane coordinator may stand down any session
duplicating an already-owned order; the stood-down session's card records
the yield."

**D4 — smallest set of standing grants for zero humans.** (1) Repo-creation
scope for session tokens (kills stop D1-2). (2) Ruleset read/write on the
Project's own repos (kills D1-4). (3) Privileged-intent pre-approval for
declared test bots (kills D1-1). (4) A session-targetable timer
(`send_later` with a session-id param — kills the watchdog relay quirk).
(5) A direct coordinator→child messaging tool (kills the relay-worker tax
on every steer).

**D5 — was "done" defined.** For build bands and testing bands, yes —
frozen specs and per-band reports made done checkable. Undefined at two
points: "testing phase complete" (the ladder has an end, but no ruling says
which bands are release-gating vs optional) and "ORDER 002 done" (blocked
on an owner click, so the session could only reach done-minus-one-click).

## E. Protocol & environment

**E1 — did the control/ ritual fit.** Mostly yes at the repo level — inbox
first, status last kept every child oriented. Where it cost: the ritual is
per-REPO but this fleet is per-LANE; until v1.4.0's per-lane heartbeats,
two Projects sharing substrate-kit had one status file and no way to signal
"this order is claimed" — today's collision rode exactly that gap. The
coordinator itself skipped the ritual for pure-orchestration turns (no repo
writes), which the protocol permits but doesn't state.

**E2 — what the ENVIRONMENT should have contained at first boot.** A
working setup script (the actual one exited 1 and killed a session — fixed
as #47); `gh` or an equivalent authenticated CLI in every container
(verification fell back to MCP tools); and a documented answer to "which
model are my children running" (the audit's biggest cannot-determine).

**E3 — what the REPO should have contained at seed.** superbot-next: the
composition root from day one (it arrived at PR #54, after the kernel —
which is why nothing could boot live earlier), and a CI gate that exercises
rendered output (the presentation gap class). substrate-kit: nothing to
add from this lane — its seed predates us; the per-lane control files it
now documents are the thing our lane needed on day one.

**E4 — what a fresh session would misunderstand first.** That this repo
hosts TWO Projects. A fresh session reading `control/inbox.md` would
execute any `new` order for the wrong lane — that is literally what
happened today. The single preventing document: a lane manifest at the top
of `control/README.md` (or the inbox header) naming each lane, its status
file, and its filename suffix.

## F. Redesign (the payload)

**F1 — three rules for the next Project's founding instructions.**
1. Every broadcast order names the lane it targets and the suffixed file
   paths it may write.
2. Live-boot the artifact at the first possible seam, not after the tree —
   the first live band found in minutes what the whole unit suite never
   would (#56, #58).
3. Environment setup scripts must be exit-0-safe before any session fleet
   runs — one non-idempotent pip line killed a session and spawned a
   zombie.

**F2 — what the MANAGER should have done differently.** Order broadcast
discipline: ORDER 005 went to multiple lanes with identical text and no
suffix/claim clause — one order, three near-executions. Otherwise the
cadence was right: orders were few, pointed at committed docs, and P-ranked;
the priority-inversion handling (kit-lab acking 005 but not rider-executing
it) shows the format works when one lane owns it.

**F3 — one capability traded for almost anything.** Direct
coordinator→child messaging. Every steer today cost a relay worker; the
stand-down race (message vs auto-merge, lost by ~minutes) might have been
won with a direct, immediate channel.

**F4 — ideal seed state, ≤10 bullets.**
- Frozen specs committed before the first builder spawns (kept — it's why
  13.6h worked).
- Setup script verified exit-0 in a throwaway session first.
- Composition root + live-boot smoke in the seed skeleton.
- Replay/parity adapter built alongside layer-V, tracking bands.
- Lane manifest in control/, suffix rule in every order template.
- Per-lane heartbeat files from the first multi-lane moment.
- Standing grants of D4 pre-approved (repo-create, rulesets, intents).
- A claim step for orders (phase line names the order being executed).
- Watchdog armed from night one with a session-targetable timer.
- Webhook subscriptions scoped to actionable events only.

## G. Addendum — KIT (substrate-kit)

Kit questions are kit-lab's to answer; their unsuffixed self-review stands.
This lane answers only where it holds independent evidence:

**G1 — adopt UX and the stranded/double-adopt pattern.** Independent
evidence: superbot-next's adoption went clean end-to-end from this lane's
vantage (engaged, gate wired, heartbeats flowing). But today's collisions
are an adopt-UX finding the kit should own: a SHARED repo advertises no
lane map, so a fresh session cannot tell adoption state per-Project — the
double-adopt and the double-executed order are the same shape (nothing
marks "claimed"). Kit-side fix beyond gates: `adopt --lane` scaffolding
(kit-lab's own filed idea) plus a lane manifest the checker can read.

**G2 — adopter telemetry.** Not this lane's question; kit-lab's answer
stands. One datum from here: the `kit:` heartbeat line was enough for the
coordinator to verify adopter state without repo access — the cheapest
transport already works.

**G3 — 3 releases in one day: pace or churn?** From the adopter side:
absorbed fine. The builder merged around the v1.2.0-era upgrades mid-build
(superbot-next #42/#44/#46 window) without a single kit-caused stall; pins
plus upgrade-verb discipline meant cadence never hurt us. Ideal rhythm from
an adopter's seat: batch to daily unless a fix is live-blocking — but
today's pace was not churn.
