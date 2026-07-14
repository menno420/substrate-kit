"""Friction-outbox pending-count advisory — fm plan A10 (ORDER 020 sub-item d).

Why + provenance: filing a §9.1 friction report rides ``session-close`` and is
best-effort — the engine cannot reach GitHub, so a report the session could not
file is written to ``<state_dir>/friction-outbox/`` for a later session (or the
owner) to drain (``friction show <name>`` prints the issue title+body,
``friction export`` re-emits them). That drain reminder lives **only** in
``cmd_session_close`` today, so a stranded envelope is invisible to every plain
``check`` / ``check --strict`` run *between* session-close seams — a friction
report can sit undrained across many sessions with nothing surfacing it. This
module lifts the same pending-count reminder into the ``check`` advisory lane so
a stranded outbox is visible on every check, not only at the session-close seam
(fm lane-write relay ORDER 020, 2026-07-14; fm plan A10).

Posture is **advisory-only, never exit-affecting** — an undrained envelope is a
follow-up nudge, not a defect in the tree under review (the reports may be
un-drainable in this environment precisely because it has no GitHub reach, so a
required-check red here would be a bomb). It mirrors the session-close
advisory's wording so the two seams read identically. Input-gated on the outbox
directory holding at least one envelope; a repo that never filed one gets no
nag. Pure stdlib.
"""

from __future__ import annotations

from pathlib import Path

from engine.checks.check_docs import Finding
from engine.loop.friction import FRICTION_LABEL, list_outbox

# How many envelope filenames to spell out inline before eliding to "…". The
# finding is a single line; a long outbox names its head and points at the
# directory for the rest.
_NAME_PREVIEW = 3

OUTBOX_KIND = "outbox-pending"


def check_outbox_pending(target: Path, state_dir: str) -> list[Finding]:
    """Return an advisory finding when the friction outbox holds envelopes.

    One finding for the whole outbox (the count is the signal, not per-file
    detail). Empty outbox → no finding. Advisory by contract — callers must
    never count this toward an exit code.
    """
    pending = list_outbox(target, state_dir)
    if not pending:
        return []
    count = len(pending)
    plural = "s" if count != 1 else ""
    names = ", ".join(p.name for p in pending[:_NAME_PREVIEW])
    if count > _NAME_PREVIEW:
        names += ", …"
    return [
        Finding(
            f"{state_dir}/friction-outbox/",
            OUTBOX_KIND,
            f"{count} friction report{plural} pending ({names}) — file each as "
            f"a `{FRICTION_LABEL}`-labeled issue on the kit repo "
            "(`friction show <name>` prints the issue title+body; "
            "`friction export` re-emits all), then delete the drained file. "
            "Surfaced at check time so a stranded outbox is visible between "
            "session-close seams (fm plan A10).",
        ),
    ]
