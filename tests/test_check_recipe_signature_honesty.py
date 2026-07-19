"""Recipe `applies-when:` signature-HONESTY advisory (wave-2 groom S8).

The complement to R11's well-formedness lint: every well-formed `applies-when:`
token is cross-checked against the recipe's own body, so a `content:<marker>` /
`path:<glob>` token the prose never mentions (a drifted signature) surfaces.
Advisory only (warn, never exit-affecting).
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_recipe_signature_honesty")

from engine.checks.check_recipe_signature_honesty import (  # noqa: E402
    RECIPE_SIGNATURE_HONESTY_KIND,
    _literal_fragments,
    check_recipe_signature_honesty,
)

# An HONEST recipe: every token's marker / glob skeleton appears in the body.
_HONEST = """\
# Some recipe

> **Status:** `reference`
>
> **applies-when:** `content:raw.githubusercontent.com, path:*.json`
>
> A recipe.

## When this applies

You read a feed over raw.githubusercontent.com and it ships as a config.json.
"""


def _write_recipe(root: Path, name: str, text: str) -> Path:
    d = root / "docs" / "recipes"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def test_honest_signature_is_silent(tmp_path: Path):
    _write_recipe(tmp_path, "r.md", _HONEST)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_content_token_absent_from_body_fires(tmp_path: Path):
    text = (
        "# R\n\n> **Status:** `reference`\n>\n"
        "> **applies-when:** `content:ghost_marker`\n>\n"
        "> A recipe.\n\n## When\n\nThis body never says the marker word.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    findings = check_recipe_signature_honesty(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == RECIPE_SIGNATURE_HONESTY_KIND
    assert findings[0].path == "docs/recipes/r.md"
    assert "ghost_marker" in findings[0].message
    assert "never mentions" in findings[0].message


def test_content_token_present_in_body_is_silent(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `content:real_marker`\n>\n"
        "> A recipe.\n\n## When\n\nThe body names real_marker right here.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_content_match_is_case_insensitive(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `content:RawURL`\n>\n"
        "> A recipe.\n\n## When\n\nThe body mentions rawurl in lowercase.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_token_not_satisfied_by_its_own_badge_line(tmp_path: Path):
    # The marker appears ONLY on the badge line — honesty must still fire,
    # because the badge line is excluded from the searched body.
    text = (
        "# R\n\n> **applies-when:** `content:only_on_badge`\n>\n"
        "> A recipe.\n\n## When\n\nNothing here repeats that word.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    findings = check_recipe_signature_honesty(tmp_path)
    assert len(findings) == 1
    assert "only_on_badge" in findings[0].message


def test_path_glob_skeleton_absent_fires(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `path:src/ghostdir/*.py`\n>\n"
        "> A recipe.\n\n## When\n\nThe body mentions no such path at all.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    findings = check_recipe_signature_honesty(tmp_path)
    assert len(findings) == 1
    assert "src/ghostdir/" in findings[0].message


def test_path_glob_skeleton_present_is_silent(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `path:*.json`\n>\n"
        "> A recipe.\n\n## When\n\nIt ships as data.json next to the code.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_pure_wildcard_glob_is_honest_by_default(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `path:*`\n>\n"
        "> A recipe.\n\n## When\n\nNo literal skeleton to trace.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_malformed_token_fails_open(tmp_path: Path):
    # A bare token (neither path:/content:) is R11's malformed-token job — S8
    # must NOT double-report it.
    text = "# R\n\n> **applies-when:** `raw.githubusercontent.com`\n>\n> A recipe.\n"
    _write_recipe(tmp_path, "r.md", text)
    assert check_recipe_signature_honesty(tmp_path) == []


def test_missing_badge_is_honesty_silent(tmp_path: Path):
    # No badge is R11's presence job, not honesty's.
    _write_recipe(tmp_path, "r.md", "# R\n\n> **Status:** `reference`\n\n> A recipe.\n")
    assert check_recipe_signature_honesty(tmp_path) == []


def test_readme_is_ignored(tmp_path: Path):
    _write_recipe(tmp_path, "README.md", "# Recipes\n\n> **applies-when:** `content:x`\n")
    assert check_recipe_signature_honesty(tmp_path) == []


def test_missing_recipes_dir_fails_open(tmp_path: Path):
    assert check_recipe_signature_honesty(tmp_path) == []


def test_multiple_tokens_each_checked(tmp_path: Path):
    text = (
        "# R\n\n> **applies-when:** `content:present_one, content:absent_two`\n>\n"
        "> A recipe.\n\n## When\n\nThe body says present_one only.\n"
    )
    _write_recipe(tmp_path, "r.md", text)
    findings = check_recipe_signature_honesty(tmp_path)
    assert len(findings) == 1
    assert "absent_two" in findings[0].message


def test_shipped_recipes_are_honest():
    # The kit's own recipes must carry honest signatures — this checker is
    # silent on the real docs/recipes/ tree (like R11).
    root = Path(__file__).resolve().parents[1]
    assert check_recipe_signature_honesty(root) == []


def test_literal_fragments_helper():
    assert _literal_fragments("*.json") == [".json"]
    assert _literal_fragments("src/checks/*.py") == ["src/checks/", ".py"]
    assert _literal_fragments("*") == []
    assert _literal_fragments("plain/path.md") == ["plain/path.md"]


def test_not_in_strict_subchecks():
    guards = pytest.importorskip("engine.guards")
    assert RECIPE_SIGNATURE_HONESTY_KIND not in guards.STRICT_SUBCHECKS
    assert "check_recipe_signature_honesty" not in guards.STRICT_SUBCHECKS
