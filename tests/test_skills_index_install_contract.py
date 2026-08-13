"""Defect 5 (v1.21.0) — the SKILLS-index template's install teaching.

The template taught *"install with `python3 bootstrap.py skills --build`"*,
which only STAGES: no kit command writes a live ``.claude/`` tree
(``cmd_skills``' own docstring), so a fresh adopter following the index ended
with 14 staged and 0 live skills while both commands exited 0 — a silent
false-done on the exact surface that tells sessions what they can invoke
(fleet-manager ``docs/findings/2026-08-09-substrate-kit-defects.md``,
defect 5, long-standing). The fix keeps the honest split: ``skills --build``
refreshes the staged tree; installing is the host's documented copy loop.

These tests pin the CONTRACT of the teaching text, not its prose: the false
claim must be absent, the true mechanism must be present, and the shell copy
loop must survive ``render()`` byte-identically (its ``$d``/``$n``/
``$(basename …)`` are not ``${slot}`` placeholders).
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.render import render

_TMPL = (
    Path(__file__).resolve().parents[1]
    / "src"
    / "engine"
    / "templates"
    / "SKILLS-index.md.tmpl"
)


def _template_text() -> str:
    return _TMPL.read_text(encoding="utf-8")


class TestSkillsIndexInstallContract:
    def test_no_line_claims_skills_build_installs(self) -> None:
        # The defect shape: "install with `python3 bootstrap.py skills
        # --build`" (any spacing/wrapping). Whatever the prose around it,
        # no sentence may pair an install claim with the staging command.
        text = _template_text()
        assert not re.search(
            r"install\s+with[^.]{0,80}skills\s+--build", text, re.I | re.S
        ), "the template must not teach `skills --build` as the install step"

    def test_staging_only_contract_is_stated(self) -> None:
        text = _template_text()
        assert re.search(
            r"no kit command ever\s+writes the live `\.claude/` tree", text
        ), "the template must state the kit never writes the live .claude tree"

    def test_the_copy_loop_is_the_documented_install(self) -> None:
        text = _template_text()
        assert 'cp "$d/SKILL.md" ".claude/skills/$n/SKILL.md"' in text
        assert "mkdir -p .claude/skills" in text
        assert re.search(
            r"diff before you copy", text, re.I
        ), "the copy overwrites kit-named local amendments — the warning ships with the loop"

    def test_copy_loop_survives_render_byte_identical(self) -> None:
        # render() substitutes only ${name} placeholders; the loop's bare
        # `$d` / `$n` / `$(basename "$d")` must come through untouched even
        # with a hostile same-named context.
        text = _template_text()
        loop = text[text.index("```bash") : text.index("```", text.index("```bash") + 7)]
        rendered = render(text, {"project_name": "x", "d": "BOOM", "n": "BOOM"})
        assert loop in rendered, "render() must not rewrite the shell copy loop"
