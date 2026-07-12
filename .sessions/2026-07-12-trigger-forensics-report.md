# 2026-07-12 — trigger forensics report preservation

> **Status:** `complete`

Run type: coordinator-directed · docs

- **📊 Model:** Fable-class · high · coordinator-directed

## Scope (what is about to happen)

Preserve the overnight trigger-forensics report as
`docs/reports/2026-07-12-trigger-forensics.md` at coordinator direction —
the read-only forensics pass (why the scheduled cron routines failed
overnight, and what else went wrong) currently exists only in a chat
report; this PR gives it a durable home. Docs + this card + a claim file
only; no code, no control-plane edits beyond the one-file claim.

Claim: `control/claims/claude-trigger-forensics-report-2026-07-12.md`
(created in this first commit, deleted at the flip).

## Close-out

**What was done (PR #262):**

- `docs/reports/2026-07-12-trigger-forensics.md` — the overnight
  trigger-forensics report preserved verbatim from the chat report:
  (a) timeline of every scheduling mechanism the seat armed, (b) ranked
  root-cause hypotheses (H1 fresh-session cron delivery broken
  platform-side; H2 env-reference defect; H3 the hard-deletion vanish;
  H4 retracted), (c) never-worked-vs-regression verdict, (d) other
  overnight anomalies, (e) recommendations (none executed — read-only
  pass), (f) honest unknowns. Owner-requested provenance line at top.
- Badged `audit` (dated snapshot) + indexed from
  `docs/operations/README.md` (the reachability root) per the three
  sibling reports' convention — the strict gate's [badge]/[reachable]
  findings required it; the index line is the one deviation from the
  "report + card + claim only" brief, flagged on the PR.
- Claim file deleted at this flip.
- **Verification:** `python3 dist/bootstrap.py check --strict` — sole
  remaining red is this card's designed born-red HOLD, flipped here.
  No code touched.

**💡 Session idea:** forensics/incident reports like this one cite
live registry ids (trigger ids, session ids, env ids) that later
sessions cannot re-verify once the registry rotates — a tiny convention
line in the reports badge ("registry facts frozen as-of <timestamp>;
do not re-probe to 'update' this file") would stop a well-meaning later
session from mutating a dated audit to match a drifted registry.
Dedup-checked `docs/ideas/`: nothing covers dated-audit immutability.

**⟲ Previous-session review:** the lab-loop stopgap card (#258) set the
bar this session leaned on — its ROUTINE STATE and deviation-flag
pattern made the forensics report's context (missed 06:08Z fire,
stopgap doctrine) legible without re-derivation. What it could have
done better: it recorded the trigger miss but left the forensics
evidence in chat only — exactly the gap this session closes; a rule of
thumb worth adopting is "an incident probed in-session earns a
docs/reports/ home in the same PR, not a chat-only writeup."

**Docs audit:** report badged + indexed (reachable); claim deleted;
nothing session-only left unhomed — the report itself was the unhomed
artifact and now has its durable home.
