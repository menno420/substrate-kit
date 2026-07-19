"""Append-log ⇄ Walls-correction disagreement advisory (night-run groom R7).

``docs/CAPABILITIES.md`` states a capability's status in two places that can
drift: a durable ``## Walls`` *correction* row ("X is NOT a wall") and the newest
``## Append log`` verdict on that capability (its ``capability|wall`` type
token). When a correction lands in one place but not the other, the ledger
contradicts itself — the merge/arm/flip self-contradiction that persisted a full
day. This advisory (warn, never exit-affecting) fires ONE finding per capability
family when the two sides disagree, and is silent when they agree or when either
side is absent.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_wall_ledger_agreement")

from engine.checks.check_wall_ledger_agreement import (  # noqa: E402
    WALL_LEDGER_DISAGREE_KIND,
    _canonicalize_title,
    _extract_bold_title,
    _keys_match,
    check_wall_ledger_agreement,
)


def _write_ledger(root: Path, text: str) -> Path:
    docs = root / "docs"
    docs.mkdir(parents=True, exist_ok=True)
    path = docs / "CAPABILITIES.md"
    path.write_text(text, encoding="utf-8")
    return path


# The historical bug: a ## Walls correction says merging is NOT a wall, but the
# newest ## Append log entry on merging still calls it a wall. They disagree.
_DISAGREE = """\
# demo — session capabilities & walls

## Walls — verified blocked

- **Merging own PRs is NOT a wall** (corrected 2026-07-18): agents merge their
  own green PRs.

## Append log — newest first

- 2026-07-17 · wall · **The classifier denies merging a PR** · e · route to owner
- 2026-07-10 · capability · merging own PRs is normal agent work · e · w
"""


def test_disagreement_fires(tmp_path: Path):
    _write_ledger(tmp_path, _DISAGREE)
    findings = check_wall_ledger_agreement(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == WALL_LEDGER_DISAGREE_KIND
    assert findings[0].path == "docs/CAPABILITIES.md"
    assert "merge/arm/flip" in findings[0].message


# Agreement: the Walls correction (NOT a wall) and the NEWEST append-log entry
# (capability) both say available. The older wall entry is superseded and must
# NOT be consulted — newest-first. This mirrors the real shipped ledger.
_AGREE = """\
## Walls — verified blocked

- **Merging own PRs is NOT a wall** (corrected 2026-07-18).

## Append log — newest first

- 2026-07-18 · capability · CORRECTION — merging is normal agent work now · e · w
- 2026-07-17 · wall · the classifier denies merging · e · w
"""


def test_agreement_is_silent(tmp_path: Path):
    _write_ledger(tmp_path, _AGREE)
    assert check_wall_ledger_agreement(tmp_path) == []


def test_newest_append_entry_wins(tmp_path: Path):
    # The older wall entry sits under a newer capability entry; using the newest
    # (capability) makes it agree with the NOT-a-wall Walls correction, so it is
    # silent. Regression guard for "newest first".
    _write_ledger(tmp_path, _AGREE)
    assert check_wall_ledger_agreement(tmp_path) == []


def test_no_walls_correction_is_silent(tmp_path: Path):
    # An append-log wall entry with NO ## Walls correction row → nothing to
    # cross-check → silent.
    _write_ledger(
        tmp_path,
        "## Append log — newest first\n\n- 2026-07-17 · wall · merging denied · e · w\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_no_appendlog_entry_is_silent(tmp_path: Path):
    # A ## Walls correction with NO append-log entry for the family → silent.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n- **Merging is NOT a wall** (corrected).\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_unrelated_capability_not_compared(tmp_path: Path):
    # A Walls correction and append-log entry about DIFFERENT capabilities never
    # cross-fire — the family keying isolates them.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Merging own PRs is NOT a wall** (corrected).\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-17 · wall · branch deletion is 403 everywhere · e · w\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_missing_file_fails_open(tmp_path: Path):
    assert check_wall_ledger_agreement(tmp_path) == []


def test_reverse_disagreement_fires(tmp_path: Path):
    # Mirror case: a ## Walls correction re-asserts a wall while the newest
    # append-log entry says capability. Still a disagreement.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Merging is a wall after all** (corrected 2026-07-19): the classifier blocks it.\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-18 · capability · merging own PRs is normal agent work · e · w\n",
    )
    findings = check_wall_ledger_agreement(tmp_path)
    assert len(findings) == 1
    assert "merge/arm/flip" in findings[0].message


def test_not_in_strict_subchecks():
    # Advisory-only: must stay OFF the exit-affecting strict surface, or a ledger
    # that momentarily drifted would red every adopter.
    guards = pytest.importorskip("engine.guards")
    assert WALL_LEDGER_DISAGREE_KIND not in guards.STRICT_SUBCHECKS
    assert "check_wall_ledger_agreement" not in guards.STRICT_SUBCHECKS


# --- S12: auto-derived families from ledger bold titles ---------------------

# A NON-seeded capability (branch deletion) whose bold title appears in BOTH
# sections and disagrees: Walls says NOT a wall (AVAILABLE), the newest append
# entry still calls it a wall (BLOCKED). The seeded merge/arm/flip family never
# touches it — only the auto-derived pass catches it.
_DERIVED_DISAGREE = """\
## Walls — verified blocked

