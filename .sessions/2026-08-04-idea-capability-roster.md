# 2026-08-04 · Capture the harness-capability-roster idea

> **Status:** `complete`

- **📊 Model:** fable-5 · high · idea/planning

💡 Session idea: **the owner's sharpest product observation of the day was
recorded nowhere until this file.** Three providers misreported their own
abilities in one day; the owner named the fix — a short harness-supplied
static-capability roster — and the estate had homes for measurements
(CAPABILITIES.md) and for law (rulings.md) but the idea itself lived only in
chat. Ideas need the conveyor as much as findings need the ledger.

## previous-session review

`2026-08-04-pl013-inhabiting-vs-observing.md` (PR #569, merged) minted the
day's law. This card captures the day's product idea — the two are siblings:
PL-013 says the environment must bind the agent; the roster idea says the
environment should also *introduce itself* to the agent.

## What shipped

`docs/ideas/harness-capability-roster-2026-08-04.md` — captured with the
owner's verbatim framing, the static/empirical division that makes it
tractable, sizing (template block, no engine change), and the evidence file.

## Verify

```bash
python3 -m pytest -q
python3 scripts/check_program_law.py
```
