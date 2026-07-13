# Night-run adopter outcomes — which kit mechanisms carried the fleet (2026-07-13)

> **Status:** `audit` (dated snapshot — ORDER 016 item 5 writeup; window
> 2026-07-12T20:00Z → ~2026-07-13T05:00Z; source code and merged PRs win
> over this file). Compiled from four read-only evidence sweeps + the kit
> seat's own record; every classification below carries its citations.
> Sweep timestamps (`date -u`): 04:56:43Z (kit seat) · 04:56:48Z (batch 1)
> · 04:56:55Z (batch 2) · 04:57:02Z (batch 3) · 04:57:15Z (batch 4).

## Method

Per repo: `git fetch origin main` on the local clone, all files read at
`origin/main` (heartbeats = `control/status.md`, session cards, findings),
plus PR listings via the GitHub API under a ~4-calls/repo cap (actual
spend: batch 1 = 4 calls across 3 repos, batch 3 = 3, batch 4 = 4,
batch 2 = ~5). Read-only throughout — no writes, comments, or trigger
mutations in any swept repo. 13 of 13 roster seats swept
(pokemon-mod-lab DARK, skipped by order). No API denials, 403s, or 429s
in any sweep; the one wall hit was on the kit seat's own evidence pass —
direct GitHub REST is closed on this surface (verbatim: `{"message":
"GitHub access is not enabled for this session. An org admin must connect
the Claude GitHub App for this organization."}`), so the `auto_merge` raw
field is cited via PR comments + status.md instead (github MCP tools work
fine).

## Headline

**11 SHIPPED · 2 IDLE-CLEAN · 0 STALLED.** 261 merged PRs across the 11
shipping adopter seats in the ~9-hour window, plus 4 kit-seat merges.
Three independent platform-side wake drops occurred; all three were
bridged by the Q-0265 failsafe ceiling. No chain died.

## Seat classification table