- **Branch deletion is NOT a wall** (corrected 2026-07-19): agents delete branches.

## Append log — newest first

- 2026-07-18 · wall · **branch deletion is 403 everywhere** · e · owner deletes it
"""


def test_derived_family_disagreement_fires(tmp_path: Path):
    _write_ledger(tmp_path, _DERIVED_DISAGREE)
    findings = check_wall_ledger_agreement(tmp_path)
    assert len(findings) == 1
    assert findings[0].kind == WALL_LEDGER_DISAGREE_KIND
    assert findings[0].path == "docs/CAPABILITIES.md"
    # The derived finding names the capability by its Walls bold title.
    assert "Branch deletion is NOT a wall" in findings[0].message
    # And it is NOT mislabelled as the seeded family.
    assert "merge/arm/flip" not in findings[0].message


def test_derived_family_agreement_is_silent(tmp_path: Path):
    # Same capability, both sides AVAILABLE — no disagreement, no finding.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Branch deletion is NOT a wall** (corrected 2026-07-19): agents do it.\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-18 · capability · **branch deletion is now agent-side** · e · w\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_derived_requires_bold_title_on_both_sides(tmp_path: Path):
    # The append-log entry names branch deletion but carries NO bold title, so no
    # family is derivable from it — silent (nothing to cross-check).
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Branch deletion is NOT a wall** (corrected 2026-07-19).\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-18 · wall · branch deletion is 403 everywhere · e · owner\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_derived_unrelated_titles_do_not_false_pair(tmp_path: Path):
    # Two bold titles with disjoint keyword sets never cross-fire.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Snapshot ingest is NOT a wall** (corrected): the relay accepts it.\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-18 · wall · **branch deletion is 403 everywhere** · e · owner\n",
    )
    assert check_wall_ledger_agreement(tmp_path) == []


def test_derived_not_double_reported_with_seeded(tmp_path: Path):
    # A merge capability carrying bold titles in BOTH sections must still fire
    # EXACTLY ONCE — through the seeded family — not a second derived finding.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Merging own PRs is NOT a wall** (corrected 2026-07-18).\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-17 · wall · **The classifier denies merging a PR** · e · owner\n",
    )
    findings = check_wall_ledger_agreement(tmp_path)
    assert len(findings) == 1
    assert "merge/arm/flip" in findings[0].message


def test_derived_fires_once_per_capability(tmp_path: Path):
    # Two append-log entries name the same derived capability; only the NEWEST
    # (topmost) is compared, and the capability fires at most once.
    _write_ledger(
        tmp_path,
        "## Walls — verified blocked\n\n"
        "- **Branch deletion is NOT a wall** (corrected 2026-07-19).\n\n"
        "## Append log — newest first\n\n"
        "- 2026-07-18 · wall · **branch deletion is 403 everywhere** · e · owner\n"
        "- 2026-07-10 · capability · **branch deletion works fine now** · e · w\n",
    )
    findings = check_wall_ledger_agreement(tmp_path)
    # Newest = the 07-18 wall entry (BLOCKED) vs Walls AVAILABLE → one finding.
    assert len(findings) == 1
    assert "Branch deletion is NOT a wall" in findings[0].message


def test_extract_bold_title():
    assert _extract_bold_title("- x **Foo bar** baz") == "Foo bar"
    # First span wins; internal whitespace/newlines collapse.
    assert _extract_bold_title("- **wrapped\n  title** rest **second**") == (
        "wrapped title"
    )
    assert _extract_bold_title("- no bold here") is None


def test_canonicalize_title_and_keys_match():
    # Stopwords ("is", "not", "a") + the ledger-noise "wall" drop out.
    assert _canonicalize_title("Branch deletion is NOT a wall") == frozenset(
        {"branch", "deletion"}
    )
    # Order/filler invariant; sub-3-char tokens dropped.
    assert _keys_match(
        _canonicalize_title("Branch deletion is NOT a wall"),
        _canonicalize_title("branch deletion is 403 everywhere"),
    )
    # Disjoint keyword sets do not match.
    assert not _keys_match(
        _canonicalize_title("Snapshot ingest is NOT a wall"),
        _canonicalize_title("branch deletion is 403"),
    )
    # An empty key never matches.
    assert not _keys_match(frozenset(), frozenset({"branch"}))
