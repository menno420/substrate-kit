---
state: promoted
origin: consumer:menno420/substrate-kit
shipped_pr: 402
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-15
outcome: shipped
---

# Engagement gate: verify wiring STRENGTH, not just existence (2026-07-12)

> **Status:** `ideas`
>
> **State:** promoted → **shipped** kit PR #402 (2026-07-15, anticipated
> in-PR date): both advisory layers — the `enforcement-weak-form` finding
> (`check_enforcement_strength`: plain-form wired door + staged gate
> carrying `--require-session-log` / diff-aware `--session-log` /
> `--inbox-base` → one advisory naming the missing legs + the staged file
> to copy, never strict-red) and the `enforcement-required-unverified`
> honesty NOTE (`required_unverified_note`, emitted by `check`'s full lane
> beside the `enforcement-native` NOTE).
> **Origin:** the residuals of two 2026-07-09 fleet-review friction
> reports, triaged and closed by the 2026-07-12 lab-loop run:
> [#36](https://github.com/menno420/substrate-kit/issues/36) report 3
> (required-check status unverifiable by agents) and
> [#38](https://github.com/menno420/substrate-kit/issues/38)
> (superbot-next's weak-form gate). This file is the backlog home for the
> kit-side halves; the adopter-side half of #38 is relayed via
> `control/status.md` ⚑ FOR MANAGER.

## The gap — two layers of the same blindness

`_enforcement_wired` answers only "does a workflow mention
`check --strict` outside a comment?" Two verified ways a repo passes that
test with a weaker door than it looks:

1. **Weak-form wiring (#38, re-verified 2026-07-12 at superbot-next
   `c03df80`):** `ci.yml`'s checkers job runs plain
   `python3 bootstrap.py check --strict` — no `--require-session-log`, no
   diff-aware `--session-log` card selection (mtime fallback grades the
   wrong card on multi-card diffs — the realized
   `folded-gate-diff-aware-card-2026-07-11.md` class), no control fast
   lane, no `--inbox-base` (the inbox append-only gate is LATENT there,
   the exact v1.7.0-wave finding that hit every adopter). The engagement
   gate reads this as fully wired.
2. **Required-ness unverifiable (#36 r3):** whether the wired check is a
   REQUIRED status check is owner-UI state, invisible in-tree and
   403-walled to agents (proven: superbot-next #51/#68 merged with red
   non-required legs). Partial coverage since: the `mergeable_state ==
   "behind"` inference recipes live in `docs/CAPABILITIES.md`
   (2026-07-10 entries) and v1.9.0's `automerge.required_context`
   plant-time validation flags a context that matches no job. Missing:
   the checker saying so honestly.

## The fix (advisory-only, both layers)

- **Strength advisory:** when the wired needle is the plain form and the
  staged `<state_dir>/ci/substrate-gate.yml` carries the stronger form,
  emit one advisory naming the missing legs (`--require-session-log`,
  diff-aware selection, `--inbox-base`) and the staged file to copy.
  Never strict-red — a hand-rolled gate is legitimate (the kit's own
  `ci.yml` folds differently).
- **Required-ness honesty:** an `enforcement-required-unverified` advisory
  note when the gate cannot confirm required-check status (always, today)
  — "owner glance needed" — optionally upgraded to a real API probe when a
  token with the right scope is present.

## Guard recipe

`src/engine/checks/check_engagement.py` `_enforcement_wired` (return shape
would grow from bool to a finding-capable probe); staged-gate reference
text under `config.state_dir`/ci/. Fixtures: plain-form workflow + staged
strong gate → advisory fires; strong-form workflow → silent. Engine
change → dist byte-pin.
