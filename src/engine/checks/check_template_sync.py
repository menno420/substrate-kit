"""check_template_sync — template↔local-copy heading-set sync advisory.

Why + provenance: the kit plants adopter docs from
``src/engine/templates/*.tmpl`` (:data:`engine.adopt.ADOPT_PLAN` maps
template → destination), and the kit's own repo carries **rendered local
copies of the same docs** (e.g. ``control/README.md``,
``control/claims/README.md``). Template and local copy are hand-synced:
every doctrine edit must land twice by hand, and a miss ships adopters a
different contract than the kit itself runs — or leaves the kit running an
older contract than the one it distributes. Two live instances in one day
(2026-07-15): the PR #395 card's observed ``control/README.md`` divergence,
and PR #397 finding ``control/claims/README.md`` lagging its shipped
template by a whole feature paragraph (the ``--order NNN`` claim contract)
for a full day. Design authority:
``docs/ideas/template-local-copy-sync-advisory-2026-07-15.md``.
Added 2026-07-15. Reliability (PL-008): UNVERIFIED — confirm its findings
against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** — the same
nudge-never-door contract as ``check_claims`` / ``check_staged_regen``: the
fix is one hand-sync edit, and doctrine-structure drift is a judgment call
(a local copy may legitimately grow a repo-specific section) that a locked
door cannot adjudicate.

What fires: for each :data:`engine.adopt.ADOPT_PLAN` pair whose template
source (``src/engine/templates/<name>``) AND destination BOTH exist in the
target tree, compare the ``## `` section-heading **sets** and yield one
``template-local-heading-drift`` finding naming the headings present on
only one side. Heading sets, not byte-diff, because local copies
legitimately diverge in prose; what must not silently diverge is doctrine
**structure** — a whole section existing on only one side is exactly the
paid class. The template-source-in-tree requirement is the self-gate: only
the kit's own repo carries ``src/engine/templates/``, so the scan costs
adopters nothing (and reads the tree, not the embedded ``_TEMPLATES``, so
a mid-session template edit is compared before the dist regen).

False-positive firewalls:

- **Fence-aware scan** — ``## `` lines inside code fences (backtick or
  tilde) never count as headings (templates carry example blocks).
- **Slot-pattern matching** — a template heading carrying ``${slot}``
  placeholders (e.g. ``Rails specific to ${project_name}``) is compared as
  a pattern: a local heading matching it with the slots filled counts as
  the same heading, never as drift.
- **Placeholder skip** — headings carrying a live ``[[fill:`` marker skip
  on either side (an unfilled hand-slot is the interview's business).
- **Live-traffic destinations skip** (:data:`LIVE_TRAFFIC_DESTS`) — the
  inbox/status bus files and the living ledgers (current-state, decisions,
  question-router, session journal) are seeded *skeletons* whose headings
  are EXPECTED to accumulate live content; structure drift there is the
  file working as designed. Non-markdown plants (``env-setup.sh``) skip by
  suffix.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from engine.adopt import ADOPT_PLAN, _adopt_dest
from engine.checks.check_docs import Finding

# Where the kit repo keeps the template sources. Presence of a pair's
# template file under this tree is the checker's self-gate: adopter repos
# have planted docs but no template sources, so nothing can compare.
TEMPLATES_RELPATH = "src/engine/templates"

# ADOPT_PLAN destinations that are seeded skeletons for LIVE traffic — the
# planted file is a starting shape the repo then fills with orders, wakes,
# ledger entries, and journal notes, each typically a new `## ` heading.
# Heading drift there is the design, not the paid hand-sync class; scanning
# them would bury the real signal (measured on the kit tree 2026-07-15:
# control/inbox.md alone carried 25 live-only headings).
LIVE_TRAFFIC_DESTS = frozenset(
    {
        "control/inbox.md",
        "control/status.md",
        "docs/current-state.md",
        "docs/decisions.md",
        "docs/question-router.md",
        ".session-journal.md",
    }
)

_SLOT_RE = re.compile(r"\$\{[^}]*\}")
_FILL_MARKER = "[[fill:"
_LIST_CAP = 6


def _headings(text: str) -> list[str]:
    """Return the ``## `` (level-2 only) heading titles, fence-aware."""
    out: list[str] = []
    fence = False
    for raw in text.splitlines():
        line = raw.rstrip()
        stripped = line.lstrip()
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = not fence
            continue
        if fence:
            continue
        match = re.match(r"^##\s+(.+)$", line)
        if match:
            out.append(match.group(1).strip())
    return out


def _slot_pattern(heading: str) -> re.Pattern[str]:
    """Compile a slotted template heading into a filled-heading matcher."""
    parts = _SLOT_RE.split(heading)
    body = r".+?".join(re.escape(part) for part in parts)
    return re.compile(rf"^{body}$")


def _heading_drift(
    template_text: str,
    local_text: str,
) -> tuple[list[str], list[str]]:
    """Return ``(template_only, local_only)`` heading titles after matching.

    Literal headings match by exact title; a slotted template heading
    consumes every local heading its filled pattern matches. ``[[fill:``
    headings are dropped from both sides before matching.
    """
    template_headings = {
        h for h in _headings(template_text) if _FILL_MARKER not in h
    }
    local_headings = {h for h in _headings(local_text) if _FILL_MARKER not in h}

    literal = {h for h in template_headings if not _SLOT_RE.search(h)}
    slotted = template_headings - literal

    template_only = literal - local_headings
    local_unmatched = local_headings - literal
    for heading in slotted:
        pattern = _slot_pattern(heading)
        matched = {h for h in local_unmatched if pattern.match(h)}
        if matched:
            local_unmatched -= matched
        else:
            template_only.add(heading)
    return sorted(template_only), sorted(local_unmatched)


def _fmt(headings: list[str]) -> str:
    shown = ", ".join(f"'{h}'" for h in headings[:_LIST_CAP])
    return shown + (" …" if len(headings) > _LIST_CAP else "")


def check_template_sync(target: Path, config: Any) -> list[Finding]:
    """Return heading-set drift findings for ``target`` (empty = in sync).

    Self-gating: pairs whose template source or destination is absent from
    the tree contribute nothing, so the scan is a no-op everywhere except
    the kit's own repo (the only tree carrying ``src/engine/templates/``).
    """
    templates_root = target / TEMPLATES_RELPATH
    if not templates_root.is_dir():
        return []
    findings: list[Finding] = []
    for template_name, plan_rel in ADOPT_PLAN:
        dest_rel = _adopt_dest(plan_rel, config)
        if not dest_rel.endswith(".md") or dest_rel in LIVE_TRAFFIC_DESTS:
            continue
        template_path = templates_root / template_name
        local_path = target / dest_rel
        if not template_path.is_file() or not local_path.is_file():
            continue
        try:
            template_text = template_path.read_text(encoding="utf-8")
            local_text = local_path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        template_only, local_only = _heading_drift(template_text, local_text)
        if not template_only and not local_only:
            continue
        segments = []
        if template_only:
            segments.append(f"template-only: {_fmt(template_only)}")
        if local_only:
            segments.append(f"local-only: {_fmt(local_only)}")
        findings.append(
            Finding(
                dest_rel,
                "template-local-heading-drift",
                f"`## ` heading set diverges from "
                f"{TEMPLATES_RELPATH}/{template_name} — "
                + " · ".join(segments)
                + " — doctrine edits must land on BOTH sides "
                "(hand-sync the lagging copy, or record the deliberate "
                "divergence in the local file's prose).",
            ),
        )
    return findings
