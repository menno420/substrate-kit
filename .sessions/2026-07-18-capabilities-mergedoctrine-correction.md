# 2026-07-18 · correct superseded landing-rule wording in CAPABILITIES append-log

> **Status:** `complete`

About to happen (opening declaration): `docs/CAPABILITIES.md`'s append-log
is newest-first, and its top entry (2026-07-17) still phrases a now-false
standing rule — "a session lands a PR ONLY by opening it READY and letting
the server-side merge-on-green workflow complete it." The binding docs and
the templates were already corrected fleet-wide (fleet #308/#309), but this
append-log residual means a reader hits the false standing rule first. Add
ONE dated 2026-07-18 correction entry at the top that supersedes that
wording; leave the historical :105 (2026-07-17) and :106 (2026-07-16)
entries untouched as dated record.

- **📊 Model:** opus-4.8 · docs-only

Run type: owner-directed fleet doctrine reconcile (#308/#309), coordinator-
assigned worker lane.

## What shipped (PR #453)

- `docs/CAPABILITIES.md` — new `2026-07-18 · capability` entry at the top of
  the append log. It marks the 2026-07-17 "session lands a PR ONLY by opening
  READY + server-side merge-on-green" line SUPERSEDED and states the current
  doctrine: agents land their own and sibling green PRs directly (github MCP /
  REST merge), flip draft→ready, and arm auto-merge as normal agent work; the
  server-side merge-on-green workflow is one landing path, not the only one; a
  one-off platform refusal is transient (attempt once, record, escalate to the
  hub), never a standing rule.
- The historical :105 (2026-07-17) and :106 (2026-07-16) entries are left
  exactly as-is — dated record, only the correction is added on top.
- No "agents cannot / walled / blocked" phrasing introduced; the entry is
  tagged `capability` so the append-log format guard stays green.

## Verification

- `kit-quality` gate: the append-log format cross-reference advisory
  (second field must be `capability|wall`) is cleared by tagging the entry
  `capability`; this session card satisfies the `--require-session-log`
  merge gate.
- The correction agrees with the already-shipped Walls-section
  "Merging own PRs is NOT a wall" (2026-07-18) and the SUPERSEDED 2026-07-10
  self-merge entries below it — the file is now internally consistent.

## 💡 Session idea

The append-log carried a self-contradiction for a full day: the Walls
section said "Merging own PRs is NOT a wall (corrected 2026-07-18)" while
the newest append-log entry (2026-07-17) still asserted the opposite
standing rule at the very top a reader sees. A cheap kit-side lint could
flag when a `## Walls` correction and the newest append-log entry disagree
on the same capability (merge/arm/flip), so a newest-first log can't leave a
stale top entry contradicting an already-applied correction.

## ⟲ Previous-session review

The 2026-07-18 de-wall sweep (kill-false-merge-walls, PR #444 and siblings)
correctly fixed the binding templates and the Walls section, but stopped at
the append-log's newest entry — a newest-first log means the last-written
entry is the first read, so a correction elsewhere in the file doesn't
neutralize a false top entry. Systemic improvement: when a session corrects
a standing rule, it should also add the dated superseding entry at the TOP
of any newest-first log that still states the old rule — not only fix the
prose section — so the reader's first hit is the current truth.
