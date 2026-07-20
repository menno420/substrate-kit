# Session — baton deliverable-freshness advisory (inverse of S4)

> **Status:** `in-progress`

- **📊 Model:** Opus 4.8 · medium · feature build
- **Branch:** `claude/baton-freshness-advisory`
- **About to do:** Build the **baton-deliverable-freshness advisory** proposed in
  the S17 card's `⟲ Previous-session review` note — a warn-only
  `check_baton_freshness` that parses the `## Next-2 baton`'s named `check_*` /
  `--flag` deliverable and warns when that deliverable **already resolves in the
  tree**, so a "build X" baton pointing at already-shipped work reds at check time
  instead of burning a worker's session (the S16 `--api-latency` incident that
  cost a real dispatch). The INVERSE of S4's `check_baton_resolves` (which flags a
  baton *path* that does NOT resolve). Friction→guard (Q-0194).

## Design decision (decide-and-flag) — NEW checker, prose extraction + shipped-suppression

- **New checker, not an extension of S4.** The two are semantic inverses on
  different token types: S4 grades baton *paths* and fires when one does NOT
  resolve; this grades baton *deliverable symbols* and fires when one DOES
  resolve. Separate finding kind, remediation, and token grammar → a new sibling
  module is cleaner than overloading `check_baton_resolves`. It reuses S4's
  section-boundary grammar (`_RE_BATON_HEADING` / `_RE_H2` / `_CONTROL_RELDIR` /
  `_STATUS_GLOB`) as the single source of truth (mirrors how S8 reused R11's
  grammar), which fixes its MODULE_ORDER slot right after S4.
- **Prose extraction, NOT code-span-only (the load-bearing call).** Real batons
  name deliverables in running prose — `S16 (--api-latency harness ...)`,
  `check_recipe_discovery advisory` — **not** in backticks. Verified against the
  live baton: `--api-latency` / `check_recipe_discovery` are plain text there. So
  a code-span-only scan (S4's grammar) would have caught **nothing** — it would
  never have flagged the very S16 case this advisory exists for. The checker
  extracts `check_[a-z0-9_]+` / `--[a-z][a-z0-9-]*` tokens from the full baton
  section text.
- **Shipped-suppression keeps it silent (the conservatism the task demands).** A
  deliverable token on a baton line ALSO carrying a completion marker
  (`shipped`/`merged`/`landed`/`done`/`complete`/`already`/`exists`/`#<digits>`/✓)
  is a REPORTED-done rank, suppressed file-wide (the tree-analogue of S17's
  already-known guard). On the live heartbeat both tokens sit on `SHIPPED via PR
  #543` / `already-shipped via #479` lines → suppressed → **silent on the current
  tree**. On the historical stale S16 baton (`the next buildable-now step is S16
  (--api-latency harness — larger, needs live GH)` — no marker) → candidate →
  resolves → **would have fired**. Both verified.
- **Resolution is the real backstop.** `check_<name>` resolves only on a `def
  <name>(` definition (or a `<name>.py` file); `--<flag>` only on an
  `add_argument("--<flag>"` registration — both immune to a docstring MENTION of
  the token, so loose prose extraction can never false-fire on a token that is
  not a genuine, already-built deliverable. Fail-open (short-alias-first argparse
  = deliberate false-negative; a missed nudge is cheap, a false-positive erodes
  trust).

## Scope

- New `src/engine/checks/check_baton_freshness.py` (advisory, stdlib-only,
  input-gated, fail-open, off `STRICT_SUBCHECKS`).
- Wired on the `posture="advisory"` seam in `src/engine/cli.py` (import + call +
  emit block, exactly mirroring S4/S17).
- Added to `MODULE_ORDER` in `src/build_bootstrap.py` after `check_baton_resolves`
  (its grammar source); dist rebuilt + byte-pinned.
- `REMEDIATIONS["baton-stale-deliverable"]` added to `check_remediate.py` (S8
  lesson: a new emittable finding kind ships with its remediation block).
- Hermetic tests in `tests/test_check_baton_freshness.py` (no network).

## Result

- [[fill: shipped files + verify counts + PR # + CI]]

## 💡 Session idea

- [[fill]]

## ⟲ Previous-session review

- [[fill]]

## ⚑ Self-initiated

- [[fill]]