| Seat | Class | Merged PRs in window | Open / parked | Heartbeat currency | Key citation |
|---|---|---|---|---|---|
| superbot (hub) | SHIPPED | 13 (#2048–#2057, #2059–#2060, #2062 incl. 3 dashboard-refresh fires) | 2 draft (#2058, #2061 — merge=deploy hold, Q-0193) | 2026-07-11T19:45Z — pre-window **by design** ("hub with NO standing seat, Q-0264; cadence irregular by design") | status.md @ 5262fe4; PR record |
| superbot-next | SHIPPED | 55 (#306–#353 range; 9 landed after the 02:47Z stamp through 04:06Z) | 16 open **per ORDER 017 rule 2** ("open PRs stay open") + 3 closed-unmerged (superseded/scratch) | 2026-07-13T02:47Z, fresh | status.md @ a4d51b6 |
| websites | SHIPPED | 42 (#207–#250; 12 after the 02:51Z stamp through 04:45Z) | 2 draft rescue PRs (#245, #249, "do not merge") | 2026-07-13T02:51:21Z, fresh | status.md @ fca1911 |
| superbot-mineverse | SHIPPED (coordinator) | 19 (#46–#64) | 0 open (API `[]`) | 2026-07-13T04:12Z, fresh — "COORDINATOR-DELEGATED heartbeat write" for the whole SuperBot World seat | status.md @ f9261a2 |
| superbot-games | SHIPPED | 13 (#65–#77) | 0 open (API `[]`) | Own file stale (2026-07-12T10:16:22Z); tonight's truth = mineverse coordinator tally | status.md @ origin/main; mineverse tally |
| superbot-idle | SHIPPED | 8 (#75–#82) | 0 open (API `[]`) | Own file stale (2026-07-12T10:17Z); coordinator tally carries the lane | status.md; mineverse tally |
| gba-homebrew | SHIPPED | 8 (#74–#81) | 6 open follow-on slices (#82–#87), zero red | Stale cycle-5 body + in-window appended dispatch section (21:27:13Z) with its own staleness note | status.md @ d87f9ad |
| trading-strategy | SHIPPED | 19 (#77–#95, all merged, 0 open) | 0 open | 2026-07-12T21:02:36Z — ~8h stale vs the #81–#95 night activity (coordinator-seat lane) | status.md @ 58d7dfb |
| venture-lab | SHIPPED | 48 (#89–#136, all merged, 0 open) | 0 open | 2026-07-13T01:49:05Z, mid-run by design ("morning tally ~06:00Z") | status.md @ b6be45b |
| idea-engine | SHIPPED | 21 (#271–#291, PROPOSALs 013–025) | 0 open | 2026-07-12T23:44:55Z — ~5h lag vs the 04:53Z HEAD, cadence lag not a stall | status.md @ a123fda |
| sim-lab | SHIPPED | 15 (#57–#71, VERDICTs 015–026) | 0 open | 2026-07-12T23:32:28Z — same benign lag; verdicts landed through 04:50Z | status.md @ 6526959 |
| superbot-plugin-hello | IDLE-CLEAN | 0 (zero PRs ever) | — | No control plane exists (`control/status.md` → `fatal: path … does not exist`) — dormant seed repo, single seed commit bbaccec 2026-07-12T13:29:35Z | batch-2 sweep |
| product-forge | IDLE-CLEAN | 0 (latest PR #23 merged 2026-07-11T19:49:48Z, pre-window) | 0 | 2026-07-11T19:39:50Z — "close-out / archived-ready"; "NO trigger remains armed"; dryness pre-declared ("inbox DRY since ORDER 004 … honesty guard held") | status.md @ 4fdfa8a |
| **substrate-kit (own seat)** | SHIPPED | 4 (#314–#316, #318) | #317 open — **ratification park** (do-not-automerge, PL-012 law surface); #319 this report | control/status.md @ 917261b, fresh (02:1xZ) | kit-seat record below |

## Mechanism analysis — what the shipping seats actually exercised

### a) auto-merge-enabler as the landing path

Installed **in-window** at four seats and immediately followed by burst
landings at each: games #67 (00:03Z, fm ORDER 029 — then #68–#77 same
night), idle #77 (00:03Z — then 7 more), gba #76 (00:09Z — then a
~80-second landing burst #75/#77–#81 at 01:43:47–01:45:06Z),
superbot-next #321 (00:06Z — heartbeat declares it "Landing mode = repo
auto-merge enabler (canonical for non-draft claude/* PRs per #321);
coordinator merge delegation retired"). idea-engine #272 patched the
enabler's branch allowlist (`fix: add claude/ to auto-merge-enabler
branch allowlist`) and then rode it for 20 more merges.

**Cleanest live-fire proof — sim-lab** (orders line, verbatim excerpts):
PR #51 "merged by github-actions[bot] with ZERO agent merge calls, 28s
open-to-merge, enabler run 29189245547 'Auto-merge enabled for PR #51 —
it merges when substrate-gate is green' … both guard classes live-fire
verified — born-red refusal on #50, arm-and-merge on #51; live-verified
again by PRs #57/#58 zero-agent-merge landings."

**The variant:** fleet-manager used a merge-on-green sweep workflow
instead (PR #146, cron `7,37 * * * *`); PR bodies #149/#150/#154/#157
state "No self-merge — merge-on-green sweeps it", with merge timestamps
consistent with sweep landings (#157 created 04:12Z, merged 04:20Z).

**Designed refusals:** the enabler sat INERT at idle and gba
(fleet-manager status: superbot-idle "zero required checks — safely
refuses to arm"; gba #76 merged with enabler INERT pending
OQ-GBA-ROM-RULESET) — refusal-to-arm behaving as designed, pending owner
OQ items B#50/B#51.

### b) Failsafe + pacemaker doctrine (Q-0265) — three drops, three bridges

Three independent platform-side wake drops tonight, **all** bridged by
the 2-hourly failsafe ceiling:

1. **kit seat:** the 01:49Z one-shot (trig_01USg5i3qna4fCX5ZeePg7Gj)
   "never delivered its wake (platform drop; failsafe bridged at 02:07Z)"
   — status.md @ 917261b line 18; failsafe trig_01EMfauRqevNovFM8dz4NLdp
   3-for-3 verified fires (22:00Z, 00:10Z, 02:07Z).
2. **fleet-manager:** PR #150 body, verbatim: "capture_notes record the
   DROPPED TICK trig_0123fu7onT7wGMNB9ZtbtdqL (send_later, scheduled
   2026-07-13T00:06:00Z … never delivered) and the seat failsafe
   trig_01UQTZFvknBosXVo4YKKfazZ (fired 00:37Z) that caught the stall."
3. **superbot-next:** "the 01:07Z-window slot wedged platform-side and
   fired late at 02:44Z; pacemaker send_later fires stalled 01:37–02:44Z,
   chain re-armed post-flush" (status.md routines line).

Plus a fourth, milder anomaly at **websites**: "the 00:45Z failsafe fire
and a ~01:39Z pacemaker tick were delivered late/missed; the chain
recovered by the 02:10Z fire — watch, no re-arm performed."

**Conclusion:** the failsafe ceiling bounded every drop at ≤2 hours; no
chain died; every seat self-documented its anomaly in its heartbeat.

### c) Born-red session gate

Exercised broadly — cards land ~1:1 with PRs at most seats (websites 34
cards, superbot-next 15, trading 14 r3-* cards matching #81–#95,
venture ~31, idea-engine one card per PROPOSAL). Live-fire verified at
sim-lab ("born-red refusal on #50", arm-and-merge on #51). fm PR bodies
#150/#152/#153/#154/#157 state "Born-red card opens this PR; flips
complete last." gba session-37 dispatch records PR #75's first commit as
card+claim (`18886c0`).

**One bug surfaced:** substrate-gate born-red **fail-open on PR-added
cards (flip-race)** — mineverse PR #50 had to land stranded close-out
flips for #48/#49, root-caused in PR #52; finding at mineverse
`docs/findings/substrate-gate-born-red-fail-open-2026-07-12.md`, fix ask
routed to this kit via mineverse control/outbox.md. Idea filed:
`docs/ideas/session-gate-flip-race-fail-open-2026-07-13.md`.

### d) Control fast lane

Heavily used everywhere for heartbeats/orders/claims: trading #79 created
21:03:48Z, merged 21:04:12Z (**24 seconds** open-to-merge); websites 7
heartbeat-only PRs (#207/#211/#212/#215/#222/#230/#238); mineverse 7 of
19 merged PRs control-only; superbot-next #322–#325/#343/#348/#353;
venture control PRs merged 24s–3min after creation; fm PR #149 body:
"Control fast lane — control/inbox.md + control/status.md only (no
session card) … check --strict green (fast lane, no card demanded)";
idea-engine #273/#278/#282/#285 explicitly "control fast lane".

### e) ORDER grammar — the dispatch fan-out worked

Owner night ORDERs landed **verbatim** via control-scribe PRs at
~00:42–00:51Z across the fleet — kit #314 (00:47:31Z), gba #77 (ORDER
005), venture #103 (ORDER 008, 00:50Z), trading #80 (ORDER 012,
00:50:47Z), fm #149 (ORDER 039, 00:42Z) + #152 (ORDER 040/041),
idea-engine #280 (ORDER 004, 00:45Z), mineverse #55 (ORDER 004, 00:48Z)
— and were executed the same night (trading ran #81–#95 to a synthesis
PR; venture ran to 48 merges; gba shipped 5 game slices; idea-engine ran
PROPOSALs 016–025).

### f) Heartbeat currency — an honest finding

Several SHIPPED seats had stale own-heartbeats: games 10:16Z and idle
10:17Z (both pre-window), trading 21:02Z vs 04:29Z last landing (~8h),
idea-engine/sim-lab ~5h cadence lag. **None were stalls.** The cause is
structural: coordinator seats carry delegated tallies — mineverse wrote
the authoritative tally for the whole SuperBot World seat
("COORDINATOR-DELEGATED heartbeat write — the coordinator seat authorized
this status overwrite"), and one coordinator session
(session_01CXEh5TBKBNTDGgsDstfcjc, "venture-lab-coordinator") runs both
venture-lab and trading-strategy. **Guidance for future sweeps: classify
by PR record + coordinator status, never by seat heartbeat staleness
alone.** Idea filed:
`docs/ideas/heartbeat-delegated-tally-guidance-2026-07-13.md`.

### g) CAPABILITIES walls discipline

Exercised, not just planted: fm status § Walls (permission-guard edits,
GH013 direct-push, send_message ACTIVE-only) including the ORDER 029
standing permission put to use ("Peer-PR merge/arm calls now run under
the owner's standing permission (ORDER 029) — games #65/#66 armed
2026-07-13T00:10Z without denial"); sim-lab OA-004 "403 on refs/tags/*
push reproduced"; idle "PLATFORM-LIMITS zero-check-runs wall added"
(close-out PR #70); superbot-next PR #308 "docs: CAPABILITIES — verified
worker-session port-oracle path" (22:01Z); product-forge's honesty guard
held through a dry night ("~9h of 15-min chain ticks found no new work;
the honesty guard held (no filler shipped)").

## What separated shipping from stalling — the honest null

**Zero seats stalled tonight, so SHIPPED-vs-STALLED discrimination is not
derivable from tonight's evidence.** The separation question is
counterfactual; what the evidence does show is the *near-stall variance*
and which mechanism absorbed each fault class:

1. **Wake drops** (3 platform-side + 1 late/missed) → absorbed by the
   Q-0265 failsafe ceiling (§b) — every drop bounded, every chain alive.
2. **Enabler INERT states** (idle, gba — zero required checks / ruleset
   pending) → absorbed by designed refusal-to-arm + owner OQ routing
   (B#50/B#51); both seats still shipped via other landing paths.
3. **Parked stacks** (superbot-next 16 open per ORDER 017 rule 2; gba 6
   open slices; superbot's 2 deploy-hold drafts; kit #317 ratification
   park) → doctrine, not stalls; each park carries its rule citation.

What IS derivable: the mechanisms that absorbed faults tonight are the
failsafe ceiling, the enabler/merge-on-green landing paths, the born-red
gate, and the control fast lane — and every anomaly was self-documented
in a heartbeat or PR body rather than discovered by the sweep.

## The kit's own seat (ORDER 016)

#314 landed ORDER 016 verbatim (merged 00:47:31Z, 6ab5caa) · #315 seed
skills — chase-references + prep-owner-steps generalized, 12 skills
(01:01:16Z, 2325e71) · #316 rationalization layer — checkpoint doctrine +
`rationalize` skill, 13 skills (01:15:48Z, 817220d) · #318 night-run
heartbeat 02:1xZ (02:13:18Z, 917261b) · **#317 OPEN — ratification park**
(item 4, rider graduation Q-0271/Q-0272): all checks green, card
complete, `do-not-automerge` applied ~01:53Z because
`check_program_law` rules rulings.md (PL-012) an owner-gated law
surface; "Auto-merge disarmed … Owner review-merges" (PR #317 comment
4953747603; status.md @ 917261b line 23). The failsafe bridged this
seat's own dropped 01:49Z one-shot at 02:07Z (§b.1). This report is item
5, PR #319.

## Coverage & caps

13 of 13 roster seats swept (pokemon-mod-lab DARK, skipped by order);
API budget respected (~1–5 calls/repo, everything else from local clones
at origin/main); no permission denials anywhere; the only wall was the
kit seat's raw-REST probe, quoted in § Method. Two oversized
`list_pull_requests` results were read from saved result files — a token
cap, not an API denial.
