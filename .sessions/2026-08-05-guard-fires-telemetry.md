# 2026-08-05 · Commit the guard-fire telemetry from the step-0 gate runs

> **Status:** `complete`

- **📊 Model:** opus-5 · high · telemetry-only

💡 Session idea: this card exists because the gate demanded it, and the gate was
right. A telemetry-only PR is exactly the shape that *feels* too small for the
ritual — which is why the requirement is mechanical rather than a judgement
call. fleet-manager let three identical PRs through today without one; the kit
held. **That difference is the whole argument for wiring a rule to a gate.**

## previous-session review

`2026-08-05-owner-provisioning-step-zero.md` (#574) added step 0 to THE
DISCOVERY RULE and closed noting it has no mechanism — nothing can gate "a
session doubted its owner", so it binds only by being read. Ten minutes later
this branch got held by a rule that *does* have one. The contrast is the
clearest evidence in the repo for why the mechanism matters more than the wording.

## What landed

- `.substrate/guard-fires.jsonl` — 28 records appended by
  `dist/bootstrap.py check --strict` across the step-0 session's gate runs. The
  kit's own guidance is to commit the delta rather than revert it, since it is
  the ledger of which guards actually fired.

## Verification

- `python3 dist/bootstrap.py check --strict` → **exit 0** on the step-0 work
  that produced these records (#574, merged green: kit-quality, Kit test suite
  and Cold-adoption smoke all success).
- No source, template or test changed here; this is the telemetry byproduct only.

**Honest null.** The first attempt at this PR was **held by the gate** for
having no session card — correctly. Recorded rather than quietly fixed, because
the hold is the interesting part: the same class of PR merged three times in
fleet-manager today with no card, because that repo's gate does not require one.
Same discipline, two enforcement levels, two different outcomes.
