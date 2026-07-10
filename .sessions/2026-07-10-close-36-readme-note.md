# 2026-07-10 — gen-2: close issue #36 — README writer-identity honesty note

> **Status:** `in-progress`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-lab issue-#36 close (report-2 second half)

## Scope

Ship the remaining half of issue #36 (report 2). The enforceable append-law
checker (`check_inbox_append`, pure-append + ORDER grammar for `control/inbox.md`)
already shipped in #87; what report 2 also asked for was the honest-README clause:
*state honestly in `control/README` that writer IDENTITY is not enforceable in-repo
on a single-account program.*

One write, control-only:

1. **`control/README.md`** — a concise `**Enforced vs. convention.**` note in the
   one-writer section: the append-only + ORDER-grammar half of the `inbox.md` rule
   is now CI-enforced by `check_inbox_append` (shipped in #87), BUT writer IDENTITY
   cannot be enforced in-repo on a single-account program (every commit
   authenticates as the same account), so *who* appends remains convention.

`control/inbox.md` and `control/status.md` untouched. No `src/` touched, so
`dist/bootstrap.py` is not regenerated. `bootstrap.py check --strict` stays green.

## 💡 Session idea

With both halves of issue #36 report 2 shipped (enforceable append-law in #87 +
this honesty note), the doc now draws the exact line between what CI guarantees and
what stays human discipline — the "honest about your walls" house pattern applied to
the coordination protocol itself.

## ⟲ Previous-session review

The prior card (2026-07-10 gen-2 session close) explicitly flagged this as a
deferred follow-up: "issue #36 report-2's honest-README line is not yet in
control/README.md." This session closes that gap. No defect inherited.
