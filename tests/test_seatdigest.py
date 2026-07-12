"""Seat-digest render surface + drift guard (grounded-skills slice 6, §7.6).

Pins the slice-6 contracts: the grammar fence-prefix pairs (the machine
extraction contract fleet-manager's regen consumes), the per-block budget
(digest + pointer, never inline), mechanical venue filtering (Project-seat
default ``autonomous-project`` + ``any``), render determinism, the adopt
plant + upgrade refresh covenant (kit-written copies regenerate; hand edits
downgrade to a report line, never clobbered), the ``seat-digest`` CLI regen
(venue preservation), and the advisory drift checker's green/red paths.
"""

from __future__ import annotations

from pathlib import Path

from engine import grammar
from engine.adopt import adopt, doc_is_untouched, record_doc_hash
from engine.checks.check_seat_digest import check_seat_digest
from engine.cli import cmd_seat_digest, main
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import build_context, find_placeholders
from engine.seatdigest import (
    seat_digest_document,
    seat_digest_relpath,
    seat_digest_text,
    skills_digest_block,
    walls_digest_block,
    walls_digest_venues,
)
from engine.skills.skills import SKILLS
from engine.upgrade import refresh_seat_digest, upgrade_report_text

_DIGEST_REL = "docs/seat-digest.md"


def _adopted(tmp_path: Path):
    root = tmp_path / "repo"
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    return root, config, backend


def _context(root: Path, config: Config) -> dict[str, str]:
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    return build_context(backend.data) if backend.data else {}


# A hand-built ledger exercising every append-log row class the digest
# must classify: venue'd wall (in-filter), legacy five-field wall (venue
# `any` by the pinned compat contract), a capability entry (never a wall),
# and a wall verified in an out-of-filter venue.
_MINI_LEDGER = f"""# demo — session capabilities & walls

{grammar.CAPABILITY_SEED_BEGIN}

## Posture decision rule — establish your venue first

- Owner-live: act directly.

## Walls — verified blocked (use the workaround; don't rediscover)

- `any` · **Tag push via git**: HTTP 403 → use the workflow_dispatch
  release path. — LAST-VERIFIED: 2026-07-12
- `routine-fired` · **Silent prompt-stalls**: pre-route around recorded
  stall classes. — LAST-VERIFIED: 2026-07-12

{grammar.CAPABILITY_SEED_END}

## Append log — newest first

Format: `{grammar.CAPABILITY_LOG_TAUGHT_FORMAT}`

- 2026-07-12 · wall · autonomous-project · MCP PR reads serve stale merge
  state · observed ~25 min lag · probe the tree instead
- 2026-07-11 · wall · legacy five-field wall finding · exact error text ·
  documented workaround
- 2026-07-10 · capability · autonomous-project · create_trigger works ·
  proven · none needed
- 2026-07-09 · wall · subagent · child sessions refused merging · refusal
  text · coordinator merges
"""


# ── grammar: the machine extraction contract ────────────────────────────────


def test_fence_prefixes_prefix_match_their_full_markers():
    # Prefix-matching is the contract: a wording tweak in the trailing
    # marker text must never orphan a fence (the capability-seed pattern).
    assert grammar.SKILLS_DIGEST_BEGIN.startswith(grammar.SKILLS_DIGEST_BEGIN_PREFIX)
    assert grammar.SKILLS_DIGEST_END.startswith(grammar.SKILLS_DIGEST_END_PREFIX)
    assert grammar.WALLS_DIGEST_END.startswith(grammar.WALLS_DIGEST_END_PREFIX)
    marker = grammar.walls_digest_begin_marker(("autonomous-project", "any"))
    assert marker.startswith(grammar.WALLS_DIGEST_BEGIN_PREFIX)
    # The three pairs are distinct namespaces (a consumer scanning one pair
    # can never capture another block's marker).
    prefixes = {
        grammar.SKILLS_DIGEST_BEGIN_PREFIX,
        grammar.WALLS_DIGEST_BEGIN_PREFIX,
        grammar.CAPABILITY_SEED_BEGIN_PREFIX,
    }
    assert len(prefixes) == 3


def test_walls_begin_marker_roundtrips_its_venue_filter():
    marker = grammar.walls_digest_begin_marker(("routine-fired", "any"))
    match = grammar.WALLS_DIGEST_VENUES_RE.search(marker)
    assert match is not None
    assert match.group(1) == "routine-fired,any"
    assert walls_digest_venues(marker) == ("routine-fired", "any")


