"""ORDER 016 seat-item 4 — Q-0271 + Q-0272 graduated into templates.

Pins the two graduation workstreams:

1. **Autonomy rider (Q-0271)** — superbot fleet-rearm-2026-07-12.md §3's
   twelve items land as [PL-012] in ``docs/program/rulings.md`` (the ruling
   body's one home), with the adopter-side operating form folded into the
   ``CONSTITUTION.md.tmpl`` autonomy rails (items 1-8, 11-12) and the
   ``routines.md.tmpl`` seat-wake section (items 9-10) — citing PL-012,
   never copying the ruling body (the register's citation rule).
2. **Reading path (Q-0272)** — superbot docs/fleet-reading-path.md's
   pattern lands as ``reading-path.md.tmpl`` planted at
   ``docs/reading-path.md`` (ADOPT_PLAN), slot-driven
   (``fleet_dark_repos`` / ``fleet_status_command`` / ``fleet_siblings``,
   none critical), routed from orientation so the plant never orphans an
   adopter's ``check --strict``.

Phrases are pinned directly against the templates (the test_grounded_tail
convention): no checker consumes these doctrine sentences; the enforcers in
play are the generic reachability walk (``check_docs.check_reachable``) and
the program-law pointer rules (``scripts/check_program_law.py``).
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.adopt")

from engine.adopt import ADOPT_PLAN, adopt
from engine.checks.check_docs import run_doc_checks
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import build_context, find_placeholders, load_templates, render


def _template(name: str) -> str:
    return load_templates()[name]


def _flat(text: str) -> str:
    """Collapse whitespace so a phrase pin survives markdown line-wrapping."""
    return " ".join(text.split())


def _adopt_into(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    return root, config


# ── workstream A: the autonomy rider (Q-0271, PL-012) ────────────────────────

# The rails' load-bearing sentences — the adopter-side operating form of
# rider items 1-8 + 11-12 (fleet-rearm §3), each citing PL-012 for depth.
_RAILS_RIDER_PINS = (
    # items 1+2 — owner absent = normal; silence = consent
    "Owner absent = normal; silence = consent.",
    "hallucinated gate",
    "reaction after visibility, never pre-approval",
    # item 3 — the landing ladder
    "An open PR is never a reason to stop.",
    "Open READY (never draft)",
    "queue ONE owner item for the systemic cause",
    # item 5 — decide-and-flag (architectural included)
    "architectural included",
    "decided-and-flagged",
    # item 6 — the owner-only list + queue-and-continue
    "Ask first only for the owner-only classes:",
    "destructive prod-data ops",
    "Queue-and-continue:",
    'never end a turn "waiting"',
    # item 4 — probe-before-wall rides the capabilities discovery rule
    "one refusal ≠ a permanent wall",
    # items 7+8 — work ladder / generative rung; routed uncertainty
    "Never idle on a drained queue.",
    "generative",
    "routed, not",
    # item 11 — volatile facts
    "Volatile facts expire.",
    "the committed tree wins",
    # item 12 — quality floor
    "The quality floor is unchanged.",
    "Never-wait ≠ bypass CI",
)


def test_constitution_rails_carry_the_rider():
    tmpl = _flat(_template("CONSTITUTION.md.tmpl"))
    for phrase in _RAILS_RIDER_PINS:
        assert phrase in tmpl, phrase


def test_constitution_rails_cite_pl012_not_the_body():
    # Cite PL-IDs for depth; the twelve-item ruling body lives only in the
    # register (docs/program/rulings.md — the citation rule).
    rails = _template("CONSTITUTION.md.tmpl").split(
        "## Autonomy rails — act vs. ask", 1
    )[1].split("\n## ", 1)[0]
    assert "PL-012" in rails
    assert "AUTONOMY RIDER v1" not in rails  # the body stays in the register


def test_constitution_rails_retire_the_ask_on_architectural_rail():
    # Q-0271 supersedes the old "Ask before ... large / cross-cutting
    # (architectural)" rail for reversible calls — the superseded text must
    # not survive alongside the new rails (update, don't stack).
    tmpl = _flat(_template("CONSTITUTION.md.tmpl"))
    assert "large / cross-cutting (architectural)" not in tmpl


def test_constitution_rails_keep_the_owner_attention_bullet():
    rails = _template("CONSTITUTION.md.tmpl").split(
        "## Autonomy rails — act vs. ask", 1
    )[1].split("\n## ", 1)[0]
    assert "Owner attention is the scarcest resource." in _flat(rails)


def test_constitution_rails_are_portably_worded():
    # Family-level phrasing only: no fleet-manager queue paths, no model
    # ids, no fleet repo names (the rider's fm:-specific mechanics are
    # generalized on graduation).
    rails = _template("CONSTITUTION.md.tmpl").split(
        "## Autonomy rails — act vs. ask", 1
    )[1].split("\n## ", 1)[0]
    for needle in ("fleet-manager", "menno420", "superbot", "fm #", "SIM-REQUEST"):
        assert needle not in rails, needle


# Seat-wake mechanics (rider items 9-10) fold into the routines doctrine.
_SEAT_WAKE_PINS = (
    "Seat wake discipline",
    "consume-before-re-arm",
    "exactly ONE outstanding pacemaker tick",
    "a wake with nothing to do is a SILENT no-op",
    "End-of-turn invariant:",
    "exactly one future tick armed",
    "re-stamped LAST after",
    "zero armed wakes is a seat-killing bug",
    "PL-012",
)


def test_routines_template_carries_the_seat_wake_mechanics():
    tmpl = _flat(_template("routines.md.tmpl"))
    for phrase in _SEAT_WAKE_PINS:
        assert phrase in tmpl, phrase


def test_register_carries_pl012_with_q0271_provenance():
    from pathlib import Path

    register = (
        Path(__file__).resolve().parents[1] / "docs" / "program" / "rulings.md"
    ).read_text(encoding="utf-8")
    assert "## [PL-012]" in register
    assert "Q-0271" in register
    # Q-0241 history stays intact: PL-002 is extended, never rewritten.
    assert "## [PL-002] Never-wait autonomy for the rebuild" in register
    assert "Q-0241" in register
    assert "Extends PL-002, does not supersede it" in _flat(register)


# ── workstream B: the reading path (Q-0272) ──────────────────────────────────

_READING_PATH_SLOTS = {"fleet_dark_repos", "fleet_status_command", "fleet_siblings"}

_READING_PATH_PINS = (
    "The standing authorization",
    "Read-only cross-repo access is standing-authorized",
    "The one command",
    "The sibling map (who is who)",
    "Tiered depth (spend turns by task depth)",
    "Tier 0",
    "Tier 3",
    "Truth rules (carry into every cross-repo read)",
    "Heartbeats are dated snapshots",
    "One writer per file",
    "⚑ blocks are the owner interface",
    # resolution method is routed to the skill, never duplicated
    "`chase-references` skill",
    "`docs/SKILLS.md`",
    "Why this exists",
)


def test_reading_path_template_in_adopt_plan():
    assert ("reading-path.md.tmpl", "docs/reading-path.md") in ADOPT_PLAN


def test_reading_path_template_carries_the_structure():
    tmpl = _flat(_template("reading-path.md.tmpl"))
    for phrase in _READING_PATH_PINS:
        assert phrase in tmpl, phrase


def test_reading_path_template_has_a_badge_in_first_12_lines():
    # The docs gate (check_docs) requires the Status badge in the first 12
    # lines of every planted doc.
    head = _template("reading-path.md.tmpl").splitlines()[:12]
    assert any("**Status:** `reference`" in line for line in head)


def test_reading_path_template_slots_are_registered_and_not_critical():
    tmpl = _template("reading-path.md.tmpl")
    slots = find_placeholders(tmpl) - {"project_name"}
    assert slots == _READING_PATH_SLOTS
    bank = {q["slot"]: q for q in QUESTIONS}
    for slot in _READING_PATH_SLOTS:
        assert slot in bank, slot
        # Not critical: a solo repo with no fleet graduates with them
        # unfilled (visible ${...} until the interview fills them).
        assert bank[slot]["critical"] is False, slot


def test_reading_path_template_renders_clean_with_slots_filled():
    context = dict(build_context({}))
    context.setdefault("project_name", "example")
    for slot in _READING_PATH_SLOTS:
        context[slot] = f"v-{slot}"
    rendered = render(_template("reading-path.md.tmpl"), context)
    assert "${" not in rendered
    for phrase in _READING_PATH_PINS:
        assert phrase in _flat(rendered), phrase


def test_reading_path_template_is_portably_worded():
    # The superbot original names its own fleet; the graduated template must
    # not (per-repo copies name THEIR siblings via the slots).
    tmpl = _template("reading-path.md.tmpl")
    for needle in ("menno420", "superbot", "fleet_status.py", "pokemon-mod-lab"):
        assert needle not in tmpl, needle


def test_orientation_routes_the_reading_path_doc():
    # Reachability wiring (the orphan-doc rule): the planted-doc list plus a
    # routed when-to-open pointer — mirroring the ROUTINES pattern. NOT the
    # K0 boot set: Q-0272 doctrine keeps the path routed, not front-loaded.
    orientation = _template("AGENT_ORIENTATION.md.tmpl")
    assert "`docs/reading-path.md`" in orientation
    assert "sibling repos in a fleet" in _flat(orientation)


def test_planted_reading_path_doc_is_reachable(tmp_path):
    # End-to-end against the real enforcer: a fresh adopt plants
    # docs/reading-path.md and the reachability walk reaches it (no orphan
    # finding).
    root, config = _adopt_into(tmp_path)
    planted = root / "docs" / "reading-path.md"
    assert planted.is_file()
    findings = run_doc_checks(
        root / config.docs_root,
        config.badge_tokens,
        config.readpath_docs,
    )
    orphans = [f for f in findings if f.kind == "reachable"]
    assert "reading-path.md" not in {f.path for f in orphans}, orphans
