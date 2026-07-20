# Fleet adopter registry

> **Status:** `living-ledger` · **Sole writer: kit-lab** (this repo)
>
> **GENERATED — do not hand-edit** — regenerate with `python3 dist/bootstrap.py currency`
> (agent-side: kit CI cannot auth to sibling repos, so CI validates
> only this file's format + staleness, never refetches).
> Generated: 2026-07-20T06:27:56Z · kit release: v1.20.1
>
> Who runs which kit version — the substrate-coordinator's
> visibility surface (inbox ORDER 003; manager research 2026-07-09).
> kit-lab is the fleet's substrate coordinator but has **zero write
> access to adopter repos** (KF-2: the lab never writes to
> consumers); this registry is generated from **read-only evidence**:
> each repo's committed tree (the vendored `bootstrap.py` header —
> the dist the repo *runs* — plus the `substrate.config.json`
> `kit_version` pin) and its own heartbeat self-report (the `kit:
> v<X.Y.Z> · check: green|red · engaged: yes|no` line planted by
> adopt since v1.3.0). A self-report alone is a claim; the tree is
> truth — disagreement is surfaced as a DRIFT row below, never
> silently resolved.

## Registry

| repo | tree (vendored dist) | config pin | self-report (`kit:` line) | engaged | verdict vs kit v1.20.1 |
|---|---|---|---|---|---|
| menno420/substrate-kit | v1.20.1 (dist/bootstrap.py) | v1.20.1 | v1.20.0 | — | ⚠️ DRIFT · current |
| menno420/superbot-next | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | no | stale (v1.17.0 < v1.20.1) |
| menno420/websites | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | stale (v1.17.0 < v1.20.1) |
| menno420/superbot | — | v1.0.0 | no `kit:` line | — | stale (v1.0.0 < v1.20.1) · pin-only (no vendored dist found) |
| menno420/superbot-games | v1.17.0 (bootstrap.py) | v1.17.0 | status.md: v1.15.0 · status-mining.md: v1.7.1 · status-exploration.md: v1.7.1 | yes | ⚠️ DRIFT · stale (v1.17.0 < v1.20.1) |
| menno420/trading-strategy | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | stale (v1.17.0 < v1.20.1) |
| menno420/gba-homebrew | v1.20.1 (bootstrap.py) | v1.20.1 | v1.17.0 | — | ⚠️ DRIFT · current |
| menno420/pokemon-mod-lab | v1.15.0 (bootstrap.py) | v1.15.0 | no `kit:` line | — | stale (v1.15.0 < v1.20.1) |
| menno420/venture-lab | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | stale (v1.17.0 < v1.20.1) |
| menno420/fleet-manager | v1.17.0 (bootstrap.py) | v1.17.0 | no `kit:` line | — | stale (v1.17.0 < v1.20.1) |
| menno420/idea-engine | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | stale (v1.17.0 < v1.20.1) |
| menno420/superbot-mineverse | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | yes | stale (v1.17.0 < v1.20.1) |

## Drift report

Tree and self-report disagree below — reconcile at the SOURCE (the adopter's own heartbeat / pin), never by hand-editing this file:

- **menno420/substrate-kit** — self-report vs tree: control/status.md claims v1.20.0 but the tree says v1.20.1
- **menno420/superbot-games** — self-report vs tree: control/status.md claims v1.15.0 but the tree says v1.17.0
- **menno420/superbot-games** — self-report vs tree: control/status-mining.md claims v1.7.1 but the tree says v1.17.0
- **menno420/superbot-games** — self-report vs tree: control/status-exploration.md claims v1.7.1 but the tree says v1.17.0
- **menno420/gba-homebrew** — self-report vs tree: control/status.md claims v1.17.0 but the tree says v1.20.1

## Row protocol

- **Columns:** `repo` (owner/name) · `tree` (the vendored dist the
  repo *runs*, parsed from its stamped header — primary truth) ·
  `config pin` (`substrate.config.json` `kit_version`, recorded by
  adopt/upgrade — secondary) · `self-report` (the heartbeat `kit:`
  line; per-lane on multi-Project repos) · `engaged` (the KL-7
  post-adopt gate, as self-reported) · `verdict` (vs the kit's
  current release; DRIFT when evidence disagrees).
- **One writer:** only kit-lab sessions regenerate this file (same
  one-writer rule as the `control/` bus). Adopters never write here
  — their channel is their own `control/status.md` `kit:` line.
- **Staleness reads as dark**, not as wrong: the `Generated:` stamp
  above is the evidence date; rerun the scan to refresh.
- **`unreadable` reads as dark too**: no transport (raw content,
  authenticated API, branch tarball) could see that repo's tree
  this run — adoption is UNKNOWN, deliberately never rendered as
  "not adopted" (private-repo 404s are transport, not evidence).
- **Roster:** `docs/fleet-repos.txt` (one `owner/repo` per line;
  extra tokens name per-lane heartbeat files).
- **Releases point back here:** every release's notes carry the
  adopter upgrade checklist (`src/build_release_json.py` appends it
  to `notes.md`), whose last step is updating the adopter's own
  `kit:` status line — the loop that keeps the self-report column
  honest.

## v1.20.1 distribution wave (2026-07-20)

Wave lane PR #548 (fm ORDER 048). Release v1.20.1 = tag `v1.20.1` →
`40eb0fe`, dist sha256
`d6c4f81565f8877f38e2b4315968fc5f22a378c9c4dfdd89f8ed02827e7f6b39`.
The `Registry` table above reflects each adopter's **main-branch tree**;
this section records the **pending upgrade PRs** the scan cannot see
(an open PR is not yet in the tree — rendered as a bullet list so these
lines stay invisible to the rows-only currency parser). Kit-distribution
files only — host workflows / control / settings / hooks untouched in
every PR. All 1.17.0 → 1.20.1 unless noted.

- **gba-homebrew** — PR #211 — **merged** (tree now v1.20.1)
- **idea-engine** — PR #740 — open · ready
- **superbot-next** — PR #602 — open · ready
- **websites** — PR #452 — open · ready
- **trading-strategy** — PR #160 — open · ready
- **superbot-games** — PR #183 — open · ready
- **venture-lab** — PR #282 — open · ready
- **superbot-mineverse** — PR #138 — open · ready
- **fleet-manager** — PR #390 — open · ready
- **superbot** — pin 1.0.0 — skip · not-applicable (pin-only nominal
  adoption; no vendored dist / `.substrate/` state — dist-vendoring
  upgrade N/A)
- **pokemon-mod-lab** — DARK (private) · skipped, adoption UNKNOWN

Each open PR reds its adopter's gate **only** on pre-existing,
resident-owned false-wall / badge doc content — the resident lane's to
reconcile, not a wave defect. As those PRs merge, the `Registry` table
above flips each row to `current` on the next `currency` scan; the
`kit:` self-report line is the adopter seat's own to update.
