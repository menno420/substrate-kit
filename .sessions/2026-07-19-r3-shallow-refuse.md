# Session · 2026-07-19 · r3-shallow-refuse

> **Status:** `complete`

Intent: task R3 under ORDER 048 — turn the shallow-clone prose trap in
`scripts/measure_grounded_skills.py` into an enforced refuse-to-publish: when
`--json` is requested and any measured repo is a shallow clone (whose M4
git-history metrics would be silently zeroed), refuse to write the JSON, print
a loud machine-greppable `REFUSE:` marker to stderr, and exit non-zero (2).

- **📊 Model:** Opus 4.8 · high · feature build
- ⚑ Self-initiated: none — R3 is baton-directed work (dispatched from
  `docs/planning/2026-07-19-night-run-idea-groom.md` R3 entry under ORDER 048),
  not self-initiated.

## What shipped (PR #492)

- **Shallow-clone refuse-to-publish** in `scripts/measure_grounded_skills.py`: the
  `--json` publish path in `main()` now checks the per-repo `shallow` flag already
  carried on the results; when `--json` is requested and any measured repo is a shallow
  clone (whose M4 git-history metrics would be silently zeroed), it refuses to write the
  JSON, prints a loud machine-greppable `REFUSE:` marker to stderr, and exits non-zero
  (2). The markdown/stdout path is unchanged — it already soft-nulls shallow rows.
- **Two tests** added to `tests/test_measure_grounded_skills.py`: a shallow-refuse case
  (asserts the `REFUSE:` marker + exit 2, no JSON written) and a positive
  full-clone-writes-JSON case (the guard does not fire when no repo is shallow).

## Verification

- `python3 -m pytest tests/test_measure_grounded_skills.py -q` → passing.
- `python3 -m pytest tests/ -q` → **1824 passed** (full suite green).
- `python3 dist/bootstrap.py check --strict` → green once this card flips `complete`
  (born-red hold released).
- PR #492 auto-merges (armed, squash) on green CI after this flip.

## 💡 Session idea

**Generalize the refuse-to-publish guard: extract a shared `require_full_history()` /
shallow-refuse helper co-located with the existing shallow logic in
`src/engine/lib/git_truth.py`** (which already owns `is_shallow()` and the graft-class
degradation), so every current and future git-history measurement script —
`measure_grounded_skills.py` (this session), `measure_pr_latency.py`, and siblings —
refuses consistently on a shallow clone instead of each re-implementing the check. Worth
having because R3 only hardened *one* of the two scripts that read git history: the same
prose trap (M4-style metrics silently zeroed on a shallow clone) still lives unguarded in
`measure_pr_latency.py`, and any next measurement script will re-open it. A single helper
turns "remember to add the check" into "call the seam" — the same refuse-to-publish
posture, enforced once. Deduped: grepped `docs/ideas/` — the only `shallow` mention
(`idea-index-merged-reality-2026-07-14.md`) is about *graceful-degradation display*, not a
shared refuse seam; the groom doc's R-slices don't cover it either.

## ⟲ Previous-session review

Previous session — **R2 `/scope-backlog-item` skill (PR #490)**. Did well: it
**pre-registered R3–R12 with recipes in the groom doc**, which is exactly why R3 was
turnkey this session — the intent, the file (`measure_grounded_skills.py`), and the shape
(REFUSE marker + exit non-zero + test) were all named before this session booted, so no
re-discovery was needed. What it (and the groom-doc format it dogfooded) could improve:
the recipes are single one-liners — R3's recipe named the *script* but not the exact file
list, acceptance criteria, or known traps, so this session still had to infer that the
`shallow` flag was already carried per-repo and that only the `--json` path (not
markdown/stdout) should refuse. System improvement it surfaces: give the
`/scope-backlog-item` skill's output a **consistent recipe template with an explicit
`files / acceptance / traps` sub-block** per item, so a future cold-start lands on a fully
specified slice instead of inferring the file list from the script name. That closes the
one inference step between "buildable-now recipe" and "turnkey build" — the same
enforce-don't-exhort instinct the skill itself embodies.
