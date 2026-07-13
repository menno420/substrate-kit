"""Auto-merge-enabler branch-allowlist preflight — the offline-verifiable half
of the enabler install-time preflight (docs/ideas/enabler-install-preflight-
2026-07-13.md).

Why + provenance: the auto-merge enabler installs cleanly into repos where it
cannot function, and the INERT state stays silent until the first parked PR.
Three seats hit it on the 2026-07-12→13 night run
(docs/reports/2026-07-13-night-run-adopter-outcomes.md §a): idle's enabler sat
INERT on zero required contexts, gba-homebrew #76 merged with the enabler
inert, and idea-engine had to hand-patch the workflow to add `claude/` to its
branch allowlist (PR #272) — its outbox flagging that a kit upgrade would
clobber the local fix.

What it flags (**advisory** — a nudge, never a locked door, the same posture
as the setup-script / seat-digest / adopters-staleness warnings):

- ``automerge-branch-drift`` — the installed
  ``.github/workflows/auto-merge-enabler.yml``'s parsed branch terms differ
  from what ``substrate.config.json`` → ``automerge.branch_patterns`` would
  regenerate. This is the idea-engine class: a hand-edited workflow (clobbered
  on the next upgrade) or a stale pre-``claim/*`` copy whose allowlist no
  longer covers the branches sessions push, so the enabler never arms those
  PRs. The fix is to put the branch list in config (where regeneration
  preserves it) and regenerate — hand edits to the kit-owned workflow are
  overwritten on ``upgrade``.

Scope — **branch half only**. The other install-time precondition (the base
branch actually REQUIRING a status-check context) cannot be verified here: the
engine is stdlib-only and offline (no rules API). That half stays owner-UI —
it is surfaced by the enabler's own PR-time ``::warning::`` (the refuse-to-arm
guard counts required contexts and refuses on zero) and by the adopt
repo-settings checklist. Naming the split here keeps the omission explicit.

Posture is **advisory-only, never exit-affecting**, and input-gated on the
enabler workflow existing (adopt plants it; a repo without it gets no nag).
The comparison is on the BRANCH EXPRESSION only, not the whole file: the
branch expr is derived purely from config, so it is stable across kit-version
bumps — a whole-file byte-compare would nag the whole fleet during version
skew (and that scan already lives in the adopt/upgrade carve-out report). Pure
stdlib, no ``subprocess`` (§3.2); unreadable files fail open (no verdict).
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.adopt import (
    AUTOMERGE_ENABLER_RELPATH,
    _automerge_branch_expr,
    _automerge_params,
)
from engine.checks.check_docs import Finding
from engine.lib.config import Config

# The two head_ref-keyed term shapes the enabler's branch expr is built from
# (adopt._automerge_branch_expr): a trailing-`*` config pattern renders as a
# prefix `startsWith`, anything else as an exact `==`. Scanning for these two
# forms yields exactly the branch terms — the repo guard keys off
# `head.repo.full_name`, the draft guard off `.draft`, the label guard off
# `labels.*.name`, none of which mention `head_ref`.
_STARTSWITH_RE = re.compile(r"startsWith\(\s*github\.head_ref\s*,\s*'([^']*)'\s*\)")
_EXACT_RE = re.compile(r"github\.head_ref\s*==\s*'([^']*)'")


def _branch_terms(expr: str) -> set[tuple[str, str]]:
    """Return the normalized set of branch terms in a workflow expression.

    Each term is ``("prefix", value)`` (a ``startsWith`` prefix match) or
    ``("exact", value)`` (a ``==`` head-ref match). A set on purpose — the
    enabler arms on the OR of its terms, so ordering and duplication carry no
    meaning; two expressions with the same term set arm identically.
    """
    terms: set[tuple[str, str]] = set()
    for value in _STARTSWITH_RE.findall(expr):
        terms.add(("prefix", value))
    for value in _EXACT_RE.findall(expr):
        terms.add(("exact", value))
    return terms


def check_automerge_preflight(target: Path, config: Config) -> list[Finding]:
    """Return advisory findings for auto-merge-enabler branch-allowlist drift.

    Engages only when the enabler workflow exists (adopt plants it; absence is
    not a finding). Advisory by contract — callers must never count these
    toward an exit code. Fail-open on unreadable files.
    """
    path = target / AUTOMERGE_ENABLER_RELPATH
    if not path.is_file():
        return []
    try:
        live_text = path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return []  # fail open — an unreadable file is not a verdict

    live_terms = _branch_terms(live_text)
    # No head_ref terms at all → not a shape this checker understands (a host
    # rewrote the arming condition wholesale); stay silent rather than nag on
    # a workflow that is intentionally off the kit's own generated shape.
    if not live_terms:
        return []

    patterns, _context = _automerge_params(config)
    expected_terms = _branch_terms(_automerge_branch_expr(patterns))
    if live_terms == expected_terms:
        return []

    live_desc = _describe(live_terms)
    expected_desc = _describe(expected_terms)
    return [
        Finding(
            AUTOMERGE_ENABLER_RELPATH,
            "automerge-branch-drift",
            f"the installed enabler arms on {live_desc}, but "
            f"`automerge.branch_patterns` would regenerate {expected_desc} — "
            "they differ, so either the workflow was hand-edited (kit-owned: "
            "`upgrade` overwrites it) or its allowlist is stale and will not "
            "arm the branches sessions push. Put the branch list in "
            "`substrate.config.json` `automerge.branch_patterns` and "
            "regenerate (`bootstrap.py upgrade` / `adopt --wire-enforcement`) "
            "so config and workflow match.",
        ),
    ]


def _describe(terms: set[tuple[str, str]]) -> str:
    """Render a branch-term set as a stable, human-readable allowlist string."""
    parts = sorted(
        f"{value}*" if kind == "prefix" else value for kind, value in terms
    )
    return "{" + ", ".join(parts) + "}" if parts else "{no agent branches}"
