# Release runbook — cutting a substrate-kit release

> **Status:** `binding`
>
> substrate-budget: 550 words
>
> The proven recipe, written once instead of reassembled from session cards
> (v1.7.1 run 29124338479 · v1.8.0 run 29133041799 · v1.9.0 run 29139623697
> all followed it). Full per-cut evidence: `control/status.md` release
> records + git history.

## 0. Preconditions

- Payload complete in `CHANGELOG.md` `[Unreleased]` — verify every shipped
  PR's entry is present BEFORE the cut.
- Decide the semver class by the §4.1 contracts (MAJOR = planted-doc /
  state / config / CLI break; MINOR = new capability; PATCH = fixes).

## 1. Claim, then bump PR (born-red)

1. Work-claim `control/claims/release-vX.Y.Z.md` on main first (control
   fast-lane PR).
2. Cut the bump branch from post-claim main; born-red session card is the
   first commit; open the PR ready + arm auto-merge at open.

## 2. The version bump (one commit set)

- **Mechanized:** `python3 scripts/cut_release.py X.Y.Z` (dry-run; `--write`
  applies) performs this section's file edits — both version homes + the
  CHANGELOG transform — and prints the remaining manual steps.
- **Version homes (both, same commit):** `src/engine/lib/config.py:31`
  (`KIT_VERSION`) and `pyproject.toml:17` (`version`).
- **CHANGELOG:** rename `[Unreleased]` → `[X.Y.Z] - <date>` (fresh empty
  `[Unreleased]` above it); keep the
  `<!-- release: breaking=… state_migration=… min_upgrade_from=… -->`
  machine comment accurate — `release.yml` refuses a version with no
  CHANGELOG section.
- **Dist regen + byte-pin:** `python3 src/build_bootstrap.py`, then confirm
  the builder's printed byte count equals `wc -c dist/bootstrap.py`
  (print==disk verified first on the v1.9.0 cut; CI's byte-equality pin
  re-checks `git diff --exit-code dist/bootstrap.py` against a fresh build).

## 3. Verify locally, flip, merge

- `python3.10 -m pytest tests/ -q` all green (Python floor 3.10, like CI).
- `python3.10 -m ruff check src/engine/` clean.
- `python3 src/build_release_json.py --version X.Y.Z --verify-only` →
  "preconditions all green".
- Repo checkers (`scripts/check_idea_index.py`, `check_program_law.py`).
- `python3 dist/bootstrap.py check --strict` — the only acceptable pre-flip
  red is the designed born-red hold naming this session's own card.
- Flip the card `complete` as the last commit; auto-merge lands it on green.

## 4. Publish

- Dispatch `release.yml` via `workflow_dispatch` with input
  `version=X.Y.Z` on main at the bump merge SHA.
- The run creates annotated tag `vX.Y.Z` and the GitHub Release with three
  assets: `bootstrap.py`, `bootstrap.py.sha256`, `release.json`.

## 5. Three-way verification (never skip)

Independently download the released `bootstrap.py`; its sha256 must equal
BOTH the `release.json` `sha256` field AND the committed
`dist/bootstrap.py` at the bump SHA. Record run id, tag object, commit SHA,
and the hash in the release record.

## 6. Aftermath

- Adopters regen: `python3 dist/bootstrap.py currency` →
  `docs/adopters.md` (close-out PR; kit's own row self-heals next regen).
- `control/status.md` release record + claim delete.
- Next slice: the distribution wave (`upgrade` each adopter, merged on
  green, then registry regen).
