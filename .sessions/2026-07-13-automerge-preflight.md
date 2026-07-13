# Session: auto-merge-enabler branch-allowlist preflight

> **Status:** `complete`
>
> Run type: routine · lab

Did: groomed the night-run backlog (friction inbox EMPTY) and shipped the
offline-verifiable half of the enabler-install-preflight idea
(`docs/ideas/enabler-install-preflight-2026-07-13.md`, night-run finding —
INERT enablers hit 3 seats). A self-silencing `check`-time advisory that
flags when the installed `auto-merge-enabler.yml`'s branch allowlist drifts
from config — the idea-engine hand-patch/stale-allowlist class (PR #272 "add
claude/ to allowlist"; outbox flagged "a kit upgrade will clobber the local
fix"). PR #321.

## What shipped

- `src/engine/checks/check_automerge_preflight.py`: a new advisory checker.
  When the planted `.github/workflows/auto-merge-enabler.yml` exists, it
  parses the live workflow's branch terms (`startsWith(github.head_ref,
  'X')` → prefix, `github.head_ref == 'Y'` → exact) into a set and compares
  it to what `automerge.branch_patterns` would regenerate (via adopt's own
  `_automerge_branch_expr` + `_automerge_params` — apples-to-apples). Drift
  → `automerge-branch-drift`, naming both allowlists and pointing the fix at
  config + a regenerate. Self-silences when they match.
- Decide-and-flag — **branch expr, not whole file**: the branch expr is
  derived purely from config, so it is stable across kit-version bumps; a
  whole-file byte-compare would nag the whole fleet during version skew (and
  that scan already lives in the adopt/upgrade carve-out report).
- Decide-and-flag — **branch half only**: the required-context precondition
  (does the base branch REQUIRE a status context) can't be verified offline
  (stdlib-only engine, no rules API). It stays owner-UI — already surfaced
  by the enabler's PR-time `::warning::` (refuse-to-arm on zero) + the adopt
  checklist. Named explicitly in the module docstring, not silently dropped.
- `src/engine/cli.py`: import + call + emit block, following the identical
  warn-only advisory contract as the setup-script / seat-digest / adopters
  nudges (never exit-affecting; full-lane only; telemetry-recorded).
- `src/build_bootstrap.py`: registered the module after `adopt.py` (reuses
  its enabler generator). `dist/bootstrap.py` regenerated (byte-pin).
- `tests/test_check_automerge_preflight.py`: 11 tests — writer/enforcer pin
  (the kit's own generated enabler passes clean), custom-config match,
  stale-allowlist + hand-edit drift reds, input-gating, no-head_ref silence,
  advisory posture under `--strict` + `--status-only`, and the term parser.
- `docs/ideas/enabler-install-preflight-2026-07-13.md` + `docs/current-state.md`
  ▶ Next action: recorded the branch half shipped and the required-context
  half + flip-race + heartbeat-tally still open.

## Verify

- `python3 -m pytest tests/ -q` → 1245 passed (1234 + 11 new)
- `python3 dist/bootstrap.py check --strict` → green except this card's own
  designed born-red hold (pre-flip); the new advisory self-silenced on the
  kit's own enabler (live branch expr {claude/, claim/} matches config).
- `python3 -m ruff check src/engine/` → All checks passed!
- `python3 src/build_bootstrap.py` → dist byte-equal after rebuild
- `python3 scripts/check_idea_index.py` → OK

## Enders

💡 **Session idea:** extend the enabler preflight to the `required_context`
knob — the engine can offline-cross-check `automerge.required_context`
(default `substrate-gate`, the context the enabler's log + adopt checklist
tell the owner to make required) against the job NAME the planted gate
workflow (`live_ci_workflow`) actually publishes. If they disagree, the
owner is told to require a context that never appears, and the enabler is
INERT forever — a name mismatch the engine can catch without the rules API
(unlike the required-*ness* half). One `_branch_terms`-style parse of the
gate workflow's `name:`, folded into this same checker. Dedup-grepped
`docs/ideas/`: `engagement-wiring-strength-verification-2026-07-12.md` is
adjacent but covers `check --strict` wiring STRENGTH + required-*ness* (the
online half); this is offline name-consistency between two planted kit files
— distinct, and small enough to graft onto today's module.

- **📊 Model:** Claude (Opus family) · high · feature build

⟲ **Previous-session review (PR #320, ORDER 016 night-run tally):** the
morning-clause tally is a model of honest measurement — it split "11 merged
+ 1 green-parked" cleanly, wrote "templates released = 0 tagged" with the
reason (graduation rides #317 ratification) instead of padding the count,
and led the report's headline with the honest null ("0 STALLED, so
shipped-vs-stalled discrimination is not derivable tonight") rather than
burying it. It also correctly routed the flip-race fail-open as an idea
(not a blind fix) — the same posture this run took. What it could have done
better: the tally names the flip-race bug in the outbox but left no pointer
FROM the bug's idea file TO the tally/report §c that cites it, so the
grooming session (this one) had to re-derive the cross-citation by reading
the report — a one-line `Cross-cited by …` was in the idea body, but the
reverse link (report → idea) is prose-only. System improvement: when a
night tally cites a routed idea, stamp the idea's `shipped_pr`/provenance
line with the tally PR too, so the backlog groom lands on the idea from
either direction.
