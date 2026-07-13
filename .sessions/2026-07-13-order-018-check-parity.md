# Session · 2026-07-13 · ORDER 018 — check --strict runs the CI substrate-gate preflight legs locally

> **Status:** `in-progress`

Intent: make repo-local `python3 bootstrap.py check --strict` run the same legs as the CI substrate-gate — a merge-base-aware inbox append-only leg (base blob derived from `origin/main` when present, self-skip otherwise) and a config-driven local preflight-scripts leg (`preflight_scripts`, default `scripts/preflight.py`, self-skip with a NOTE when absent) — so a tree failing either CI leg also fails plain local `check --strict` (ORDER 018 / idea-engine ASK 002).
