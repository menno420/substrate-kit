# R10 — harness `--freeze` self-citing reproduce block

> **Status:** `in-progress`

**What.** Add `--freeze` to `scripts/measure_grounded_skills.py`: given `--json`/`--commit-results`, emit the output's sha256 + a paste-ready reproduce block, and write a `<output>.freeze` sidecar — every window run becomes self-citing and tamper-evident. Honors the shallow-clone refuse guard.

**About to do.** Add the flag, the sha256+reproduce emission, a stderr paste block, and 7 tests. Rank R10 from docs/planning/2026-07-19-night-run-idea-groom.md; claim `claude/r10-harness-freeze`.

[[fill: enders resolved at flip — 💡 idea · ⟲ prev-session review · ⚑ Self-initiated · 📊 Model]]
