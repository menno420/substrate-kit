# 2026-08-05 · Close out the session's guard-fire telemetry, and name the loop

> **Status:** `complete`

- **📊 Model:** opus-5 · high · telemetry-only

💡 Session idea: **`check --strict` writes to a tracked file, so verifying a
commit dirties the tree that commit just cleaned.** Follow the discipline
literally — commit the delta, then run the gate post-commit to verify — and you
generate a new delta every round. It terminated four times today only because a
human stopped running the check. That is a real wart in an otherwise sound
ritual, and it is worth a design decision rather than a habit of quietly
discarding the tail.

## previous-session review

`2026-08-05-guard-fires-telemetry.md` (#575) was held by the gate for having no
session card, correctly, and recorded the contrast with fleet-manager merging
three identical PRs without one. Landing it produced this delta, which is the
loop above. The mechanism that caught the missing card is the same mechanism
that cannot stop generating work for itself.

## What landed

- `.substrate/guard-fires.jsonl` — 29 records from the verification run on #575.

## Verification

- The content verified is #575's, which passed `dist/bootstrap.py check
  --strict` → **exit 0** before merge, and merged with its CI green.
- **The gate was deliberately NOT re-run after this commit**, and that is the
  point of the card. Re-running it would append fresh records and re-dirty the
  tree, producing the next round of exactly this PR. Nothing here changes
  source, templates or tests — it is the gate's own output, so gating it again
  measures nothing and costs another cycle.

**Honest null.** Three options existed and none is clearly right: commit and
re-verify (loops), commit and stop (this — breaks the post-commit rule for one
narrow file), or discard the tail (contradicts the kit's own "commit the delta,
do not revert"). Choosing the second is a judgement, not a rule the repo
supports, and it is flagged rather than hidden. A durable fix would be for
`check` to write telemetry only under CI, or for the ritual to name this file as
exempt from the post-commit re-run.
