---
state: promoted
origin: lab
shipped_pr: 95
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-10
outcome: shipped
---

# ON-arm "missing: Model line" persistent red — needle vs card format (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run 2026-07-09-run01 — the judge
> flagged it as PL-006 material: "a red that contradicts visible evidence
> is exactly the 'bug in the check' class", report §5.5 item 3) →
> investigated (PR #40) → **shipped** (kit PR #95, 2026-07-10: both
> remaining halves — planted `label (needle)` pairs in
> `_adopt_sessions_readme()` + misses report as ``label (expected
> `needle`)``).

## The finding

Every ON-arm `check --strict` reading across the whole run reported the
current session card `missing: Model line` — yet both cards visibly carried
a Model line. The mismatch is the **form**: the arm sessions wrote
`> **Model:** claude-fable-5` while the checker's configured needle is the
`📊 Model:` marker (`session_markers` default; the PL-004 harvest parses
`- **📊 Model:** <model> · <effort> · <task-class>`). Evidence:

- `bench/results/cold-start/2026-07-09-run01/s-row-facts.md` § "ON arm
  check --strict readings" (all three exit-1 readings verbatim) and the two
  guard-fires.jsonl entries quoted there.
- The T2 card's text is quoted in the ON-T4 transcript
  (`.../on/T4/transcript.jsonl` line 4); the T4 card in its Write call.
- Judge report §5.5 item 3 (checker-false-red suspicion, PL-006).

## Investigation disposition (2026-07-09, run-2 harness-prep session, PR #40)

**Resolved to the arm-authoring-gap side — with the gap traced one level
deeper, to the planted doc itself.** Verified against the committed run-1
transcripts:

- The ON-arm transcripts contain **zero** 📊 characters anywhere; both
  cards wrote `> **Model:** claude-fable-5` (`on/T4/transcript.jsonl` —
  grep the `Model:**` form).
- The arm DID read its planted `.sessions/README.md`
  (`on/T2/transcript.jsonl` line 40-41) — and that doc says only
  "a log must carry these markers: Status badge, Session idea,
  Previous-session review, **Model line**". Labels, no byte-forms: the
  composer `_adopt_sessions_readme()` (`src/engine/adopt.py`) joins
  `m["label"]` and never renders `m["needle"]`, so an arm session has no
  way to learn the `📊 Model:` form from inside the arm. The agent wrote a
  reasonable Model line; the needle scan (correctly, per its config)
  called it missing.
- **Separate from the harvest-shadowing bug** fixed in PR #40
  (`parse_model_line` last-needle selection): that bug required the needle
  to be PRESENT and a later prose mention to shadow it; here the needle
  was never written at all. Two different defects on the same marker.

**Remaining fix (stays open):** (c) plant the byte-form — render
`label (needle)` pairs in `_adopt_sessions_readme()` (guard recipe:
that function + a `test_adopt.py` assertion that the planted README
contains each configured needle) — plus (a) the checker message naming the
expected form on a miss ("missing `📊 Model:` marker") in the
`missing_markers` reporting path. Both engine-side → dist regen.

## The question to decide (investigate, then fix one side)

Is this an **arm-authoring gap** (the adopted repo's planted
`.sessions/README.md` documents the `📊 Model:` form — did the arm sessions
have that doc and ignore it, or was the planted convention text unrendered/
absent in the arm?) or a **checker false-red class** (the needle demands
one exact byte-form and treats an unambiguous `> **Model:**` line as
missing — "missing" is then the wrong word for "present in a different
form")? Check the ON arm's planted `.sessions/README.md` in the run
protocol and the needle in `session_markers` / the engine's session-log
checker. Likely outcome is one of: (a) checker message improved to name
the expected form ("missing `📊 Model:` marker (found a bare `Model:`
line)"), (b) needle relaxed to accept both, or (c) T-task protocol ensures
the convention doc is rendered in the arm — plus a PL-006 note either way.

## Done-when

Run-2's ON arm either reads `check --strict` clean after its sessions
write cards, or reds with a message that names the exact expected form —
no red that contradicts what an agent can see on the card.
