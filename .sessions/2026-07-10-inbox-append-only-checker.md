# 2026-07-10 — gen-2: inbox append-only checker (issue #36 rpt 2)

> **Status:** `in-progress`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side checker (single scoped
  PR: enforce control/inbox.md pure-append + ORDER grammar on the control lane)

## Scope

Session goal: gen-2 kit-side fix for issue #36 report 2. `control/inbox.md` is the
manager's ORDER bus — one writer, append-only by protocol (`control/README.md`) — but
that law was convention-only: PR #34 (an ORDER append) merged 19 s after open with
nothing checking the change was pure-append, that existing ORDERs were untouched, or
that the appended text was a valid ORDER block. Any session could rewrite or erase
orders on a green control-only PR.

Fix: a new `check_inbox_append` checker (`src/engine/checks/check_inbox_append.py`)
that verifies a `control/inbox.md` change is PURE-APPEND vs the merge-base (the base
file's bytes are a prefix of the new file) and that the appended text follows the
ORDER-block grammar. Diff access mirrors the session-log gate — the engine never shells
out (§3.2 subprocess ban), so CI extracts the merge-base blob with git and hands the
path in via `check --inbox-base <file>`; the checker only reads two files and compares.
Wired into `cmd_check` (rides the finding loop like every checker) and into
`.github/workflows/ci.yml` as a dedicated step running on BOTH lanes. Shipped with its
regression tests: a non-append diff reds, a legitimate pure-append greens.

Writer IDENTITY is deliberately not enforced — on a single-account program it is not
enforceable in-repo (issue #36 report 2); this gate enforces the append LAW, the part
that lives in the bytes. Scope is report 2 ONLY — report 1 shipped in #86, report 3 is
out. Touches only `src/engine/checks/` (+ its cli/build registration), `dist/bootstrap.py`
(regenerated), `tests/`, and this card.

## 💡 Session idea

The `--inbox-base` "CI extracts the git blob, the pure-stdlib engine only diffs two
files" split is now used by both the session-log gate and this inbox gate. A named
convention for "diff-aware control-lane checkers" (CI does the git work, the engine
receives file paths) would let the next such check inherit the pattern instead of
re-deriving where the base ref comes from.

## ⟲ Previous-session review

The prior card (2026-07-10 fix-engagement-comment-leniency, issue #36 rpt 1) closed
`complete` with `check --strict` green and shipped as #86. No defect inherited; this
session picks up the sibling report-2 work it explicitly scoped out.
