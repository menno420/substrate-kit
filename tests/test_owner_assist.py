"""Owner-assist output standard (grounded-skills slice 4, plan §3/§7.4).

One home for the standard's grammar: the Q-0263.2 structured-choice phrases,
the risk-class tokens, and the vague-destination scan live in
``engine.grammar``; the ``/intake`` skill body, the doctrine templates
(control-README as the canonical home, collaboration-model, CONSTITUTION,
question-router), and ``check_owner_actions`` all carry/consume the same
constants — these tests pin every leg against that one home, so skill text,
template text, and enforcer cannot drift (the slice-3 card's prerequisite:
shared constants / shared test-pins, not textual copies).

Delivery default pinned per the owner-ruled §8 Q1=A: control-plane rendered
link + 3-line digest in chat, with full-text-in-chat as the fallback where
the plane cannot render the repo yet.
"""

from __future__ import annotations

import re

import pytest

pytest.importorskip("engine.grammar")

from engine import grammar
from engine.render import load_templates
from engine.skills.skills import get_skill


def _template(name: str) -> str:
    return load_templates()[name]


# ── the shared pins: skill body ↔ grammar constants ──────────────────────────


def test_intake_body_carries_every_structured_choice_phrase():
    body = get_skill("intake")["body"]
    for phrase in grammar.STRUCTURED_CHOICE_PHRASES:
        assert phrase in body, phrase


# ── the canonical home: control-README ───────────────────────────────────────


def test_control_readme_carries_the_standard_section():
    tmpl = _template("control-README.md.tmpl")
    assert "## Owner-assist output standard" in tmpl
    for phrase in grammar.STRUCTURED_CHOICE_PHRASES:
        assert phrase in tmpl, phrase
    for token in grammar.RISK_CLASS_TOKENS:
        assert token in tmpl, token
    assert grammar.RISK_CLASS_LABEL in tmpl


def test_control_readme_owner_action_block_teaches_the_risk_line():
    tmpl = _template("control-README.md.tmpl")
    section = tmpl.split("## ⚑ needs-owner — the OWNER-ACTION item format", 1)[1]
    match = re.search(r"```(?:markdown)?\n(.*?)```", section, re.DOTALL)
    assert match is not None
    block = match.group(1)
    assert grammar.RISK_CLASS_LABEL in block
    assert any(token in block for token in grammar.RISK_CLASS_TOKENS)


def test_control_readme_pins_the_q1a_delivery_default():
    # §8 Q1=A: control-plane link + 3-line digest default; full-text-in-chat
    # fallback where the plane cannot render.
    tmpl = _template("control-README.md.tmpl")
    assert "3-line digest" in tmpl
    assert "control-plane" in tmpl
    assert "fallback" in tmpl


def test_control_readme_link_rules():
    tmpl = _template("control-README.md.tmpl")
    assert "never the repo root" in tmpl
    assert "&refresh=1" in tmpl
    assert "ref=main" in tmpl


def test_control_readme_worked_example_is_complete():
    # The §3.4 worked example: digest + rendered deep link + six-field ask
    # with its risk class — every rule of the standard in one output.
    tmpl = _template("control-README.md.tmpl")
    section = tmpl.split("## Owner-assist output standard", 1)[1]
    example = re.search(r"```\n(.*?)```", section, re.DOTALL)
    assert example is not None
    text = example.group(1)
    assert "Digest:" in text
    assert grammar.OWNER_ACTION_BLOCK_TOKEN in text
    for alts in grammar.OWNER_ACTION_FIELDS:
        # HOW appears as the paste-ready variant "HOW (paste-ready):".
        label = alts[0].rstrip(":")
        assert label in text, label
    assert grammar.RISK_CLASS_LABEL in text
    assert any(token in text for token in grammar.RISK_CLASS_TOKENS)


def test_control_readme_worked_example_where_is_not_vague():
    # Dogfood: the example's own WHERE value must never trip the checker's
    # vague-destination scan.
    tmpl = _template("control-README.md.tmpl")
    for line in tmpl.splitlines():
        stripped = line.strip()
        if not stripped.startswith("WHERE:"):
            continue
        value = stripped.partition(":")[2].strip()
        if any(w in value.lower() for w in grammar.VAGUE_DESTINATION_WORDS):
            assert any(m in value for m in grammar.DESTINATION_SHAPE_MARKS), value


# ── the doctrine templates ────────────────────────────────────────────────────


def test_collaboration_model_carries_the_standard():
    tmpl = _template("collaboration-model.md.tmpl")
    for phrase in grammar.STRUCTURED_CHOICE_PHRASES:
        assert phrase in tmpl, phrase
    for token in grammar.RISK_CLASS_TOKENS:
        assert token in tmpl, token
    assert "Owner-assist output standard" in tmpl  # points at the home
    assert "3-line digest" in tmpl


def test_constitution_carries_the_pointer_weight_line():
    tmpl = _template("CONSTITUTION.md.tmpl")
    assert "owner-assist standard" in tmpl
    assert grammar.STRUCTURED_CHOICE_PHRASES[0] in tmpl  # bolded recommendation
    assert grammar.STRUCTURED_CHOICE_PHRASES[1] in tmpl  # one letter
    for token in grammar.RISK_CLASS_TOKENS:
        assert token in tmpl, token


def test_question_router_options_are_structured_choices():
    tmpl = _template("question-router.md.tmpl")
    assert grammar.STRUCTURED_CHOICE_PHRASES[0] in tmpl
    assert grammar.STRUCTURED_CHOICE_PHRASES[1] in tmpl
    assert grammar.STRUCTURED_CHOICE_PHRASES[2] in tmpl


def test_no_template_leaks_an_unrendered_slot_in_the_new_text():
    # The standard's text is slot-free prose — a stray ${...} would re-banner
    # every planted copy as unrendered forever.
    for name in (
        "control-README.md.tmpl",
        "collaboration-model.md.tmpl",
        "CONSTITUTION.md.tmpl",
        "question-router.md.tmpl",
    ):
        tmpl = _template(name)
        if "Owner-assist output standard" in tmpl:
            section = tmpl.split("Owner-assist output standard", 1)[1]
            assert "${" not in section.split("\n## ", 1)[0], name
