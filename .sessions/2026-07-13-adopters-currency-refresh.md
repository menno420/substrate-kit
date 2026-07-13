# 2026-07-13 — adopters registry currency refresh

> **Status:** `in-progress`

Intent: re-verify docs/adopters.md against actual adopter trees (registry
generated 2026-07-12T18:31:47Z is stale — dry-run at HEAD 96bece9 shows
superbot-next / websites / trading-strategy / venture-lab have reconciled
their DRIFT rows since) and regenerate it via the kit's own tooling
(`python3 dist/bootstrap.py currency`), never by hand.
