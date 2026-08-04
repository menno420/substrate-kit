# 2026-08-04 · Gate-collision guard in skill bodies + effort tiers xhigh/max

> **Status:** `complete`

- **📊 Model:** fable-5 · high · runtime bugfix

💡 Session idea: **a template slot can collide with a hardcoded step and the
render looks perfectly healthy.** Three planted skills said "run
`${verify_command}` and `bootstrap.py check --strict`" — correct for every
adopter except the one whose verify_command IS that check, where the two steps
silently became one and the repo's other gate (its false-wall guard) fell out
of the ritual entirely. A slot and a literal in the same list need a
collision clause, because the failure renders as harmless repetition, which
no reader flags and no checker sees.

## previous-session review

`2026-08-04-idea-capability-roster.md` (PR #570, merged) captured the day's
product idea. This card ships the day's two mechanical kit fixes, both
discovered by fleet-manager sessions being caught by (or catching) the kit's
own machinery.

## What shipped

- **`src/engine/skills/skills.py`** — quality-gate, session-close and
  upgrade-distribution bodies now carry a collision clause: if
  `${verify_command}` is already the strict check, run the repo's other
  boot-file gates instead of silently stopping at one.
- **`src/engine/grammar.py`** — `MODEL_EFFORT_VALUES` extended with `xhigh`
  and `max`: the harness has shipped a five-tier effort ladder since Opus 4.7
  (2026-04) and the card lint rejected true self-reports, forcing a session
  running at `max` to record `high` (fleet-manager card, 2026-08-04). The
  lint's job is honest telemetry; the tuple was the dishonest part.
- `dist/bootstrap.py` rebuilt.

## Verify

```bash
python3 -m pytest        # 2081 passed, 1 skipped
```
