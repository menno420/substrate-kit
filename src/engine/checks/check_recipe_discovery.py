"""Recipe `applies-when:` DISCOVERY advisory — warn-only, NEVER exit-affecting.

Provenance: docs/planning/2026-07-19-night-run-idea-groom-wave2.md rank S17 (the
final rank; from the R11 pinned-feed / applies-when card). Sibling of
R5/R7/R11/S3/S4/S8 on the same advisory seam. This is the check the R11 recipe
DEFERRED: it only earns existence once >=2 recipes carry `applies-when:`
signatures (the recipe's own escalation rule — don't pre-build a discovery check
for a single instance). That threshold is now MET, so S17 ships it.

Why this exists — the DISCOVERY complement to R11 (well-formedness) and S8
(signature-honesty). R11 makes every `docs/recipes/` graduation carry a
machine-readable `applies-when:` structural signature (a comma-separated list of
`path:<glob>` / `content:<marker>` tokens describing the *shape a repo grows*
when the recipe applies). S8 keeps that signature honest against its own recipe
body. S17 turns the signature outward: for an ADOPTER tree that has grown the
shape a recipe describes, nudge toward the recipe. **Discovery, not
enforcement** — the point is to surface a portable pattern the adopter may not
know exists, never to fail a build.

Distinct from S8: S8 cross-checks a token against its OWN recipe's prose
(tokens-vs-body honesty); S17 matches a recipe's signature against the ADOPTER's
OWN tree (signature-vs-tree discovery).

What it does: for each recipe file under docs/recipes/ (excluding README.md)
carrying a well-formed `applies-when:` badge, every signature token is matched
against the adopter tree:

- `path:<glob>` — matches if some scanned file's repo-relative path (or its
  basename, for a slash-free glob) fnmatches the glob.
- `content:<marker>` — matches if some scanned file contains the marker
  substring (case-insensitively).

A recipe fires ONE discovery advisory only when its FULL signature matches
(every token present — the conjunction: the repo grew the whole shape), AND two
correctness guards both pass:

1. **Self-reference exclusion** — docs/recipes/ is excluded from the scan, so a
   recipe describing its own markers is never counted as adopter evidence (the
   tree-level analogue of S8's body-minus-badge guard). Without this every
   recipe would trivially match itself.
2. **Already-known suppression** — if the recipe is already referenced anywhere
   in the tree OUTSIDE docs/recipes/ (a doc links it, a session card cites it,
   a status line names it), the adopter already knows the recipe → no nudge.
   This is what makes it DISCOVERY, not nagging: it stays quiet on the authoring
   repo (whose recipes are referenced everywhere) and fires only on a fresh
   adopter that grew the shape but never heard of the recipe.

Search hygiene: kit machinery + VCS/build noise are excluded from BOTH the
signature scan and the reference scan (bootstrap.py, .substrate/, .git/,
__pycache__/, node_modules/, .venv/, venv/). Files larger than 512 KiB and
non-UTF-8 files are skipped (fail-open — a binary/huge file is never a verdict).

Posture — ADVISORY only, wired on the posture="advisory" seam in cli.py exactly
like check_recipe_applies_when / check_recipe_signature_honesty. NOT in
STRICT_SUBCHECKS — a discovery nudge is an invitation to read a recipe, not a
defect to fail an adopter on. Input-gated + fail-open: no docs/recipes/ dir
yields nothing. The badge grammar (`_RE_APPLIES_WHEN` + `_RE_TOKEN` +
`_HEADER_LINES` + `_RECIPES_RELDIR`) is imported from check_recipe_applies_when
as the SINGLE SOURCE OF TRUTH so the three recipe lints can never drift on what a
valid token is. Stdlib only.
"""

from __future__ import annotations

import fnmatch
import os
import re
from pathlib import Path

from engine.checks.check_docs import Finding

# Single source of truth for the badge grammar — reuse R11's regexes so the
# three recipe lints (well-formedness, honesty, discovery) can never disagree on
# what a valid `applies-when:` badge or token looks like. The dist flattens every
# engine module into one namespace and strips this intra-package import, so the
# names resolve there too (check_recipe_applies_when precedes this module in
# MODULE_ORDER).
from engine.checks.check_recipe_applies_when import (
    _HEADER_LINES,
    _RE_APPLIES_WHEN,
    _RE_TOKEN,
    _RECIPES_RELDIR,
)

# Named RECIPE_DISCOVERY_KIND (not a bare FINDING_KIND) — the dist concatenates
# every engine module into one namespace, so a second top-level FINDING_KIND
# would collide. The value is the finding kind (the `[<kind>]` tag `check`
# prints).
RECIPE_DISCOVERY_KIND = "recipe-discovery"

# Directories pruned from every walk: VCS/build noise + documented kit machinery
# (CLAUDE.md search hygiene). docs/recipes/ is pruned separately (self-reference).
_PRUNE_DIRS = frozenset(
    {".git", "__pycache__", "node_modules", ".venv", "venv", ".substrate"}
)
# A single file that is kit machinery (the generated single-file dist an adopter
# receives) — excluded by name wherever it sits.
_PRUNE_FILE = "bootstrap.py"

