# Fleet adopter registry

> **Status:** `living-ledger` · **Sole writer: kit-lab** (this repo)
>
> **GENERATED — do not hand-edit** — regenerate with `python3 dist/bootstrap.py currency`
> (agent-side: kit CI cannot auth to sibling repos, so CI validates
> only this file's format + staleness, never refetches).
> Generated: 2026-07-15T12:09:23Z · kit release: v1.17.0
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

| repo | tree (vendored dist) | config pin | self-report (`kit:` line) | engaged | verdict vs kit v1.17.0 |
|---|---|---|---|---|---|
| menno420/substrate-kit | v1.17.0 (dist/bootstrap.py) | v1.0.0 | v1.17.0 | — | ⚠️ DRIFT · current |
| menno420/superbot-next | v1.17.0 (bootstrap.py) | v1.17.0 | v1.16.0 | — | ⚠️ DRIFT · current |
| menno420/websites | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | current |
| menno420/superbot | — | v1.0.0 | no `kit:` line | — | stale (v1.0.0 < v1.17.0) · pin-only (no vendored dist found) |
| menno420/superbot-games | v1.17.0 (bootstrap.py) | v1.17.0 | status.md: v1.15.0 · status-mining.md: v1.7.1 · status-exploration.md: v1.7.1 | yes | ⚠️ DRIFT · current |
| menno420/trading-strategy | v1.17.0 (bootstrap.py) | v1.17.0 | no `kit:` line | — | current |
| menno420/gba-homebrew | v1.17.0 (bootstrap.py) | v1.17.0 | no `kit:` line | — | current |
| menno420/pokemon-mod-lab | v1.15.0 (bootstrap.py) | v1.15.0 | no `kit:` line | — | stale (v1.15.0 < v1.17.0) |
| menno420/venture-lab | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | current |
| menno420/fleet-manager | v1.17.0 (bootstrap.py) | v1.17.0 | no `kit:` line | — | current |
| menno420/idea-engine | v1.17.0 (bootstrap.py) | v1.17.0 | v1.17.0 | — | current |
| menno420/superbot-mineverse | v1.17.0 (bootstrap.py) | v1.17.0 | v1.16.0 | — | ⚠️ DRIFT · current |

## Drift report

Tree and self-report disagree below — reconcile at the SOURCE (the adopter's own heartbeat / pin), never by hand-editing this file:

- **menno420/substrate-kit** — tree-internal: vendored dist says v1.17.0 but substrate.config.json pins v1.0.0
- **menno420/superbot-next** — self-report vs tree: control/status.md claims v1.16.0 but the tree says v1.17.0
- **menno420/superbot-games** — self-report vs tree: control/status.md claims v1.15.0 but the tree says v1.17.0
- **menno420/superbot-games** — self-report vs tree: control/status-mining.md claims v1.7.1 but the tree says v1.17.0
- **menno420/superbot-games** — self-report vs tree: control/status-exploration.md claims v1.7.1 but the tree says v1.17.0
- **menno420/superbot-mineverse** — self-report vs tree: control/status.md claims v1.16.0 but the tree says v1.17.0

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
