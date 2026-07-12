"""Orientation-budget gate — the K0 <=7,000-word boot-read cap (Lane B6).

Orientation cost is the tax every session pays before real work starts, so
the kit meters it: the *boot set* (``config.orientation["boot_docs"]``,
falling back to ``config.readpath_docs`` when empty) must total no more than
``config.orientation["budget_words"]`` words. Boot-doc entries name files
under ``docs_root``; an entry containing ``/`` resolves from the project root
instead, so hosts can meter root-level docs (a journal, a CLAUDE.md) too.

Per-doc self-caps ride on top: a doc whose first 12 lines declare
``substrate-budget: N words`` is individually capped at N — a living doc can
pin its own growth ceiling without touching config.

Finding kinds: ``orientation-missing`` (a boot doc is absent),
``orientation-budget`` (the total blows the budget), ``orientation-doc-cap``
(a self-capped doc outgrew its declared cap). Findings reuse the ``Finding``
record from ``engine.checks.check_docs``.

Headroom advisory (the K0 headroom gauge — seat-baton item, spec of record
``.sessions/2026-07-10-nightcap-docs-reconcile.md`` § 💡): the budget gate
used to bite silently — no signal until ``check --strict`` went red, then an
iterative trim loop, one full check run per guess (the 7,250-word live hit;
a second live hit sat at 6,992/7,000 with 8 words of headroom and no
warning). :func:`check_orientation_headroom` turns the cliff into a gauge:
when the boot-set total reaches ``orientation["headroom_warn_ratio"]``
(default 0.95) of the budget without exceeding it, it emits ONE
``orientation-headroom`` advisory naming total/budget, the exact words of
headroom, and the per-doc word split (largest first) so a docs session sees
the pressure — and where the weight is — BEFORE committing. The same split
now rides the over-budget ``orientation-budget`` finding, so the trim loop
is targeted, not guess-and-recheck.

Added 2026-07-12 (K0 headroom advisory, PR #308). Reliability (PL-008):
UNVERIFIED — confirm its findings against ground truth a few times across
sessions before trusting it; **delete the advisory if it proves unreliable
over multiple sessions.** Posture is **advisory-only, never
exit-affecting** (§8 Q2=B advisory-first) — the same nudge-never-door
contract as ``check_claims`` / ``check_skill_grounds`` /
``check_seat_digest``. The budget gate itself is unchanged and still
exit-affecting.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding
from engine.lib.config import Config

# `substrate-budget: 500 words` — the per-doc self-cap declaration.
_OB_SELF_CAP_RE = re.compile(r"substrate-budget:\s*(\d+)\s*words", re.IGNORECASE)
_OB_HEAD_LINES = 12
_OB_TOTAL_KEY = "_total"


def _ob_word_count(path: Path) -> int | None:
    """Return the doc's word count, or ``None`` when it cannot be read."""
    try:
        return len(path.read_text(encoding="utf-8").split())
    except (OSError, UnicodeDecodeError):
        return None


def _ob_self_cap(path: Path) -> int | None:
    """Return the doc's declared self-cap from its first 12 lines, if any."""
    try:
        head = path.read_text(encoding="utf-8").splitlines()[:_OB_HEAD_LINES]
    except (OSError, UnicodeDecodeError):
        return None
    match = _OB_SELF_CAP_RE.search("\n".join(head))
    return int(match.group(1)) if match else None


def _ob_rel(path: Path, root: Path) -> str:
    """Return ``path`` relative to ``root`` (posix) when possible, else str."""
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def orientation_word_count(root: Path, boot_docs: list[Path]) -> dict[str, int]:
    """Return per-doc word counts plus a ``_total`` for the boot set.

    Keys are paths relative to ``root`` where possible. A missing or
    unreadable doc counts 0 here — ``check_orientation_budget`` is the layer
    that reports it.
    """
    counts: dict[str, int] = {}
    total = 0
    for doc in boot_docs:
        words = _ob_word_count(doc) or 0
        counts[_ob_rel(doc, root)] = words
        total += words
    counts[_OB_TOTAL_KEY] = total
    return counts


def _ob_split(counts: dict[str, int]) -> str:
    """Return the per-doc word split, largest first, as one message segment.

    ``"docs/current-state.md 3850 · docs/AGENT_ORIENTATION.md 3100"`` — the
    gauge half of the headroom advisory: which docs carry the weight. The
    ``_total`` row is excluded; ties break alphabetically for a stable
    message.
    """
    docs = sorted(
        (item for item in counts.items() if item[0] != _OB_TOTAL_KEY),
        key=lambda item: (-item[1], item[0]),
    )
    return " · ".join(f"{path} {words}" for path, words in docs)


