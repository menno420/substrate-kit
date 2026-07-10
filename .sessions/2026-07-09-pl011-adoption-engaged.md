# Session 2026-07-09 — PL-011: adoption is not done until ENGAGED (owner-review PR)

> **Status:** `complete` *(PR #26 — `do-not-automerge` at creation,
> deliberately LEFT OPEN for owner review: the merge is the ratification.)*

**Scope:** the PL-register half of band KL-7 (the adopt-engage gate, PR #25,
merged): a new program-law block **[PL-011]** making "an adoption is not done
until it is ENGAGED" binding program-wide — the doctrine whose kit-side
mechanism (D-0006, `check_engagement.py`) PR #25 ships. Per §8.3 a
program-law change rides its **own `do-not-automerge` PR, never bundled into
a band PR**: labeled at creation, driven CI-green, **left OPEN for the
owner.**

## What shipped

- **`docs/program/rulings.md` [PL-011]** — decided block, appended (next
  free id after PL-010): a kit adoption reaches *done* only at the ENGAGED
  state (rendered docs · CI running `check --strict` · session loop
  running); a planted-but-never-engaged repo is a **stranded adoption — an
  incident, not an onboarding**. Extends PL-007 (enforce, don't exhort) to
  the adoption lifecycle stage; amends nothing. Provenance chain in the
  block: fleet review §4 → owner P0 directive → kit D-0006 / PR #25 →
  this PR's owner-reviewed merge as ratification.

## Run report

- **📊 Model:** fable-5 · high · docs-only

### ⚑ Self-initiated / decide-and-flag (PL-001)

1. **Label-race guard verified live before writing the law**: the enabler
   run for this PR shows its "Enable native auto-merge" step **skipped**
   (fresh-label re-read saw `do-not-automerge`) — the #22 incident class is
   confirmed closed for this PR; the labeled-event disarm workflow covers
   any later arming.
2. **Stamp-discipline trip, caught by CI on the merge result and fixed**:
   PL-011's provenance originally cited the literal `D-0006` id, and #25's
   merge (mid-session) made `docs/current-state.md` that id's stamped home —
   the `stamp` checker correctly held kit-quality red ("cited from 2
   docs"). Fix: the provenance now names the ledger entry by band + PR +
   path instead of the raw token (one-home rule kept intact). `origin/main`
   was merged into the branch so every check ran on the true merge result
   before the re-push.

### 💡 Session idea (dedup-checked against docs/ideas/ + roadmap)

**Law-PR template**: `check_program_law --label-gate` enforces the label,
but the §8.3 own-PR + decision-brief-as-body + merge-is-ratification shape
is still re-derived from precedent (#22, this PR) each time. A tiny
`docs/program/law-pr-template.md` (title grammar, body skeleton, the
label + leave-open checklist) would make the next law change mechanical.
Noted here (small); not filed as a backlog file to keep this PR
docs/program-only.

### ⟲ Previous-session review — the KL-7 band session (PR #25, same run)

Its born-red→green discipline worked exactly as designed (the card held CI
red through the mid-session #17 merge conflict), and the conflict
resolution honestly renumbered its D-entry (D-0005→D-0006) instead of
fighting for the id. One improvement it surfaces: it verified "consumer #0
is engaged-green" locally but did not leave a standing assertion that the
KIT repo itself stays engaged — the ci.yml session-gate step covers it
implicitly (check --strict on the kit tree), which is real enforcement,
but a one-line comment there naming the engagement gate would make the
dogfood explicit for the next reader.

## KPIs / verification (this worktree)

- `python3 scripts/check_program_law.py` → **OK with PL-011** (grammar,
  gap-free monotonic IDs, provenance-required, pointer rules).
- `python3 -m pytest tests/test_check_program_law.py -q` → 26 passed
  (the census test allows gap-free appended amendments — the PL-010
  precedent shape).
- Label gate: PR #26 carries `do-not-automerge` from creation → the
  `--label-gate` required-check step reads the fresh label and passes;
  auto-merge verified **not armed** (enabler arm step skipped).
- Diff surface: `docs/program/rulings.md` + this card only.
