# Claim — claude/model-line-family-level

- `claude/model-line-family-level` · **Model-line family-level naming fix** — the planted `.sessions/README.md` model doctrine bans only "full dated" model IDs, so exact-but-undated model-ID tokens slip through (the websites #178 cleanup class); widen the ban to ANY exact model ID, align the telemetry Model-line advisory, tests, CHANGELOG, dist rebuild · expected files: `src/engine/adopt.py`, `src/engine/loop/telemetry.py`, `.sessions/README.md`, `tests/test_adopt.py`, `tests/test_telemetry.py`, `CHANGELOG.md`, `dist/bootstrap.py` · 2026-07-12