# Never read a file larger than this into memory for marker matching (fail-open).
_MAX_BYTES = 512 * 1024

# Wildcard characters that mark a glob as non-literal (for the basename heuristic).
_RE_GLOB_HAS_SLASH = re.compile(r"/")


def _iter_files(root: Path, *, skip_recipes: bool):
    """Yield (relative_path_str, absolute Path) for scannable files under root.

    Prunes VCS/build noise, the .substrate/ kit dir, and (when skip_recipes)
    the docs/recipes/ tree; skips the generated bootstrap.py by name."""
    recipes_abs = (root / _RECIPES_RELDIR).resolve()
    for dirpath, dirnames, filenames in os.walk(root):
        # prune noisy dirs in place so os.walk does not descend into them
        dirnames[:] = [d for d in dirnames if d not in _PRUNE_DIRS]
        if skip_recipes:
            here = Path(dirpath).resolve()
            if here == recipes_abs or recipes_abs in here.parents:
                dirnames[:] = []
                continue
        for name in filenames:
            if name == _PRUNE_FILE:
                continue
            abs_path = Path(dirpath) / name
            try:
                rel = abs_path.relative_to(root).as_posix()
            except ValueError:
                rel = name
            yield rel, abs_path


def _read_text_lc(path: Path) -> str | None:
    """Lower-cased file text, or None if too large / unreadable / non-UTF-8."""
    try:
        if path.stat().st_size > _MAX_BYTES:
            return None
        return path.read_text(encoding="utf-8").lower()
    except (OSError, UnicodeDecodeError, ValueError):
        return None


def _path_token_matches(glob: str, rel_paths: list[str]) -> bool:
    """True if `glob` fnmatches some repo-relative path (or basename for a
    slash-free glob)."""
    has_slash = _RE_GLOB_HAS_SLASH.search(glob) is not None
    for rel in rel_paths:
        if fnmatch.fnmatch(rel, glob):
            return True
        if not has_slash and fnmatch.fnmatch(rel.rsplit("/", 1)[-1], glob):
            return True
    return False


def _signature_matches(
    tokens: list[str], rel_paths: list[str], contents_lc: list[str]
) -> bool:
    """True only if EVERY well-formed token matches the tree (the conjunction:
    the repo grew the whole shape). A malformed token (R11's job) fails open —
    it is treated as satisfied so discovery never depends on a broken tag."""
    for token in tokens:
        if _RE_TOKEN.match(token) is None:
            continue  # malformed → R11 flags it; do not let it block discovery
        kind, _, value = token.partition(":")
        kind = kind.strip().lower()
        value = value.strip()
        if kind == "path":
            if not _path_token_matches(value, rel_paths):
                return False
        elif kind == "content":
            needle = value.lower()
            if not any(needle in body for body in contents_lc):
                return False
    return True


def _already_referenced(stem: str, rel_paths: list[str], contents_lc: list[str]) -> bool:
    """True if the recipe (by filename stem) is already named anywhere in the
    scanned (non-recipe) tree — a path mentioning it or a body citing it."""
    stem_lc = stem.lower()
    if any(stem_lc in rel.lower() for rel in rel_paths):
        return True
    return any(stem_lc in body for body in contents_lc)


def check_recipe_discovery(target, config=None) -> list[Finding]:
    """Advisory: an adopter tree whose shape matches a recipe's `applies-when:`
    signature — and which does not already reference the recipe — is nudged
    toward it.

    Advisory only — the caller wires this on posture="advisory" and never counts
    it toward the exit code. Input-gated + fail-open. config accepted for
    signature parity with the other advisory checks; unused today."""
    target = Path(target)
    recipes_dir = target / _RECIPES_RELDIR
    if not recipes_dir.is_dir():
        return []  # input-gated: no recipes shipped here

    # Scan the adopter tree ONCE (docs/recipes/ excluded — self-reference guard).
    rel_paths: list[str] = []
    contents_lc: list[str] = []
    for rel, abs_path in _iter_files(target, skip_recipes=True):
        rel_paths.append(rel)
        body = _read_text_lc(abs_path)
        if body is not None:
            contents_lc.append(body)

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
            continue  # no badge → R11's well-formedness job, not discovery's
        tokens = [t.strip() for t in match.group(1).split(",") if t.strip()]
        if not tokens:
            continue  # empty badge → R11's job

        if not _signature_matches(tokens, rel_paths, contents_lc):
            continue  # tree has not grown this recipe's full shape
        if _already_referenced(path.stem, rel_paths, contents_lc):
            continue  # adopter already knows this recipe → discovery, not nagging

        findings.append(
            Finding(
                rel,
                RECIPE_DISCOVERY_KIND,
                "this tree matches the recipe's `applies-when:` signature "
                f"(`{match.group(1)}`) but never references the recipe — you may "
                f"have grown the shape it describes. Read `{rel}` and copy the "
                "pattern if it fits (discovery, not enforcement — this never "
                "affects the exit code).",
            ),
        )
    return findings
