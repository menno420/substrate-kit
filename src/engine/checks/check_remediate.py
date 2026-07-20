"""`check --remediate <finding-kind>` — paste-ready remediation lookup.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md S7 (this PR).
Sibling of R6's `check --explain-wall` lookup (check_no_false_walls.explain_wall):
a PRINT-ONLY CLI convenience, never a gate.

Why this exists: when `check` surfaces an advisory (or a red gate) it names the
finding kind — `folded-gate-mtime-picker`, `recipe-applies-when`, `stale-wall`,
`wall-ledger-disagree`, `baton-unresolved`, `ungroomed-ideas` — and its message
describes the fix in prose. A host then has to re-derive the exact paste-ready
form from that prose. This lookup hands back the ready-to-apply remediation block
for a named kind directly, so the "what do I actually paste/edit to clear this?"
step is one command instead of a re-read.

What it is NOT: it does not scan the tree, produce findings, modify any file, or
affect an exit code. It is a static registry lookup — `remediate(kind)` returns
the block string or ``None`` — wired into the CLI on the same pre-check dispatch
seam as `--explain-wall` (`_cmd_remediate` always returns 0). This keeps S7
contained and reversible by construction: there is no file-rewriting path, so
there is nothing to make opt-in beyond the explicit `--remediate <kind>` flag it
already is.

Scope of the seeded registry: exactly the finding kinds whose fix has a concrete,
paste-ready form documented at its own source of truth. `folded-gate-mtime-picker`
reuses ``check_folded_gate.REMEDIATION_SNIPPET`` verbatim (single source of truth —
imported, not copied). The rest are derived from each checker's own Finding
message. An unknown/absent kind is not an error — the command lists the covered
kinds and exits 0, so a host discovers the vocabulary without guessing.

Stdlib only; never raises on a lookup.
"""

from __future__ import annotations

# Un-aliased on purpose: the dist concatenates every engine module into one flat
# namespace and STRIPS these intra-package imports, so `check_remediate` must
# reference `FINDING_KIND` / `REMEDIATION_SNIPPET` by the exact names
# `check_folded_gate` defines them (both are unique top-level symbols — every
# other checker names its kind `<X>_KIND` precisely to avoid a `FINDING_KIND`
# collision, so these two resolve unambiguously to the folded-gate module).
# An aliased import here breaks the dist (NameError) and trips
# test_no_aliased_intra_package_imports_in_engine.
from engine.checks.check_folded_gate import FINDING_KIND, REMEDIATION_SNIPPET

# ── the paste-ready blocks ────────────────────────────────────────────────
# Each value is the remediation a host applies to clear the keyed finding kind.
# Derived from each checker's own Finding message (its source-of-truth fix) so a
# correction shipped here can never drift from the finding that points at it —
# the folded-gate block is IMPORTED from the checker, not duplicated.

_RECIPE_APPLIES_WHEN = """\
Add a well-formed `applies-when:` badge to the recipe header (first lines),
so a future discovery check can match an adopter's seam to this recipe:

    > **applies-when:** `path:<glob>, content:<marker>`

Each token is `path:<glob>` (a repo-relative file glob) or `content:<marker>`
(a literal string that must appear in a matched file), comma-separated. Example:

    > **applies-when:** `path:.github/workflows/*.yml, content:--require-session-log`
"""

_STALE_WALL = """\
Re-verify the wall today, then refresh its date in docs/CAPABILITIES.md by
appending a dated row to the `## Append log` section (do NOT silently bump the
old date — append the fresh evidence):

    - YYYY-MM-DD · wall · <venue> · <finding> · <evidence> · <workaround>

If the re-attempt SUCCEEDS, the wall was transient — correct or delete the wall
row instead (a false wall is not a standing limit). If it still refuses, the
fresh dated row clears the staleness window.
"""

_DATELESS_WALL = """\
This `wall` row in docs/CAPABILITIES.md carries no parseable date, so the
staleness re-verify rule (check_stale_walls) can never fire on it — it hardens
into an un-auditable claim. Stamp it with a date so the cadence can catch it:

- A `## Walls` seed row → append a trailing verification stamp:

      - **<wall title>**: <finding> → <workaround>. — LAST-VERIFIED: YYYY-MM-DD

- A `## Append log` wall row → give it the leading log date the format requires:

      - YYYY-MM-DD · wall · <finding> · <evidence> · <workaround>

Use today's date only if you re-verified the wall today; otherwise use the date
it was actually last confirmed. Once dated, check_stale_walls owns its re-verify
cadence (default 14 days).
"""

_WALL_LEDGER_DISAGREE = """\
The `## Walls` correction row and the newest `## Append log` entry for this
capability disagree. Reconcile them in docs/CAPABILITIES.md so both state the
SAME current verdict:

1. Decide the true current status by re-attempting the capability once.
2. Update the `## Walls` correction row to that verdict.
3. Append a dated `## Append log` row recording the re-attempt + its result:

       - YYYY-MM-DD · <capability> · <verdict> · <evidence>

The append log is the running record; the Walls row is the current summary —
after reconciliation the newest append-log entry and the Walls row must agree.
"""

_BATON_UNRESOLVED = """\
The `## Next-2 baton` in control/status*.md cites a repo-relative path (or
`path#anchor`) that no longer resolves. Update the baton token to a path/anchor
that exists on disk:

1. Find the current home of the work (it was likely renamed/moved/merged):
       git log --diff-filter=D --name-only -- '<old-path>'   # if deleted
2. Edit the `## Next-2 baton` code span to the real current path (and, for an
   `#anchor`, a heading that exists in that file).
3. If the pointed-at work is DONE, retarget the baton at the next real slice
   instead of leaving a dead pointer.
"""

_UNGROOMED_IDEAS = """\
There are `💡` session-idea lines on cards newer than the newest groom doc —
so a "backlog dry" claim would be false. Run a groom pass before claiming the
ladder is exhausted:

1. Collect the ungroomed `💡` lines (cards under .sessions/ newer than the
   newest docs/planning/*groom*.md) plus any docs/ideas/ intake.
2. Dedup, classify (buildable-now / needs-planning / owner-gated), and rank the
   buildable-now slices into a NEW docs/planning/<date>-*groom*.md doc.
3. Retarget the `## Next-2 baton` at the top-ranked new slice.

The `/groom-ideas` skill drives this end-to-end.
"""

# Registry: finding kind -> paste-ready remediation block. Keyed by the EXACT
# `Finding.kind` string each checker emits, so `check --remediate <kind>` takes
# the same token the check output prints in `[<kind>]`.
REMEDIATIONS: dict[str, str] = {
    FINDING_KIND: REMEDIATION_SNIPPET,
    "recipe-applies-when": _RECIPE_APPLIES_WHEN,
    "stale-wall": _STALE_WALL,
    "dateless-wall": _DATELESS_WALL,
    "wall-ledger-disagree": _WALL_LEDGER_DISAGREE,
    "baton-unresolved": _BATON_UNRESOLVED,
    "ungroomed-ideas": _UNGROOMED_IDEAS,
}


def available_remediation_kinds() -> tuple[str, ...]:
    """The finding kinds that carry a paste-ready remediation block, sorted."""
    return tuple(sorted(REMEDIATIONS))


def remediate(kind: str) -> str | None:
    """Return the paste-ready remediation block for finding ``kind``, or ``None``
    when no remediation is registered for it. A pure lookup — never raises, never
    touches the filesystem."""
    if not isinstance(kind, str):
        return None
    return REMEDIATIONS.get(kind.strip())
