"""The measurement-claim provenance advisory (PL-013).

The failure class it guards is narrow and load-bearing: a number published with
no stated instrument **has no source to lose to**, so PL-006's "source wins"
can never adjudicate it and nothing can ever show it wrong. It then compounds
into every decision taken on top of it. The imported case: `4.71 taps/s`
sampled at 30 fps from a natively 60 fps recording, a design constraint built
on that number, and the constraint later cited as the reason the design was
trustworthy — three internally-consistent layers, no gate able to see any of
them.

The load-bearing NEGATIVES are what keep this advisory honest, and most of the
tests below pin them: a document outside a measurements-style directory never
flags (ordinary prose quotes numbers constantly), a non-result badge never
flags (a `plan` may carry illustrative figures), and a document with no numeric
result table never flags. This checker asks ONE binary question — does the
document say where its numbers came from — and never inspects an individual
number.

**The sensitivity tests are the ones that matter most here**, and they exist
because the first draft failed them. Testing for the vocabulary alone
(`measured` / `inferred` / `assumed`) fired on ZERO of the seven spider-swing
documents PL-013 was extracted from: every one already used "measured" in
ordinary prose. `test_incidental_prose_use_still_fires` and its bolded sibling
are that corpus in miniature, and they are the reason the real test requires a
labelled provenance statement AND the vocabulary, not either alone.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_claim_provenance")

from engine.checks.check_claim_provenance import (
    CLAIM_PROVENANCE_KIND,
    check_claim_provenance,
)

# A results document with the shape the checker cares about: a result-bearing
# badge, two numeric table rows, and NO provenance marker anywhere.
_UNMARKED = """\
# Tap rate — 2026-08-01

> **Status:** `reference`

| metric | value |
| --- | ---: |
| taps per second | 4.71 |
| peak burst | 12.0 |
"""

# The same document with its provenance stated.
_MARKED = """\
# Tap rate — 2026-08-01

> **Status:** `reference`

**Provenance:** measured from the device recordings, frame-stepped at the
native 60 fps.

