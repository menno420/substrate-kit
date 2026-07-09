# Session 2026-07-09 — KL-0 finish: founding plan travels + kit dogfoods itself

> **Status:** `complete`

**Planned:** copy the kit-lab founding plan into `docs/planning/` (byte-identical, per its
"this plan travels" clause), then run the §3.3 dogfood seed — `python3.10 dist/bootstrap.py adopt`
on the kit's own tree (the sanctioned consumer-#0 path) — answer the derivable interview slots,
render the planted docs live, and fill `docs/current-state.md` with the true state (KL-0 done,
next action = KL-1 first act: CI delta vs plan §3.2).

## What shipped

- **Plan travel**: `docs/planning/kit-lab-founding-plan-2026-07-07.md`, byte-identical to the
  superbot original (sha256 `ac3e355b…` verified both sides); provenance in the commit message.
- **Dogfood seed (§3.3)**: one-time committed render via `python3.10 dist/bootstrap.py adopt
  --target .` — planted `CONSTITUTION.md`, `docs/` skeleton (12 docs + `docs/ideas/README.md`),
  `.session-journal.md`, `.sessions/README.md`, `.substrate/` (state + staged claude / skills /
  agents / hooks / CI material), `project.index.json`, `substrate.config.json`. All 13 interview
  slots filled through the kit's own `answer` / `confirm` / `render --live`; mode = `active`
  (the kit repo runs its full workflow from birth); `render` reports 0 unfilled placeholders.
- **Current-state seed**: `docs/current-state.md` records KL-0 DONE and the next action —
  KL-1 first act, the CI + settings delta vs plan §3.2, with the five observed gaps enumerated.
- 440 tests green in 2.08 s (`python3.10 -m pytest tests/ -q`); `check --strict` exit 0 at close.

## ⚑ Self-initiated (deviations from the letter, per decide-and-flag)

1. **Vendored root `bootstrap.py` removed post-adopt.** §3.3 rules self-operation is
   *exclusively via `dist/bootstrap.py`*; a root duplicate would silently drift from the
   CI-byte-pinned dist. The staged hook templates' `bootstrap.py` command rows are covered by
   the hooks README relocation fill-table.
2. **Six pointer stubs** planted at the travelled plan's companion-link filenames (badged
   `historical`, each an absolute URL to the superbot-resident canonical) so the byte-identical
   plan passes the kit's own `check --strict` link check — the same absolute-URL device the plan
   itself prescribes for the bench spec's travel (§10 KL-5 row).
3. **PR split into #4 + #5.** Auto-merge on #4 fired the instant it was armed — this repo has no
   required status checks, so the born-red gate had no bite and the card-only PR merged alone.
   Work continued on a follow-up branch; merge armed only after completion. This live-proves
   §3.2 item 7 and is recorded as gap #1 in current-state ▶ Next action.

## Friction → guard candidates (for KL-1)

- Auto-merge + no required checks = instant merge of a born-red card (the whole point of the
  gate inverted). Guard: §3.2 item 7 — ruleset making `kit-quality` required, then the session
  gate (item 5). Until that lands, arm auto-merge only after the final push.
- `adopt` vendors `bootstrap.py` into a target that already ships `dist/bootstrap.py` (the kit
  repo itself). Guard candidate: skip vendoring when the target root contains the generating
  `dist/bootstrap.py` — small engine change, KL-1 rider.
- `session-close` reflection mining ingested this card's *section headers* ("## ⚑
  Self-initiated…", "## 💡 Session idea") as lesson texts R-0001/R-0002 — the miner keys on the
  marker emoji anywhere in a line, including headings. Guard candidate: skip `#`-prefixed lines.

## 💡 Session idea

Add a `--pointer-stub <url>` planting mode to `adopt`/`render` (or a tiny `stub` verb): a
one-command way to plant a `historical`-badged pointer doc for a link target that lives in
another repo. Travelled plans are a standing feature of this program (every consumer will
import plans whose companions stay home), and hand-writing stubs is exactly the kind of
mechanical ceremony the kit exists to absorb.

## ⟲ Previous-session review

The kickoff session (PRs #1–#3) did the extraction cleanly — full tree + tests in one PR,
CI with a real cold-adoption smoke, CODEOWNERS — and its CI choice (tests + adopt smoke) was
the right minimal core. What it missed: repo settings that make gates bite (no ruleset, no
required check) and the §3.2 items 2/3/5/6 jobs — which this session then felt directly when
PR #4 auto-merged born-red. Concrete workflow improvement: a kickoff/checklist step "arm the
ruleset the moment CI exists" — the gap between *a check running* and *a check required* is
invisible until something merges through it.

## KPIs / verification

- `python3.10 -m pytest tests/ -q` → 440 passed.
- `python3.10 dist/bootstrap.py check --strict` → exit 0.
- `python3.10 dist/bootstrap.py ask` → "no pending questions — all slots filled."
