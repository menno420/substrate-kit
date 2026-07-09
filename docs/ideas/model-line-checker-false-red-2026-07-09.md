---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# ON-arm "missing: Model line" persistent red — needle vs card format (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (B1 record session, run 2026-07-09-run01 — the judge
> flagged it as PL-006 material: "a red that contradicts visible evidence
> is exactly the 'bug in the check' class", report §5.5 item 3).

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
