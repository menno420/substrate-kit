# 2026-07-17 — Version-home → adopters-regen advisory (`adopters-version-lag`)

> **Status:** `in-progress`

📊 Model: Claude Opus 4.8 (1M) · standard · engine-checker build

Rung 4 (self-initiated, contained + reversible). Builds the previous session's
Q-0089 ender idea (card `.sessions/2026-07-17-reconcile-438-downstream.md`):
couple a version-home change to a downstream-regen advisory so a "fix-at-source"
session (like #438) can't leave `docs/adopters.md` silently stale for a day
until the next wake catches it on sight.

⚑ Self-initiated: prev-card Q-0089 idea → guard (friction → guard).

## Intent

`#438` bumped a *version home* (`substrate.config.json` + `config.py KIT_VERSION`)
at the source, but nothing flagged that the discovery-generated `docs/adopters.md`
was now stale — the existing `adopters-stale` advisory only fires on **calendar
age** (>14 days), and adopters.md was freshly regenerated (<14d), so age never
fired. The version-home-move class slips straight through.

## Design (decide-and-flag)

The idea literally described a **git-log** signal ("adopters.md's Generated
timestamp predates the latest commit touching a version-home"). Engine **checker**
code bans `subprocess`/git (§3.2 — checkers are pure/deterministic), so a git
approach can't live in a checker. A **better, git-free** implementation of the
same intent is available: `render_adopters` already stamps the registry with the
kit version it was generated against —
`> Generated: <stamp> · kit release: v<KIT_VERSION>` (currency.py:530; the
generator passes `KIT_VERSION` from config.py, cli.py:2905). So the pure signal is
a **version-value comparison**: parse adopters.md's embedded `kit release: vA`,
read the target tree's current version home (`substrate.config.json` `kit_version`,
kept synced to `KIT_VERSION` by `cut_release.py` since #438), and fire an advisory
when they differ — "the version home moved after the last `bootstrap currency`."
This is Q-0014's "assume he'd want the better one": more precise than a timestamp
(compares the version itself), deterministic, no subprocess, correct for the
`target` semantics (validates the committed tree, not the running engine), and it
keys off the exact file (`substrate.config.json`) whose #438 change started the
drift tail. Advisory-only, never a gate — fail-open on any missing/unparseable
input (matches the `adopters-stale` posture).

## Did

(filled at close)

## Verify

(filled at close)