def _ob_boot_paths(root: Path, config: Config) -> list[Path]:
    """Resolve the configured boot set to concrete paths.

    Explicit ``orientation["boot_docs"]`` entries: a bare name resolves under
    ``docs_root``, an entry with ``/`` resolves from the project root. The
    ``readpath_docs`` fallback resolves under ``docs_root`` unconditionally —
    matching ``check_reachable``, which reads the same key.
    """
    orientation = config.orientation or {}
    docs_root = root / config.docs_root
    explicit = list(orientation.get("boot_docs") or [])
    if explicit:
        # Explicit boot docs: a bare name resolves under docs_root, an entry
        # with "/" resolves from the project root (CONSTITUTION.md etc.).
        return [root / e if "/" in e else docs_root / e for e in explicit]
    # readpath_docs fallback: resolve under docs_root unconditionally, matching
    # check_reachable — the two consumers of that key must agree.
    return [docs_root / e for e in config.readpath_docs]


def check_orientation_budget(root: Path, config: Config) -> list[Finding]:
    """Meter the boot-read set against the orientation budget.

    Reports missing boot docs (``orientation-missing``), a total word count
    over ``orientation["budget_words"]`` (``orientation-budget``), and any doc
    that outgrew its own ``substrate-budget: N words`` self-cap
    (``orientation-doc-cap``).
    """
    findings: list[Finding] = []
    boot_paths = _ob_boot_paths(root, config)
    for doc in boot_paths:
        if not doc.is_file():
            msg = "boot doc missing — fix the path or the orientation config"
            findings.append(Finding(_ob_rel(doc, root), "orientation-missing", msg))

    counts = orientation_word_count(root, boot_paths)
    budget = int((config.orientation or {}).get("budget_words", 7000))
    total = counts[_OB_TOTAL_KEY]
    if total > budget:
        msg = (
            f"boot-read set totals {total} words, over the "
            f"{budget}-word orientation budget — trim or demote a boot doc"
            f" (split: {_ob_split(counts)})"
        )
        findings.append(Finding(_OB_TOTAL_KEY, "orientation-budget", msg))

    for doc in boot_paths:
        cap = _ob_self_cap(doc)
        if cap is None:
            continue
        words = counts.get(_ob_rel(doc, root), 0)
        if words > cap:
            msg = f"doc is {words} words, over its {cap}-word self-cap"
            findings.append(Finding(_ob_rel(doc, root), "orientation-doc-cap", msg))
    return findings


def check_orientation_headroom(root: Path, config: Config) -> list[Finding]:
    """Warn when the boot set nears the budget — the K0 headroom gauge.

    Emits at most ONE ``orientation-headroom`` finding, when the boot-set
    total is at or above ``orientation["headroom_warn_ratio"]`` (default
    0.95) of ``budget_words`` but not over it — over-budget is the gate's
    verdict (:func:`check_orientation_budget`), not this advisory's; firing
    both would double-report one condition. The message names total/budget,
    the exact words of headroom, and the per-doc split (largest first).

    **Advisory-only by contract, never exit-affecting** — the caller prints
    it in a warn-only block and never counts it toward the exit code (see
    the module docstring's PL-008 header). A ``headroom_warn_ratio`` at or
    above 1 disables the gauge (the cliff itself is the gate's job); at or
    below 0 it warns on every run — a host can pin either extreme.
    """
    orientation = config.orientation or {}
    try:
        ratio = float(orientation.get("headroom_warn_ratio", 0.95))
    except (TypeError, ValueError):
        ratio = 0.95
    budget = int(orientation.get("budget_words", 7000))
    if ratio >= 1 or budget <= 0:
        return []
    boot_paths = _ob_boot_paths(root, config)
    counts = orientation_word_count(root, boot_paths)
    total = counts[_OB_TOTAL_KEY]
    if not (budget * ratio <= total <= budget):
        return []
    msg = (
        f"boot-read set at {total}/{budget} words — {budget - total} words "
        f"of headroom (>={ratio:.0%} of budget; trim before the cliff) "
        f"(split: {_ob_split(counts)})"
    )
    return [Finding(_OB_TOTAL_KEY, "orientation-headroom", msg)]
