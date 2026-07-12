# 2026-07-12 — lab-loop: friction-inbox clear (stopgap run)

> **Status:** `in-progress`

Run type: routine · lab

- **📊 Model:** fable-5 · high · lab-loop

⚑ **Model-class deviation (D-11):** the lab loop's default is Sonnet-class;
this run executes on the seat's Fable-class model because the daily trigger
missed its 06:08Z fire again and the slice rides the coordinator's stopgap
doctrine in-session (PR #257's ROUTINE STATE record) — not a scheduled
fresh-session fire. D3's ≥3-fire count is NOT advanced by this run.

## Scope (what is about to happen)

Stopgap in-session execution of the daily kit-lab loop slice per
`docs/operations/lab-loop.md`. STEP 1 (friction triage) found the inbox
NON-empty: issues #36–#39, all filed 2026-07-09 from the fleet adoption
review, none ever dispositioned. STEP 2 pick — under the owner's 2026-07-11
feature FREEZE (v1.12.1 cut), the slice IS the friction-inbox clear: verify
each report against kit v1.12.1 source, disposition each issue
(comment + close per the runbook), route the still-real residuals into
`docs/ideas/` backlog files, and append the four triage rows to
`bench/results/friction/index.json` (the triage-time evidence family,
`bench/README.md` — append-only). Zero code, zero new checker/command/
template surface (freeze-compatible). Bench run-10 stays honestly gated:
⚑ 14/15 (pin PRs #220/#238) unratified, and this seat neither runs arms
inline nor spawns runners.

Claim handled in-PR (the #257 stopgap precedent): single-seat,
coordinator-directed slice; this born-red PR opened at session start is the
in-flight signal.

## Close-out

**What was done (PR #258):**

- **STEP 1 — friction triage (the slice itself):** all four open `friction`
  issues (#36–#39, filed 2026-07-09 by the fleet adoption review, never
  dispositioned) verified against kit v1.12.1 source, dispositioned
  (comment + close on each), residuals routed:
  - **#36** (kit, 3 reports): r1 comment-leniency **fixed-in-v1.7.0** (PR
    #86 — `_strip_comment` before the needle test, verified in
    `check_engagement.py`); r2 inbox append-only **fixed-in-v1.7.0** (PR
    #87 `check_inbox_append`, gate wiring completed v1.7.1); r3
    required-check blind spot **partial** (CAPABILITIES.md
    `mergeable_state` recipes + v1.9.0 `required_context` plant-time
    validation) — residual backlogged. Closed.
  - **#37** (superbot, native-consumer state): **still real** — re-verified
    pin `1.0.0` + zero `check --strict` workflows; PL-011 merged without
    the state. Backlogged at
    `docs/ideas/engagement-native-consumer-state-2026-07-12.md`. Closed.
  - **#38** (superbot-next, weak gate): **partially overtaken** (dist
    v1.12.1, required checks armed via named-gates.yml) — but `ci.yml`
    still runs the plain weak-form `check --strict` (re-verified at
    c03df80). Adopter half relayed via `control/status.md` ⚑ FOR MANAGER;
    kit half backlogged at
    `docs/ideas/engagement-wiring-strength-verification-2026-07-12.md`
    (shared with #36 r3). Closed.
  - **#39** (websites, regen-lag): **still real as a class** — no such
    checker exists (grep-verified). Backlogged at
    `docs/ideas/staged-artifact-regen-lag-checker-2026-07-12.md`. Closed.
- **Evidence base deepened:** first four rows appended to
  `bench/results/friction/index.json` (the triage-time family,
  `bench/README.md` — B3's friction-rate sweep never re-scrapes issue
  comments). Append-only law respected (old rows `[]` → prefix holds).
- **Drift fixed on sight:** `docs/current-state.md` ▶ Next action still
  penciled "cut v1.13.0 → 7-repo wave" — overtaken by the v1.12.1 freeze
  cut + completed distribution; rewritten to the true post-freeze state
  (then trimmed to keep the boot-read set under the 7000-word budget — the
  first rewrite pushed it to 7064, a self-caused red caught by `check`).
- **Heartbeat (surgical):** phase prepend (stopgap run 1 record), ROUTINE
  STATE stopgap-run line, ⚑ FOR MANAGER relay bullet (sbn weak-form gate),
  last-shipped prepend, `updated:` bump.
- **Honest gating notes:** bench run-10 (next-queue top) NOT run — judges
  best after ⚑14/15 (pins #220/#238) ratify, and this stopgap seat neither
  runs arms/judging inline nor spawns runners. No release duty (freeze; no
  unreleased increment). Freeze respected: zero code, zero new
  checker/command/template surface — docs/evidence/grooming only.
- **Verification:** `python3 dist/bootstrap.py check --strict` — sole
  remaining red is the designed born-red HOLD naming this card (budget
  finding fixed in-PR before the flip); `python3 -m pytest tests/ -q` →
  **1057 passed** (no code touched).

**💡 Session idea:** the friction-disposition loop should leave a
machine-readable breadcrumb ON the issue itself — a one-line
`disposition: fixed-in-vX.Y.Z | backlogged-at-<path> | not-a-kit-issue`
trailer in the closing comment, grammar-pinned like the ORDER block — so
`check`/a future B3 sweep can grade triage SLA and disposition mix without
parsing prose. Today the bench row carries the data but is written by the
same session that writes the comment; a pinned trailer grammar would let
an independent sweep cross-check rows against issues (the
no-self-grading instinct applied to triage records). Dedup-checked:
nothing in `docs/ideas/` covers triage-record grammar.

**⟲ Previous-session review:** the #257 stopgap-doctrine card did exactly
what a failsafe record should — its ROUTINE STATE doctrine line was
directly executable by this session (probe → confirm miss → run in-session
→ flag deviation), zero re-derivation needed. What it missed: it recorded
the stopgap *procedure* but not the *queue state* the stopgap run would
face — this session had to re-derive "what does the runbook demand and
what's gated" from current-state + status. Improvement: a stopgap/handoff
record should name the expected next slice and its gates in one line (the
runbook's STEP-2 answer, pre-computed), the same way the archive-ready
note does for session resumption. Small, but it is the difference between
a doctrine and a brief.

**Docs audit:** new ideas indexed in `docs/ideas/README.md` (checker
`check_idea_index` green); bench rows in the append-only index;
disposition comments live on the four closed issues; heartbeat + Next
action current; nothing session-only left unhomed.
