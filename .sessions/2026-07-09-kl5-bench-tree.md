# Session 2026-07-09 — KL-5 (2/2): the bench/ tree

> **Status:** `complete` *(PR #17 — CI-green with this flip, and the PR then
> **stays OPEN on purpose**: it carries `do-not-automerge` and awaits the
> owner's blessing of the first rubric version per §5.0. Only the merge is
> pending, and it is the owner's.)*

**What happened (founding plan §10 KL-5 row, second half; §5.0/§5.1):**

- **`bench/rubric/cold-start-rubric.md`** — THE B1 judge rubric (the
  twice-lost artifact, now pinned): fixed judge instructions
  (score-behavior-not-artifact-presence, partial-blinding honesty), the
  M1/M2/M3 measure table, per-task judge items T1–T5 (T5's items: did the
  guard fire, did the session obey, is the repair genuine), the F-5 pass
  bar restated as the FLIP TARGET (advisory-to-pass, KF-5), and the judge's
  output format. **`bench/rubric/allocation-rubric.md`** — B2: objective
  gates decide first, judge scores quality between passing outputs per the
  8 PL-004 classes, cost tiebreaks.
- **`bench/tasks/T1–T5.md`** — fixed prompt texts (fenced; the runner
  substitutes nothing), grounded in companion D §3.1 + the Phase-2.5 runs;
  absolute spec URLs in `bench/README.md` so the spec survives travel.
  **T5 break-a-rule** (D-17) is new: the prompt itself instructs the
  session to skip write-back on a tiny fix; the ON arm runs
  `--wire-enforcement` — the instruction-vs-guard tension IS the
  measurement.
- **`bench/seeds/make_seed.py`** — parameterized generator: fresh surface
  names per `--seed` (anti-memorization), same shape every run (1 package ×
  store/ops/cli + 6 passing tests + README), and the SAME seeded untested
  bug class (case-sensitive filter whose docstring/README promise
  insensitivity — the Phase-2.5 bug class, kept for comparability).
  Deterministic: same seed ⇒ byte-identical.
- **`bench/score_m1.py`** — scripted M1 over a defined **event-JSONL**
  transcript format (tool_use / tool_result / text); mutating = file tools
  or Bash matching a deliberately-broad mutation regex (over-matching only
  stops the count early — conservative).
- **`bench/run_ab.py`** — `prepare` (seed once → identical arms → git seed
  commit → ON-arm adopt, `--wire-enforcement` auto when T5 in set → the
  §5.1 **smoke step**, refusing to proceed on a broken arm) · `collect`
  (files transcript/diff + scores M1 immediately — raw artifacts are
  committed, §5.0) · `record` (schema-checked, run_id-deduped, append-only
  row). The harness never talks to a model; sessions and judge are
  separate invocations per the separation law.
- **`bench/results/{cold-start,allocation,guards,ideas,friction}/index.json`**
  — append-only, seeded `[]`. The `friction` family lands the KL-4 session
  idea (triage-time rows so B3 never re-scrapes issue comments).
- **`scripts/check_bench_integrity.py` + CI step** — layer 1 of the D-24
  two-layer pin, enforcing from birth: pin-path (`rubric|tasks|seeds`)
  changes must ride a `do-not-automerge` PR (label read from the event
  payload; skipped outside PR context), and `bench/results/` is
  append-aware immutable (deletes/edits red; index appends + new run dirs
  allowed). Q-0105 provenance header; layer 2 is the 👤 P10 ruleset.
- **auto-merge-enabler race guard** (see flag 1): the enabler re-reads
  labels FRESH from the API after a grace beat before arming.
- **Verified:** 609/609 pytest (587 → 609; 21 new: seeds determinism/shape/
  bug, M1 scoring incl. Bash patterns, recorder schema/dedupe/append, 11
  integrity-checker cases on scratch git repos) · ruff engine bans green
  (bench/ excluded from bare-ruff parity like scripts/) · dist byte-equal
  (no engine change) · `check_program_law` OK · **the integrity checker
  self-verified against THIS PR's real diff** (8 pin findings without the
  label → exit 1; labeled → exit 0) · **live harness drive**: `prepare`
  built both arms + adopted + smoke green; `score_m1` CLI correct. **NO
  benchmark arm was run and NO score recorded** — B1's baseline firing is a
  separate later step after the rubric merges (never-grade-own-substrate).

