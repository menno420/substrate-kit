---
state: captured
origin: consumer:menno420/superbot
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Engagement gate: a "native-substrate consumer" state for pin-only repos (2026-07-12)

> **Status:** `ideas`
>
> **State:** captured → route: quick-win-sized engine change, **frozen until
> the 2026-07-11 feature freeze lifts** (new checker semantics = new surface).
> **Origin:** consumer:menno420/superbot — friction issue
> [#37](https://github.com/menno420/substrate-kit/issues/37), filed by the
> 2026-07-09 fleet adoption review; triaged and closed by the 2026-07-12
> lab-loop run (this file is the backlog home).

## The gap

PL-011 (`docs/program/rulings.md`) defines adoption-done as ENGAGED:
rendered docs + enforcement wired (a CI workflow runs `check --strict`) +
session loop running. superbot is the definitional hole: it carries
adoption evidence (`substrate.config.json` pin — `check_engagement.py`'s
`_adoption_evidence` treats a recorded pin as adopted) but has **zero**
workflows containing `check --strict` — while being the repo with the
STRONGEST native enforcement in the fleet (required code-quality check,
born-red session merge-gate, 850+ session cards). If the engagement gate
ever ran there it would red `enforcement-unwired` on a repo whose door is
real, just not kit-shaped — a false positive of the exact
"looks-X-isn't" class PL-011 targets, inverted.

Re-verified at triage (2026-07-12): superbot pin still `1.0.0`,
`.github/workflows/` still has no `check --strict`/`bootstrap` hit;
PL-011 merged (owner-merged #26, 2026-07-10) **without** a
native-consumer state — the #37 input arrived after the ruling text was
drafted and was never incorporated.

## The fix (either shape, decide at build time)

1. **An allowlisted evidence class:** `substrate.config.json` gains a
   declared `native_gate` field (e.g. the workflow path + required-check
   context that constitutes the door); `_enforcement_wired` accepts a
   declaration whose named workflow exists, reporting it distinctly
   (`enforcement-native` — visible, never silent).
2. **Or:** the engagement checker accepts any workflow matching the
   declared native gate needle, not just `check --strict`.

Both keep PL-011's letter (a door must exist and be visible in-tree) while
ending the pin-only false-positive class. Severity today LOW (nothing runs
the gate on superbot), MEDIUM the moment superbot upgrades from pin-only —
which is itself owner-gated.

## Guard recipe

`src/engine/checks/check_engagement.py` — `_adoption_evidence` (pin
detection) + `_enforcement_wired` (the needle test) are the two anchors; a
fixture repo with a pin + a declared native gate + no `check --strict`
workflow must read ENGAGED-native, and the same fixture without the
declaration must stay `enforcement-unwired`. Engine change → dist byte-pin.
