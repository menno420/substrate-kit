"""Recipe `applies-when:` signature-HONESTY advisory — warn-only, NEVER exit-affecting.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md rank S8 (from
the R11 pinned-feed / applies-when card). Sibling of R5/R7/R11/S3/S4 on the same
advisory seam.

Why this exists — the complement to R11's WELL-FORMEDNESS lint. R11
(`check_recipe_applies_when`) gives every `docs/recipes/` graduation a
`> **applies-when:** <signature>` badge and warns when the badge is
*missing, empty, or malformed*. But a badge can be perfectly well-formed and
still be DISHONEST: it can name a `content:<marker>` the recipe body never
mentions, or a `path:<glob>` whose literal skeleton the recipe never describes —
the classic drift where a marker is renamed in the recipe prose but the badge
still cites the old token. A future discovery check (S17) will grep an adopter
tree for these tokens to nudge toward the matching recipe; a token that does not
even appear in its OWN recipe's body is a false lead. S8 catches that drift:
cross-check every token against the recipe body, advisory-only.

What it does: for each recipe file under docs/recipes/ (excluding README.md)
that carries a well-formed `applies-when:` badge, each signature token is
cross-checked against the recipe body (the whole file MINUS the badge line
itself, so a token can never satisfy honesty via its own declaration):

- `content:<marker>` — the marker substring must appear (case-insensitively)
  somewhere in the body. If it does not, the token names a signal the recipe
  never documents → ONE advisory.
- `path:<glob>` — the glob's literal (non-wildcard) fragments must each appear
  in the body. A glob like `*.json` requires `.json` in the body;
  `src/engine/checks/*.py` requires both `src/engine/checks/` and `.py`. A pure-
  wildcard glob (`*`) has no literal skeleton to trace → honest by default
  (fail-open). If any literal fragment is absent → ONE advisory.

Only WELL-FORMED tokens are honesty-checked. A missing/empty badge or a
malformed token is R11's job — S8 fails open on those (no double-noise). The
badge grammar (`_RE_APPLIES_WHEN` + `_RE_TOKEN` + `_HEADER_LINES`) is imported
from `check_recipe_applies_when` as the SINGLE SOURCE OF TRUTH so the two lints
can never drift on what a valid token is.

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_recipe_applies_when / check_wall_ledger_agreement. NOT in
STRICT_SUBCHECKS — a drifted signature is a nudge to reconcile, not a defect to
fail an adopter on. Input-gated + fail-open: no docs/recipes/ dir, or an
unreadable file, yields nothing. Stdlib only.
"""

from __future__ import annotations

import re

from engine.checks.check_docs import Finding

# Single source of truth for the badge grammar — reuse R11's regexes so the
# well-formedness lint and this honesty lint can never disagree on what a valid
# `applies-when:` badge or token looks like. The dist flattens every engine
# module into one namespace and strips this intra-package import, so the names
# resolve there too (check_recipe_applies_when precedes this module in
# MODULE_ORDER).
from engine.checks.check_recipe_applies_when import (
    _HEADER_LINES,
    _RE_APPLIES_WHEN,
    _RE_TOKEN,
    _RECIPES_RELDIR,
)

# Named RECIPE_SIGNATURE_HONESTY_KIND (not a bare FINDING_KIND) — the dist
# concatenates every engine module into one namespace, so a second top-level
# FINDING_KIND would collide. The value is the finding kind (the `[<kind>]` tag
# `check` prints).
RECIPE_SIGNATURE_HONESTY_KIND = "recipe-signature-drift"

# Wildcard characters that split a `path:` glob into its literal skeleton.
_RE_GLOB_WILDCARD = re.compile(r"[*?\[\]]")


def _literal_fragments(glob: str) -> list[str]:
    """The non-wildcard literal fragments of a path glob.

    `*.json` -> ['.json']; `src/checks/*.py` -> ['src/checks/', '.py'];
    `*` -> [] (pure wildcard — nothing to trace, honest by default)."""
    return [frag for frag in _RE_GLOB_WILDCARD.split(glob) if frag]


def check_recipe_signature_honesty(target, config=None) -> list[Finding]:
    """Advisory: every well-formed `applies-when:` token is honest to the recipe
    body — its content marker / path-glob skeleton actually appears in the prose.

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
            lines = path.read_text(encoding="utf-8").splitlines()
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable recipe is not a verdict

        header = "\n".join(lines[:_HEADER_LINES])
        match = _RE_APPLIES_WHEN.search(header)
        if match is None:
            continue  # no badge → R11's well-formedness job, not honesty's

        tokens = [t.strip() for t in match.group(1).split(",") if t.strip()]
        if not tokens:
            continue  # empty badge → R11's job

        # Body = the whole file MINUS every line carrying the badge, so a token
        # can never satisfy honesty via its own `applies-when:` declaration.
        body_lc = "\n".join(
            ln for ln in lines if _RE_APPLIES_WHEN.search(ln) is None
        ).lower()

        for token in tokens:
            if _RE_TOKEN.match(token) is None:
                continue  # malformed → R11 flags it; honesty fails open
            kind, _, value = token.partition(":")
            kind = kind.strip().lower()
            value = value.strip()
            if kind == "content":
                if value.lower() not in body_lc:
                    findings.append(
                        Finding(
                            rel,
                            RECIPE_SIGNATURE_HONESTY_KIND,
                            f"`applies-when:` content token `{token}` names a "
                            "marker the recipe body never mentions — the "
                            "signature has drifted from the prose. Reconcile "
                            "them: fix the token, or describe the marker in the "
                            "recipe body (a future discovery check greps this "
                            "token in adopter trees, so it must be real).",
                        ),
                    )
            elif kind == "path":
                missing = [f for f in _literal_fragments(value) if f.lower() not in body_lc]
                if missing:
                    findings.append(
                        Finding(
                            rel,
                            RECIPE_SIGNATURE_HONESTY_KIND,
                            f"`applies-when:` path token `{token}` names path "
                            f"fragment(s) {missing} the recipe body never "
                            "mentions — the signature has drifted from the "
                            "prose. Reconcile them: fix the glob, or reference a "
                            "matching path in the recipe body.",
                        ),
                    )
    return findings
