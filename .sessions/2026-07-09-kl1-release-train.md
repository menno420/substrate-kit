# Session 2026-07-09 — KL-1 release train → v1.0.0

> **Status:** `in-progress`

**About to do (founding plan §4 + §10 KL-1 row, one session, 2 PRs + tag):**

- **PR A (this PR):** `KIT_VERSION` constant + new `Config.kit_version` dataclass field
  (survives `from_dict`) + `--version` CLI flag + version stamp in the dist header
  (`build_bootstrap.py`); adopt records `kit_version` + planted-doc sha256 hashes;
  `CHANGELOG.md` (keep-a-changelog, 1.0.0 section); `LICENSE` (MIT — owner item P8,
  recorded default, ⚑); `release.yml` (v* tag → fresh-dist byte check → sha256 →
  Release with bootstrap.py + bootstrap.py.sha256 + release.json; refuses without a
  matching CHANGELOG section); `reconciliation_prs` default 20→30; `_ENGINE_MANIFEST`
  dropped from the dist (§3.4 — `init --unpack` never shipped).
- **PR B:** `upgrade` CLI verb per §4.3 — archive old dist to `.substrate/backup/`
  first, staged regeneration, hash-based planted-doc diff report, `--apply-docs`
  (untouched docs only), state backup + `upgrade --rollback`.
- **Then:** tag `v1.0.0` on the final merge commit, verify `release.yml` publishes
  the Release with all three assets.

This card is shared by both PRs of the train; it flips `complete` as the session's
deliberate last step.
