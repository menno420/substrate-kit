# 2026-07-10 — gen-2: fix engagement-checker comment-leniency (issue #36 rpt 1)

> **Status:** `complete`

- **📊 Model:** claude-opus-4-8 · high · gen-2 kit-side checker fix (single scoped
  PR: strip `#`-comment content before the `enforcement-unwired` needle test)

## Scope

Session goal: fix the engagement gate's comment-leniency bug (issue #36 report 1).
`_enforcement_wired` (`src/engine/checks/check_engagement.py`) substring-matches
`check --strict` across whole workflow files, so a workflow whose only mention of the
command sits inside a `#` comment (`# TODO someday run check --strict here`) falsely
clears the gate — a repo looks ENGAGED with a dead door. Fix: strip `#`-prefixed
comment content per line before the needle test (still forgiving of hand-rolled gates,
immune to comments), shipped with a known-bad fixture test that must RED as
`enforcement-unwired`, plus a kept assertion that a genuinely-wired workflow still
passes (no false-negative regression). Scope is report 1 ONLY — report 2 (inbox
append-only checker) and report 3 are out of this PR. Touches only
`src/engine/checks/`, `tests/`, and this card.

## 💡 Session idea

The four `enforcement-unwired`-style substring gates elsewhere in the kit may share this
comment-leniency shape; a shared `_strip_comment` helper (or a tiny "code-not-comment
contains" util) would let every needle check inherit the fix instead of re-deriving it.

## ⟲ Previous-session review

The prior card (2026-07-10 coordinator-dispatch inbox check) closed cleanly as a
stand-down with `check --strict` green; no defect inherited. This session picks up fresh
kit-side work on the born-red engagement checker it references.
