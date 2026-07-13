---
state: promoted
origin: consumer:menno420/superbot-mineverse
shipped_pr: 342
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-13
outcome: shipped
---

# Session gate: fix the born-red fail-open on PR-added cards (flip-race) (2026-07-13)

> **Status:** `ideas`
>
> **State:** shipped — split closure, both halves resolved (PR #342,
> ORDER 019 item 1).
> **Origin:** consumer — surfaced live on the 2026-07-12→13 night run at
> superbot-mineverse: PR #50 had to land stranded close-out flips for PRs
> #48/#49, root-caused in PR #52; finding preserved at mineverse
> `docs/findings/substrate-gate-born-red-fail-open-2026-07-12.md`, fix ask
> routed to this kit via mineverse control/outbox.md. Cross-cited by the
> night-run report `docs/reports/2026-07-13-night-run-adopter-outcomes.md`
> §c.

## The gap

The born-red session gate could fail open in a flip race on PR-added cards:
a card's flip could merge without the gate holding, leaving stranded
in-progress cards that a later PR must sweep. The mineverse finding file
carries the reproduction.

## Outcome (honest closure, 2026-07-13, PR #342)

Two distinct halves; both are closed, by different PRs:

- **CI-side fail-open — VERIFIED ALREADY CLOSED at HEAD, not by this
  idea's PR.** The v1.10.0 added-card HOLD closed it (`check_added_card`,
  `src/engine/checks/check_session_log.py` — the `session-card-hold`
  finding; shipped PR #176, tightened through v1.12.x: modified siblings
  gate through the locked door, deletions hard-red). Mineverse's own live
  gate is the installed v1.15.0 generated workflow, which carries the
  hold — the stranded cards it swept predate/raced that protection window.
  PR #342 PINS the hold→release cycle with regression tests through the
  real CLI path (`tests/test_cli_gate.py::
  test_flip_race_added_card_holds_then_releases_on_flip` and the
  diff-derived-lane sibling) so the race cannot silently reopen.
- **Local-selection false-green (the remaining live defect) — FIXED by
  PR #342.** `check`'s fallback lane picked the gated card by newest
  mtime; after merging origin/main a sibling's COMPLETED card carries the
  freshest mtime, so local `check --strict` validated the WRONG card and
  went green while the session's own card was still in-progress
  (reproduced live, sim-lab V051; routed as idea-engine ASK 003). The
  lane now derives the card set from the merge-base diff vs origin/main
  (`engine.cli._derive_diff_session_cards`, a documented §3.2 git
  carve-out mirroring `_derive_inbox_base`), grades fail-closed
  (`_select_gate_card`), and keeps newest-by-mtime only as the non-git
  fallback.

## Size / risk

Contained gate-logic change + regression tests pinning the race; reversible;
engine change → dist byte-pin in the same PR (as shipped).
