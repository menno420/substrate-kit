"""Verify-before-assert — the ``CLAUDE.md.tmpl`` claim-verification rule.

Pins the working-agreement section that moves provenance discipline from the
*artifact* to the *assertion*. Provenance labelling (``measured`` ·
``inferred`` · ``assumed``) fires when someone writes a provenance block, so
provenance blocks read honestly; nothing fires when a claim is typed in prose,
which is where unchecked assertions are actually made.

Phrases are pinned directly against the template, per the same reasoning as
``test_grounded_tail``: the slice-2/3/4/5/8 grammar rule homes a phrase only
when BOTH a writer (template) and an enforcer (checker) consume it, and no
checker consumes a doctrine sentence. Portably worded — no repo names, dates or
fleet ids, so every adopter's rendered agreement carries it unchanged.

Provenance: adopter session 2026-08-03, three confident claims that each cost
one command to check — a capability wall contradicted by ``printenv``, a tool's
behaviour contradicted by re-running it, and a string called invented that a
``grep`` found in the source. Two explanations offered for the pattern were
themselves unchecked and wrong, which is why the rule names that case
explicitly.
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.render")

from engine.render import load_templates


def _template(name: str) -> str:
    return load_templates()[name]


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase pin survives markdown line-wrapping."""
    return " ".join(text.split())


_CLAIM_PINS = (
    # the rule itself, in imperative form
    "If a statement is checkable with one command, run the command before "
    "writing the sentence.",
    # the three worked examples — one per class of check
    "`printenv` before \"the credential is missing\"",
    "`grep -rn <term>` before \"that string does not exist\"",
    "re-run the tool before describing what it does",
    # why it is not already covered by provenance labelling
    "applies at the moment of **stating**, not at the moment of writing the doc",
    # the self-directed case, which is the one that goes unchecked
    "A plausible cause is not a checked cause",
    "check the explanation too",
)


def test_claude_template_carries_every_claim_pin():
    tmpl = _flat(_template("CLAUDE.md.tmpl"))
    for phrase in _CLAIM_PINS:
        assert _flat(phrase) in tmpl, phrase


def test_claim_rule_sits_next_to_the_change_rule():
    # Deliberate placement: an agent reading "how do I verify" finds both
    # halves together — the change gate and the claim gate.
    tmpl = _template("CLAUDE.md.tmpl")
    assert "## Verifying a claim" in tmpl
    assert tmpl.index("## Verifying a change") < tmpl.index("## Verifying a claim")


def test_claim_rule_is_a_practice_not_a_declared_limitation():
    # check_no_false_walls scans src/engine/templates/*.tmpl: a forward-binding
    # surface records capabilities and practices, never standing limitations.
    # This rule tells an agent what to DO before asserting; it must never read
    # as "an agent cannot know X".
    section = _template("CLAUDE.md.tmpl").split("## Verifying a claim", 1)[1]
    section = section.split("\n## ", 1)[0].lower()
    for forbidden in ("cannot ", "can't ", "unable to", "not allowed to", "no access"):
        assert forbidden not in section, forbidden
