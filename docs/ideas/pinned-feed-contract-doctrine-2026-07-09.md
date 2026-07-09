---
state: captured
origin: consumer:menno420/superbot
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Pinned feed contract — doctrine for cross-repo committed-artifact seams (2026-07-09)

> **Status:** `ideas`
>
> **State:** captured (consumer-proven pattern, superbot PR #1884 + websites
> PR #11, 2026-07-09). **Origin:** consumer — the pattern was built and proven
> estate-side first; this capture is the promotion path into kit doctrine.

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

## Lands with

A groomed-ideas increment (post-#17), or the first kit-lab consumer that
grows a committed-artifact feed of its own.
