# 2026-07-14 · cross-branch ORDER-collision guard (build the #364 groomed idea)

> **Status:** `complete`

About to happen (opening declaration): build the guard groomed in
`docs/ideas/order-claim-cross-branch-collision-2026-07-14.md` (landed by
PR #364, merge `2a2d92b`) — the #362/#363 duplicate-work root cause. Scope:
an optional ` · order NNN` work-claim grammar segment (kit-owned constant in
`engine.grammar`), `bootstrap claim --order NNN` rendering it (with a
refuse-unless-`--force` guard when another live claim on a DIFFERENT branch
already names that order), and a `check_claims` cross-branch order-collision
advisory (advisory-only, never exit-affecting — posture preserved). Engine
change → dist regen byte-pin; tests for the collision fixture, the
no-false-positive lane, and the refusal/--force paths.

- **📊 Model:** Claude (Fable family) · high · feature/build

Run type: self-initiated · lab (per the #364 groom's named next step)

## What shipped (PR #365, parked for review-merge — auto-merge NOT armed)

- `engine.grammar`: `WORK_CLAIM_ORDER_RE` + `work_claim_order_ids()` — ONE
  parsing home (EAP §6.8) for the optional ` · order NNN` claim segment;
  free-text `ORDER NNN` on the bullet line also keys the scan (hand-written
  claims stay visible).
- `engine.claim`: `normalize_order` / `claim_order_ids`;
  `render_claim(order=...)` renders the segment, round-trip verified.
- `check_claims`: new `claims-order-collision` advisory — 2+ live claim
  files on DISTINCT branch tokens naming one order id. Advisory-only,
  never exit-affecting (strict-green pin test); `_claim_dirs` renamed
  public `claim_scan_dirs` so the verb scans the same dir set.
- `bootstrap claim --order NNN`: writes the segment; REFUSES when another
  live claim on a different branch names that order; `--force` overrides
  for a deliberate split (checker keeps flagging). Order-less claims and
  own-claim refresh unaffected — fully backward-compatible.
- Claims README template teaches the segment + advisory kind (kit's own
  planted copy lags by design until the release wave — the #362 precedent).
- Tests +24 (collision fixture checker+verb, free-text mention,
  no-false-positive lanes incl. `reorder 020` prose, --force, cross-location,
  strict-stays-green). Suite 1499→1523 passed, 1 skipped unchanged.
  Preflight 7/7 green; dist regen byte-stable (3× identical sha256).

## Decide-and-flag

- **Verb-side refusal (refuse-unless-`--force`) added on top of the idea
  file's advisory-only sketch.** The idea sketched only the checker
  advisory; the refusal lives in the WRITER (a session's own tool moment),
  not in `check` — so the checker's advisory posture is untouched while
  the verb catches the collision at the cheapest instant, and `--force`
  preserves the legitimate one-order-two-branch split the idea defended.
- **Heartbeat updated surgically** (one outcome line above `orders:`),
  leaving the coordinator's `updated:` stamp and wholesale-overwrite
  semantics alone — this seat is not the file's sole-writer session.
- **Idea frontmatter NOT flipped to shipped** — `check_idea_index` verifies
  ship claims against merged reality; the flip belongs to the session that
  review-merges #365.

## 💡 Session idea

`bootstrap claim --order` should also read the heartbeat `orders:` line and
warn (not refuse) when the named order already appears in `done=` — the
other half of the ORDER-020 incident window: a fresh fire re-executing an
order that a sibling already completed is the same waste as the twin-build,
and the verb already loads the control conventions needed to see it.
Dedup-checked against docs/ideas/ — not captured anywhere.

## ⟲ Previous-session review

Reviewing the ORDER-020 incident pair (#362 / #363): both sessions executed
cleanly in isolation — green, tested, dist-stable — and the losing session
(#363) handled the collision honestly (closed as superseded, no
re-litigation, groomed the root cause instead of salvage-churning). The
systemic miss: neither session claimed the ORDER in a place the other could
see before building; the groom session named the gap precisely but stopped
at a captured idea. Concrete workflow improvement (shipped this session):
the claim verb now makes the ORDER reference structured and REFUSES the
second cross-branch claim, so the #363 build cost is spent at claim time
(seconds) instead of after a full implementation. Remaining improvement for
a next session: routine/lab-loop prompts should instruct claiming with
`--order NNN` BEFORE consuming an inbox ORDER, so the guard engages by
default rather than by discipline.

## ⚑ Self-initiated

This slice was self-initiated per the #364 groom's named next step (the
idea file's "Next:" line + the groom card's 💡 ender); no inbox ORDER
served. Flagged here per the accountability convention.

## Documentation audit

CHANGELOG Added entry (PR #365 named); current-state Next-action handoff
updated (BUILT/REMAINS); heartbeat outcome line appended; claim file
deleted via the verb (dogfood both lanes); idea file deliberately left
`captured/open` pending merge; nothing chat-only remains.
