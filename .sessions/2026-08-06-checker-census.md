# 2026-08-06 · Classify every checker, and take the heuristics off the agent's channel

> **Status:** `complete`

- **📊 Model:** opus-5 · high · foundation-verification

💡 Session idea: **the kit's advisory tier is not a weak gate, it is a loud
one.** Measured today: `check --strict` output is 87% advisory on substrate-kit
and 90% on fleet-manager, both exiting 0. Every firing tag is an aging nag or a
false positive — 13 walls titled `'any'`, a "command" called `READ FIRST`. The
signal-to-noise ratio in the exact channel an agent reads to decide whether it
is done is about 1:9. Nothing was wrong with any individual checker's
reasoning; the failure is that nothing ever classified them, so they all print.

## previous-session review

`2026-08-05-telemetry-close.md` (#576) closed the guard-fire telemetry loop and
flagged, as an honest null, that `check --strict` dirties the tree it verifies.
That wart is real and this session hits it too — the same commit-the-delta-and-
stop discipline applies here, and for the same reason.

The foundation continuation doc (`fleet-manager
docs/findings/2026-08-05-foundation-continuation.md` § 5) reasoned that the
advisory field should come off the agent's feedback channel, and labelled the
conclusion `REVIEWED` — argued, not measured. This session measures it.

## What this lands

- `src/engine/guards.py` — `CHECKER_CENSUS`, the fifth pinned surface: every
  checker `cmd_check` invokes, classified `DETERMINISTIC` or `HEURISTIC` with a
  reason, plus a `gate_ready` flag on the deterministic ones. Anchor floors and
  pure accessors, matching the four censuses already there.
- `tests/` — a meta-test asserting bidirectional set-equality between the
  census and the live `cmd_check` / `_extra_check_findings` call sites, so a
  checker cannot ship unclassified.
- `src/engine/cli.py` — advisory emission routed by the census. Deterministic
  advisories stay inline; heuristic ones go to the advisory report and leave a
  single summary line behind. Guard-fire telemetry is unchanged for both.
- `bootstrap.py check --gate-preview` — reports which deterministic checkers
  *would* red this tree if promoted, so the promotion can be measured across
  all adopters instead of guessed.

## Verification

- `python3 -m pytest tests/ -q` → **2124 passed, 1 skipped** (exit 0, read
  directly, not through a pipe).
- `python3 -m ruff check src/engine/` → **All checks passed** (the no
  print/assert/subprocess bans).
- `python3 src/build_bootstrap.py` re-run; `dist/bootstrap.py` byte-pin holds.
- CI at `ca5a6a4` confirmed the three substantive steps green — *Kit test
  suite*, *Dist byte-equality pin*, *Engine lint bans* — with the ONLY red
  being *Session gate (§3.2 — the born-red discipline)*, i.e. this card. The
  two sibling job reds are the documented legacy aliases that report
  `kit-quality`'s result verbatim (`WORKFLOW_JOB_CENSUS`).
- Effect measured on two trees: `check --strict` **47 → 7 lines** here,
  **89 → 10** on fleet-manager; exit codes unchanged on both; all findings
  still reachable under `--advisories`.
- `check --gate-preview` → 0 deterministic sites carry findings on either
  tree, so promoting them would red neither.
- Every doc named by the new `CONSTITUTION.md` boot path verified to exist
  before landing.

**Honest nulls.**

- **The promotion is not made.** The handoff asked for the deterministic
  checkers to be wired to the gate; they are classified and the routing is
  built, but flipping eight checkers to hard-red across ~22 adopters on two
  trees' worth of evidence is the same unverified change this surface exists
  to catch. `--gate-preview` turns it into a sweep. That sweep is the next
  slice and it has not been run.
- **The 21 heuristic checkers were classified, not repaired.** The
  `'any'`-titled stale-wall rows and the `READ FIRST` skill-grounds rows are
  real bugs in those extractors. Moving them off the channel makes them cheap
  to leave broken, which is also how they stay broken.
- **§ 5 of the continuation doc asked for a scheduled owner report** of the
  suppressed tail. Not built. `--advisories` and the guard-fire ledger hold
  the data; nothing yet delivers it to him on a cadence.
- **Whether a session legitimately wanted the removed signal is
  `UNVERIFIED`** and cannot be measured from inside the session that removed
  it. Mitigated only by nothing being deleted.

⟲ The telemetry wart from the previous card recurred exactly as it predicted:
`check --strict` appends to `.substrate/guard-fires.jsonl`, so verifying a
commit dirties the tree it just cleaned. Followed the same resolution —
commit the delta, stop, do not loop.
