"""Recipe `applies-when:` tag presence advisory — warn-only, NEVER exit-affecting.

Provenance: docs/planning/2026-07-19-night-run-idea-groom.md R11 (from the
pinned-feed-contract card). Sibling of R5/R7 on the same advisory seam.

Why this exists: a graduated recipe under docs/recipes/ is a portable pattern an
adopter copies when its repo grows the shape the recipe describes. R11 gives each
graduation a machine-readable `applies-when:` structural signature so a FUTURE
discovery check can nudge an adopter that has grown a matching seam toward the
relevant recipe. That future nudge only earns existence once >=2 recipes carry
signatures (the recipe's own escalation rule); R11 ships only the tag + this
well-formedness readout so every graduation carries a usable signature from the
start. Discovery, not enforcement — advisory only.

What it does: for each recipe file under docs/recipes/ (excluding README.md),
require a well-formed `> **applies-when:** \`<signature>\`` badge in the doc's
header (first 12 lines). The signature is a comma-separated list of tokens, each
`path:<glob>` (a file-path glob a future check greps an adopter tree for) or
`content:<marker>` (a content substring marker). A recipe with no badge, an
empty signature, or a token that is neither `path:`/`content:` gets ONE advisory.

Carried as a blockquote badge line (mirroring the existing `> **Status:**`
badge), NOT a top-of-file `--- ... ---` YAML block: the kit engine is
deliberately PyYAML-free and has no frontmatter parser, so the badge-line form
reuses the proven Status-badge regex style with zero new parsing machinery
(decide-and-flag, R11).

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_wall_ledger_agreement / check_folded_gate. NOT in STRICT_SUBCHECKS —
a missing tag is a nudge to add one, not a defect to fail an adopter on.
Input-gated + fail-open: no docs/recipes/ dir, or an unreadable file, yields
nothing. Stdlib only.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

_RECIPES_RELDIR = "docs/recipes"

# The badge line: `> **applies-when:** \`<signature>\``. Group 1 = the raw
# signature inside the backticks.
_RE_APPLIES_WHEN = re.compile(r"\*\*applies-when:\*\*\s*`([^`]*)`", re.IGNORECASE)

# A well-formed signature token: `path:<glob>` or `content:<marker>`.
_RE_TOKEN = re.compile(r"^(?:path|content):\S.*$", re.IGNORECASE)

# Header window to scan for the badge, mirroring the docs-gate 12-line window.
_HEADER_LINES = 12

# Named RECIPE_APPLIES_WHEN_KIND (not FINDING_KIND) — the dist concatenates every
# engine module into one namespace, so a second top-level FINDING_KIND would
# collide. The value is the finding kind.
RECIPE_APPLIES_WHEN_KIND = "recipe-applies-when"


def check_recipe_applies_when(target: Path, config=None) -> list[Finding]:
    """Advisory: every docs/recipes/ graduation (except README.md) carries a
    well-formed `applies-when:` structural-signature badge.

    Advisory only — the caller wires this on posture="advisory" and never counts
    it toward the exit code. Input-gated + fail-open. config accepted for
    signature parity with the other advisory checks; unused today."""
    recipes_dir = target / _RECIPES_RELDIR
    if not recipes_dir.is_dir():
        return []  # input-gated: no recipes shipped here

    findings: list[Finding] = []
    for path in sorted(recipes_dir.glob("*.md")):
        if path.name.lower() == "readme.md":
            continue
        rel = f"{_RECIPES_RELDIR}/{path.name}"
        try:
            header = "\n".join(
                path.read_text(encoding="utf-8").splitlines()[:_HEADER_LINES]
            )
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable recipe is not a verdict

        match = _RE_APPLIES_WHEN.search(header)
        if match is None:
            findings.append(
                Finding(
                    rel,
                    RECIPE_APPLIES_WHEN_KIND,
                    "recipe graduation is missing an `applies-when:` badge in its "
                    f"header (first {_HEADER_LINES} lines) — add "
                    "`> **applies-when:** \`<signature>\`` (a comma-separated list "
                    "of `path:<glob>` / `content:<marker>` tokens) so a future "
                    "discovery check can match an adopter's seam to this recipe.",
                ),
            )
            continue

        tokens = [t.strip() for t in match.group(1).split(",") if t.strip()]
        if not tokens:
            findings.append(
                Finding(
                    rel,
                    RECIPE_APPLIES_WHEN_KIND,
                    "recipe `applies-when:` badge is empty — give it at least one "
                    "`path:<glob>` or `content:<marker>` signature token.",
                ),
            )
            continue

        bad = [t for t in tokens if _RE_TOKEN.match(t) is None]
        if bad:
            findings.append(
                Finding(
                    rel,
                    RECIPE_APPLIES_WHEN_KIND,
                    f"recipe `applies-when:` has malformed token(s) {bad} — each "
                    "token must be `path:<glob>` or `content:<marker>`.",
                ),
            )
    return findings
