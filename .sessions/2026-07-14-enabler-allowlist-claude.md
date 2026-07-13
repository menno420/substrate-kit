# 2026-07-14 — ORDER 019 item 2 / ASK 001: enabler allowlist `claude/*` — verification (no-op)

> **Status:** `complete`

About to: verify ORDER 019 item 2 (ASK 001 relay: "add `claude/` to the
auto-merge-enabler template allowlist", evidenced by idea-engine's jammed
green PR #271) against kit HEAD, and land the finding. Pre-dispatch
verification already indicates the claim is stale — the allowlist appears to
contain `claude/*` (and `claim/*`) since PR #300 — so the expected deliverable
is a verification-report PR only: no template or engine change, citations to
the exact source lines, heartbeat fact line, and this card.

Did (findings — no template/code change; verification record only):

- **The ask** (control/inbox.md @ 6de4494, ORDER 019 item 2): "ASK 001: add
  `claude/` to the auto-merge-enabler template allowlist — one-line, jammed
  green PR evidenced (#271) (idea-engine control/outbox.md ASK 001 @2808b16)".
- **STALE — already satisfied at source:** `src/engine/adopt.py` @ 6de4494
  line 1059 — `DEFAULT_AUTOMERGE_BRANCH_PATTERNS = ("claude/*", "claim/*")`
  (rationale comment ~1050–1061); `dist/bootstrap.py` @ 6de4494 line 12384
  identical; kit's own `.github/workflows/auto-merge-enabler.yml` @ 6de4494
  lines 53–54 match. Landed via PR #300, commit 18e5adc,
  2026-07-12T18:53:23Z — ~3h BEFORE ASK 001 was filed (2026-07-12T21:49:25Z).
- **Test-pinned already:** `tests/test_adopt.py` lines 1240–1241 assert
  `"claude/*"` and `"claim/*"` in `DEFAULT_AUTOMERGE_BRANCH_PATTERNS`;
  `tests/test_check_automerge_preflight.py` pins `_automerge_branch_expr`
  against the live workflow.
- **Evidencing jam resolved:** idea-engine PR #271 MERGED
  2026-07-12T21:35:36Z (jam was historical: first check wave 21:08Z had
  enable-auto-merge skipped; idea-engine's local fix PR #272 → daf9d50 added
  `claude/`; second wave 21:35Z succeeded). idea-engine's live
  `.github/workflows/auto-merge-enabler.yml` @ main 872c6fc already contains
  `startsWith(github.head_ref, 'claude/')`.
- **Conclusion:** no kit change needed; idea-engine's "verified-needed" (next
  kit-upgrade PR retains the `claude/` line) is satisfied by the current
  template. Deliverable = report PR #339 only.

Verify: `python3 -m pytest tests/ -q` → 1284 passed in 24.78s;
`python3 dist/bootstrap.py check --strict` → exit 0, red only on this card's
own designed born-red hold pre-flip (plus the standing preflight-script NOTE).

💡 Session idea: ASK staleness pre-check — when a manager relays an adopter
ASK into an inbox worklist, the relay should carry the kit HEAD SHA the ask
was verified against, and the sweeper should re-check the ask against current
kit HEAD before dispatch. ASK 001 was filed ~3h after #300 had already
shipped the fix, so this whole dispatch was avoidable — one SHA field plus one
pre-dispatch grep is cheaper than a full worker session. Dedup: closest
existing entry is `docs/ideas/dispatch-race-reverify-clause-2026-07-10.md`,
which puts re-verify on the *dispatched worker*; this is the missing upstream
half (relay/sweeper-side), kept card-only to hold this PR to its
control/+.sessions/ scope.

⟲ Previous-session review: `.sessions/2026-07-13-skill-grounds-dot-paths.md`
did exemplary evidence work — 0/0/0/0 four-adopter survey before tightening,
a mutation test proving the guard actually fires, and byte-stable dist regen
×2 — and its own review already named the improvement (commit the survey
harness). One concrete workflow improvement from this session's vantage: its
card cites adopter clones by bare SHA (superbot-next@4cc4b05 …) with no note
of *when* those SHAs were HEAD; the same staleness class that produced this
session's no-op dispatch would be caught earlier if evidence citations
carried a checked-at timestamp alongside the SHA.

⚑ Self-initiated: none.

- **📊 Model:** fable-5 · default · verification/no-op-report
