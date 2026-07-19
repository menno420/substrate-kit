# 2026-07-19 — Folded-gate diff-aware advisory sub-check (`folded-gate-check`)

> **Status:** `complete`

- **📊 Model:** opus-4.8 · high · feature build

Building the rank-2 folded-gate-diff-aware-card advisory `check` sub-check per
`docs/planning/2026-07-19-needs-planning-recipes.md` §2 —
`src/engine/checks/check_folded_gate.py` (advisory, never exit-affecting) +
cli.py wiring + tests + dist rebuild.

## 💡 Session idea (Q-0089)

**`check_folded_gate` remediation snippet.** The advisory shipped this session
only NAMES the workflow that folded the diff-aware card-derivation gate. Extend
it to also emit the exact diff-aware card-derivation block to port — copied from
the planted kit `ci.yml` session-gate step (the canonical reference the
`folded-gate-diff-aware-card` idea already points adopters at) — so a host fixes
the fold in one paste instead of reverse-engineering it from the reference
workflow. Enforce-don't-exhort taken one step further: the checker doesn't just
flag the miss, it hands over the fix. Worth having because the folded-gate class
recurs across hosts (superbot-next `gate`, websites `quality.yml`), and a
self-emitting snippet turns each fix from a reverse-engineering task into a copy.
Deduped against `docs/ideas/` — `folded-gate-diff-aware-card-2026-07-11.md`
describes the detection advisory and the manual port, but not a snippet the
advisory emits itself.

## ⟲ Previous-session review (Q-0102)

The previous session (pinned-feed-contract graduation, PR #482) graduated the
rank-1 recipe cleanly — it promoted the idea file idea→shipped, reconciled the
idea body State line so the body-state-drift leg passed, re-verified the byte-pin
post-commit, and left a genuinely useful baton naming this rank-2 folded-gate
pick, so this session started with zero re-deciding. What it could have done
better: its own 💡 session idea (an `applies-when:` recipe-discovery frontmatter
tag) was deduped against `docs/ideas/` but left card-only — a substantial idea
that lives only in a session card is at risk of dropping out of the Q-0089
grooming loop, which grooms `docs/ideas/`, not session cards. Concrete workflow
improvement it surfaces: when a session idea is substantial and actionable (not
a one-liner), the flip commit should also drop it into `docs/ideas/` + the README
index, so the idea backlog — not just the session log — carries it forward.
