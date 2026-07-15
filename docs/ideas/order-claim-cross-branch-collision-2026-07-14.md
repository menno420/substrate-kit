---
state: promoted
origin: lab
shipped_pr: 365
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-14
outcome: shipped
---

# Work claims miss cross-branch ORDER collisions (2026-07-14)

> **Status:** `ideas`
>
> **State:** shipped — kit PR #365 (2026-07-14): `engine.grammar`
> `WORK_CLAIM_ORDER_RE` + `work_claim_order_ids()`, the claim verb's
> `--order NNN` segment (round-trip verified) with a refusal when another
> live claim on a different branch already names that order, and the
> `check_claims` `claims-order-collision` advisory (advisory-only, never
> exit-affecting). Doc segments (this file's flip, the local claims-README
> order-segment sync, the lab-loop STEP 2 claim-the-ORDER-first line)
> completed by kit PR #397 (2026-07-15).
> (Originally: captured at the lab-loop run close-out 2026-07-14.
> **Origin:** lab — two routine lab-loop fires the same night both consumed
> the same unacked `control/inbox.md` ORDER and built duplicate PRs (#362
> landed; #363 closed as superseded), each unaware of the other.)

**One line:** the `bootstrap claim` / `check_claims` work-claim system keys its
duplicate scan on the **branch token** (`claude/<slug>`), so two sessions on
different branches doing the **same work** (same ORDER, or overlapping scope)
each write a distinct, non-colliding claim file and never see each other —
exactly the parallel-work case the claim system exists to protect.

## Evidence (this run, verifiable)

- ORDER 020 (fm lane-write relay) landed in `control/inbox.md` at
  2026-07-14T04:12Z, ten minutes *after* the 04:02Z `status.md` heartbeat
  declared the backlog "DRY". Its two open BUILD sub-items (d = A10
  friction-outbox advisory, e = INC-29 pointer casing) sat unacked.
- Two routine fires picked it up concurrently. One built PR **#362** (advisory
  inline in `cmd_check`, kind `friction-outbox-pending`) and merged to main
  as `e7c0a5e`. The other (this session) built PR **#363** (the same two
  sub-items, advisory as a standalone `check_outbox.py` module) — a full,
  green, tested implementation of identical scope. #363 was closed as
  superseded the moment the collision surfaced; the build effort was wasted.
- Both sessions would have written a work claim (`control/claims/claude-<slug>.md`)
  for their OWN branch. `check_claims`' duplicate scan keys on the branch
  token (`WORK_CLAIM_BULLET_RE`, `src/engine/claim.py`), so two DIFFERENT
  branches serving the SAME order are not duplicates by its definition — the
  scan is silent by construction.

## Why the existing machinery doesn't catch it

- `claim.py` / `cmd_claim`: the claim file is per-branch; its scope is
  free-text bold prose, with no structured ORDER/work key. Ownership and
  duplicate detection both hinge on the branch token, so "who holds this
  branch's claim" is answerable but "is anyone else already doing this ORDER"
  is not.
- `check_claims`: dedupe is by claim owner (branch), not by work overlap.
- `check_status_current` heartbeat gate: pins `status.md` currency, but says
  nothing about an inbox ORDER that arrived after the last heartbeat and is
  still unacked — so a fresh fire that reads `status.md` ("backlog dry") and
  skips the inbox tail can miss the order entirely (a separate but adjacent
  gap; see the adjacent-idea note below).

## Proposed mechanism (sketch — not yet built)

Give a work claim an optional **structured work key** and let the scan flag
cross-branch overlap on that key rather than only branch identity:

1. **Claim carries the ORDER it serves.** Extend the claim grammar with an
   optional trailing ` · order NNN` (or ` · scope <key>`) segment, rendered by
   `bootstrap claim --order NNN` from the same `engine.grammar` constants the
   enforcer reads (the writer==enforcer discipline the claim/heartbeat writers
   already follow). Backward-compatible: order-less claims stay valid.
2. **Cross-branch overlap advisory.** `check_claims` (or a small sibling)
   emits an advisory when ≥2 live claim files on different branches name the
   same order/scope key: "branch A and branch B both claim ORDER 020 — one is
   likely duplicate work; confirm before building." Advisory-only, never
   exit-affecting (a genuine hand-off split of one order across two branches
   is legitimate — this is a nudge, not a lock).
3. **Boot-time visibility.** A routine fire that is about to consume an ORDER
   greps `control/claims/` for an existing claim naming that order first —
   documented in the lab-loop prompt's STEP 2 (claim the ORDER before
   building), so the claim exists early enough for a sibling to see it.

Alternatives weighed: a hard lease (first-claimer locks the order) is
tempting but over-constrains — it breaks the legitimate one-order-two-branches
split and needs conflict resolution the advisory avoids. A coordinator-side
assignment (the coordinator hands each order to exactly one seat) is the
heaviest fix and lives in coordinator-owned protocol, not the kit engine —
out of scope for a contained kit build, though the coordinator may prefer it.

## Why now / cost

- Contained to `claim.py` + `check_claims.py` + the shared grammar constant +
  the lab-loop prompt line; engine change → dist byte-pin; advisory posture
  means zero risk to green adopters. Evidence tier: a realized same-night
  collision with two PR numbers, not a hypothetical.
- **Shipped:** parts 1–2 (grammar segment + `claim --order` writer flag +
  verb refusal + `claims-order-collision` advisory + tests, engine change →
  dist byte-pin) in kit PR #365 (2026-07-14); part 3 (boot-time visibility —
  the lab-loop STEP 2 claim-the-ORDER-before-building line) plus this file's
  lifecycle flip and the local claims-README sync in kit PR #397
  (2026-07-15). The adjacent [[unacked-order-vs-heartbeat]] visibility gap
  (an order newer than the status heartbeat should be surfaced mechanically
  so a fresh fire sees it before treating the tree as idle) remains open —
  that one is about *noticing* an order, this one about *not colliding* on
  it.
