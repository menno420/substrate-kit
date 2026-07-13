# 2026-07-13 · si-coordinator-close — coordinator seat ender (retro + capability bake + heartbeat)

> **Status:** `in-progress`

About to do: close the Self Improvement coordinator seat (boot
2026-07-12T20:4xZ → close 2026-07-13T10:4xZ) — full retro in this card,
bake the send_later tombstone-less-drop finding into `docs/CAPABILITIES.md`,
file two prompt-delta proposals to `control/outbox.md`, and post the
SEAT CLOSED heartbeat to `control/status.md`.

## Retro — SI coordinator seat, 2026-07-12T20:4xZ → 2026-07-13T10:4xZ

### (a) Shipped & parked

Evening loop: **#308** K0 headroom gauge (174b113) · **#310** current-state
condensation 6913→2862 words (c5ef5b9) · **#311** gate-shadowing
ground-truth + idea reconcile (cf0fa24) · **#312** idea-drift guard
(1086dd5) · **#313** heartbeat (ebc1be9).

Night run, ORDER 016: **#314** order landed verbatim (6ab5caa) · **#315**
seed skills chase-references + prep-owner-steps → registry (2325e71) ·
**#316** rationalize skill + checkpoint doctrine (817220d) · **#318**
heartbeat · **#319** adopter-outcome report, 14 seats 12 SHIPPED / 2
IDLE-CLEAN / 0 STALLED (b171d02) · **#320** ORDER 016 tally (847e7df) ·
**#323** ORDER 017 thorough report (df6fa9c).

**PARKED:** #317 rider (PL-012) + reading-path graduation — head 82fca96,
all checks green, `do-not-automerge` law-gate ratification park; landing
path is owner review-merge.

All merged payloads were diff-confirmed by read workers same-session.
Nothing was attempted-and-dropped.

### (b) Struggles

- **#314 first push went red** on the CI-only diff-aware
  inbox-order-grammar gate — missing `priority:`/`do:`/`why:`/`done-when:`
  framing; local strict passes without `--inbox-base`. Fixed in-PR; the
  owner's verbatim text was untouched.
- **Platform send_later drop:** trig_01USg5i3qna4fCX5ZeePg7Gj (fire_at
  01:49Z) never delivered AND left no tombstone — absent from all 1203
  `list_triggers` records at the 10:40Z audit. The failsafe bridged at
  02:07Z.
- **Stale-idea misdirect:** the slice-3 dispatch was misdirected by a stale
  idea-file body (frontmatter said shipped #187, body said captured) —
  root-caused into the #312 guard.
- **Seat walls:** MCP `pull_request_read` GET omits the `auto_merge` field;
  the issue timeline is unreachable — so the #317 disarm actor (attributed
  menno420, comment signed Claude Code) is unprovable from this seat.

### (c) Went well — successors should repeat all four

1. **Strict serialization of dist-byte-pin PRs:** 12 landings, zero merge
   conflicts.
2. **Verify-at-HEAD after every child claim (Q-0120):** caught a
   branch-head-vs-squash sha mixup and the stale-idea misdirect.
3. **Two-layer wakes** (15-min pacemaker + `0 */2` failsafe) survived the
   platform drop.
4. **Child-per-slice with self-contained briefs + time-boxed slice E**
   (parallel read-only sweep) hit the 06:00Z deadline with 40 min spare.

### (d) Surprises & open questions

- The fleet survey found **0 stalled seats** — the discrimination goal
  returned an honest null.
- kit-lab fresh-session-per-fire **DELIVERED on schedule 06:10Z** — first
  proven scheduled delivery; settles the forensics question.
- One tick fired 25 min late (armed 02:24Z, fired 02:49Z).
- **Open question:** should pacemaker ticks carry sequence numbers so drops
  surface at the next wake by gap-detection instead of forensics?

## Enders

- **📊 Model:** Fable-class (Claude 5 family)

💡 **Session idea:** sequence-numbered pacemaker ticks — each tick message
carries `tick N`; the wake handler compares against the heartbeat's
last-tick line; a gap = detected drop, no forensics needed. Dedup'd vs
`docs/ideas/` — distinct from seat-digest-adaptive-clip, the flip-race fix,
and the enabler preflight.

⟲ **Previous-session review (2026-07-12 seat: bench run-10 + close-out
#306/#307):** it left a verified trigger ledger that made boot cutover
trivial — repeat that. Its gap: no tick-delivery ledger, which tonight's
silent drop showed is worth adding (hence the 💡 above).
