# 2026-07-12 — ORDER 015: dead boot-pointer fix + gate-integrity verify

> **Status:** `complete`

- **📊 Model:** fable-5 · high · order-execution

## Scope (what is about to happen)

About to execute inbox ORDER 015 (2026-07-12T08:30Z, P1): kill the
dead-boot-pointer class in `src/engine/templates/AGENT_ORIENTATION.md.tmpl`
(engine-computed `${agreement_home}` slot: `.claude/CLAUDE.md` when live or
opted-in, else the always-planted root `CONSTITUTION.md`) with regression
tests + dist rebuild, and settle the VERIFY-FIRST rider: fixture-based
evidence that the shipped session gate holds an added in-progress card red,
retracting the v3.1 census's "added-card advisory loophole" /
"severity-tier drift" claims. Lane claim:
`control/claims/claude-order-015-boot-pointer.md` (merged to main via #260
@ 5bc24ac).

## Close-out

**Claim A (dead boot pointer) — REAL, fixed (PR #261):**

- Premise re-verified at HEAD: the template's lines 10–12 and 34 hardcoded
  `.claude/CLAUDE.md`, while `ADOPT_PLAN` (src/engine/adopt.py) plants the
  router unconditionally and `CLAUDE.md.tmpl` is deliberately staged-only —
  live only under the explicit `include_claude` opt-in. Verified dead in
  3/3 adopters (superbot-next dab14ad, venture-lab f92a2ef, fleet-manager
  6391b2f: all have `docs/AGENT_ORIENTATION.md` live, none have
  `.claude/CLAUDE.md`, all have root `CONSTITUTION.md`).
- Fix (the minimal shape that keeps one-home): new engine-computed slot
  `agreement_home` — logic in ONE place, `engine.render.agreement_home()`
  (returns `.claude/CLAUDE.md` iff live in the target or `include_claude`
  for this run, else `CONSTITUTION.md`); added to `ENGINE_CONTEXT_KEYS`;
  injected at adopt (next to the `integration_mode` idiom), at upgrade's
  `_upgrade_context` (same existence rule as `_doc_plan`, so doc-diff
  classification can't misclassify an untouched orientation doc as
  diverged), and at `cmd_render` (staged/live renders never strand the
  slot). Template: both hardcoded references replaced with
  `${agreement_home}`; section-anchor prose made generic (CONSTITUTION.md
  has no "Orientation — read first" / "Verifying a change" sections, so the
  pointer now names "the working agreement" + its orientation/verify
  guidance, valid for both targets).
- Rendered pointer lines, verified both modes:
  - default adopt: "The boot set lives in the working agreement —
    \`CONSTITUTION.md\` — and its" / "See the working agreement
    (\`CONSTITUTION.md\`) and its verify guidance"; the string
    `.claude/CLAUDE.md` appears NOWHERE in the rendered doc.
  - include_claude adopt: "The boot set lives in the working agreement —
    \`.claude/CLAUDE.md\` — and its".
- Tests: 3 new (default-adopt pointer + no-dead-string, include_claude
  pointer, `agreement_home()` unit) — suite 1060 passed. `ruff check
  src/engine/` clean. `dist/bootstrap.py` rebuilt via
  `python3 src/build_bootstrap.py` (byte-pin green: committed dist ==
  fresh build). Carried to adopters at the next release wave.

**Claim B (gate integrity) — NOT REAL at HEAD, RETRACTED (evidence below).**

## Gate-integrity fixture evidence

Fixture: a pristine copy of origin/main @ 5bc24ac (git archive, shipped
`dist/bootstrap.py` untouched) in the session scratchpad
(`order015-fixture/`, not committed), plus one synthetic added card
`.sessions/2026-07-12-fixture.md` with badge `in-progress`.

**In-progress card — both gate shapes hold RED (exit 1):**

Command A (the kit ci.yml Session-gate shape):

```
$ python3 dist/bootstrap.py check --strict --require-session-log --session-log .sessions/2026-07-12-fixture.md
check: session log .sessions/2026-07-12-fixture.md is missing: Session idea (expected `💡`), Previous-session review (expected `previous-session review`), a completed Status (badge still says in-progress)
check: HOLD (by design): session card .sessions/2026-07-12-fixture.md declares an in-progress Status — the born-red session gate holds the merge red until the card flips complete. This red is the designed hold, not a defect; nothing to investigate.
EXIT=1
```

Command B (the generated adopter gate's added-card invocation, verbatim
shape from `live_ci_workflow`):

```
$ python3 dist/bootstrap.py check --strict --session-log .sessions/__born-red-card-added__.md --added-card .sessions/2026-07-12-fixture.md
check: 1 finding(s):
  [session-card-hold] .sessions/2026-07-12-fixture.md: born-red HOLD: this PR ADDS a session card that declares an in-progress/drafted Status — the gate holds the merge red until the card flips complete (designed hold, not a defect). Without this hold a card-only born-red PR with auto-merge pre-armed merges the instant CI reports (superbot-games #40 merged in 24 s on exactly this).
check: --session-log .sessions/__born-red-card-added__.md does not exist (advisory — not a failure).
check: HOLD (by design): session card .sessions/2026-07-12-fixture.md declares an in-progress Status — the born-red session gate holds the merge red until the card flips complete. This red is the designed hold, not a defect; nothing to investigate.
EXIT=1
```

**Same card flipped `complete` + required markers — both shapes GREEN
(exit 0):**

```
$ python3 dist/bootstrap.py check --strict --require-session-log --session-log .sessions/2026-07-12-fixture.md
check: session log .sessions/2026-07-12-fixture.md complete.
check: all checks passed.
EXIT=0

$ python3 dist/bootstrap.py check --strict --session-log .sessions/__born-red-card-added__.md --added-card .sessions/2026-07-12-fixture.md
check: --session-log .sessions/__born-red-card-added__.md does not exist (advisory — not a failure).
check: all checks passed.
EXIT=0
```

**Source citations (verified this session):** kit `ci.yml` Session gate
(lines ~221–272) grades every diff card through
`check --strict --require-session-log`; the generated adopter gate uses
`--added-card` (adopt.py ~918–924) → `check_added_card`
(check_session_log.py ~174–215) → born-red HOLD findings are never
allowlistable and exit 1 in strict (cli.py ~832–859, 1215); the #228
G-1 (modified-sibling cards graded through the locked door) and G-2
(card deletions hard-red) fixes are live (adopt.py ~889–907). No formal
severity tiers exist; every advisory lane matches its documented contract
(docs/operations/auto-merge-guards.md guard 6 enforcing; the D-0007 split
at cli.py; the unadopted auto-draft carve-out is documented and gate-mode
unaffected).

**Verdict: the added-card advisory loophole is CLOSED at HEAD (#228
G-1/G-2 live); severity-tier drift NOT FOUND — the v3.1 census
gate-integrity claims are RETRACTED.**

## Session enders

💡 **Session idea:** an adopt-time dead-pointer linter — after render,
grep every planted doc for repo-path references (`.claude/...`, `docs/...`,
root-level `*.md`) and fail (or loudly warn) when a referenced path does
not exist in the target tree. Generalizes this bug class beyond the one
pointer the template happened to hardcode: any future template edit that
names a file the adopt doesn't install gets caught at plant time instead
of shipping to 3/3 adopters. Cheap: the doc set is small and the check is
a path-exists loop over regex hits.

⟲ **Previous-session review:** the #258 lab slice's friction triage fed
this session directly — sbn's weak-form-gate finding and this ORDER's
census rider both trace to the same failure class: gates/pointers
*claimed* but never *verified* against the shipped artifact. The
fixture-evidence pattern used here (pristine copy of main + synthetic
input + verbatim command/exit-code transcript on the card) is the reusable
answer, and it is cheap — ~5 commands. Concrete workflow improvement:
when a census/review claims a guard is broken, the FIRST move should be a
fixture run of the shipped guard, not a source-reading argument — the
transcript settles it either way and doubles as retraction evidence.

Documentation audit: `check --strict` green at flip (below); the durable
homes are this card (evidence), control/status.md (heartbeat + cadence
record correction), and the engine/template/tests diff itself. Claim file
deleted this commit.