def test_default_venues_are_grammar_venue_tokens():
    # The Project-seat default filter is drawn from the slice-5 venue
    # vocabulary — never an ad-hoc spelling.
    for venue in grammar.SEAT_DIGEST_DEFAULT_VENUES:
        assert venue in grammar.CAPABILITY_VENUE_TOKENS
    assert grammar.SEAT_DIGEST_DEFAULT_VENUES == ("autonomous-project", "any")


def test_venue_parse_fails_open_to_the_default():
    assert walls_digest_venues("no marker here") == (
        grammar.SEAT_DIGEST_DEFAULT_VENUES
    )
    # Unknown tokens are dropped; an all-unknown filter falls back whole.
    assert walls_digest_venues("venues=made-up,any") == ("any",)
    assert walls_digest_venues("venues=made-up") == (
        grammar.SEAT_DIGEST_DEFAULT_VENUES
    )


# ── the skills digest block ──────────────────────────────────────────────────


def test_skills_digest_names_every_skill_within_budget():
    block = skills_digest_block()
    assert block.startswith(grammar.SKILLS_DIGEST_BEGIN)
    assert block.endswith(grammar.SKILLS_DIGEST_END)
    for skill in SKILLS:
        assert f"`{skill['name']}`" in block
    assert len(block) <= grammar.SEAT_DIGEST_BLOCK_BUDGET
    assert "`docs/SKILLS.md`" in block  # digest + pointer, never inline
    assert block == skills_digest_block()  # deterministic


# ── the walls digest block ───────────────────────────────────────────────────


def test_walls_digest_filters_by_venue_mechanically():
    block = walls_digest_block(_MINI_LEDGER)
    # In-filter: `any` seed row, `autonomous-project` append row, and the
    # legacy five-field wall (compat contract: venue-less reads as `any`).
    assert "Tag push via git" in block
    assert "MCP PR reads serve stale merge state" in block
    assert "legacy five-field wall finding" in block
    # Out-of-filter venues and non-wall tags stay out.
    assert "Silent prompt-stalls" not in block
    assert "child sessions refused merging" not in block
    assert "create_trigger works" not in block  # a capability, never a wall
    assert len(block) <= grammar.SEAT_DIGEST_BLOCK_BUDGET
    assert "`docs/CAPABILITIES.md`" in block


def test_walls_digest_venue_filter_is_parameterizable():
    block = walls_digest_block(_MINI_LEDGER, venues=("routine-fired", "any"))
    assert "Silent prompt-stalls" in block
    assert "MCP PR reads serve stale merge state" not in block
    assert "venues=routine-fired,any" in block  # the filter rides the marker


def test_walls_digest_strips_freshness_stamps():
    # The digest points at the ledger for evidence/freshness — stamps stay
    # at the source (and a date in the digest would churn the byte compare).
    block = walls_digest_block(_MINI_LEDGER)
    assert "LAST-VERIFIED" not in block


def test_walls_digest_truncates_into_the_budget_with_a_pointer_row():
    walls = "\n".join(
        f"- `any` · **Wall {i}**: a long finding line about surface {i} that "
        "keeps going with enough words to cost real budget → workaround "
        f"number {i}."
        for i in range(50)
    )
    ledger = _MINI_LEDGER.replace(
        "- `any` · **Tag push via git**: HTTP 403 → use the workflow_dispatch\n"
        "  release path. — LAST-VERIFIED: 2026-07-12",
        walls,
    )
    block = walls_digest_block(ledger)
    assert len(block) <= grammar.SEAT_DIGEST_BLOCK_BUDGET
    assert "more — read `docs/CAPABILITIES.md`." in block


def test_walls_digest_missing_ledger_renders_honest_placeholder():
    block = walls_digest_block(None)
    assert "no capability ledger found" in block
    assert len(block) <= grammar.SEAT_DIGEST_BLOCK_BUDGET


def test_walls_digest_no_matching_walls_says_so():
    ledger = "# bare\n\n## Append log\n\n(nothing yet)\n"
    block = walls_digest_block(ledger)
    assert "no walls recorded for these venues" in block


# ── the full document ────────────────────────────────────────────────────────


