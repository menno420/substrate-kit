"""check_archive_ready — archive-note unresolved-slot / residue advisory.

Why + provenance: slice S4 of the archive-ready close-out plan
(``docs/planning/2026-07-15-archive-ready-close-out-plan.md`` §5). The
archive-ready surface (S1 template + doctrine, S2 ``archive-prep`` verb,
S3 REQUIRES-PROBE resolve semantics) drafts
``docs/retro/archive-ready-<date>.md`` when a long-running chat is about to
be archived; the note is "done" only when every ``[[fill:]]`` slot is
resolved with live facts and no guarded-slot default survives
marker-stripping (the sham resolution S3's ``probe_slot_residue`` catches).
Until this slice, that verdict surfaced only when a session *re-ran the
verb* — a note landed half-resolved and never revisited stayed silently
incomplete, which is exactly the chat-only-knowledge leak the surface
exists to prevent (plan §1: a pointed-at lessons file that did not exist; a
"disarmed" failsafe found still armed by the live probe). This checker puts
the same verdict on every ``check --strict`` run instead.

Added 2026-07-16. Reliability (PL-008): UNVERIFIED — confirm its findings
against ground truth a few times across sessions before trusting it;
**delete this if it proves unreliable over multiple sessions.**

Posture is **advisory-only, never exit-affecting** (plan §4.3: the idea
text says "holds ``check --strict`` advisory-red"; shipping it as an
advisory matches the kit's PL-008 pattern and cannot brick an adopter's
gate on a false positive). Graduation to a hard / preflight leg is a later,
deliberate decision after the checker proves itself.

What fires — one finding per ``docs/retro/archive-ready-*.md`` note that is
not genuinely complete:

- ``archive-note-unresolved-slots`` — the note still carries ``[[fill:]]``
  slots (counted by :data:`DRAFT_FILL_TOKEN`, the same token the
  session-log checker counts by). Knowledge is still chat-only.
- ``archive-note-slot-residue`` — zero slots remain, but a doctrine-guarded
  slot's templated default text survives with the markers stripped
  (:func:`engine.loop.archive.probe_slot_residue` — the S3 seam, reused
  verbatim; this checker adds no second fingerprint implementation).

Self-gating: no ``docs/retro/`` directory or no ``archive-ready-*`` notes →
the scan contributes nothing, so repos that never archive pay nothing. A
genuinely completed note (zero slots, zero residue — e.g. the hand-written
2026-07-11 evidence note) is silent; plan §7's no-retroactive-regen
non-goal holds. Every note is scanned, not just the newest: an old
half-resolved note is precisely the leak worth surfacing.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from engine.checks.check_docs import Finding
from engine.checks.check_session_log import DRAFT_FILL_TOKEN
from engine.loop.archive import (
    ARCHIVE_TEMPLATE_NAME,
    _NOTE_GLOB,
    _RETRO_DIR,
    probe_slot_residue,
)
from engine.render import load_templates


def _archive_ready_residue_names(residue: list[str]) -> str:
    """Collapse ``probe_slot_residue`` findings to their guarded-slot names."""
    return ", ".join(finding.split(":", 1)[0] for finding in residue)


def check_archive_ready(target: Path, config: Any) -> list[Finding]:
    """Return incomplete-archive-note findings for ``target`` (empty = ok).

    One finding per note, unresolved slots first (a marker-carrying note is
    "unresolved", never residue — the same precedence
    ``ensure_archive_draft`` applies).
    """
    retro = target / config.docs_root / _RETRO_DIR
    if not retro.is_dir():
        return []
    try:
        # Loaded once for every note's residue probe; an embedded-template
        # miss fails the whole scan open — an advisory must never crash
        # `check` (the ensure_archive_draft fail-open contract, applied
        # here as silence).
        template = load_templates()[ARCHIVE_TEMPLATE_NAME]
    except Exception:
        return []
    findings: list[Finding] = []
    for note in sorted(retro.glob(_NOTE_GLOB)):
        try:
            text = note.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        rel = f"{config.docs_root}/{_RETRO_DIR}/{note.name}"
        slots = text.count(DRAFT_FILL_TOKEN)
        if slots:
            findings.append(
                Finding(
                    rel,
                    "archive-note-unresolved-slots",
                    f"{slots} [[fill:]] slot(s) still unresolved — knowledge "
                    "is still chat-only; resolve each with live facts "
                    "(REQUIRES-PROBE slots by wholesale replacement with "
                    "probe output), write the confirmation LAST, land the "
                    "note on main before the chat closes "
                    "(docs/operations/archive-ready-close-out.md).",
                ),
            )
            continue
        residue = probe_slot_residue(text, template=template)
        if residue:
            findings.append(
                Finding(
                    rel,
                    "archive-note-slot-residue",
                    "zero [[fill:]] slots remain but templated default text "
                    f"survives in guarded slot(s): "
                    f"{_archive_ready_residue_names(residue)} — the note is "
                    "NOT complete (S3 resolve semantics); replace the "
                    "surviving instruction text wholesale with freshly "
                    "probed output, then land the note on main.",
                ),
            )
    return findings
