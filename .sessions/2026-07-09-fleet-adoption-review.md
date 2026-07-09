# Session 2026-07-09 — fleet adoption review (owner-directed) + control-lane status gate

> **Status:** `complete` *(PR #35 — auto-merge armed at open via MCP, per convention)*

**Scope (about to do):** the owner-directed fleet adoption review, consolidated
from five completed read-only assessments (kit / superbot / superbot-next /
websites / context self-sufficiency). One coherent PR: (1) the durable review
report at `docs/reports/2026-07-09-fleet-adoption-review.md` (per-repo
verdicts, findings tables, the kit's-own-promises proofs, the owner-directed
context-self-sufficiency lens, rollout coordination notes, fixed/filed/⚑
needs-owner close); (2) **ship the med fast-lane fix** — the CI control fast
lane (kit `ci.yml` + the planted `substrate-gate.yml` template) skips
`check_status_current` on exactly the PRs that write control files, so a
heartbeat-deleting control-only PR rides the lane GREEN while `check --strict`
would exit 1 — add a status-scoped check step to the lane itself (`check
--strict --status-only`), dist rebuilt, tests pinned; (3) file the non-shipped
gaps as `friction` issues per the kit's protocol. Hard rails honored: no
bench/ writes, no version bump / release cut, PR #26 untouched (PL-011 +
cite-never-copy tension routed to the owner, not resolved).

## What shipped (PR #35)

- **`docs/reports/2026-07-09-fleet-adoption-review.md`** — the durable
  review: verdicts kit **OK** / superbot **OK-pin-only** / superbot-next
  **DEGRADED** / websites **OK-recovered**; per-repo findings tables with
  dispositions; the kit's-own-promises proofs (engagement gate fires
  verbatim; v1.2.0 assets == tag == main, sha256 `258ab02a…`); the
  context-self-sufficiency lens (kit MEDIUM · superbot-next MEDIUM-LOW ·
  websites MEDIUM-HIGH; the `control-README.md.tmpl:5` finding — the kit
  plants a superbot pointer into every adopter; the cite-never-copy tension
  quoted exactly with 3 carve-out shapes, **⚑ routed to the owner**); rollout
  coordination (superbot-next #69 / websites #31 reviewed, not duplicated);
  Fixed / Filed / ⚑ Needs-owner close (5 owner items). Linked from
  `docs/current-state.md` (pointer block + Recently shipped + In flight).
- **The fast-lane fix (D-block appended to `docs/decisions.md`)**: new
  `check --status-only` scoped mode (`src/engine/cli.py` — allowlist +
  guard-fires identical to a full run; session-log seam untouched so the
  lane can't deadlock); a `Control-status gate` step ON the lane in kit
  `.github/workflows/ci.yml` **and** the planted `substrate-gate.yml`
  template (`src/engine/adopt.py`); `dist/bootstrap.py` regenerated
  (byte-pin); 5 new tests (`test_ci_control_lane.py`, `test_adopt.py`,
  `test_cli_gate.py` ×3). Reproduced before/after on a v1.2.0 fixture —
  verbatim outputs in the report §2.2.
- **CHANGELOG `[Unreleased]`**: Added (`--status-only`) + Fixed (the lane
  bypass). No version bump, no release — next release carries it to
  adopters.
- **Friction filed (label `friction`)**: kit
  [#36](https://github.com/menno420/substrate-kit/issues/36) (3 reports:
  enforcement-wired comment leniency · inbox append-only unenforced ·
  required-check verifiability), superbot
  [#37](https://github.com/menno420/substrate-kit/issues/37) (PL-011
  "native-substrate consumer" state), superbot-next
  [#38](https://github.com/menno420/substrate-kit/issues/38) (workflow half
  of the gate fix, post-#69), websites
  [#39](https://github.com/menno420/substrate-kit/issues/39)
  (regeneration-lag checker).
- **control/status.md overwritten** (per-session ritual): ORDER 003
  **acked, not executed** — its done-when requires a release cut, which
  this session's owner mandate excludes; left for the next kit-band
  session.

## Run report

- **📊 Model:** fable-5 · high · review/verify

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **⚑ `--status-only` as an engine CLI mode**, not an inline-python
   workflow step: one verifiable seam that both the kit's CI and every
   adopter's planted gate share, testable in the suite, and consistent
   (allowlist + guard-fires behave identically on both lanes). Veto path:
   revert the CLI flag, inline the 5-line checker call in the two
   workflows.
2. **⚑ Friction filed as 4 per-repo envelopes (6 reports)** matching the
   issue #15 precedent, rather than 6 single-item issues — keeps the lab
   loop's per-report triage shape.
3. **⚑ ORDER 003 acked-not-executed** (see above) — flagged here and in
   the status overwrite rather than silently skipped.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Surface-scoped check lanes as a registry, not flags** — `--status-only`
is the first *surface-scoped* check mode, and friction #36 report 2 (inbox
append-only checker) will want to ride the same control lane. Instead of
accreting one flag + one workflow edit per checker, let checkers declare a
`surface` ("control", "docs", "sessions") and give `check` a
`--surface control` selector: the lane workflow never changes again when a
new control-surface checker lands — it automatically runs everything
registered for that surface. One list + one filter in `cmd_check`; the
workflows stay frozen text (which is exactly what the textual CI pins
want). Not filed as its own idea file: it composes with #36's inbox checker
(same seam, same lane) — noted for the groom pass to fold in when that
checker is built.

### ⟲ Previous-session review — v1.2.0 release cut (PR #32)

Strong: a clean one-PR release with honest KF-5 handling (standing B1 PASS
cited, no fresh firing, reasons in the notes) and the deliberate
last-act status overwrite riding the new lane as its first live exercise.
What it missed — found by this session: the lane it shipped was
**checker-free on its own subject files** (a control-only PR skipped
`check_status_current`, the one checker that validates control files), so
the first live ride proved "green reports fast" but nobody asked "green
*after checking what*?". **Workflow improvement:** when shipping a skip
lane, enumerate which checkers validate the *skipped surface* and keep
those ON the lane — a one-line design-time checklist question ("what still
runs here?") would have caught this bypass the day it shipped.

## KPIs / verification (this worktree)

- `python3 -m pytest tests/ -q` → **688 passed** (683 + 5 new).
- `python3 -m ruff check src/engine/` → clean; dist regenerated, byte-pin
  verified by the suite.
- `python3 scripts/check_idea_index.py` / `check_program_law.py` /
  `check_bench_integrity.py` → OK.
- Stamp discipline: D-id double-citations (report vs ledger pointer)
  caught by `check` locally and de-duplicated before push.
- Before/after bypass reproduction: lane verdict `control_only=true` with
  `check --strict` exit 1 (before); new fast-lane step exit 1 on the same
  tree, exit 0 on a healthy heartbeat (after).
- Born-red gate: this card held `check --strict --require-session-log`
  red until the final flip.