def test_document_carries_both_fences_and_the_contracts():
    doc = seat_digest_document("demo", _MINI_LEDGER)
    order = [
        doc.index(grammar.SKILLS_DIGEST_BEGIN_PREFIX),
        doc.index(grammar.SKILLS_DIGEST_END_PREFIX),
        doc.index(grammar.WALLS_DIGEST_BEGIN_PREFIX),
        doc.index(grammar.WALLS_DIGEST_END_PREFIX),
    ]
    assert order == sorted(order)  # skills fence, then walls fence
    # The extraction contract names all three prefix pairs where the
    # artifact lives (the fm regen tool's interface documentation).
    assert grammar.CAPABILITY_SEED_BEGIN_PREFIX in doc
    # The no-third-copy deferral chain (plan §4.2e), stated explicitly.
    assert "seat-local source of truth" in doc
    assert "derived render" in doc.lower()
    assert "fleet aggregation point" in doc
    assert "No third authored copy" in doc
    # Deterministic + no interview slots (a generated doc must never carry
    # the UNRENDERED banner or a byte-churning date).
    assert doc == seat_digest_document("demo", _MINI_LEDGER)
    assert not find_placeholders(doc)
    assert "> **Status:** `reference`" in doc


# ── adopt: the plant ─────────────────────────────────────────────────────────


def test_adopt_plants_the_digest_and_records_its_hash(tmp_path):
    root, config, backend = _adopted(tmp_path)
    path = root / _DIGEST_REL
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    # Rendered from the just-planted ledger, not a placeholder.
    assert "workflow_dispatch" in text
    assert grammar.SKILLS_DIGEST_BEGIN_PREFIX in text
    assert doc_is_untouched(backend, _DIGEST_REL, text)
    # Fresh plant is byte-identical to the shared render path (the drift
    # guard's green precondition).
    assert text == seat_digest_text(root, config, _context(root, config))


def test_adopt_keeps_an_existing_digest(tmp_path):
    root, config, backend = _adopted(tmp_path)
    path = root / _DIGEST_REL
    path.write_text("hand-rolled\n", encoding="utf-8")
    report = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert any(f"kept: {_DIGEST_REL}" in line for line in report)
    assert path.read_text(encoding="utf-8") == "hand-rolled\n"


# ── upgrade: the derived-render refresh ──────────────────────────────────────


def test_refresh_regenerates_a_kit_written_digest_after_ledger_moves(tmp_path):
    root, config, backend = _adopted(tmp_path)
    ledger = root / "docs" / "CAPABILITIES.md"
    appended = grammar.capability_log_line_example(venue="autonomous-project")
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + appended,
        encoding="utf-8",
    )
    lines = refresh_seat_digest(root, config, backend)
    assert any("regenerated" in ln for ln in lines)
    after = (root / _DIGEST_REL).read_text(encoding="utf-8")
    assert "fire_trigger on a cross-session binding refused" in after
    # The regen re-records the hash: the doc stays kit-written for the
    # NEXT refresh (unlike the consumer-owned ledger, which never does).
    assert doc_is_untouched(backend, _DIGEST_REL, after)


def test_refresh_is_an_honest_noop_when_current(tmp_path):
    root, config, backend = _adopted(tmp_path)
    before = (root / _DIGEST_REL).read_text(encoding="utf-8")
    lines = refresh_seat_digest(root, config, backend)
    assert any("already current" in ln for ln in lines)
    assert (root / _DIGEST_REL).read_text(encoding="utf-8") == before


def test_refresh_never_clobbers_a_hand_edited_digest(tmp_path):
    root, config, backend = _adopted(tmp_path)
    path = root / _DIGEST_REL
    edited = path.read_text(encoding="utf-8") + "\nhand note\n"
    path.write_text(edited, encoding="utf-8")
    lines = refresh_seat_digest(root, config, backend)
    assert any("NOT regenerated" in ln for ln in lines)
    assert any("bootstrap.py seat-digest" in ln for ln in lines)
    assert path.read_text(encoding="utf-8") == edited


def test_refresh_preserves_the_committed_venue_filter(tmp_path):
    root, config, backend = _adopted(tmp_path)
    custom = seat_digest_text(
        root,
        config,
        _context(root, config),
        venues=("routine-fired", "any"),
    )
    path = root / _DIGEST_REL
    path.write_text(custom, encoding="utf-8")
    record_doc_hash(backend, _DIGEST_REL, custom)
    ledger = root / "docs" / "CAPABILITIES.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8")
        + grammar.capability_log_line_example(venue="routine-fired"),
        encoding="utf-8",
    )
    lines = refresh_seat_digest(root, config, backend)
    assert any("regenerated" in ln for ln in lines)
    after = path.read_text(encoding="utf-8")
    assert "venues=routine-fired,any" in after  # never silently reset


