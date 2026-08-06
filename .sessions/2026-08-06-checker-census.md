# 2026-08-06 · Classify every checker, and take the heuristics off the agent's channel

> **Status:** `in-progress`

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

Filled at close. Born red: this card is `in-progress` and the gate holds the
merge until it flips.
