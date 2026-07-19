"""Folded-gate diff-aware advisory — warn-only, NEVER exit-affecting.

Provenance: ``docs/planning/2026-07-19-needs-planning-recipes.md`` §2 and
``docs/ideas/folded-gate-diff-aware-card-2026-07-11.md`` (origin consumer
superbot-next, live-verified in the v1.9.0 distribution wave).

Why this exists: kit PR #19 made the session gate PR-diff-aware — the engine
(``check --session-log <card>``), the kit's own ``ci.yml``, and the generated
adopter gate (``engine/adopt.py`` ``live_ci_workflow``) all derive the card to
grade from the PR's diff instead of the newest-by-mtime picker. But some hosts
do NOT run the planted gate — they hand-FOLDED the session-gate step into their
own CI (superbot-next as a ``gate`` job; websites in ``quality.yml``). Those
host-authored copies froze at the pre-#19 newest-by-mtime picker, so in a fresh
CI checkout (every mtime flattened) they can grade a SIBLING's ``complete`` card
instead of the PR's own in-progress one — a misgrade in the loosening direction.
The kit never regenerates host-authored workflows, so a template change cannot
fix it; the only kit-side surface that DOES run in adopter repos is ``check``
itself. This checker is that surface.

What it does: scan ``.github/workflows/*.yml`` (and ``*.yaml``) in the repo
being checked; for any workflow that invokes the session gate's locked door
(``--require-session-log``) WITHOUT passing the diff-aware selection flag
(``--session-log`` / ``--added-card`` as a distinct token), emit ONE advisory
naming the file. A folded gate that already ports the diff-aware block — and the
kit's own ``ci.yml`` and the planted ``substrate-gate`` (both of which pass
``--session-log``) — stay silent.

Posture — ADVISORY only (warn-only, never exit-affecting): this returns a single
``list[Finding]`` with no gate tier, so it is wired on the advisory path in
``cli.py`` (``posture="advisory"``) exactly like the claims-format / model-line
/ adopter-registry nags. It is deliberately NOT in ``STRICT_SUBCHECKS`` — a hard
red would break every adopter that legitimately folds its gate before they can
react (and the actual host ports are cross-repo follow-ons, not landable from the
kit). Input-gated + fail-open like every checker: no ``.github/workflows/`` dir,
or an unreadable file, yields nothing (an absent/unreadable file is not a
verdict). Stdlib only.

Substring-trap note: ``--require-session-log`` is matched as the gate signal;
the diff-aware flag ``--session-log`` is matched as its OWN token (a negative
lookbehind excludes the ``require-`` prefix) so the locked-door flag can never
be mistaken for the diff-aware one — otherwise the advisory would never fire.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.checks.check_docs import Finding

# The session-gate "locked door" — a folded gate that grades sessions at all
# carries this flag (``check --strict --require-session-log``).
_RE_GATE_INVOKED = re.compile(r"--require-session-log\b")

# The PR-diff-aware selection flags (kit PR #19). ``--session-log`` is matched
# as its OWN token: the negative lookbehind rejects the ``require-`` prefix so
# ``--require-session-log`` (the locked-door flag) is NOT read as diff-aware.
_RE_SESSION_LOG = re.compile(r"(?<!require-)--session-log\b")
_RE_ADDED_CARD = re.compile(r"--added-card\b")

_WORKFLOWS_RELDIR = ".github/workflows"

FINDING_KIND = "folded-gate-mtime-picker"


def _folds_gate_without_diff_awareness(text: str) -> bool:
    """True when ``text`` invokes the session-gate locked door but passes no
    diff-aware selection flag — a hand-folded gate still relying on the engine's
    newest-by-mtime picker (which is arbitrary in a flat-mtime CI checkout)."""
    if not _RE_GATE_INVOKED.search(text):
        return False
    diff_aware = bool(_RE_SESSION_LOG.search(text)) or bool(
        _RE_ADDED_CARD.search(text)
    )
    return not diff_aware


def check_folded_gate(target: Path) -> list[Finding]:
    """Return advisory findings for host-folded session gates that froze at the
    pre-#19 newest-by-mtime card picker.

    Advisory only — the caller wires this on the ``posture="advisory"`` path and
    NEVER counts it toward the exit code. Fail-open: an absent
    ``.github/workflows/`` directory or an unreadable workflow file yields no
    finding.
    """
    workflows_dir = target / _WORKFLOWS_RELDIR
    if not workflows_dir.is_dir():
        return []  # input-gated: no workflows to scan
    findings: list[Finding] = []
    paths = sorted(workflows_dir.glob("*.yml")) + sorted(
        workflows_dir.glob("*.yaml")
    )
    for path in paths:
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue  # fail open — an unreadable file is not a verdict
        if not _folds_gate_without_diff_awareness(text):
            continue
        relpath = f"{_WORKFLOWS_RELDIR}/{path.name}"
        findings.append(
            Finding(
                relpath,
                FINDING_KIND,
                f"{relpath} folds the session gate (`--require-session-log`) "
                "without the diff-aware `--session-log`/`--added-card` "
                "selection, so it still grades the newest-by-mtime card — in a "
                "flat-mtime CI checkout that can misgrade a SIBLING session's "
                "`complete` card instead of this PR's own in-progress one (the "
                "loosening misgrade kit PR #19 fixed). Port the diff-aware "
                "card-derivation block from the planted substrate-gate / the "
                "kit's own `.github/workflows/ci.yml` (grade every "
                "`git diff` card via `--session-log`, added cards via "
                "`--added-card`).",
            ),
        )
    return findings
