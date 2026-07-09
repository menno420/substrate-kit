# The kit's house style — opinionated defaults, not config

> **Status:** `binding`
>
> Founding plan §3.4 / decision D-7: the conventions below are **declared
> house style, deliberately hardcoded** rather than configuration. Config
> sprawl is a worse failure mode than opinionation — a consumer that truly
> needs a different marker **forks the constant** (one obvious place each,
> listed per row) instead of the kit growing a knob per emoji. This file is
> the one place the opinions are written down.

## The marker set (emoji as machine-parseable grammar)

| Marker | Meaning | Where hardcoded |
|---|---|---|
| 💡 | Session idea — one genuine new idea per session, mined into reflections | `src/engine/loop/reflections.py` (`_REF_IDEA_MARK`), `session_markers` default in `src/engine/lib/config.py` |
| ⚑ | Self-initiated work / friction flag — the accountability line the owner filters on | `src/engine/loop/reflections.py` (`_REF_FLAG_MARK`) |
| ⟲ | Previous-session review — the self-auditing chain | session-log convention (`.sessions/README.md`); the checker needle is the phrase "previous-session review" |
| 📊 | Model/effort/task-class run-report line (the PL-004 telemetry feed; lands as a required needle at KL-3) | session-log convention; harvest wiring is band KL-3 |
| 👤 | Owner-action item (portal clicks, credentials, rulings only the owner can execute) | docs convention (plans, current-state) |

These emoji are **grammar, not decoration**: the reflection miner, the
session-log checker, and the run-report harvest parse them. A consumer that
renames one must fork the constant *and* keep its own docs consistent — the
kit will not carry per-marker config.

## Session discipline

- **Born-red session card:** every session's first commit creates
  `.sessions/<date>-<slug>.md` with `> **Status:** `in-progress`` — the
  session gate holds the merge until the badge flips to a ready token as the
  deliberate last step. The badge **value** is part of completeness (an
  `in-progress`/`wip`/`hold` badge is incomplete even with all markers
  present).
- **PR opens early and READY, never draft** — the card is what holds the
  merge, so the in-flight signal costs nothing and parallel sessions see the
  lane.
- **Session enders** (before the flip): 💡 one genuine idea · ⟲ previous-
  session review · docs audit. Forced filler is worse than none.

## Doc conventions

- **Status-badge taxonomy** (first 12 lines of every live doc):
  `binding` · `living-ledger` · `reference` · `plan` · `historical` · `audit`
  · `owner-guidance` · `ideas` · `archive` — defaults in
  `src/engine/lib/config.py` (`_default_badge_tokens`; this one IS config,
  extendable per repo, but the default taxonomy is the house vocabulary).
- **ADR path:** `docs/decisions/NNN-*.md` — ADR files are badge-exempt (they
  carry their own Accepted/Superseded lifecycle); the doc checker recognizes
  exactly this shape (`src/engine/checks/check_docs.py`).
- **Ledger grammar:** append-only `## [D-NNNN]` / `## [Q-NNNN]` /
  `## [PL-NNN]` blocks — status/date/verdict/provenance fields, superseded
  never deleted. Rule docs cite bare IDs; ledgers hold the narrative.
- **Provenance + reliability header** on every adopted tool (PL-008): why ·
  date · "unverified until proven" · "delete this if unreliable over multiple
  sessions."

## Rollout order (guided mode)

`GUIDED_ROLLOUT` in `src/engine/lib/modes.py` fixes the practice order:
`session_logs → idea_lifecycle → question_router → session_enders → gates`.
The *pacing* is config (`cadence.guided_practice_sessions`); the *order* is
house style — logs before ideas before the router before enders before gates,
because each practice is the scaffolding the next one writes into.

## Why not config?

Every row above was a candidate knob at extraction (founding plan §3.4). The
ruling (D-7): a knob multiplies test surface and documentation for a
preference no real consumer has voiced, and divergent marker dialects would
break the one thing the program actually needs — cross-repo parseability of
session records (the PL-004/PL-005 telemetry and the kit-lab's sweeps read
these markers program-wide). Opinionation is the feature.
