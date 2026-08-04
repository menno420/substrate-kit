"""Task→skill router — the ``CLAUDE.md.tmpl`` routing section.

Pins the working-agreement section that makes skill invocation part of the
task instead of a memory feat. Rationale (PL-013): a skill is only binding on
a session that loads it, and the only file every session reads
unconditionally is the planted working agreement — so the router lives there,
naming each recurring kit task class next to the skill that carries its
standard.

Phrases are pinned directly against the template, per the same reasoning as
``test_verify_before_assert``: no checker consumes a doctrine sentence, so
the test is the enforcing half. Portably worded — no repo names, dates or
fleet ids; the local-extension clause tells adopters to append rows rather
than fork the section.

Provenance: adopter observation 2026-08-04 — a well-made skill set sat
invisible because nothing in the boot path routed to it; the owner's ask,
verbatim in spirit: skills must fire at the right times without the owner
remembering they exist.
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.render")

from engine.render import load_templates


def _flat(text: str) -> str:
    return " ".join(text.split())


_ROUTER_PINS = (
    # the section heading
    "## Task → skill routing — invoking the skill IS part of the task",
    # the binding rule, with its law citation
    "loading that skill is part of doing the task",
    "a skill you didn't load can't bind you (PL-013: readable is not binding)",
    # the local-extension clause — adopters append rows, never fork the router
    "Repo-local skills extend this table, not replace it",
    # the defect framing that gives reviews something to check
    "a defect in the session, not a stylistic choice",
)

# every kit-shipped recurring-task skill must have a row
_ROUTED_SKILLS = (
    "`intake`",
    "`chase-references`",
    "`prep-owner-steps`",
    "`scope-backlog-item`",
    "`rationalize`",
    "`quality-gate`",
    "`session-close`",
    "`release`",
    "`upgrade-distribution`",
)


def test_router_section_pinned() -> None:
    flat = _flat(load_templates()["CLAUDE.md.tmpl"])
    for pin in _ROUTER_PINS:
        assert _flat(pin) in flat, f"router pin missing from CLAUDE.md.tmpl: {pin!r}"


def test_router_routes_the_recurring_kit_skills() -> None:
    flat = _flat(load_templates()["CLAUDE.md.tmpl"])
    for name in _ROUTED_SKILLS:
        assert name in flat, f"kit skill has no router row in CLAUDE.md.tmpl: {name}"
