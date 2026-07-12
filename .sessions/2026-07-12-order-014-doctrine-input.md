# 2026-07-12 — ORDER 014: prompt-template hardening input

> **Status:** `complete`

- **📊 Model:** fable-5 · high · order-execution

## Scope (what is about to happen)

About to execute inbox ORDER 014 (2026-07-11T23:45Z, P1): author the
prompt-template hardening input for the 2026-07-12 fleet prompt rebuild —
`docs/reports/2026-07-12-prompt-template-hardening-input.md` (must-carry
doctrine list per regression class, template-graduation map, corrections to
stale kit facts in the fleet prompts) — plus a `control/outbox.md` pointer,
a surgical `control/status.md` heartbeat update, and the claim-file delete.
Lane claim: `control/claims/claude-order-014-doctrine-input.md` (merged to
main via #255 @ 18a9f58).

This card opened the PR born-red by design (session gate HOLD); the
close-out, 💡 idea, and ⟲ review sections below were written at flip time.

## Close-out

**What was done (PR #256):**

- **Premise verified first:** ORDER 014 present verbatim in
  `control/inbox.md` at HEAD 1295d73; `control/claims/` empty (README only);
  the only open PRs the parked pins #220/#238 — nobody on the order.
- **Claim landed on main FAST:** #255 (squash 18a9f58) via the control fast
  lane, one-file claim per `control/claims/README.md` grammar.
- **The deliverable:**
  `docs/reports/2026-07-12-prompt-template-hardening-input.md` — (a) the
  must-carry seat-prompt doctrine per regression class (routine
  arming/seat-dependence + pacing, landing path/born-red gates + label
  races, verify-don't-trust/probe-not-record, heartbeat grammar, claims,
  preflight sync), each with cited incidents + enforcing-guard status;
  (b) the template-graduation map — landing-path and routines doctrine are
  the missing templates (fm meta.md's own "known kit gap"); (c) six
  fact-check verdicts on the fleet prompts fetched at fm HEAD e801da5c
  (retired trigger ids, archived-session binding, lab-loop's falsified
  "cannot arm itself", stale counts, the display anomalies, instructions.md
  clean). Badged `audit`, linked from `docs/operations/README.md`
  (reachability root).
- **`control/outbox.md` CREATED** (did not exist — the ORDER names it as the
  pointer home; header follows the one-writer protocol) with the ORDER 014
  deliverable pointer entry.
- **Heartbeat (surgical):** `updated:` bump; ORDER 014 DONE sentence
  prepended to phase; orders acked/done append 014; last-shipped updated;
  ONE ROUTINE STATE line recording the two registry display anomalies
  (env id + model-class reads; probed 2026-07-12 ~00:08Z, no churn).
  Everything else byte-identical.
- **Verification:** `python3 -m pytest tests/ -q` → 1057 passed;
  `python3 dist/bootstrap.py check --strict` → sole pre-flip finding the
  designed born-red HOLD naming this card (two self-caused findings — badge
  token + orphan reachability — fixed in-PR before the flip).
- **Close mechanics:** claim `control/claims/claude-order-014-doctrine-input.md`
  deleted; this card flipped `complete` as the deliberate last step.

## 💡 Session idea

Render the seat-prompt doctrine blocks from ONE template source: the kit
already owns the portable doctrine (CONSTITUTION/collaboration-model
templates) and the fleet prompts hand-copy it — which is exactly how the
§(c) staleness class regenerates. A `bootstrap render --seat-prompt` target
(or a `seat-prompt.md.tmpl` whose rendered block the fleet-manager package
files include verbatim, with a generated "NOT SOURCE OF TRUTH" marker) would
make a fleet prompt structurally unable to drift from kit truth — the same
move that ended heartbeat-grammar drift (grammar.py as the single constants
home, pinned by tests).

## ⟲ Previous-session review

The #252/#253 pair is the strongest verify-don't-trust evidence the lane has:
two sessions in one evening independently probe-corrected routine-state
records (the failsafe "already deleted" yet armed; the loop "verified live"
yet vanished), and #253's exhaustive 718-entry walk upgraded #252's hedged
negative to CONFIRMED — exactly the "walk absence proofs to exhaustion"
discipline its own review called for. What the pair leaves undone: both
lessons live in prose and session cards only; #252's registry-snapshot-diff
idea (committed list_triggers snapshot diffed against ROUTINE STATE ids at
every heartbeat) is reinforced, not shipped — it would have caught the
vanished loop trigger mechanically and is the natural next kit checker.
