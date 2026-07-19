---
state: promoted
origin: consumer:menno420/superbot
shipped_pr: 482
shipped_repo: menno420/substrate-kit
merged_date: 2026-07-19
outcome: shipped
---

# Pinned feed contract — doctrine for cross-repo committed-artifact seams (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured → promoted → shipped (kit PR #482, 2026-07-19 — the
> doctrine note landed as `docs/recipes/pinned-feed-contract.md` + a
> CONSTITUTION rider). **Origin:** consumer — the pattern was built and proven
> estate-side first (superbot PR #1884 + websites PR #11, 2026-07-09); this
> capture is the promotion path into kit doctrine.

## The seam class

A recurring estate shape the kit has no doctrine for: **repo A commits a
generated artifact** (superbot's `console.json`, `site.json`,
`dashboard.json`) and **repo B consumes it over a raw URL**
(websites' dashboard/botsite fetch raw.githubusercontent.com). The two repos
share an *implicit* schema — no shared CI, no shared types — so a
producer-side family/field rename silently blanks or corrupts the consumer
page (superbot's BUG-0022 desync class). As the estate multiplies repos
(kit-lab, superbot-next, trading), this seam multiplies with it.

## The proven pattern (one estate instance, end-to-end)

Shipped 2026-07-09 for the `console.json` seam:

1. **Producer commits a versioned contract file** next to the artifact
   (`botsite/data/console_data_contract.json`: `version` + top-level families
   + guaranteed fields per record). Editing it + bumping `version` is the
   explicit, reviewable act of changing the contract.
2. **Producer stamps the version into the artifact** (`meta.schema_version`)
   and enforces fail-closed in its CI: producer-constants⇄contract parity,
   family whitelist *both directions* (extra = leak, missing = blanked
   consumer), per-record field whitelists (superbot
   `check_dashboard_data.check_console_subset`, CI via tests).
3. **Consumer pins the contract copy it was built against** and runs the two
   cheap render-time checks — version match + contracted families present —
   surfacing drift as an honest banner where the owner looks (websites
   `data_source.console_contract_issue`; never-fake-data posture).

Evidence it earns doctrine: the *first* consumer-side pass against the real
contract caught a live defect (ideas/bugs consumed as lists, feed ships
counter dicts — stat tiles rendered dict-key counts; its test fixture encoded
the same wrong shape, so tests were green while the page was wrong).

## What the kit could ship (when groomed forward)

Smallest useful form first — a **doctrine note** (CONSTITUTION/COLLABORATION
template rider or a `docs/` recipe): "a committed artifact consumed by
another repo carries a committed, versioned shape contract; producer enforces
fail-closed in CI; consumer pins the version and verifies at render time."
Later, if instances repeat: a template contract file + parity-test scaffold
in the planted docs, and/or an engine check that a declared cross-repo feed
names its contract. Not built in the capture session by design.

## Shipped

kit PR #482 (2026-07-19) graduated the smallest useful form: the recipe
`docs/recipes/pinned-feed-contract.md` (full pattern + copy-paste contract
skeleton + estate proof + escalation boundary), its `docs/recipes/README.md`
index, and a one-bullet `CONSTITUTION.md.tmpl` rider ("Cross-repo feeds carry
a pinned contract") so every adopter's rendered constitution points at it. The
heavier escalation (planted template contract file, parity-test scaffold, an
engine check that a declared feed names its contract) is deliberately **not**
built — doctrine first, scaffolding only if instances actually repeat across
adopters. Ships to adopters via the next kit release.

## Lands with

Shipped as a groomed-ideas increment (kit PR #482). A future kit-lab consumer
that grows a committed-artifact feed of its own is the natural first proving
ground for the recipe.
