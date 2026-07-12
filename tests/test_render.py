"""Tests for the template render mechanism + template/bank coherence."""

import build_bootstrap
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import KIT_VERSION
from engine.render import (
    ENGINE_CONTEXT_KEYS,
    agreement_home,
    build_context,
    find_placeholders,
    load_templates,
    render,
)


def test_find_placeholders():
    assert find_placeholders("${a} text ${b}") == {"a", "b"}
    assert find_placeholders("no placeholders here") == set()


def test_render_substitutes_filled_and_leaves_unfilled_visible():
    out = render("Hello ${name}, welcome to ${place}.", {"name": "Ada"})
    assert "Ada" in out
    assert "${place}" in out  # unfilled slot stays visible, not blank


def test_build_context_from_slot_values():
    state = {"slot_values": {"project_name": {"value": "Demo"}}}
    assert build_context(state) == {"project_name": "Demo", "kit_version": KIT_VERSION}


def test_build_context_always_injects_kit_version():
    # The engine-computed key (ORDER 003): every render path flows through
    # build_context, so the planted control/status.md `kit:` line always
    # renders with the real running version — and a (hypothetical) slot of
    # the same name would win over the constant.
    assert build_context({})["kit_version"] == KIT_VERSION
    state = {"slot_values": {"kit_version": {"value": "9.9.9"}}}
    assert build_context(state)["kit_version"] == "9.9.9"


def test_agreement_home_tracks_installed_working_agreement(tmp_path):
    # The engine-computed boot pointer (ORDER 015): .claude/CLAUDE.md only
    # when it is live in the target (or this adopt run opts in), else the
    # always-planted root CONSTITUTION.md — never a pointer to a file the
    # default adopt doesn't install.
    assert agreement_home(tmp_path) == "CONSTITUTION.md"
    assert agreement_home(tmp_path, include_claude=True) == ".claude/CLAUDE.md"
    (tmp_path / ".claude").mkdir()
    (tmp_path / ".claude" / "CLAUDE.md").write_text("x", encoding="utf-8")
    assert agreement_home(tmp_path) == ".claude/CLAUDE.md"


def test_load_templates_returns_core_set():
    templates = load_templates()
    assert "CLAUDE.md.tmpl" in templates
    assert "AGENT_ORIENTATION.md.tmpl" in templates
    assert "current-state.md.tmpl" in templates


def test_templates_only_reference_known_bank_slots():
    # Every placeholder must map to a bank slot, so a fully-filled interview
    # renders with zero leftovers (template/bank coherence guard).
    bank_slots = {q["slot"] for q in QUESTIONS}
    for name, text in load_templates().items():
        # ENGINE_CONTEXT_KEYS are engine-computed (build_context injects
        # them), so a template may reference them without a bank question.
        unknown = find_placeholders(text) - bank_slots - ENGINE_CONTEXT_KEYS
        assert not unknown, f"{name} references non-bank slots: {unknown}"


def test_full_fill_renders_without_leftovers():
    context = {q["slot"]: f"v-{q['slot']}" for q in QUESTIONS}
    context.update({key: f"v-{key}" for key in ENGINE_CONTEXT_KEYS})
    for name, text in load_templates().items():
        assert find_placeholders(render(text, context)) == set(), name


def test_templates_embedded_in_bootstrap():
    assert "_TEMPLATES = {" in build_bootstrap.build()


def test_render_leaves_host_dollar_content_untouched():
    # render() must act ONLY on ${braced} placeholders — never the $$ / unbraced
    # $word forms that string.Template.safe_substitute silently transforms. Host
    # shell/price/LaTeX content ($$pid, $$5, $$LaTeX$$) survives render --live.
    ctx = {"name": "Ada"}
    assert render("kill $$pid — costs $$5/run", ctx) == "kill $$pid — costs $$5/run"
    assert render("unbraced $name stays literal", ctx) == "unbraced $name stays literal"
    assert render("filled ${name}", ctx) == "filled Ada"


def test_render_and_find_placeholders_never_disagree_on_dollars():
    # An escaped $${X} must not become a live-looking ${X} that then reports as
    # an unfilled slot (the safe_substitute trap). With X not a slot, everything
    # but the real ${z} is left byte-for-byte.
    text = "keep $${X} and $$ and $y; fill ${z}"
    assert find_placeholders(text) == {"X", "z"}
    out = render(text, {"z": "Z"})
    assert out == "keep $${X} and $$ and $y; fill Z"


def test_find_placeholders_outside_code_strips_spans_and_fences():
    # Queued fix 4 (the #148/#150 poison): dollar-brace literals inside
    # inline code spans and fenced blocks are prose about a token, not
    # unfilled slots; bare ones still count.
    from engine.render import find_placeholders_outside_code

    text = (
        "bare ${live_slot} here\n"
        "a mention of `${span_slot}` in backticks\n"
        "```\n${fenced_slot} inside a fence\n```\n"
        "and `code with ${another_span}` again\n"
    )
    assert find_placeholders_outside_code(text) == {"live_slot"}
    # A fully-clean doc and a code-only doc both scan empty.
    assert find_placeholders_outside_code("plain prose") == set()
    assert find_placeholders_outside_code("`${only_span}`") == set()
