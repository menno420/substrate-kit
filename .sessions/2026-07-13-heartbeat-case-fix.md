# 2026-07-13 — heartbeat `updated:` prefix case-insensitivity

> **Status:** `complete`

⚑ Self-initiated: friction → guard from PR #326 — a live heartbeat written
as `Updated:` failed `[status-no-heartbeat]` because `UPDATED_LINE_RE`
requires a lowercase prefix; this session makes the enforcer accept the
casing variant (checker fix over exhortation, PL-007) with tests + dist
regen.

About to happen: make `engine.grammar.UPDATED_LINE_RE` match the `updated:`
prefix case-insensitively, pin both casings in the test suite, regenerate
`dist/bootstrap.py` via `python3 src/build_bootstrap.py`, verify with the
full pytest suite + `python3 dist/bootstrap.py check --strict`.

## What happened

- Friction verified at HEAD 949875c: `UPDATED_LINE_RE =
  re.compile(r"^updated:\s*(\S+)", re.MULTILINE)` at
  `src/engine/grammar.py:97` (dist copy at `dist/bootstrap.py:737`); the
  #326 merge commit's second commit message names the exact red
  ("UPDATED_LINE_RE requires ^updated: (case-sensitive); 'Updated:' failed
  [status-no-heartbeat]").
- Path A taken (decide-and-flag, flagged on PR #328): prefix match is now
  case-insensitive (`re.IGNORECASE`). Sole consumer is
  `check_status_current.parse_heartbeat`; every template writes canonical
  lowercase; no documented lowercase dependency (grammar's D-7 note is
  about config knobs, not casing). Same leniency instinct as
  `KIT_LINE_RE`'s bullet/bold-label tolerance — accepting an alternate only
  withholds a red, never adds one. Canonical writer form stays lowercase,
  pinned in `test_grammar.py`.
- Tests: both casings pinned — `Updated:`/`UPPERCASE` parse
  (`test_parse_heartbeat_accepts_case_variant_prefix`), gate-level twin
  (`test_fresh_capitalized_heartbeat_is_clean_too`), writer-canonical +
  enforcer-leniency pin in `test_grammar.py`. Dist regenerated via
  `python3 src/build_bootstrap.py`, never hand-edited.
- Verification: `python3 -m pytest tests/ -q` → **1247 passed in 20.84s**;
  `python3 dist/bootstrap.py check --strict` red ONLY on this card's
  designed born-red hold; `ruff check src/engine/` all passed;
  idea-index + program-law checkers OK; second dist rebuild byte-stable.
- PR #328 opened born-red right after the first commit (8900b2f); claim
  `control/claims/heartbeat-case-fix.md` added in the same commit and
  deleted in the flip commit. Auto-merge deliberately NOT armed by this
  session — landing is the enabler's / a reviewing session's.

## Enders

- **📊 Model:** fable-5 · medium · friction-guard

💡 **Session idea:** grammar enforcers should emit a NEAR-MISS diagnosis
instead of their generic finding when a line almost matches — e.g.
`[status-no-heartbeat]` on a file containing an `updated:` line whose
*timestamp* failed to parse should say "found `updated:` but
`<token>` is not ISO-8601", not "still the adopt seed?". The #326 class
(prefix casing) is now forgiven, but the bad-timestamp / `updated =` /
missing-colon near-miss classes still produce a finding that hides what
the writer actually wrote. Dedup'd vs `docs/ideas/`: no existing
grammar/near-miss/diagnosis entry (closest are model-line payload lint and
heartbeat-verb, both different surfaces).

⟲ **Previous-session review (2026-07-13 adopters currency refresh, #325):**
clean single-purpose slice — regenerated the registry via the kit's own
tooling instead of hand-editing, and its card separated remaining DRIFT
rows into "reconcile at source, not here", which stopped a successor from
misfixing them kit-side. Its gap: it verified `check --strict` green but
didn't note that the check run appends to `.substrate/guard-fires.jsonl`,
leaving a stray tracked-file modification for the next session to puzzle
over — this session hit exactly that and had to `git checkout --` it;
worth one line in the card or a .gitignore-style decision for check-run
telemetry on non-close-out branches.
