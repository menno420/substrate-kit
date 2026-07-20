# Cut release v1.20.0 — reconcile CHANGELOG, cut dist, publish, verify

> **Status:** `in-progress`

**Session:** 2026-07-20 · Self Improvement work-loop · substrate-kit
**Baton:** release cut v1.20.0. Provenance: fm ORDER 048 standing grant + coordinator dispatch. Status.md at HEAD (#546) records the wave-2 buildable ladder S2–S17 CONSUMED and "next release held for wave authorization" — this dispatch IS that authorization. v1.19.0 is the current release (tag `v1.19.0` @ 598f820); everything merged since (R5/#495 → baton advisory/#545) is unreleased and adopter-visible → a MINOR bump.

## What this session does (about to do)

1. Reconcile `CHANGELOG.md` `[Unreleased]` → a v1.20.0 section covering every feature PR since v1.19.0 (R5–R15, S2–S17, baton advisory), cited against the actual `git log v1.19.0..origin/main`.
2. `python3 scripts/cut_release.py 1.20.0 --write --rebuild-dist` — bumps both version homes, restructures the CHANGELOG, rebuilds + byte-pins `dist/bootstrap.py` (folds FOLLOWUP step 2, #541), re-stamps the self-row (#488).
3. Verify: `python3 -m pytest tests/ -q` (expect ~2052 passing) + `python3 dist/bootstrap.py check --strict`.
4. Publish via `release.yml` `workflow_dispatch` (tag-push is 403-walled) once the bump is on main.
5. Three-way sha256 verification (`scripts/verify_release.py`).
6. CAPABILITIES.md dated-append row for the 2026-07-16 adopter-wave classifier denial (venue-specific/transient, cites PR #420).
7. Regenerate `docs/adopters.md`; update `control/status.md` heartbeat with a `kit: v1.20.0` line (written LAST, before the flip).

Born-red on purpose: this card holds the merge (session-gate) until the deliberate final `complete` flip after the heartbeat is written.

- **📊 Model:** opus-4.8 · high · mechanical refactor — release cut v1.20.0
- **⚑ Self-initiated:** NOT self-initiated — release cut executed under fm ORDER 048 standing grant + coordinator dispatch. Source-verified before building: confirmed v1.19.0 is the latest release (tag list + CHANGELOG top), `[Unreleased]` is empty, no open PR / branch / claim holds the release lane, and the v1.20.0 PR set was reconciled against the real `git log v1.19.0..origin/main` (task-cited #482/#484 confirmed already-released in ≤v1.19.0 and therefore NOT claimed as v1.20.0 content — cite-real-PRs discipline).
- **💡 Session idea:** _to be filled before flip._
- **⟲ Previous-session review:** _to be filled before flip._
