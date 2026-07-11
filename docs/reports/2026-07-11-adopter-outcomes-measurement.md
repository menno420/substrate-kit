# Adopter outcomes measurement — before/after kit adoption (2026-07-11)

> **Status:** `audit` (dated snapshot) — findings report for the
> measure-adopter-outcomes lane (claim `control/claims/measure-adopter-outcomes.md`,
> PR #245; report PR #247). Four read-only measurement passes (kit recon; fleet
> classification + drift + claim sweep; superbot before/after; websites +
> superbot-next deep dive) synthesized here. All numbers carry their n and
> window; negative findings are the headlines, by design.

## 1. Headline verdict

**The before/after question — "does kit adoption reduce owner-steering, false
claims, and time-to-ship?" — is answerable for at most 1 of 10 adopters, and
even that one only descriptively. No causal effect is measurable today; the
fleet was born inside the kit by design.**

Classification of all 10 registry adopters (created_at and adoption-PR merge
times verified against GitHub, not assumed from wave cards):

| repo | created_at (UTC) | adoption PR (merged) | pre-adoption history | supports before/after? |
|---|---|---|---|---|
| substrate-kit | 2026-07-07T21:39:56Z | #5 self-adopt (2026-07-09T02:42:30Z) | ~1.2 days | no (consumer #0 — it *is* the kit) |
| superbot | 2025-08-10T21:39:44Z | #1879 pin v1.0.0 (2026-07-09T04:17:50Z) | **~332 days** | **the only candidate — but pin-only** |
| superbot-next | 2026-07-07T20:08:08Z | #1 (2026-07-08T16:17:36Z) | ~20 h (one stub commit) | no |
| websites | 2026-07-09T00:41:59Z | #1 (2026-07-09T01:14:41Z) | ~33 min | no |
| superbot-games | 2026-07-09T14:21:38Z | #3 (2026-07-09T16:42:21Z) | ~2.3 h | no |
| trading-strategy | 2026-07-09T12:26:35Z | #1 (2026-07-09T16:48:40Z) | ~4.4 h | no |
| gba-homebrew | 2026-07-09T23:56:44Z | #2 (2026-07-10T02:14:22Z) | ~2.3 h | no |
| pokemon-mod-lab | 2026-07-09T23:58:13Z | #2 (2026-07-10T02:35:45Z) | ~2.6 h | no |
| venture-lab | 2026-07-09T22:33:24Z | #4 (2026-07-10T03:01:50Z) | ~4.5 h | no |
| fleet-manager | 2026-07-09T16:56:41Z | #2 (2026-07-09T17:10:07Z) | ~13 min | no |

