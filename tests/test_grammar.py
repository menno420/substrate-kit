"""Writer↔enforcer agreement — the control-plane grammar has ONE home (EAP §6.8).

The whole point of ``engine.grammar``: the format the planted templates TEACH
(control/README.md's fenced format blocks, the seeded control files) must
satisfy the regexes the ENFORCERS run (``check_inbox_append``,
``check_owner_actions``, ``check_status_current``, ``check_claims``,
``currency``). Before §6.8 each enforcer re-derived its own copy of the
grammar and the two halves could silently drift — the manager's own seeded
orders once failed the kit's 1.7.0 grammar. These tests pin three layers:

- **one-home identity** — the enforcers consume the grammar module's own
  objects (not re-compiled lookalikes), so there is nothing left to drift;
- **taught text parses** — the example lines the templates teach writers
  satisfy the enforcer regexes as written;
- **canonical examples pass the enforcers end-to-end** — the grammar module's
  own example renderers (the smallest correct writer output) produce zero
  findings from the full checker entry points.
"""

from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path

import pytest

pytest.importorskip("engine.grammar")

from engine import grammar
from engine.checks import check_claims as claims_mod
from engine.checks import check_inbox_append as inbox_mod
from engine.checks import check_owner_actions as owner_mod
from engine.checks.check_claims import check_claims
from engine.checks.check_inbox_append import check_inbox_append
from engine.checks.check_owner_actions import check_owner_actions
from engine.checks.check_status_current import parse_heartbeat
from engine.currency import parse_kit_line
from engine.render import load_templates, render

NOW = datetime(2026, 7, 10, 13, 0, tzinfo=timezone.utc)


def _template(name: str) -> str:
    return load_templates()[name]


def _fenced_block(text: str, heading: str) -> str:
    """Return the first fenced code block after ``heading`` in ``text``."""
    section = text.split(heading, 1)[1]
    match = re.search(r"```(?:markdown)?\n(.*?)```", section, re.DOTALL)
    assert match is not None, f"no fenced block after {heading!r}"
    return match.group(1)


# ── one-home identity: enforcers consume grammar's own objects ───────────────


def test_enforcers_consume_the_grammar_module_objects():
    """The §6.8 point in one assert-set: no enforcer keeps its own copy."""
    assert inbox_mod.ORDER_HEADER_RE is grammar.ORDER_HEADER_RE
    assert inbox_mod.ORDER_HEADER_PREFIX is grammar.ORDER_HEADER_PREFIX
    assert inbox_mod.ORDER_REQUIRED_FIELDS is grammar.ORDER_REQUIRED_FIELDS
    assert owner_mod.OWNER_ACTION_FIELDS is grammar.OWNER_ACTION_FIELDS
    assert owner_mod.NEEDS_OWNER_TOKEN is grammar.NEEDS_OWNER_TOKEN
    assert claims_mod.ORDERS_LINE_RE is grammar.ORDERS_LINE_RE
    assert claims_mod.ORDERS_DONE_RE is grammar.ORDERS_DONE_RE
    assert claims_mod.ORDERS_CLAIMED_BY_RE is grammar.ORDERS_CLAIMED_BY_RE
    assert claims_mod.WORK_CLAIM_BULLET_RE is grammar.WORK_CLAIM_BULLET_RE
    assert claims_mod.WORK_CLAIM_DATE_RE is grammar.WORK_CLAIM_DATE_RE


def test_templates_point_writers_at_the_grammar_module():
    """The taught docs carry the source-of-truth pointer (the writer half)."""
    assert "src/engine/grammar.py" in _template("control-README.md.tmpl")
    assert "src/engine/grammar.py" in _template("control-claims-README.md.tmpl")


# ── taught text parses: control-README order format ─────────────────────────


def test_taught_order_header_matches_the_enforcer_regex():
    block = _fenced_block(
        _template("control-README.md.tmpl"),
        "## `inbox.md` order format",
    )
    header = block.splitlines()[0]
    assert grammar.ORDER_HEADER_RE.match(header), header


def test_taught_order_block_carries_every_required_field():
    block = _fenced_block(
        _template("control-README.md.tmpl"),
        "## `inbox.md` order format",
    )
    body = block.splitlines()[1:]
    for fieldname in grammar.ORDER_REQUIRED_FIELDS:
        assert any(ln.startswith(fieldname) for ln in body), fieldname


def test_inbox_seed_taught_header_matches_the_enforcer_regex():
    """The inbox seed teaches the append shape inline — it must parse too."""
    seed = _template("control-inbox.md.tmpl")
    match = re.search(r"`(## ORDER [^`]+)`", seed)
    assert match is not None
    assert grammar.ORDER_HEADER_RE.match(match.group(1)), match.group(1)


# ── taught text parses: control-README status format ────────────────────────


def test_taught_status_block_lines_parse():
    block = _fenced_block(
        _template("control-README.md.tmpl"),
        "## `status.md` format",
    )
    assert grammar.UPDATED_LINE_RE.search(block)
    assert grammar.ORDERS_LINE_RE.search(block)
    assert grammar.ORDERS_DONE_RE.search(block)
    assert grammar.NEEDS_OWNER_TOKEN in block
    # The kit: line placeholder version can't parse (it's `v<X.Y.Z>`), but
    # the line itself and its check/engaged fields must.
    assert grammar.KIT_LINE_RE.search(block)
    _version, check, engaged = parse_kit_line(block)
    assert check == "green"
    assert engaged == "yes"


