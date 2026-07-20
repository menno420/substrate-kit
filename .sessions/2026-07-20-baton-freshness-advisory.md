# Session — baton deliverable-freshness advisory (inverse of S4)

> **Status:** `complete`

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

- **Shipped:** `src/engine/checks/check_baton_freshness.py` (new), wired in
  `src/engine/cli.py` (import + `posture="advisory"` call + emit block),
  `MODULE_ORDER` in `src/build_bootstrap.py` after `check_baton_resolves` (its
  grammar source), `REMEDIATIONS["baton-stale-deliverable"]` +
  docstring-header kind list in `src/engine/checks/check_remediate.py`,
  `dist/bootstrap.py` rebuilt + byte-pinned (**1320533 bytes**, build
  idempotent), `tests/test_check_baton_freshness.py` (**+27 hermetic tests**).
  Colliding module constants renamed `_PRUNE_DIRS`/`_MAX_BYTES` →
  `_BATON_FRESH_*` (the dist flattens all engine modules into one namespace;
  `check_recipe_discovery` already owned those names — caught by
  `test_check_namespace`).
- **Verify:** full suite **2052 passed, 1 skipped** (2025 baseline + 27);
  `python3 dist/bootstrap.py check --strict` green (only red = the by-design
  born-red HOLD on this card while in-progress); the advisory is **SILENT on the
  real tree** (no `baton-stale-deliverable` finding — both live-baton tokens sit
  on SHIPPED/#PR lines → shipped-suppressed); `check --strict` stays **7
  sub-checks** (off STRICT_SUBCHECKS); `ruff check src/` clean.
- **Behavior confirmed (regression pair locked in tests):** fires ONE nudge on
  the historical stale S16 baton shape (`--api-latency` named to-build, no
  marker, resolves in tree); silent on the current healthy baton (every
  deliverable acknowledged with a PR#/SHIPPED marker); silent on an unbuilt
  deliverable, a docstring-only mention, a `tests/`-fixture registration, and
  `bootstrap.py`.
- **PR #545** — https://github.com/menno420/substrate-kit/pull/545
- **Baton → band-consumed (buildable band DRY):** with this shipped and the
  wave-2 ladder S2–S17 exhausted, no agent-buildable slice remains; remaining
  work is owner-gated (adopter wave / 5 ⚑) or cross-repo. Per coordinator
  refinement 2026-07-20 the baton is advanced to the honest band-consumed state,
  **not** a fabricated wave-3 rank.

## 💡 Session idea

**A phantom-shipped-claim advisory over the heartbeat's own ledger** — reuse the
deliverable-resolution primitive this checker introduced (`def <name>(` /
`add_argument("--flag"` / `<name>.py`) in the OTHER direction: scan the
`control/status*.md` phase line + `## Recently shipped` narrative for `#NNN`
entries that CLAIM a `check_*` / `--flag` deliverable shipped, and warn when that
deliverable does NOT resolve in the tree — a "shipped #NNN" claim with no
matching code is a phantom-shipped ledger entry (the mirror of this session's
stale-baton: baton-freshness = named-to-build-but-exists; phantom-shipped =
named-shipped-but-absent). Together the two advisories close the heartbeat's
deliverable-truth loop from both sides. Deduped against `docs/ideas/` (the one
near hit, `idea-index-merged-reality-2026-07-14.md`, verifies `docs/ideas/`
frontmatter `shipped_pr` via git-truth — a different surface: frontmatter vs. the
control-plane heartbeat ledger, and PR-existence vs. deliverable-symbol
resolution). Genuinely believe it: I just built the resolver and the S16 incident
proves the heartbeat's shipped-claims are exactly what drift.

## ⟲ Previous-session review

Previous session was **S17 — `check_recipe_discovery` (#543)**. Done well: it
made the RIGHT collision-guard call — greppng the tree first, finding S16's
`--api-latency` already shipped (#479), and honest-nulling to S17 rather than
blindly building the stale baton's target; and its `⟲` note didn't stop at "I
dodged a bug" but converted the friction into a concrete, buildable proposal
(this very advisory), which is the self-auditing loop working as designed. What
it (and the whole S4→S17 chain) could have done better: **S4 built
`check_baton_resolves` to grade baton PATHS but stopped there** — the deliverable
axis was left ungraded for thirteen ranks while the exact gap it left open (a
baton naming already-built work) sat live and eventually cost a real dispatch.
The lesson: when a checker grades one axis of an artifact (a baton's *paths*), the
*inverse/complementary* axis (its *deliverables*) is a first-class candidate to
name in the same session's `⟲`/💡, not something to discover only after it bites.
**System improvement it surfaces:** the resolution primitive I wrote (does a
named `check_*`/`--flag` exist in the tree?) is reusable telemetry-of-truth — the
phantom-shipped 💡 above is one consumer, and a shared "deliverable resolver"
helper would let the next such advisory ship in half the code (the same
consolidation instinct as S17's own TreeCorpus 💡).

## ⚑ Self-initiated

- **Yes — self-initiated (friction→guard, Q-0194).** This advisory was proposed
  by the S17 card's `⟲` note and built under the fm ORDER 048 standing grant +
  coordinator dispatch; no owner sign-off needed — it is a contained, reversible,
  advisory-only addition (off STRICT_SUBCHECKS, never exit-affecting) that lands
  on green CI. The friction it converts to a guard: a stale `## Next-2 baton`
  pointing at already-shipped work (the S16 `--api-latency` incident) now reds at
  check time instead of burning a successor's session.
- **Decide-and-flag:** built as a NEW sibling checker (not an S4 extension) and
  chose PROSE extraction over code-span-only — both flagged with rationale on the
  card + PR; either is reversible. No owner decision gated this.
