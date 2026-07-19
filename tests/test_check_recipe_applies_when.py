"""Recipe `applies-when:` tag advisory (night-run groom R11).

Every docs/recipes/ graduation (except README.md) must carry a well-formed
`> **applies-when:** \`<signature>\`` badge — a comma-separated list of
`path:<glob>` / `content:<marker>` tokens — so a future discovery check can match
an adopter's seam to a recipe. Advisory only (warn, never exit-affecting).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_recipe_applies_when")

from engine.checks.check_recipe_applies_when import (  # noqa: E402
    RECIPE_APPLIES_WHEN_KIND,
    check_recipe_applies_when,
)

_GOOD = """\
# Some recipe

> **Status:** `reference`
>
> **applies-when:** `content:raw.githubusercontent.com, path:*.json`
>
> A recipe.
"""


def _write_recipe(root: Path, name: str, text: str) -> Path:
    d = root / "docs" / "recipes"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def test_wellformed_tag_is_silent(tmp_path: Path):
    _write_recipe(tmp_path, "r.md", _GOOD)
    assert check_recipe_applies_when(tmp_path) == []


def test_missing_tag_fires(tmp_path: Path):
    _write_recipe(tmp_path, "r.md", "# R\n\n> **Status:** `reference`\n\n> A recipe.\n")
    findings = check_recipe_applies_when(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == RECIPE_APPLIES_WHEN_KIND
    assert findings[0].path == "docs/recipes/r.md"
    assert "missing" in findings[0].message


def test_empty_tag_fires(tmp_path: Path):
    _write_recipe(tmp_path, "r.md", "# R\n\n> **applies-when:** ``\n")
    findings = check_recipe_applies_when(tmp_path)
    assert len(findings) == 1
    assert "empty" in findings[0].message


def test_malformed_token_fires(tmp_path: Path):
    _write_recipe(tmp_path, "r.md", "# R\n\n> **applies-when:** `raw.githubusercontent.com`\n")
    findings = check_recipe_applies_when(tmp_path)
    assert len(findings) == 1
    assert "malformed" in findings[0].message


def test_readme_is_ignored(tmp_path: Path):
    _write_recipe(tmp_path, "README.md", "# Recipes\n\n> **Status:** `reference`\n")
    assert check_recipe_applies_when(tmp_path) == []


def test_missing_recipes_dir_fails_open(tmp_path: Path):
    assert check_recipe_applies_when(tmp_path) == []


def test_multiple_recipes_each_checked(tmp_path: Path):
    _write_recipe(tmp_path, "good.md", _GOOD)
    _write_recipe(tmp_path, "bad.md", "# B\n\n> **Status:** `reference`\n")
    findings = check_recipe_applies_when(tmp_path)
    assert len(findings) == 1
    assert findings[0].path == "docs/recipes/bad.md"


def test_not_in_strict_subchecks():
    guards = pytest.importorskip("engine.guards")
    assert RECIPE_APPLIES_WHEN_KIND not in guards.STRICT_SUBCHECKS
    assert "check_recipe_applies_when" not in guards.STRICT_SUBCHECKS