def test_taught_claimed_by_example_parses():
    """The live example in § Claiming an order is the claim parser's shape."""
    text = _template("control-README.md.tmpl")
    match = re.search(r"`(orders: acked=[^`]*claimed-by:[^`]*)`", text)
    assert match is not None, "the README teaches a claimed-by example"
    parsed = grammar.ORDERS_CLAIMED_BY_RE.search(match.group(1))
    assert parsed is not None
    ids, lane, ts = parsed.groups()
    assert ids == "007+008"
    assert lane == "coordinator-lane"
    assert ts == "2026-07-09T18:38Z"


def test_taught_owner_action_block_carries_every_canonical_field():
    block = _fenced_block(
        _template("control-README.md.tmpl"),
        "## ⚑ needs-owner — the OWNER-ACTION item format",
    )
    for alternatives in grammar.OWNER_ACTION_FIELDS:
        assert alternatives[0] in block, alternatives[0]


# ── taught text parses: the rendered status seed ─────────────────────────────


def test_status_seed_kit_line_and_orders_line_parse():
    seed = render(
        _template("control-status.md.tmpl"),
        {"project_name": "demo", "kit_version": "1.2.3"},
    )
    assert parse_kit_line(seed) == ("1.2.3", "red", "no")
    assert grammar.ORDERS_LINE_RE.search(seed)
    assert grammar.NEEDS_OWNER_TOKEN in seed
    # The seed's `updated:` is DELIBERATELY unparseable — born-red until the
    # first real heartbeat. Pin that too: a parse here would defuse the gate.
    assert parse_heartbeat(seed) is None


def test_claims_readme_taught_bullet_token_parses():
    text = _template("control-claims-README.md.tmpl")
    match = re.search(r"^\s*`` (- .*?) ``", text, re.MULTILINE)
    assert match is not None, "the claims README teaches the bullet inline"
    bullet = match.group(1)
    token = grammar.WORK_CLAIM_BULLET_RE.search(bullet)
    assert token is not None
    assert token.group(1) == "branch-or-scope"


# ── canonical examples pass the enforcers end-to-end ─────────────────────────


def test_order_block_example_passes_check_inbox_append(tmp_path):
    base = tmp_path / "base-inbox.md"
    seed = render(_template("control-inbox.md.tmpl"), {"project_name": "demo"})
    base.write_text(seed, encoding="utf-8")
    inbox = tmp_path / "control" / "inbox.md"
    inbox.parent.mkdir(parents=True)
    inbox.write_text(seed + "\n" + grammar.order_block_example(), encoding="utf-8")
    assert check_inbox_append(tmp_path, base) == []


def test_order_block_example_header_and_fields_parse():
    lines = grammar.order_block_example().splitlines()
    assert grammar.ORDER_HEADER_RE.match(lines[0])
    for fieldname in grammar.ORDER_REQUIRED_FIELDS:
        assert any(ln.startswith(fieldname) for ln in lines[1:]), fieldname


def test_owner_action_example_satisfies_check_owner_actions(tmp_path):
    status = tmp_path / "control" / "status.md"
    status.parent.mkdir(parents=True)
    status.write_text(
        "# demo · status\n"
        + grammar.updated_line_example()
        + f"{grammar.NEEDS_OWNER_TOKEN}: one structured ask below\n"
        + grammar.owner_action_block_example(),
        encoding="utf-8",
    )
    assert check_owner_actions(tmp_path) == []


def test_orders_line_example_with_claim_is_clean_in_check_claims(tmp_path):
    status = tmp_path / "control" / "status.md"
    status.parent.mkdir(parents=True)
    status.write_text(
        "# demo · status\n"
        + grammar.updated_line_example()
        + grammar.orders_line_example(claimed=True),
        encoding="utf-8",
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_work_claim_bullet_example_is_clean_in_check_claims(tmp_path):
    claims_dir = tmp_path / "control" / "claims"
    claims_dir.mkdir(parents=True)
    (claims_dir / "example-branch.md").write_text(
        grammar.work_claim_bullet_example(date="2026-07-10"),
        encoding="utf-8",
    )
    assert check_claims(tmp_path, now=NOW) == []


def test_heartbeat_and_kit_line_examples_parse():
    ts = parse_heartbeat(grammar.updated_line_example())
    assert ts == datetime(2026, 7, 10, 12, 0, tzinfo=timezone.utc)
    assert parse_kit_line(grammar.kit_line_example("9.9.9")) == (
        "9.9.9",
        "green",
        "yes",
    )


def test_kit_repos_own_inbox_satisfies_the_taught_grammar():
    """Dogfood: consumer #0's real inbox parses under the shared grammar.

    The §6.8 provenance was the manager's seeded orders failing the kit's
    grammar — this pins that the kit's own live bus stays parseable.
    """
    inbox = Path(__file__).resolve().parents[1] / "control" / "inbox.md"
    text = inbox.read_text(encoding="utf-8")
    headers = [
        ln
        for ln in text.splitlines()
        if ln.startswith(grammar.ORDER_HEADER_PREFIX)
    ]
    assert headers, "the kit's own inbox carries orders"
    for header in headers:
        assert grammar.ORDER_HEADER_RE.match(header), header
