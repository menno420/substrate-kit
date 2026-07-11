---
state: promoted
origin: consumer:menno420/websites
shipped_pr: 187
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-11
outcome: shipped
---

# `_MODEL_DOCTRINE_PHRASE` exact-substring match is emphasis-blind (2026-07-11)

> **Status:** `ideas`
>
> **State:** captured. **Origin:** consumer — websites, live-verified during
> the v1.10.0 distribution wave. **Priority: minor** (harmless noise,
> idempotent afterwards).

## The finding (websites #105)

The retroactive model-doctrine append (kit #176, `_merge_model_doctrine`)
detects an already-present doctrine by exact-substring match on
`_MODEL_DOCTRINE_PHRASE` ("family-level model name your own
harness/environment reports"). websites' hand-merged copy (their #101)
carried Markdown emphasis INSIDE the phrase — "…model name **your own
harness/environment reports this session**" — so the match missed it and
the upgrade appended a near-duplicate doctrine paragraph to
`.sessions/README.md`.

Harmless (append-only, provenance-marked, host bytes preserved) and
idempotent going forward — the appended copy carries the bare phrase — but
it is noise on every adopter that hand-merged the doctrine
pre-retroactively with any emphasis/rewording inside the phrase.

## Proposed fix direction

Make the detection emphasis-insensitive: strip `*`/`_`/backticks (or
regex with optional emphasis runs between tokens) before the substring
test. One normalizer + one regression fixture (emphasis-wrapped phrase →
no append). Quick-win lane; engine change → dist byte-pin.
