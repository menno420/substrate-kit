"""check_card_residue — session-card sham-resolution (residue) advisory.

Why + provenance: the KL-5 generalization of the archive-note residue guard
(S3 ``probe_slot_residue``, PR #414; S4 ``check_archive_ready``, PR #416 —
idea filed on the archive-probe-s3 session card). Session cards have the
identical sham corridor, and it matters MORE here: the session gate
(``check_session_log`` via the kit-quality workflow) counts ``[[fill:]]``
tokens only, so a card whose slots were "resolved" by stripping the markers
while keeping the drafted hint text in place currently passes the
MERGE-BLOCKING gate — a looks-done-isn't card buys a merge. This checker
puts the S3 verdict on every ``check --strict`` run for the card surface,
via the shared fingerprint core (``engine.lib.residue`` — one
implementation, no second copy; the S4 rule applied at lib level).

Added 2026-07-16. Reliability (PL-008): UNVERIFIED — confirm its findings
against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** — deliberately mirroring
how S4 introduced the archive advisory. Wiring residue into the
merge-blocking gate lanes themselves is a LATER, deliberate graduation:
an unverified fingerprint heuristic must not gain merge-blocking power on
day one (a false positive would brick a genuine session's merge), and the
advisory period is what earns that trust.

What fires — one ``session-card-slot-residue`` finding per session card
that *declares itself finished* (Status not in-progress/drafted) while a
drafted judgment-slot hint survives with its markers stripped. Cards still
carrying ``[[fill:]]`` slots are skipped (the gate's drafted-vs-completed
report owns that state), as are in-progress cards (judged only at
completion — the born-red HOLD owns the mid-flight state) and README.md.
Code spans and fences are stripped before probing (cards that *discuss*
the draft mechanism quote hints in backticks — prose mentions are not
residue). Self-gating: no sessions dir → the scan contributes nothing.
Every card is scanned, not just the newest — an old sham card is exactly
the leak worth surfacing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.checks.check_docs import Finding
from engine.checks.check_session_log import status_in_progress, unresolved_fill_count
from engine.lib.residue import probe_card_residue


def check_card_residue(target: Path, config: Any) -> list[Finding]:
    """Return sham-resolved-card findings for ``target`` (empty = ok)."""
    sessions = target / config.sessions_dir
    if not sessions.is_dir():
        return []
    findings: list[Finding] = []
    for card in sorted(sessions.glob("*.md")):
        if card.name == "README.md":
            continue
        try:
            text = card.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if unresolved_fill_count(text):
            continue  # drafted — the gate's slot count owns that report
        if status_in_progress(text):
            continue  # mid-flight — judged only once the card declares done
        guilty = probe_card_residue(text)
        if guilty:
            findings.append(
                Finding(
                    f"{config.sessions_dir}/{card.name}",
                    "session-card-slot-residue",
                    "zero [[fill:]] slots remain but drafted hint text "
                    f"survives in judgment slot(s): {', '.join(guilty)} — "
                    "the card is NOT a completed close-out (KL-5 "
                    "wholesale-replacement semantics); stripping the "
                    "[[fill:]] markers around a drafted hint is not a "
                    "resolution — replace each surviving hint wholesale "
                    "with genuine session text.",
                ),
            )
    return findings