## ⚑ Flags

1. ⚑ **Live incident, fixed in-band (Q-0194 friction → guard):** the
   auto-merge-enabler ARMED auto-merge on this very PR at open — its
   job-level label condition reads the creation-time payload, and an
   MCP-created PR gets its label in a second call moments later. Disarmed
   by hand within a minute (the disable call succeeding is the proof it was
   armed); the enabler now sleeps a grace beat and re-reads labels fresh
   before arming. Without the fix, flipping this card would have
   self-merged the owner-blessing PR.
2. ⚑ Decide-and-flag: the M1 transcript contract is a defined event-JSONL
   (documented in `score_m1.py`) rather than any raw session-log format —
   the runner normalizes; the scorer stays format-stable across harness
   changes.
3. ⚑ Decide-and-flag: a fifth results family `friction` beyond the plan's
   four — routes the KL-4 idea to its named home; same append-only law.
4. ⚑ Decide-and-flag: this card flips `complete` so kit-quality is GREEN on
   the open PR (per the band instruction): the blessing gate is the
   `do-not-automerge` label + unarmed auto-merge, not a red check. The
   session-gate hold is thereby released deliberately; only the owner's
   merge is pending.
5. ⚑ Self-initiated: the enabler workflow edit (flag 1) was not in the band
   spec — shipped as the cheapest enforcing prevention for a gate hole that
   fired live on exactly the integrity-critical PR class it exists to
   protect.

## 💡 Session idea

**Scorer-drift replay:** stamp `score_m1.py`'s own version (a constant, or
the file's git blob hash) into every `m1.json` it writes, and add a
`run_ab.py verify` subcommand that re-scores the committed transcripts of
recorded runs and diffs against their stored M1 — so a future change to the
mutation regex or word counting is caught as *scorer drift* (re-score ≠
recorded score → the trend line's comparability broke) instead of silently
bending the B1 trend. Lands with: the first real B1 firing or the KL-6
sweep work. Dedup-checked against `docs/ideas/` (nothing covers scorer
versioning).

## ⟲ Previous-session review (kl5-auto-draft)

Strong: it live-tested the full draft→gate→resolve→harvest loop on a scratch
adopt before shipping, and its flag-3 discipline (its own card tripping the
fill counter → code-span exemption + regression test in the same PR) is
Q-0194 working exactly as written. Miss: it opened its PR with the standard
arm-immediately flow and never questioned whether the *enabler side* had the
same label-freshness assumption — the race this session then hit live was
one payload-read away from being predicted there. **Workflow improvement:**
when a PR class exists whose whole point is "never auto-merge" (this repo
now has one), every mechanism that can arm a merge needs a fresh-state
re-check at arm time, not a snapshot check at event time — now enforced in
the enabler; apply the same lens to any future merge-arming mechanism (P10's
path-scoped required review stays the durable layer 2).

## Docs audit

`check --strict --require-session-log` green at flip; CHANGELOG
`[Unreleased]` gained Added (bench tree) + Fixed (enabler race);
current-state in-flight (#17 + the race field note), stability (KL-5 both
halves), and Next action (owner blessing → B1 firing → KL-6) all updated;
`bench/README.md` carries the absolute companion-D/report URLs and the
run-B1 procedure; the PR body makes the blessing decision self-contained;
nothing left chat-only.

- **📊 Model:** fable-5 · high · kernel/architecture design

**Post-blessing addendum (2026-07-09):** first rubric version owner-blessed
("you can merge 17", then direct "merge 17" in-session); branch updated
against main (#24) with mechanical conflict resolution (CHANGELOG regrouped,
current-state reality), blessing provenance recorded as D-0005 in
`docs/decisions.md` by the merge-prep session.
