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

## Did (PR #441)

- `src/engine/checks/check_adopters_current.py` — new `adopters-version-lag`
  **advisory** finding. Two pure helpers: `_embedded_kit_version(text)` parses
  the registry's `kit release: v<X.Y.Z>` stamp; `_current_version_home(target)`
  reads `substrate.config.json` `kit_version` (json, fail-open). Fires when both
  parse and differ. Warn-only, rides the existing `adopters_advisories` surface
  in `cmd_check` (cli.py:1839) — no cli change needed. Docstring updated.
- `tests/test_check_adopters_current.py` — +5 tests: version-home-moved fires
  (the #438 class, young stamp so `adopters-stale` can't); match → silent;
  no-config fail-open; unparseable-config fail-open; version-lag rides alongside
  `adopters-stale` on an old-and-superseded registry. 1721 → 1726 passed.
- `dist/bootstrap.py` rebuilt via `src/build_bootstrap.py`, byte-stable across
  two runs (+65 lines, checker already in MODULE_ORDER).

## Verify

- `python3 -m pytest tests/ -q` → **1726 passed, 1 skipped** (41.9s).
- `python3 dist/bootstrap.py check --strict` → clean except the designed
  born-red Session-gate HOLD (flipped `complete` as the final step).
- Live real-tree proof: embedded `v1.18.0` == home `v1.18.0` → no false positive.

## 💡 Session idea (Q-0089)

**Adopter-report ↔ tree-truth self-DRIFT nag.** `docs/adopters.md` already
distinguishes an adopter's heartbeat self-report (`kit: v… · check: …`) from its
committed tree (the vendored `bootstrap.py` header + `substrate.config.json`
pin), and surfaces disagreement as a DRIFT row — but that verdict is only fresh
at `bootstrap currency` time (network, agent-side). A cheap pure companion: a
`check` advisory that, for the **kit's own row**, re-derives the tree-source
version from the local `dist/bootstrap.py` header at check-time and warns if it
disagrees with the registry's recorded self-pin — the same "recorded vs live"
coupling this PR applies to the version home, applied to the kit's own registry
row, catching a stale self-row the instant the dist rebuilds. Not built.

## ⟲ Previous-session review (Q-0102)

Of the reconcile-#438-downstream session (card
`.sessions/2026-07-17-reconcile-438-downstream.md`): genuine remark — it did the
right disciplined thing, regenerating `docs/adopters.md` by *discovery* rather
than hand-patching the one stale row, and it explicitly logged the friction as a
Q-0089 idea instead of just fixing-and-forgetting — which is exactly why this
session had a ready, well-scoped rung to build. Small miss: it left the idea at
"couple version-home changes to a downstream-regen advisory" without noting the
§3.2 subprocess ban that shapes the whole implementation (git-in-checker is
banned), so this session had to discover the constraint before it could pick the
version-value approach. System improvement it surfaces: an idea born from a
*checker* friction should carry a one-line "checker constraints apply (§3.2 —
pure, no subprocess)" tag so the building session inherits the boundary — folded
into this card's design note. Beyond that, nothing to invent.

## Doc audit (Q-0104)

Self-initiated rung; no owner decisions to route. The advisory + its provenance
live in the checker docstring, this card, and the PR #441 body. Backlog readout
carried in the heartbeat. Nothing captured only in chat.

