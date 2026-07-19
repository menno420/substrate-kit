# Pinned feed contract — cross-repo committed-artifact seams

> **Status:** `reference`
>
> A recipe: the proven discipline for a **committed artifact one repo generates
> and another repo consumes over a raw URL**. Graduated from the estate pattern
> shipped 2026-07-09 (superbot PR #1884 producer + websites PR #11 consumer).
> **NOT SOURCE OF TRUTH** for any adopter's code — it is the pattern to copy,
> not a contract to import.

## When this applies

You have this seam the moment **repo A commits a generated artifact**
(`console.json`, `site.json`, `dashboard.json`, …) and **repo B reads it over a
raw URL** (`raw.githubusercontent.com/…`). The two repos share an *implicit*
schema — no shared CI, no shared types — so a producer-side family or field
rename silently blanks or corrupts the consumer page. That is the feed-desync
bug class (superbot's BUG-0022): tests stay green on both sides while the live
page renders empty or wrong, because each side encodes its own copy of the
shape and they drift apart unseen.

The fix is to make the shape **explicit, versioned, and checked on both sides**.

## The contract, in three parts

**1 · The producer commits a versioned contract file next to the artifact.**
A small JSON file (`<feed>_data_contract.json`) that declares `version`, the
top-level families, and the guaranteed fields per record. Editing it and
bumping `version` is the *explicit, reviewable act* of changing the shape — the
one place a family or field may be added, renamed, or removed.

**2 · The producer stamps the version into the artifact and enforces
fail-closed parity in CI.** Every emitted feed carries `meta.schema_version`
equal to the contract's `version`. A CI check (a test, so it gates merges)
asserts, all fail-closed:

- **producer constants ⇄ contract parity** — the exporter's own field/family
  constants equal the contract's, as sets;
- **family whitelist, both directions** — an extra family is a leak; a
  *missing* family is a blanked consumer (the desync direction that matters);
- **per-record field whitelists** — an extra field fails; for record types the
  consumer iterates, a missing field fails too;
- **a missing or unparseable contract file is itself an error** — the contract
  is load-bearing, never optional.

**3 · The consumer pins the contract copy it was built against and verifies at
render time.** The consumer commits a byte-copy of the contract whose `_comment`
names the canonical producer URL and the upgrade ritual. At render time it runs
two cheap checks and surfaces drift as an **honest banner where the owner looks
— never faked data**:

- **version match** — `feed.meta.schema_version == pinned.version`;
- **contracted families present** — every `top_level` family exists in the feed.

A mismatch renders a visible "the upstream shape may have changed; parts of this
page may be empty — nothing below is faked" banner instead of a silently wrong
page. Field-level checks stay producer-side (where the constants live); the
consumer runs only the two cheap visible checks.

## Contract-file skeleton (copy-paste)

```json
{
  "_comment": "Shape contract for the committed feed `<path/to/feed.json>` — the single source of truth for its cross-repo consumers. Producer and CI checker both validate against this file, so a producer-side family/field rename fails CI here instead of silently blanking a consumer page. Keys list the GUARANTEED fields per record (values may be null); a field or family may only be added/renamed/removed by editing THIS file and bumping `version` (the feed carries the version as meta.schema_version). Consumers pin a copy of this file and verify meta.schema_version against it at render time.",
  "version": 1,
  "top_level": ["meta", "..."],
  "meta": ["generated_at", "schema_version"],
  "<record_family>": ["<guaranteed_field>", "..."]
}
```

The consumer's pinned copy is identical except its `_comment` names the
canonical producer URL and says: *to upgrade, sync this copy from the canonical
file and adapt the templates in the same commit.*

## Estate reference (the proof)

Shipped end-to-end 2026-07-09 for superbot's `console.json` feed:

- **Producer** — [superbot PR #1884](https://github.com/menno420/superbot/pull/1884):
  `botsite/data/console_data_contract.json` (the versioned file),
  `scripts/export_dashboard_data.py` (`meta.schema_version` stamp),
  `scripts/check_dashboard_data.py::check_console_subset` (fail-closed parity,
  CI-enforced via `tests/unit/scripts/`).
- **Consumer** — [websites PR #11](https://github.com/menno420/websites/pull/11):
  `dashboard/console_data_contract.json` (pinned copy),
  `dashboard/data_source.py::console_contract_issue` (the two render-time
  checks), the honest drift banner in `dashboard/templates/console.html`.

Why it earned graduation: the *first* consumer-side pass against the real
contract caught a live defect — `ideas`/`bugs` ship as counter dicts, the page
rendered them as lists, and both test fixtures had encoded the same wrong shape,
so tests were green while the page was wrong. The contract is what made the
drift visible.

## Scope — doctrine first, scaffolding only if it repeats

Ship the **discipline** (this recipe + the CONSTITUTION rider) first. Do **not**
pre-build the heavier machinery — a planted template contract file, a
parity-test scaffold, or an engine check that a declared feed names its contract
— until instances actually repeat across adopters. The pattern is cheap to apply
by hand from this skeleton; premature scaffolding is speculative weight.