def test_refresh_skips_when_no_digest_planted(tmp_path):
    root, config, backend = _adopted(tmp_path)
    (root / _DIGEST_REL).unlink()
    assert refresh_seat_digest(root, config, backend) == []


def test_upgrade_report_carries_the_seat_digest_section():
    text = upgrade_report_text(
        "1.0.0",
        [],
        [],
        seat_digest=["seat-digest: regenerated docs/seat-digest.md (…)"],
    )
    assert "## Seat-digest refresh" in text
    assert "regenerated docs/seat-digest.md" in text
    # Absent lines → absent section (silence is honest).
    assert "Seat-digest refresh" not in upgrade_report_text("1.0.0", [], [])


# ── the CLI regen ────────────────────────────────────────────────────────────


def test_cmd_seat_digest_regenerates_and_rerecords(tmp_path):
    root, config, backend = _adopted(tmp_path)
    ledger = root / "docs" / "CAPABILITIES.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + grammar.capability_log_line_example(
            venue="autonomous-project",
        ),
        encoding="utf-8",
    )
    assert cmd_seat_digest(root) == 0
    text = (root / _DIGEST_REL).read_text(encoding="utf-8")
    assert "fire_trigger on a cross-session binding refused" in text
    fresh_backend = JsonStateBackend(root / config.state_dir / "state.json")
    assert doc_is_untouched(fresh_backend, _DIGEST_REL, text)


def test_cmd_seat_digest_venue_override_and_preservation(tmp_path):
    root, config, backend = _adopted(tmp_path)
    # Override writes the requested filter onto the marker…
    assert (
        main(
            [
                "seat-digest",
                "--target",
                str(root),
                "--venue",
                "routine-fired",
                "--venue",
                "any",
            ],
        )
        == 0
    )
    text = (root / _DIGEST_REL).read_text(encoding="utf-8")
    assert "venues=routine-fired,any" in text
    # …and a bare regen preserves it instead of resetting to the default.
    assert cmd_seat_digest(root) == 0
    text = (root / _DIGEST_REL).read_text(encoding="utf-8")
    assert "venues=routine-fired,any" in text


# ── the drift guard (advisory, PL-008) ───────────────────────────────────────


def test_checker_green_on_a_fresh_adopt(tmp_path):
    root, config, _backend = _adopted(tmp_path)
    assert check_seat_digest(root, config, context=_context(root, config)) == []


def test_checker_flags_a_stale_digest_and_names_the_fix(tmp_path):
    root, config, _backend = _adopted(tmp_path)
    ledger = root / "docs" / "CAPABILITIES.md"
    ledger.write_text(
        ledger.read_text(encoding="utf-8") + grammar.capability_log_line_example(
            venue="autonomous-project",
        ),
        encoding="utf-8",
    )
    findings = check_seat_digest(root, config, context=_context(root, config))
    assert [f.kind for f in findings] == ["seat-digest-stale"]
    assert "bootstrap.py seat-digest" in findings[0].message
    # The named fix actually clears the finding (the closed loop).
    assert cmd_seat_digest(root) == 0
    assert check_seat_digest(root, config, context=_context(root, config)) == []


def test_checker_rerenders_with_the_committed_venue_filter(tmp_path):
    # A non-default venue choice is NOT drift: the fresh render must reuse
    # the committed doc's own venues= marker.
    root, config, _backend = _adopted(tmp_path)
    assert cmd_seat_digest(root, venues=["routine-fired", "any"]) == 0
    assert check_seat_digest(root, config, context=_context(root, config)) == []


def test_checker_flags_an_over_budget_block(tmp_path):
    root, config, _backend = _adopted(tmp_path)
    path = root / _DIGEST_REL
    text = path.read_text(encoding="utf-8")
    padding = "- padding row far beyond any budget\n" * 60
    bloated = text.replace(
        grammar.SKILLS_DIGEST_END,
        padding + grammar.SKILLS_DIGEST_END,
    )
    path.write_text(bloated, encoding="utf-8")
    kinds = {
        f.kind for f in check_seat_digest(root, config, context=_context(root, config))
    }
    assert kinds == {"seat-digest-stale", "seat-digest-over-budget"}


def test_checker_engages_only_when_the_digest_exists(tmp_path):
    root, config, _backend = _adopted(tmp_path)
    (root / _DIGEST_REL).unlink()
    assert check_seat_digest(root, config, context=_context(root, config)) == []
