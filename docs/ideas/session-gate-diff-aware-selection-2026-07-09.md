---
state: promoted
origin: lab
shipped_pr: 19
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-09
outcome: shipped
---

# PR-diff-aware session-gate card selection (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (💡, `.sessions/2026-07-09-kl1-ci-delta.md`) → promoted →
> **shipped** same day (kit PR #19). **Origin:** lab — the KL-1 session's own
> CI friction (it had to ship a `touch`-from-git mtime-restore shim).

## The idea

`check` picked the "current" session card as newest-by-mtime — a heuristic a
fresh CI checkout silently degrades (every mtime flattens to checkout time),
which forced the kit's CI to restore card mtimes from git commit times before
the session gate, and which every `adopt --wire-enforcement` consumer would
inherit via the planted `substrate-gate.yml`. The durable fix: an explicit
selector in the engine plus diff-derived selection in the workflows.

## What shipped (PR #19)

- **`check --session-log <file>`** — gate on the named card explicitly;
  a missing named file counts as an *absent* log (advisory by default, hard
  failure under `--require-session-log`), never a silent fallback to a
  different card. No argument → the mtime guess, unchanged (fail-open,
  backward-compatible).
- **Kit `ci.yml`**: the session-gate step derives the card from
  `git diff --name-only <range> -- '.sessions/*.md'` (PR base range on
  pull_request, `event.before..sha` on push) and passes it via
  `--session-log`; the mtime-restore shim is deleted.
- **Planted `substrate-gate.yml`** (`live_ci_workflow`): the same diff-aware
  step travels to every consumer; `sessions_dir` threads through.

## Survive window

Merged 2026-07-09 → the D-15 revert-scan may flip `outcome: survived` from
2026-08-08.