| metric | value |
| --- | ---: |
| taps per second | 6.60 |
| peak burst | 18.0 |
"""


def _write(root: Path, relative: str, text: str = _UNMARKED) -> Path:
    path = root / "docs" / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_unmarked_measurement_doc_fires(tmp_path: Path):
    # The whole point: a result-badged doc under measurements/ presenting
    # numeric rows with no stated instrument.
    _write(tmp_path, "measurements/2026-08-01-taps.md")
    findings = check_claim_provenance(tmp_path)
    assert len(findings) == 1
    finding = findings[0]
    assert finding.kind == CLAIM_PROVENANCE_KIND
    assert finding.path == "measurements/2026-08-01-taps.md"
    assert "provenance" in finding.message


def test_marked_measurement_doc_is_silent(tmp_path: Path):
    # A single well-formed marker answers the binary question the checker asks.
    _write(tmp_path, "measurements/2026-08-01-taps.md", _MARKED)
    assert check_claim_provenance(tmp_path) == []


@pytest.mark.parametrize("marker", ["measured", "inferred", "assumed"])
def test_each_vocabulary_word_silences_a_labelled_doc(tmp_path: Path, marker: str):
    # All three PL-013 words count, in any case, mid-sentence — given a label.
    text = _UNMARKED.replace(
        "| metric | value |",
        f"**Provenance:** {marker.capitalize()} at source resolution.\n\n"
        "| metric | value |",
    )
    _write(tmp_path, "measurements/2026-08-01-taps.md", text)
    assert check_claim_provenance(tmp_path) == []


@pytest.mark.parametrize(
    "sentence",
    [
        # Verbatim shapes from the seven spider-swing documents that motivated
        # PL-013. Each one satisfied the first draft's vocabulary-only test.
        "He is right, and the exploit is now measured.",
        "What each upgrade track is worth, measured per track in isolation.",
        "This was inferred from L20 footage alone.",
        # ...including the two that carry the word in BOLD, which is why
        # emphasis alone was not a sufficient discriminator either.
        "**He is right, and the exploit is now measured.**",
        "It reads **0.00 in every policy measured**, at every level.",
    ],
)
def test_incidental_prose_use_still_fires(tmp_path: Path, sentence: str):
    # THE regression test. A results document that happens to use a provenance
    # word in prose has not stated its provenance, and a checker that goes
    # quiet on it is a false green — PL-006 calls that the check's own bug.
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace("| metric | value |", f"{sentence}\n\n| metric | value |"),
    )
    findings = check_claim_provenance(tmp_path)
    assert len(findings) == 1
    assert "no labelled provenance statement" in findings[0].message


def test_label_without_vocabulary_still_fires(tmp_path: Path):
    # The other half of the AND: labelling a provenance section but never
    # classifying a claim leaves the reader no better off.
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace(
            "| metric | value |",
            "## Provenance\n\nTaken from the recordings.\n\n| metric | value |",
        ),
    )
    findings = check_claim_provenance(tmp_path)
    assert len(findings) == 1
    assert "never classifies a claim" in findings[0].message


@pytest.mark.parametrize(
    "label",
    [
        "## Provenance",
        "### Claim provenance (PL-013)",
        "**Provenance (PL-013): measured** — 60 fps capture.",
        "| Metric | Value | Provenance |",
    ],
)
def test_any_label_shape_counts(tmp_path: Path, label: str):
    # The rule is "the author labelled it", not "the author matched a template".
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace(
            "| metric | value |",
            f"{label}\n\nRate measured at 60 fps.\n\n| metric | value |",
        ),
    )
    assert check_claim_provenance(tmp_path) == []


def test_prose_doc_outside_a_measurement_dir_never_flags(tmp_path: Path):
    # Ordinary docs quote numbers all the time without claiming measurement.
    _write(tmp_path, "technical/testing.md")
    assert check_claim_provenance(tmp_path) == []


def test_benchmarks_and_instrumentation_dirs_are_in_scope(tmp_path: Path):
    # The directory vocabulary is three names, not one.
    _write(tmp_path, "benchmarks/run.md")
    _write(tmp_path, "instrumentation/probe.md")
    findings = check_claim_provenance(tmp_path)
    assert {f.path for f in findings} == {
        "benchmarks/run.md",
        "instrumentation/probe.md",
    }


def test_nested_measurement_dir_is_in_scope(tmp_path: Path):
    # Scope is any ancestor directory, not just the immediate parent.
    _write(tmp_path, "measurements/2026-08/taps.md")
    assert len(check_claim_provenance(tmp_path)) == 1


def test_non_result_badge_never_flags(tmp_path: Path):
    # A `plan` may carry illustrative numbers without claiming to have measured
    # anything — flagging it would be noise, and noise is how advisories die.
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace("`reference`", "`plan`"),
    )
    assert check_claim_provenance(tmp_path) == []


def test_badgeless_doc_never_flags(tmp_path: Path):
    # No badge at all -> not classifiable as result-bearing -> silent.
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace("> **Status:** `reference`\n", ""),
    )
    assert check_claim_provenance(tmp_path) == []


@pytest.mark.parametrize("badge", ["reference", "living-ledger", "audit"])
def test_every_result_badge_is_in_scope(tmp_path: Path, badge: str):
    _write(
        tmp_path,
        "measurements/2026-08-01-taps.md",
        _UNMARKED.replace("`reference`", f"`{badge}`"),
    )
    assert len(check_claim_provenance(tmp_path)) == 1


def test_doc_with_no_numeric_table_never_flags(tmp_path: Path):
    # Prose about a measurement is not a reported result.
    _write(
        tmp_path,
        "measurements/2026-08-01-notes.md",
        "# Notes\n\n> **Status:** `reference`\n\nThe rate looked high.\n",
    )
    assert check_claim_provenance(tmp_path) == []


def test_single_numeric_row_never_flags(tmp_path: Path):
    # One row is below the two-row threshold: a lone incidental figure must not
    # pull a document into scope.
    _write(
        tmp_path,
        "measurements/2026-08-01-notes.md",
        "# Notes\n\n> **Status:** `reference`\n\n| metric | value |\n",
    )
    assert check_claim_provenance(tmp_path) == []


def test_missing_docs_tree_fails_open(tmp_path: Path):
    # Input-gated: no docs/ at all -> [], no exception.
    assert check_claim_provenance(tmp_path) == []


def test_empty_measurements_dir_fails_open(tmp_path: Path):
    (tmp_path / "docs" / "measurements").mkdir(parents=True)
    assert check_claim_provenance(tmp_path) == []


def test_unreadable_document_fails_open(tmp_path: Path):
    # An undecodable file is not a verdict — it is skipped, and the readable
    # sibling is still judged. Fail-open, never fail-loud.
    bad = tmp_path / "docs" / "measurements" / "binary.md"
    bad.parent.mkdir(parents=True, exist_ok=True)
    bad.write_bytes(b"\xff\xfe\x00 not utf-8")
    _write(tmp_path, "measurements/2026-08-01-taps.md")
    findings = check_claim_provenance(tmp_path)
    assert [f.path for f in findings] == ["measurements/2026-08-01-taps.md"]


def test_config_argument_is_accepted_and_ignored(tmp_path: Path):
    # Call-site symmetry with the advisory siblings: cli.py passes config.
    _write(tmp_path, "measurements/2026-08-01-taps.md")
    assert check_claim_provenance(tmp_path, {"cadence": {}}) == check_claim_provenance(
        tmp_path,
    )


def test_one_finding_per_document_not_per_row(tmp_path: Path):
    # The advisory is a document-level nudge. A 40-row table must not emit 40
    # warnings — that is how a warn-only surface becomes unreadable.
    rows = "\n".join(f"| m{i} | {i}.0 |" for i in range(40))
    _write(
        tmp_path,
        "measurements/2026-08-01-wide.md",
        f"# Wide\n\n> **Status:** `reference`\n\n{rows}\n",
    )
    assert len(check_claim_provenance(tmp_path)) == 1


def test_findings_are_sorted_by_path(tmp_path: Path):
    # Deterministic output: two sessions checking the same tree print the same
    # order, so a diff of check output is meaningful.
    for name in ("c.md", "a.md", "b.md"):
        _write(tmp_path, f"measurements/{name}")
    paths = [f.path for f in check_claim_provenance(tmp_path)]
    assert paths == sorted(paths)


def test_not_in_strict_subchecks():
    # PL-013 scope declares this deliberately advisory. A regression that
    # classified it strict would red every adopter carrying an existing
    # measurement document at once — exhortation wearing enforcement's clothes,
    # the precise opposite of the intended nudge.
    guards = pytest.importorskip("engine.guards")
    assert CLAIM_PROVENANCE_KIND not in guards.STRICT_SUBCHECKS
    assert "check_claim_provenance" not in guards.STRICT_SUBCHECKS


def test_claim_provenance_kind_has_remediation():
    # S8 coverage lesson: every emittable advisory Finding kind carries a
    # paste-ready remediation block.
    remediate = pytest.importorskip("engine.checks.check_remediate")
    block = remediate.remediate(CLAIM_PROVENANCE_KIND)
    assert block is not None
    assert "measured" in block