Nine adopters were born 13 minutes to ~20 hours before their kit-install PR —
there is no "before" period to compare against. The one repo with a real
pre-period, superbot, is **pin-only by owner decision** (PR #1879's own body:
no `.substrate/`, no vendored dist, its own session tooling). Its born-red
gate, claims convention, and ledger checkers are superbot-native and predate
the kit — **the kit was extracted FROM superbot** (#1649 built the substrate
in-tree 2026-07-02; #1783 the enforcement layer 2026-07-07). Nothing
operational changed at superbot's adoption boundary, so its before/after
deltas are descriptive of the boundary window, not kit-attributable.

## 2. Time-to-ship

**Superbot (the only before/after series — descriptive only):** merged PRs
reconstructed from full deepened origin/main history; open-time proxy
validated against GitHub created_at to 0.1–0.3 min error on 3 PRs;
squash-merged PRs excluded from latency (their GitHub-exact latencies match
the merge-style medians, so no skew).

| window | merged | latency n | median | p90 |
|---|---|---|---|---|
| 7d before pin (07-02 → 07-09) | 229 | 186 (43 squash excl.) | **6.7 min** | 133.7 min |
| after pin (07-09 → 07-11T21:10Z) | 125 | 98 (22 squash excl.) | **9.5 min** | 41.3 min |
| 30d before (06-09 → 07-09) | 1,159 | 933 | 7.8 min | 44.5 min |

No material change: median open→merge sits at ~7–10 min in every window.
Auto-merge-on-green (superbot's native Q-0123/Q-0127 machinery) predates the
kit there. The before-7d p90 is driven by two backlog-clearing batch sweeps
on 2026-07-04 (parked dependabot #1555–#1560 + Codex-review #1695–#1699), not
slow CI.

**Post-adoption baselines (born-with-kit adopters — baselines for future
measurement, not effects):**

| repo | window | n merged | median | p90 | max |
|---|---|---|---|---|---|
| websites | 07-09T01:14Z → 07-11T20:24Z | 151 | 2.4 min | 14.1 min | 4.1 h (#141, owner-click hold) |
| superbot-next | 07-08T16:17Z → 07-11T20:33Z | 211 | 1.9 min | 14.0 min | 5.3 h (#95) |

Median ≈ one CI run; the p90 tail is born-red card holds + red CI + the #141
merge-freeze window.

## 3. False claims — near-zero and self-correcting fleet-wide

**Superbot (both periods):** ~130 merged-claims across 90 session cards (20
newest pre-boundary + all 70 post-boundary) verified against origin/main
merge commits = **0 contradictions**. Before sample: 16/16 distinct claimed
PRs verified (e.g. #1853 → `9c23e78f5c`); after: 67 distinct claimed PRs all
verified (e.g. #1886 → `f18db769c9`, dependabot batch #1762–#1766 all
present). Superbot's native gates were already delivering this; the kit can
claim none of it.

**Mid-tier sweep (superbot-games / venture-lab / fleet-manager):** 16/16
claims accurate against GitHub state — including exact merge-minute matches
(superbot-games #9 "owner clicked 19:02Z" → merged 19:02:46Z; fleet-manager
"fm #68 MERGED ~11:48Z" → 11:48:30Z) and correctly-recorded **negative**
outcomes (superbot-games #4 "CLOSED unmerged" → confirmed closed, merged:false;
fleet-manager tenure claim "30/30 of #57–#86 merged" → all 30 verified).

**The ONE confirmed false-"shipped": superbot-next PR #44** (merged
2026-07-09T04:23:26Z, 65 s after open). Title/body claimed "Upgrade vendored
substrate-kit dist to v1.0.0"; the actual diff was 1 file, +17 lines — the
in-progress session card only, bootstrap.py untouched. Root cause (per #46's
body): the pre-v1.0.0 kit's own `check --strict` didn't enforce session-card
markers, so the born-red hold didn't hold and auto-merge fired — **the kit's
own too-weak gate caused it**. Self-caught and corrected by #46 (merged
04:29:45Z, +17,163 lines); false state on main ≈ 6 minutes, incident recorded
in the PR title itself.

**Registry drift is stale self-reporting, not deception.** All 7 drift rows
in `docs/adopters.md` (generated 2026-07-11T19:40Z) verified against primary
evidence:

| repo | self-report (`kit:` line) | tree (vendored dist) |
|---|---|---|
| substrate-kit (config pin) | v1.0.0 | v1.12.0/v1.12.1 |
| superbot-next | v1.10.1 | v1.12.0 |
| superbot-games (mining) | v1.7.1 | v1.12.0 |
| superbot-games (exploration) | v1.7.1 | v1.12.0 |
| trading-strategy | v1.7.1 → **reconciled** (#62, 07-11T20:01Z) | v1.12.0 |
| venture-lab | v1.10.1 | v1.12.0 |
| fleet-manager | v1.7.0 | v1.12.0 |

The mechanism is structural: distribution-wave upgrade PRs deliberately touch
kit-owned files only (owner directive Q-0261.3 — no lane content, no
`control/status.md` edits), so the tree advances while the lane-owned
heartbeat line waits for the lane's next overwrite. superbot-games PR #22
flags this exact debt in its own body; trading-strategy's row closed the loop
as designed 21 minutes after the registry was generated.

**Websites' two self-corrected wrong operational verdicts** (both documented
in its `docs/retro/continuous-mode-lessons-2026-07-11.md` §2): (a) five
consecutive heartbeats mis-derived the healthcheck cron next-fire ("~02:17Z";
`17 */6` anchors 00/06/12/18), fixed at #96 with an incident test
(`scripts/cron_slots.py`); (b) heartbeats #134–#144 declared the 12:17Z
healthcheck slot "never delivered" while the run existed (event: schedule,
created 13:52:38Z, success) — corrected ~18:2xZ. False operational verdicts
that propagated before correction, not merged/shipped lies.

Counter-evidence of honesty discipline: superbot-next's status refused
`done=004` across many heartbeats ("bands 7–9 haven't run yet");
closed-unmerged PRs (websites #5/#9/#22, sbn #60) are nowhere described as
landed; venture-lab self-caught its own overstated "Green in CI" wording and
shipped the real fix (kit-tests workflow #22/#28).

## 4. Owner-steering — the honest measurement wall

**Direct steering is unmeasurable by author identity.** ALL activity in every
window posts under the owner's login `menno420` — agents operate under his
account/token (e.g. superbot-next #111 comment 4938516715: author menno420,
OWNER, signed "Generated by Claude Code"). Superbot commit-identity audit
since 06-09: 2,035 `Claude <noreply@anthropic.com>`, 1,465 GitHub
merge/squash commits, 166 dashboard-bot, and even the 29 `Menno|Menno`
commits are Codex agent sessions (#1695–#1698 first commits). **Zero
provably human-typed commits found.**

Measurable proxies:

- **Superbot owner-lane Q-blocks** (directive/decided headings in the
  question router, 268 unique Q-ids): 30d before = 1.6/day; **7d before =
  5.1/day** (bursts 07-03 ×18, 07-07 ×13); **after = 4.3/day** (12 blocks /
  2.8 d). Flat across the boundary, and the climb predates the pin — the
  steering spike is the fleet program, not the kit.
- **Corrective manager ORDERs**: 6 of 24 across websites + superbot-next.
  websites 2/11 (ORDER 004 session-card backfill; ORDER 010 model-attribution
  correction, PR #59 squash `2c89e96` evidence); superbot-next 4/13 (003
  stale-PR close, 004 warn-escalation regression + "PASS (live) must never
  contradict the owner's eyes", 006 half-delivered retro, 011 owner override
  of the SB_TEST_DB_HOSTS guard, Q-0263.1).

## 5. Nulls & incidents

- **Alleged superbot-next mid-v1.10.x-wave force-push of origin/main: NOT
  CONFIRMED — null finding.** Method: all 212 merged sbn PRs traceable to
  commits on current origin/main; every push-event CI head SHA an ancestor of
  current origin/main — 60 sbn ci.yml runs (07-11T05:16Z–20:33Z, spanning the
  whole v1.10.0→v1.12.0 wave) + 60 websites quality.yml runs (03:36Z–20:24Z):
  **0 orphaned SHAs in either repo**; no force-push mention in any card,
  status history, or retro. Caveats: a same-tree force-push or deleted
  workflow runs would evade this; windows before 07-11 ~05:16Z/03:36Z and
  non-main refs unchecked; the force-push activity API wasn't available.
- **Incident A — sbn #44/#46 premature merge** (04:22–04:30Z, 2026-07-09):
  the one confirmed false-shipped, §3 above. The kit didn't prevent it — its
  own pre-v1.0.0 gate caused it; the v1.0.0 engine #46 shipped closed it
  (echoed same day by websites #24 "Fix leaky born-red session gate").
- **Incident B — sbn kit gate red on main, recovered honestly:** ORDER 001
  (07-09T12:07Z) tasked clearing the "Kit check --strict" red; #69 (merged
  14:29:15Z) walked the engagement gate RED → GREEN (9 planted docs
  unrendered, 8 unfilled slots); #96 (v1.2.0→v1.6.0, 19:59:51Z) shipped the
  honest fixes; first `kit: … check: green` line lands in #96's merge commit
  `9761db4`. **No false claim — the red was reported truthfully throughout.**

## 6. Confounds (all material)

1. **Born-with-kit design** — 9/10 adopters have no before period (gen-2
   blueprint seeds are born-right on purpose).
2. **Pin-only superbot** — kit machinery never engaged; the kit was extracted
   from superbot's native workflow.
3. **Model-mix shift at the boundary** — the EAP 3-model fleet (Fable 5 /
   Opus 4.8 / Sonnet 5) launched via superbot #1877/#1878 merged
   07-09T01:18/01:39Z, hours before the pin.
4. **Fleet program launch same day (07-09)** — post-boundary owner attention
   and throughput reflect the program, not the kit.
5. **Window asymmetry** — the after-window is 2.7 days; p90 on n=98 is noisy.
6. **Agent-under-owner-identity** — direct human steering invisible to any
   author-based metric (§4).

## 7. What would make this measurable

1. **Pre-register per-adopter baselines now.** The currency checker already
   sweeps every adopter; extend it (or a sibling script) to snapshot
   per-adopter PR-latency medians/p90 and claim-audit results into a dated,
   append-only baseline file. Future waves then have a real "before" — today's
   §2 baselines (websites 2.4/14.1 min, sbn 1.9/14.0 min, n=151/211) are the
   first entries.
2. **Keep the registry drift checker as the standing false-claim
   instrument.** It is the one instrument that already catches the dominant
   real drift class (stale heartbeat `kit:` lines) mechanically; §3's 7-row
   table came straight from it. The first future adopter with genuine pre-kit
   history (an established repo, not a blueprint seed) would be the first true
   before/after test — measure it against the pre-registered protocol above,
   not retrospectively.
