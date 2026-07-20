"""Recipe `applies-when:` DISCOVERY advisory (wave-2 groom S17).

The discovery complement to R11 (well-formedness) + S8 (honesty): for an adopter
tree that has grown a recipe's `applies-when:` structural shape but never
references the recipe, nudge toward it. Advisory only (warn, never
exit-affecting). All tests are hermetic — no network.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_recipe_discovery")

from engine.checks.check_recipe_discovery import (  # noqa: E402
    RECIPE_DISCOVERY_KIND,
    _path_token_matches,
    _signature_matches,
    check_recipe_discovery,
)

# A recipe carrying a two-token signature: a content marker + a path glob.
_RECIPE = """\
# Pinned feed contract

> **Status:** `reference`
>
> **applies-when:** `content:raw.githubusercontent.com, path:*.json`
>
> A recipe about consuming a feed over a raw URL as committed JSON.

## Body

You read raw.githubusercontent.com and it ships as config.json.
"""


def _write_recipe(root: Path, name: str, text: str) -> Path:
    d = root / "docs" / "recipes"
    d.mkdir(parents=True, exist_ok=True)
    p = d / name
    p.write_text(text, encoding="utf-8")
    return p


def _grow_shape(root: Path) -> None:
    """Give the adopter tree BOTH signature tokens: a .json file and a file
    mentioning the raw.githubusercontent.com marker (outside docs/recipes/)."""
    (root / "feed.json").write_text('{"x": 1}\n', encoding="utf-8")
    (root / "loader.py").write_text(
        "URL = 'https://raw.githubusercontent.com/o/r/main/feed.json'\n",
        encoding="utf-8",
    )


# ── the happy path: shape grown, recipe unknown → ONE nudge ───────────────────


def test_matching_tree_unreferenced_recipe_nudges(tmp_path: Path):
    _write_recipe(tmp_path, "pinned-feed-contract.md", _RECIPE)
    _grow_shape(tmp_path)
    findings = check_recipe_discovery(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == RECIPE_DISCOVERY_KIND
    assert findings[0].path == "docs/recipes/pinned-feed-contract.md"


# ── correctness guard 1: self-reference exclusion ─────────────────────────────


def test_recipe_own_markers_do_not_self_match(tmp_path: Path):
    # ONLY the recipe file mentions the markers / there is no adopter .json.
    # The recipe body names raw.githubusercontent.com and config.json, but
    # docs/recipes/ is excluded from the scan, so the tree has NOT grown the
    # shape → no nudge.
    _write_recipe(tmp_path, "pinned-feed-contract.md", _RECIPE)
    assert check_recipe_discovery(tmp_path) == []


# ── correctness guard 2: already-known suppression ────────────────────────────


def test_already_referenced_recipe_is_suppressed(tmp_path: Path):
    _write_recipe(tmp_path, "pinned-feed-contract.md", _RECIPE)
    _grow_shape(tmp_path)
    # A session card in the tree names the recipe by stem → adopter knows it.
    sess = tmp_path / ".sessions"
    sess.mkdir()
    (sess / "card.md").write_text(
        "We adopted pinned-feed-contract already.\n", encoding="utf-8"
    )
    assert check_recipe_discovery(tmp_path) == []


# ── conjunction: a partial match does not fire ────────────────────────────────


def test_partial_signature_does_not_fire(tmp_path: Path):
    _write_recipe(tmp_path, "pinned-feed-contract.md", _RECIPE)
    # Only the content marker is present; no .json file → path token unmatched.
    (tmp_path / "loader.py").write_text(
        "URL = 'https://raw.githubusercontent.com/o/r/main/x'\n", encoding="utf-8"
    )
    assert check_recipe_discovery(tmp_path) == []


# ── input-gating + README skip ────────────────────────────────────────────────


def test_no_recipes_dir_is_silent(tmp_path: Path):
    (tmp_path / "feed.json").write_text("{}\n", encoding="utf-8")
    assert check_recipe_discovery(tmp_path) == []


def test_readme_is_never_a_recipe(tmp_path: Path):
    # README.md carrying a would-be signature is skipped; only graduations count.
    _write_recipe(tmp_path, "README.md", _RECIPE)
    _grow_shape(tmp_path)
    assert check_recipe_discovery(tmp_path) == []


def test_no_badge_recipe_is_silent(tmp_path: Path):
    _write_recipe(
        tmp_path,
        "plain.md",
        "# Plain\n\n> **Status:** `reference`\n>\n> No signature here.\n",
    )
    _grow_shape(tmp_path)
    assert check_recipe_discovery(tmp_path) == []


# ── kit-machinery exclusion: bootstrap.py / .substrate/ never count ───────────


def test_kit_machinery_does_not_satisfy_the_signature(tmp_path: Path):
    _write_recipe(tmp_path, "pinned-feed-contract.md", _RECIPE)
    # The ONLY places the markers appear are excluded machinery: bootstrap.py
    # (the generated dist) mentions the content marker and .substrate/ holds the
    # .json. Neither should count → no false discovery.
    (tmp_path / "bootstrap.py").write_text(
        "# embeds raw.githubusercontent.com and feed.json literally\n",
        encoding="utf-8",
    )
    sub = tmp_path / ".substrate"
    sub.mkdir()
    (sub / "backup.json").write_text("{}\n", encoding="utf-8")
    assert check_recipe_discovery(tmp_path) == []


# ── pure-logic units ──────────────────────────────────────────────────────────


def test_path_token_matches_glob_across_slashes_and_basename():
    rels = ["data/nested/feed.json", "src/loader.py"]
    assert _path_token_matches("*.json", rels) is True  # * crosses /
    assert _path_token_matches("data/nested/*.json", rels) is True
    assert _path_token_matches("*.toml", rels) is False


def test_signature_matches_requires_all_tokens():
    rels = ["feed.json"]
    contents = ["reads raw.githubusercontent.com here"]
    both = ["content:raw.githubusercontent.com", "path:*.json"]
    assert _signature_matches(both, rels, contents) is True
    # drop the json file → path token fails → conjunction fails
    assert _signature_matches(both, [], contents) is False


def test_malformed_token_fails_open_in_matcher():
    # A malformed token (R11's job, not discovery's) is treated as satisfied so
    # discovery never depends on a broken tag.
    rels = ["feed.json"]
    contents = ["raw.githubusercontent.com"]
    toks = ["content:raw.githubusercontent.com", "path:*.json", "garbage-token"]
    assert _signature_matches(toks, rels, contents) is True
