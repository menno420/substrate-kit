"""The 📊 Model-line payload lint (idea model-line-payload-lint-advisory-2026-07-11).

Pins both halves of the writer/enforcer pair plus the lint's own contract:

- **grammar**: the model-line constants live once in ``engine.grammar`` and
  ``loop.telemetry`` consumes THE SAME objects (writer/enforcer-shared
  constants, EAP §6.8 — the harvest and the lint cannot drift apart); the
  canonical example renderer round-trips through the shared parser and lints
  clean; the taught byte-form appears verbatim in the kit's own
  ``.sessions/README.md`` (the writer-side teaching text).
- **enforcer**: the mutation arc — a malformed payload (wrong separators /
  missing field) fires ``model-line-shape``, the fixed line reads clean, and
  an exact model-ID token fires ``model-line-exact-id``; off-taxonomy effort
  / task-class segments fire their advisories while a decorated (prefix-
  matching) class passes.
- **scope discipline**: only completed cards are judged (in-progress /
  drafted / ``[[fill:]]`` cards never), code spans and fenced blocks never
  fire, last-valid-wins mirrors the harvest, needle absence is the marker
  gate's job (no finding), and the checker is input-gated + fail-open.
- **posture**: advisory-only — ``check --strict`` stays exit 0 on a tree
  whose only defect is a drifted Model payload.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_model_line")

from engine import grammar
from engine.checks.check_model_line import check_model_line, model_line_findings
from engine.loop import telemetry

GOOD_LINE = "- **\N{BAR CHART} Model:** fable-5 · high · feature build\n"


def _card(text: str) -> str:
    """A minimal COMPLETED card wrapping ``text``."""
    return f"# card\n\n> **Status:** `complete`\n\n{text}"


def _kinds(text: str) -> list[str]:
    return [kind for kind, _ in model_line_findings(_card(text))]


# ---------------------------------------------------------------------------
# grammar — one home, shared objects, taught form
# ---------------------------------------------------------------------------


def test_telemetry_consumes_grammar_constants():
    # Identity, not equality: the harvest and the lint judge with THE SAME
    # objects, so one edit reaches both (the EAP §6.8 anti-drift contract).
    assert telemetry.TASK_CLASSES is grammar.MODEL_TASK_CLASSES
    assert telemetry.MODEL_LINE_NEEDLE is grammar.MODEL_LINE_NEEDLE
    assert telemetry._EXACT_MODEL_ID_RE is grammar.EXACT_MODEL_ID_RE
    assert telemetry._parse_model_payload is grammar.parse_model_payload


def test_task_classes_are_the_nine_pl004_classes():
    assert len(grammar.MODEL_TASK_CLASSES) == 9
    assert "feature build" in grammar.MODEL_TASK_CLASSES  # the PL-010 ninth


def test_example_round_trips_and_lints_clean():
    example = grammar.model_line_example()
    # splitlines-shaped, like every real consumer (no trailing newline).
    payload = example.strip("\n").split(grammar.MODEL_LINE_NEEDLE, 1)[1]
    parsed = grammar.parse_model_payload(payload)
    assert parsed == {
        "model": "fable-5",
        "effort": "high",
        "task_class": "feature build",
        "tokens_out": None,
    }
    assert model_line_findings(_card(example)) == []


def test_taught_format_is_what_the_kit_readme_teaches():
    # Writer half: the kit's own .sessions/README.md carries the taught
    # byte-form verbatim — the string lint messages quote as the fix path.
    readme = Path(__file__).resolve().parents[1] / ".sessions" / "README.md"
    assert grammar.MODEL_LINE_TAUGHT_FORMAT in readme.read_text(encoding="utf-8")


# ---------------------------------------------------------------------------
# enforcer — the mutation arc (malformed → fires; fixed → clean; ID → flagged)
# ---------------------------------------------------------------------------


def test_malformed_shape_fires():
    # Wrong separators / missing field: one `·` short of the taught form.
    findings = model_line_findings(_card("- **\N{BAR CHART} Model:** fable-5 · high\n"))
    assert [kind for kind, _ in findings] == ["model-line-shape"]
    message = findings[0][1]
    assert grammar.MODEL_LINE_TAUGHT_FORMAT in message  # the verbatim fix path
    assert "records NOTHING" in message  # loud: harvest silently misses this card


def test_wrong_separator_fires_shape():
    assert _kinds("- **\N{BAR CHART} Model:** fable-5 - high - docs-only\n") == [
        "model-line-shape",
    ]


def test_fixed_line_is_clean():
    assert model_line_findings(_card(GOOD_LINE)) == []


def test_exact_model_id_token_fires():
    findings = model_line_findings(
        _card("- **\N{BAR CHART} Model:** claude-fable-5 · high · docs-only\n"),
    )
    assert [kind for kind, _ in findings] == ["model-line-exact-id"]
    assert "family-level" in findings[0][1]


def test_dated_id_suffix_fires():
    assert _kinds("- **\N{BAR CHART} Model:** fable-5-20260714 · high · docs-only\n") == [
        "model-line-exact-id",
    ]


def test_off_taxonomy_effort_fires():
    findings = model_line_findings(
        _card("- **\N{BAR CHART} Model:** fable-5 · standard effort · docs-only\n"),
    )
    assert [kind for kind, _ in findings] == ["model-line-effort"]
    assert "low | medium | high" in findings[0][1]


def test_unrecorded_effort_is_advisory_silent():
    # The sanctioned TERMINAL value for retro-backfills (idea
    # model-line-unrecorded-effort-marker-2026-07-15): an honest repair of a
    # card whose author never self-reported effort must not nag — the nag
    # invites a later wake to invent a tier, the exact corruption the PR #390
    # sweep avoided.
    from engine.checks.check_model_line import MODEL_EFFORT_UNRECORDED

    assert MODEL_EFFORT_UNRECORDED == "unrecorded"
    # ... and it stays OUT of the live taxonomy — not an escape hatch.
    assert MODEL_EFFORT_UNRECORDED not in grammar.MODEL_EFFORT_VALUES
    assert (
        _kinds("- **\N{BAR CHART} Model:** fable-5 · unrecorded · docs-only\n") == []
    )


def test_unrecorded_silences_only_the_effort_advisory():
    # Other defects on the same line still fire — `unrecorded` sanctions the
    # effort segment only, never the whole payload.
    kinds = _kinds("- **\N{BAR CHART} Model:** claude-fable-5 · unrecorded · release\n")
    assert kinds == ["model-line-exact-id", "model-line-class"]


def test_harvest_records_unrecorded_verbatim():
    # The harvest half is UNCHANGED by the sanction: `unrecorded` lands in
    # the PL-004 row verbatim, like any effort value.
    parsed = telemetry.parse_model_line(
        "- **\N{BAR CHART} Model:** fable-5 · unrecorded · docs-only\n",
    )
    assert parsed is not None and parsed["effort"] == "unrecorded"
    record = telemetry._build_model_usage_record("2026-07-15-retro-fix", parsed)
    assert record["effort"] == "unrecorded"
    assert record["model"] == "fable-5"


def test_off_taxonomy_class_fires():
    findings = model_line_findings(
        _card("- **\N{BAR CHART} Model:** fable-5 · high · release\n"),
    )
    assert [kind for kind, _ in findings] == ["model-line-class"]
    assert "prefix-match" in findings[0][1]


def test_decorated_class_prefix_matches_clean():
    # "docs-only — oracle pin edit" is a valid decorated report, not drift.
    assert (
        _kinds("- **\N{BAR CHART} Model:** fable-5 · high · docs-only — oracle pin edit\n")
        == []
    )


def test_multiple_defects_fire_separately():
    kinds = _kinds("- **\N{BAR CHART} Model:** claude-opus-4-8 · seat-worker · bench\n")
    assert kinds == ["model-line-exact-id", "model-line-effort", "model-line-class"]


# ---------------------------------------------------------------------------
# scope discipline — mirror the harvest, never double-report the marker gate
# ---------------------------------------------------------------------------


def test_no_needle_is_not_this_lints_finding():
    assert model_line_findings(_card("no report here\n")) == []


def test_code_span_mention_never_fires():
    text = "prose about the `\N{BAR CHART} Model:` marker convention\n" + GOOD_LINE
    assert model_line_findings(_card(text)) == []


def test_fenced_example_never_fires():
    text = "```\n- **\N{BAR CHART} Model:** bad\n```\n" + GOOD_LINE
    assert model_line_findings(_card(text)) == []


def test_fill_stand_in_line_is_skipped():
    text = "- **\N{BAR CHART} Model:** [[fill: model]] · effort · class\n"
    assert model_line_findings(_card(text)) == []


def test_last_valid_wins_like_the_harvest():
    # A corrected report later in the card supersedes the drifted one — the
    # lint judges exactly the line the harvest would record.
    drifted = "- **\N{BAR CHART} Model:** claude-fable-5 · high · release\n"
    assert model_line_findings(_card(drifted + GOOD_LINE)) == []
    # And the reverse order judges the (later) drifted line.
    assert [k for k, _ in model_line_findings(_card(GOOD_LINE + drifted))] == [
        "model-line-exact-id",
        "model-line-class",
    ]


def test_malformed_plus_valid_line_is_clean():
    # Shape only fires when NO line parses — the harvest still records the
    # valid line, so there is no telemetry loss to warn about.
    malformed = "- **\N{BAR CHART} Model:** fable-5 · high\n"
    assert model_line_findings(_card(malformed + GOOD_LINE)) == []


# ---------------------------------------------------------------------------
# check_model_line — tree scan, completeness gate, fail-open
# ---------------------------------------------------------------------------


def _write_card(directory: Path, name: str, status: str, line: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    path = directory / name
    path.write_text(
        f"# card\n\n> **Status:** `{status}`\n\n{line}",
        encoding="utf-8",
    )
    return path


def test_scan_flags_only_completed_cards(tmp_path):
    sessions = tmp_path / ".sessions"
    bad = "- **\N{BAR CHART} Model:** claude-fable-5 · high · docs-only\n"
    _write_card(sessions, "2026-07-14-bad.md", "complete", bad)
    _write_card(sessions, "2026-07-14-red.md", "in-progress", bad)
    _write_card(sessions, "2026-07-14-good.md", "complete", GOOD_LINE)
    findings = check_model_line(tmp_path, sessions_dir=".sessions")
    assert [(f.path, f.kind) for f in findings] == [
        (".sessions/2026-07-14-bad.md", "model-line-exact-id"),
    ]


def test_drafted_fill_card_is_never_judged(tmp_path):
    sessions = tmp_path / ".sessions"
    _write_card(
        sessions,
        "2026-07-14-draft.md",
        "complete",
        "[[fill: close-out]]\n- **\N{BAR CHART} Model:** bad · line\n",
    )
    assert check_model_line(tmp_path, sessions_dir=".sessions") == []


def test_readme_is_skipped(tmp_path):
    sessions = tmp_path / ".sessions"
    _write_card(
        sessions,
        "README.md",
        "complete",
        "- **\N{BAR CHART} Model:** claude-x · y · z\n",
    )
    assert check_model_line(tmp_path, sessions_dir=".sessions") == []


def test_missing_sessions_dir_is_input_gated(tmp_path):
    assert check_model_line(tmp_path, sessions_dir=".sessions") == []


def test_window_bounds_the_scan_to_newest_cards(tmp_path):
    # The check-time default judges only the newest completed cards (noise
    # bound: 124/178 of the kit's own historical cards drifted at build
    # time); window=0 is the unbounded measurement lane.
    sessions = tmp_path / ".sessions"
    bad = "- **\N{BAR CHART} Model:** fable-5 · high · release\n"
    _write_card(sessions, "2026-01-01-old-drift.md", "complete", bad)
    _write_card(sessions, "2026-07-14-new-good.md", "complete", GOOD_LINE)
    assert check_model_line(tmp_path, sessions_dir=".sessions", window=1) == []
    unbounded = check_model_line(tmp_path, sessions_dir=".sessions", window=0)
    assert [f.path for f in unbounded] == [".sessions/2026-01-01-old-drift.md"]


# ---------------------------------------------------------------------------
# posture — advisory-only, never exit-affecting
# ---------------------------------------------------------------------------


def test_advisory_never_reds_strict_check(tmp_path, capsys):
    # A tree whose ONLY defect is a drifted Model payload on a completed card
    # must stay exit 0 under --strict; the lint surfaces as a warning.
    from engine.cli import main

    sessions = tmp_path / ".sessions"
    _write_card(
        sessions,
        "2026-07-14-drift.md",
        "complete",
        "- **\N{BAR CHART} Model:** claude-fable-5 · high · docs-only\n"
        "💡 idea\nprevious-session review\n",
    )
    exit_code = main(["check", "--strict", "--target", str(tmp_path)])
    out = capsys.readouterr().out
    assert exit_code == 0
    assert "model-line payload advisory" in out
    assert "model-line-exact-id" in out
    assert "never exit-affecting" in out
