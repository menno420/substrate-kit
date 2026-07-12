"""Self-propagation doctrine (grounded-skills slice 8, plan §7.8).

One home for the doctrine's pinned phrases: ``engine.grammar``'s
``SELF_PROPAGATION_PHRASES``. The CONSTITUTION template's working-agreement
clause and the planted skill index's "Growing the set" section (the clause's
pointer target) both carry every phrase — these tests pin both legs against
that one home, so clause and index cannot drift (the slice-4/5 shared-pin
pattern: shared constants, not textual copies).

Provenance (executable twin of superbot doctrine, not paraphrase drift —
full dates in the grammar module's section comment): Q-0194 friction→guard
(2026-06-22, promoted binding 2026-06-28), Q-0106 propose-don't-apply
(2026-06-12), Q-0172 ship-anytime-with-accountability (2026-06-17).
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.grammar")

from engine import grammar
from engine.render import build_context, load_templates, render


def _template(name: str) -> str:
    return load_templates()[name]


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase pin survives markdown line-wrapping."""
    return " ".join(text.split())


# ── the one home ─────────────────────────────────────────────────────────────


def test_phrase_tuple_carries_every_named_constant():
    assert grammar.SELF_PROPAGATION_PHRASES == (
        grammar.SELF_PROPAGATION_REFLEX,
        grammar.SELF_PROPAGATION_REGISTRY,
        grammar.SELF_PROPAGATION_GROWTH_LOOP,
        grammar.SELF_PROPAGATION_FREE_LANE,
        grammar.SELF_PROPAGATION_BOUND_LANE,
    )
    assert len(set(grammar.SELF_PROPAGATION_PHRASES)) == len(
        grammar.SELF_PROPAGATION_PHRASES
    )


def test_provenance_cite_names_the_three_superbot_rulings():
    for q in ("Q-0194", "Q-0106", "Q-0172"):
        assert q in grammar.SELF_PROPAGATION_PROVENANCE, q


# ── the clause: CONSTITUTION.md.tmpl ─────────────────────────────────────────


def test_constitution_clause_carries_every_phrase():
    tmpl = _flat(_template("CONSTITUTION.md.tmpl"))
    for phrase in grammar.SELF_PROPAGATION_PHRASES:
        assert phrase in tmpl, phrase


def test_constitution_clause_points_at_the_skill_index_growing_section():
    # The clause is one bullet plus a pointer into docs/SKILLS.md — the
    # doctrine's *how* lives at the index's "Growing the set", not re-essayed.
    tmpl = _template("CONSTITUTION.md.tmpl")
    clause = tmpl.split("Skills self-propagate", 1)[1].split("\n- ", 1)[0]
    assert "docs/SKILLS.md" in clause
    assert "Growing the set" in clause


def test_constitution_clause_cites_provenance():
    tmpl = _template("CONSTITUTION.md.tmpl")
    assert grammar.SELF_PROPAGATION_PROVENANCE in tmpl


def test_constitution_clause_routes_binding_text_to_the_question_router():
    # The bound lane: binding working-agreement text + executable config are
    # PROPOSED (docs/question-router.md), never self-applied — with the
    # in-session owner-directed exception recorded with its provenance id.
    tmpl = _template("CONSTITUTION.md.tmpl")
    clause = tmpl.split("Skills self-propagate", 1)[1].split("\n- ", 1)[0]
    assert "docs/question-router.md" in clause
    assert grammar.SELF_PROPAGATION_BOUND_LANE in clause
    assert "owner directs the change live in-session" in clause
    assert "provenance id" in clause


def test_constitution_keeps_the_propose_dont_apply_section_intact():
    # Accept criterion (plan §7.8): the wording keeps the EXISTING
    # propose-don't-apply boundary intact — the clause defers to the
    # "Changing the rules" section, it does not replace or contradict it.
    tmpl = _template("CONSTITUTION.md.tmpl")
    assert "## Changing the rules — propose, don't apply" in tmpl
    assert "by **proposal**, never by silent edit" in tmpl
    clause = tmpl.split("Skills self-propagate", 1)[1].split("\n- ", 1)[0]
    assert "Changing the rules" in clause


# ── the pointer target: SKILLS-index.md.tmpl "Growing the set" ───────────────


def test_skills_index_growing_the_set_carries_every_phrase():
    tmpl = _template("SKILLS-index.md.tmpl")
    section = _flat(tmpl.split("## Growing the set", 1)[1])
    for phrase in grammar.SELF_PROPAGATION_PHRASES:
        assert phrase in section, phrase
    assert grammar.SELF_PROPAGATION_PROVENANCE in section


def test_skills_index_points_back_at_the_agreement_home():
    # The reverse pointer rides the engine-computed ${agreement_home} key
    # (ENGINE_CONTEXT_KEYS) — never a hardcoded filename, the ORDER 015
    # dead-boot-pointer lesson.
    tmpl = _template("SKILLS-index.md.tmpl")
    section = tmpl.split("## Growing the set", 1)[1]
    assert "${agreement_home}" in section


# ── renders in fresh adopts (plan §7.8 accept criterion) ─────────────────────


def test_clause_renders_slot_free_in_a_fresh_adopt_context():
    # The doctrine's text is slot-free prose: rendered with the fresh-adopt
    # context (empty slots + the engine keys every adopt/upgrade/render path
    # injects), the clause and the Growing-the-set section carry every phrase
    # and strand no ${...} — a stray slot would re-banner every planted copy.
    context = dict(build_context({}))
    context.setdefault("agreement_home", "CONSTITUTION.md")
    constitution = render(_template("CONSTITUTION.md.tmpl"), context)
    clause = constitution.split("Skills self-propagate", 1)[1].split("\n- ", 1)[0]
    assert "${" not in clause
    for phrase in grammar.SELF_PROPAGATION_PHRASES:
        assert phrase in _flat(clause), phrase

    index = render(_template("SKILLS-index.md.tmpl"), context)
    section = index.split("## Growing the set", 1)[1]
    assert "${" not in section
    assert "CONSTITUTION.md" in section
    for phrase in grammar.SELF_PROPAGATION_PHRASES:
        assert phrase in _flat(section), phrase
