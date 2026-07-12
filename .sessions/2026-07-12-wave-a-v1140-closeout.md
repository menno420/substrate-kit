# 2026-07-12 — kit v1.14.0 distribution wave A close-out

> **Status:** `complete`

- **📊 Model:** Fable 5 · distribution-wave close-out

## Scope (what is about to happen)

wave A close-out: adopters regen + status record + claim delete + team-memory
gotchas append.

## What happened

- **Adopters regen** (runbook §6): `python3 dist/bootstrap.py currency` ran
  clean first try (no SSL retry). All four wave-A rows read **tree v1.14.0**:
  superbot-next (current · self-report DRIFT v1.12.1 — chronic heartbeat-lag
  class), websites (current · DRIFT v1.12.0, same class), superbot-games
  (current · DRIFT — status-mining/exploration at v1.7.1, main status has no
  kit: line), trading-strategy (current · DRIFT v1.13.0, same class). Kit's
  own row: the deliberate tree-internal pin DRIFT (§7 ⚑), not chased. With
  wave B's rows already current (#280), **all 9 vendored trees read
  v1.14.0** — the v1.14.0 distribution is complete.
- **control/status.md**: wave-A v1.14.0 record prepended to phase (per-repo:
  PR · merge SHA · CI · tree-verified; kit row-1 verify no-op with the
  three-way sha256), capability-seed wave outcomes, lane-owed follow-ups
  condensed, wave findings (dirty-PR invisible-red; Actions run-creation
  stall 13:45–14:12 UTC), blockers claim note updated (control/claims/ back
  to README-only). Wave B's record untouched.
- **control/claims/wave-a-v1.14.0.md deleted** (lane terminal).
- **Team memory** (kit-upgrade-distribution-gotchas): new "Verified at the
  v1.14.0 wave A" section — dirty-PR invisible-red gotcha + cure, the
  Actions stall window, capability-seed outcomes, no-SKILLS-orphan
  recurrence, websites pin-test line move (:149), trading-strategy +
  venture-lab enablers confirmed live; description parenthetical updated.
- Wave B's close-out (#280) had landed BEFORE this one — no conflict; each
  wave edited only its own status rows, and this regen snapshots the final
  all-nine-current state.

## 💡 Session idea

The dirty-PR invisible-red class (mergeable_state "dirty" → zero workflow
runs, get_status pending/0) is now a twice-recorded diagnosis pattern
(v1.9.0 memory line + superbot-next #260). The `upgrade-distribution` skill
body should gain a one-line triage step — "PR shows no CI at all →
check mergeable_state FIRST" — so the diagnosis lives in the runbook agents
actually execute, not only in team memory prose.

## ⟲ Previous-session review

The wave-A distribution legs handed this close-out paste-ready facts
(per-repo merge SHAs, seed outcomes, lane-owed lists), making it purely
mechanical — the same strength the wave-B close-out noted. Best diagnostic
work of the wave: identifying the superbot-next #260 zero-runs state as a
mergeable_state "dirty" conflict rather than chasing token/webhook theories
— that turned an apparent platform outage into a two-command fix.
Improvement: the guard-fires.jsonl cross-PR conflict has now bitten three
times (sbn #166, gba #67, sbn #260); the `merge=union` gitattribute idea
filed at the v1.13.0 wave should be promoted from idea to kit change — a
planted .gitattributes line would retire the whole class.
