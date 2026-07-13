# 2026-07-13 · night-outcomes — adopter-outcome writeup (ORDER 016 item 5)

> **Status:** `complete`

Did: night-run adopter-outcome sweep + report under ORDER 016 item 5 —
classified all 13 roster seats plus the kit's own seat for the
2026-07-12T20:00Z→~05:00Z window and correlated the outcomes with the kit
mechanisms the shipping seats exercised. PR #319.

## What shipped

- `docs/reports/2026-07-13-night-run-adopter-outcomes.md`: the report —
  headline **11 SHIPPED · 2 IDLE-CLEAN · 0 STALLED** (superbot 13 merges ·
  superbot-next 55 · websites 42 · mineverse 19 · games 13 · idle 8 · gba
  8 · trading 19 · venture 48 · idea-engine 21 · sim-lab 15; plugin-hello
  dormant seed, product-forge archived-by-design). Mechanism analysis with
  citations: enabler installed in-window at 4 seats + sim-lab's zero-agent-
  merge live-fire proof; three platform-side wake drops ALL bridged by the
  Q-0265 failsafe ceiling; born-red gate exercised broadly + the one bug of
  the night (flip-race fail-open, mineverse finding); control fast lane
  (24s open-to-merge floor); owner ORDER fan-out landed verbatim
  ~00:42–00:51Z fleet-wide; heartbeat-currency honest finding (delegated
  coordinator tallies); CAPABILITIES walls discipline. Plus the honest
  null: zero seats stalled, so shipped-vs-stalled discrimination is not
  derivable from tonight's evidence — what is derivable is which
  mechanisms absorbed faults.
- `docs/operations/README.md`: reachability link for the report (the
  reports reachability root — kept out of the K0 boot set by design).
- 3 guidance-delta idea files + README backlog entries (each deduped
  against `docs/ideas/` first):
  `session-gate-flip-race-fail-open-2026-07-13.md`,
  `enabler-install-preflight-2026-07-13.md`,
  `heartbeat-delegated-tally-guidance-2026-07-13.md`.
- Pre-flip CI triage: the three reds on 79df313 (kit-quality + the two
  legacy alias contexts "Kit test suite" / "Cold-adoption smoke") all
  trace to the single designed born-red hold — the aliases fail-by-design
  whenever kit-quality is not success (the KL-1 PR #7 skipped-alias hole,
  ci.yml `legacy-alias-*`). Local: pytest 1234 passed; `check --strict`
  red only on this card's hold. Nothing to fix; the flip clears all three.

## Verify

- `python3 -m pytest tests/ -q` → 1234 passed
- `python3 dist/bootstrap.py check --strict` → green except this card's
  own designed born-red hold (pre-flip; re-run after the flip below)

## Enders

💡 **Session idea:** a `night-run outcome sweep` kit skill — tonight's
survey procedure (fetch origin/main heartbeats → PR listings under an API
cap → classify SHIPPED/IDLE-CLEAN/STALLED by PR record + coordinator
status → mechanism citations) was re-derived from scratch for this report;
as a registered method skill it becomes reusable at every seat and every
recurring night run. Dedup-grepped `docs/ideas/` + the 13-skill registry
(`src/engine/skills/skills.py`) — no sweep/survey skill or idea exists.

- **📊 Model:** Claude (Fable family)

⟲ **Previous-session review (PR #317, rider graduation / ratification
park):** the parking order was followed exactly right — auto-merge
disarmed BEFORE the `do-not-automerge` label, CI re-run post-label, and
the owner-gate rationale (PL-012 law surface per check_program_law)
recorded in a PR comment + status.md + the PR body, so the park is
triple-cited and auditable. What it could have done better: disarm state
is only provable by prose on this surface (the raw `auto_merge` REST
field is walled), so tonight's audit had to trust three prose citations.
System improvement: have the disarm workflow leave a machine-readable
receipt (a check run or a structured comment marker) so a parked PR's
disarm state is verifiable without prose trust — candidate for the next
groom pass alongside the flip-race fix.
