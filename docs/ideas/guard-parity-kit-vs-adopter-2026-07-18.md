---
state: captured
origin: lab
shipped_pr: null
shipped_repo: null
merged_date: null
outcome: open
---

# Guard-parity meta-test: kit-vs-adopter guard drift detector (2026-07-18)

> **Status:** `ideas`

**One line:** add a kit test (or a kit-quality lint step) that asserts every
*enforcing* guard step in `.github/workflows/ci.yml`'s `kit-quality` job has a
mirrored counterpart in `src/engine/adopt.py` `live_ci_workflow()` — or an
explicit allowlist entry marking it kit-only-by-design — so the kit's own CI
and the generated adopter CI can never silently diverge.

**Why:** this very session (PR #457) existed only because the claims-only
fast-lane guard shipped to the kit's own CI in PR #455 but *not* to the
generated adopter CI, and nothing detected that drift until a human queued it
as a baton item. The two guard surfaces — kit-own `ci.yml` and
adopter-generated `live_ci_workflow()` — carry overlapping-by-design guard
stacks (inbox append-only gate, born-red session gate, claims-only fast-lane
guard), but agreement between them is maintained by hand. A parity check would
catch kit-vs-adopter guard drift automatically, turning a "notice it later,
queue it as a baton" loop into a red CI signal the same PR that introduces the
gap.

**Shape:** small, test-only, reversible. Enumerate the enforcing guard steps in
each surface by a stable marker (step name / `::error::` token), diff the two
sets, and fail when a kit-quality guard has no adopter mirror and no
`kit-only-by-design` allowlist entry (and vice-versa). Complements — does not
duplicate — the added-card-vs-modified-card lane-parity meta-test in
`docs/planning/2026-07-16-overnight-veto-menu.md` (that asserts two *lanes* of
one surface share a helper; this asserts two *surfaces* share a guard set).

**Size:** small (one checker/test + an allowlist constant).
