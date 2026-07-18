# Session · 2026-07-18 · self-row-registry-stamp

> **Status:** `complete`

Intent: automate the substrate-kit self-row registry stamp (B-2) — add a
born-red gate + wire a network-free self-restamp into `cut_release.py` so the
version-bump PR itself carries the correct self-row.

- **📊 Model:** Opus 4.8 · high · kit-engine feature + CI gate
- ⚑ Self-initiated: none — B-2 is a groomed-baton slice (docs/planning/2026-07-19-grounded-skills-window-run.md) under the ORDER 048 standing grant.

About to: automate the substrate-kit self-row registry stamp — add a born-red
gate (`adopters-self-row-stale` in `check_adopters_current.py`, self-row
scoped) + wire a network-free self-restamp (`local_self_scan` /
`restamp_self_row` in `currency.py`) into `scripts/cut_release.py` so the
version-bump PR itself carries the correct self-row.

## What shipped

Automated the substrate-kit **self-row** registry stamp so a version-bump PR
carries the correct self-row inline, removing the manual aftermath hop. Two
halves:

- **Born-red gate** `adopters-self-row-stale` in
  `src/engine/checks/check_adopters_current.py` — self-row-scoped: reds CI when
  the substrate-kit self-row in `docs/adopters.md` goes stale versus the local
  kit version home, so the kit's own row can no longer silently lag its own
  version.
- **Network-free self-restamp** — `local_self_scan` + `restamp_self_row` in
  `src/engine/currency.py` — wired into `scripts/cut_release.py`, so the
  release-bump PR stamps the correct self-row inline instead of deferring it to
  a manual aftermath edit. No network dependency; runs off the local version
  home.
- `dist/bootstrap.py` rebuilt (byte-pin gate green on fresh rebuild).

Verify: `python3 -m pytest tests/ -q` → 1786 passed; dist byte-clean on fresh
rebuild; `python3 dist/bootstrap.py check --strict` red only on this card's
born-red hold (no other findings). Independent review returned **SHIP**.

## 💡 Session idea (Q-0089)

**Rebuild dist BEFORE the self-restamp in the release flow (or render a
"pending-rebuild" marker in the self-row tree cell).** `restamp_self_row` bumps
the self-row's config-pin cell but leaves the tree cell (dist header version)
lagging until the aftermath dist rebuild, so a release-bump PR momentarily
commits a `docs/adopters.md` whose own self-row shows a DRIFT verdict against
the kit itself. A follow-up could reorder the release flow to rebuild dist
first (or write a `pending-rebuild` marker into the tree cell) so the bump PR
always commits a clean, non-self-drifting self-row. Worth having: it closes the
one window where the self-row automation this wake added still commits a
transiently-inconsistent self-row. Dedup-checked: no `restamp`/`self-row`/`tree
cell` idea exists under `docs/ideas/` — the two grep hits (README.md:269,
heartbeat-verb-2026-07-09.md:15) are the unrelated CLI restamp verb (PR #346)
and the restamp-lane `--full` contract, not this self-row tree-cell lag. Card
flag only, matching the recent 💡 convention (no idea file).

## ⟲ Previous-session review (Q-0102)

Of the 2026-07-18 B-1 guard-surface-census wake (PR #470): **genuine credit** —
it read all six workflow jobs from ground truth and asserted **bidirectional**
set-equality against the live `jobs:` keys, so a new, removed, OR renamed job
now reds CI (the rename-in-place case is covered by the set-equality, not a
gap). **What it could improve:** the census pins the NAME set but trusts the
**hand-declared KIND** (GATE_PINNED / ALIAS / AUTOMATION) — the tests check
reason length and kind-membership, not whether a job classified AUTOMATION
actually cannot red a PR, so a job's kind could silently drift from declared
(AUTOMATION) to actual (gating) without the census noticing. **System
improvement it surfaces:** cross-check each census kind against a ground-truth
signal (is the job in the `main` ruleset's required checks? does the job run
pytest / `check`?) so KIND can't drift undetected from what the workflow
actually does — the natural next census rung after the NAME-set pin.
