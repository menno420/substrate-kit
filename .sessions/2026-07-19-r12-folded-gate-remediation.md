# R12 — check_folded_gate remediation snippet

> **Status:** `in-progress`

**What.** Extend the `check_folded_gate` advisory so that, when a host workflow folds the session gate without the diff-aware selection, its finding ALSO emits a paste-ready diff-aware card-derivation block — the host fixes the fold in one paste instead of hand-porting from prose. Advisory, never exit-affecting.

**About to do.** Add a `REMEDIATION_SNIPPET` constant (the kit's own diff-aware `ci.yml` gate, adopter-interpreter form) to `src/engine/checks/check_folded_gate.py` and append it to the Finding message; rebuild `dist/bootstrap.py` (the checker is in MODULE_ORDER) and commit the byte-pinned dist alongside; extend `tests/test_check_folded_gate.py` to assert the snippet is emitted and is itself a valid diff-aware gate. Checker stays advisory (off STRICT_SUBCHECKS). Rank R12 from docs/planning/2026-07-19-night-run-idea-groom.md; claim `claude/r12-folded-gate-remediation`.

[[fill: enders resolved at flip — 💡 idea · ⟲ prev-session review · ⚑ Self-initiated · 📊 Model]]
