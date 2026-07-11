# 2026-07-11 — run-8 countermeasure: close the CONTENT gap

> **Status:** `complete`

- **📊 Model:** fable-5 · high · feature build

## Scope (what is about to happen)

Coordinator-dispatched worker slice (claim `control/claims/run8-content-gap.md`
on main @ 83c5c39 before build). Run-8 (PR #215, report
`bench/results/cold-start/2026-07-11-run08/report.md`) proved the delivery
chain works — ON arms opened `HANDOFF.md` in their FIRST tool call, first
card-continuity conversion — but the payload was empty: the auto-draft card
carried 8 unresolved `[[fill:]]` slots, ON ended `check --strict` exit=1, and
the judge ruled "orientation cost paid; intended benefit not realized" (ON M1
2223/2506 vs OFF 905/1628 on T2/T4). Three deliverables, each with tests:

1. **Substantive arrival surface** — pre-fill the auto-draft from harvestable
   facts (reflog commit subjects, prior card's resolved pointer, the existing
   changed-file evidence), reserve `[[fill:]]` for the genuinely unknowable,
   and let `HANDOFF.md` carry an auto-derived trail when the card's pointer
   is unresolved (`src/engine/loop/handoff.py`, `handoff_pointer.py`).
2. **Cut orientation cost** — trim the run-8-observed ceremony reads:
   dedupe the CLAUDE.md/AGENT_ORIENTATION read-first lists + verify blocks,
   route (not front-load) CAPABILITIES/orientation, condense CONSTITUTION
   boilerplate (`src/engine/templates/*.tmpl`). Bounded to observed waste.
3. **Unfilled-slots → strict-RED fix** — an unadopted auto-draft (engine-
   authored `drafted` card nobody touched) is ADVISORY in the bare
   `check --strict` mtime-fallback lane; gate mode (`--require-session-log`
   / `--session-log` / `--added-card`) keeps blocking
   (`src/engine/checks/check_session_log.py`, `src/engine/cli.py`).

CHANGELOG `[Unreleased]` entries (next-release payload; NO release cut this
slice). Dist regenerated (byte-pin). NOT touched: `bench/rubric*` (parallel
§3 pin lane, claim `rubric-t5-v2-align.md`), `control/inbox.md`, sibling
cards, index.json.

## Close-out

Shipped the declared scope exactly — build commit 6fcaf80, flip-complete is
this commit. Tests **1012 → 1029** (+17: 8 handoff-harvest, 4 pointer-trail,
5 gate-lane); ruff clean; dist byte-pin clean (**689586 B**); idea-index /
program-law / bench-integrity OK; `check --strict --status-only` exit 0 on
the overwritten heartbeat. End-to-end driven in a scratch adopt: the
Stop-hook draft now carries `commits this session (1): "add report command
to CLI"`; `HANDOFF.md` carries the evidence trail at **85 words ≤ the 113
pin**; the next session's bare `check --strict` is exit 0 with the
`session-log-draft` advisory while `--require-session-log` stays exit 1.

Design decisions (decided-and-flagged, evidence on each):
- **D1 trail rides the shared composer** (push + file can't drift) and only
  fires when the card's pointer is UNRESOLVED — a resolved human pointer
  wins (leanness). Evidence: run-8 report §2 T4 ("ON's real context came
  from reading `cli.py`"; the card ON-T4 opened is quoted in full in the
  transcript at L4 — 8 slots, zero content).
- **D2 kept bounded** — only the four surfaces run-8 ON demonstrably read
  without payoff (T2 transcript L3/L5/L19/L21; T4 L18) were trimmed/re-
  routed; no doc-system redesign, contracts test-pinned.
- **D3 detection is the badge VALUE, not a substring** — the regression test
  caught the "*(auto-drafted …)*" prose false-positive on a flipped badge;
  `_STATUS_VALUE_RE` parses the backticked value. Advisory scoped to the
  mtime-fallback lane only; born-red/gate lanes byte-unchanged.

Mid-slice: two coordinator red-pings on the born-red head 23864c2 —
job-log-verified per PL-006 as the designed hold + legacy-alias mirrors
(job 86560943881, verbatim "HOLD (by design)… nothing to investigate");
the W-9 class, not a defect. One local trap: an f-string `\N{…}` escape in
an expression part is a SyntaxError on the 3.10 floor — caught by the local
suite before push.

## 💡 Session idea

Teach the auto-draft to pre-fill `Decisions made:` from a mechanical
source: `grep` the session's own commit bodies for "decided"/"decide-and-
flag" lines (the reflog harvest already parses `.git/logs/HEAD`; commit
BODIES need object parsing — loose-object zlib is stdlib). Run-8 showed
every harvestable slot the engine fills is arrival content the cold session
doesn't re-derive; decisions are the highest-value slot still blank, and
sessions that follow the repo convention already write them into commit
messages.

## ⟲ Previous-session review

The run-8 session (#215/#218) executed a hard spec cleanly — the seam smoke
+ A/B control turned an environment failure into a reproducible finding,
and its report's §2/§5 evidence quotes made THIS slice's design derivable
without re-reading six transcripts blind (that's what a good record buys).
One improvement it surfaced: its close-out (#218) updated phase/health/
last-shipped but left the `notes:` line describing the run-7 close — the
notes chain skipped a link (this slice's overwrite carries it forward
correctly). Workflow improvement: the status-overwrite recipe should name
`notes:` explicitly in its checklist so the chain can't skip.

