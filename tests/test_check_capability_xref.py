"""The OWNER-ACTION ↔ CAPABILITIES cross-reference advisory (queue item 8).

The #68 card's 💡 idea: an ask's ``VERIFIED-NEEDED`` (ORDER 008) and the
capability ledger (ORDER 006) are two halves of one loop — a wall cited by
an owner-ask should be recorded in ``docs/CAPABILITIES.md``, and a ledger
that records the cited surface as verified-WORKING means the ask may rest
on a fallen wall. These tests pin the checker's posture: advisory-only
(never exit-affecting), input-gated on the control/ protocol, coarse
token-overlap matching (fail-open, never a verdict), judgment-shaped asks
out of scope. They cover the two findings — ``owner-ask-wall-unrecorded``
and ``owner-ask-capability-resolved`` — plus the clean and empty paths.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.checks.check_capability_xref")

from engine.checks.check_capability_xref import (
    CAPABILITIES_RELPATH,
    check_capability_xref,
)
from engine.checks.check_status_current import STATUS_RELPATH
from engine.cli import cmd_check


def _write(root: Path, rel: str, text: str) -> Path:
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def _ask(item_id: str, title: str, verified: str) -> str:
    return (
        f"⚑ OWNER-ACTION {item_id} — {title}\n"
        "WHAT: One plain sentence.\n"
        "WHERE: Settings → somewhere\n"
        "HOW: click the button\n"
        "WHY-IT-MATTERS: it matters.\n"
        "UNBLOCKS: the next step.\n"
        f"VERIFIED-NEEDED: {verified}\n"
    )


def _status(asks: str) -> str:
    return (
        "# x · status\nupdated: 2026-07-10T11:00Z\nphase: testing\n"
        "health: green\nlast-shipped: none\nblockers: none\n"
        "orders: acked=001 done=001\n⚑ needs-owner: see below\n\n"
        f"{asks}\n"
        "notes: none\n"
    )


def _ledger(walls: str = "", caps: str = "", log: str = "") -> str:
    return (
        "# x — session capabilities & walls\n\n"
        "## Capabilities — verified working\n\n"
        f"{caps}\n"
        "## Walls — verified blocked (use the workaround; don't rediscover)\n\n"
        f"{walls}\n"
        "## Append log — newest first\n\n"
        f"{log}\n"
    )


# A wall-shaped ask citing the ruleset/api.github.com wall.
RULESET_ASK = _ask(
    "2",
    "required-check swap",
    "no agent path to rulesets exists — direct api.github.com HTTP is "
    "403-blocked through the proxy; Settings → Rules is owner-only UI.",
)
RULESET_WALL = (
    "- **`api.github.com` direct HTTP**: 403-blocked through the proxy —\n"
    "  rulesets are unreachable; GitHub access is MCP-tools-only.\n"
)


# ---------------------------------------------------------------------------
# Input gating + fail-open
# ---------------------------------------------------------------------------


def test_no_control_protocol_no_findings(tmp_path):
    assert check_capability_xref(tmp_path) == []


def test_no_owner_action_blocks_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_unreadable_heartbeat_fails_open(tmp_path):
    (tmp_path / STATUS_RELPATH).mkdir(parents=True)
    assert check_capability_xref(tmp_path) == []


def test_missing_heartbeat_file_is_not_this_checkers_finding(tmp_path):
    # check_status_current owns status-missing; this checker stays silent.
    _write(tmp_path, "control/inbox.md", "# inbox\n")
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# Scope — judgment asks and field-less asks are skipped
# ---------------------------------------------------------------------------


def test_judgment_ask_is_out_of_scope(tmp_path):
    # A product/owner-judgment ask never needs a ledger entry — even when
    # its prose contains wall vocabulary ("not a technical wall").
    ask = _ask(
        "8",
        "upgrade decision",
        "the pin is a recorded owner decision — product judgment, "
        "not a technical wall; agents don't overrule a deliberate stance.",
    )
    _write(tmp_path, STATUS_RELPATH, _status(ask))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_ask_without_wall_markers_is_skipped(tmp_path):
    ask = _ask("5", "confirm MIT", "a license choice is a legal decision.")
    _write(tmp_path, STATUS_RELPATH, _status(ask))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


def test_ask_without_verified_needed_is_other_checkers_finding(tmp_path):
    # A field-less ask is check_owner_actions' owner-action-fields finding.
    block = "⚑ OWNER-ACTION 1 — do a thing\nWHAT: a thing, 403-blocked.\n"
    _write(tmp_path, STATUS_RELPATH, _status(block))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger())
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# The happy path — a cited wall the ledger records is clean
# ---------------------------------------------------------------------------


def test_recorded_wall_is_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL))
    assert check_capability_xref(tmp_path) == []


def test_wall_tagged_append_log_entry_also_counts(tmp_path):
    log = (
        "- 2026-07-10 · wall · api.github.com direct HTTP 403-blocked\n"
        "  through the proxy; rulesets unreachable · exact error captured ·\n"
        "  workaround: MCP tools only.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# owner-ask-wall-unrecorded — the ledger doesn't know this wall
# ---------------------------------------------------------------------------


def test_unrecorded_wall_flags(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    # Ledger exists but records a completely different wall.
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(walls="- **Branch deletion**: refused everywhere.\n"),
    )
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-wall-unrecorded"]
    assert findings[0].path == STATUS_RELPATH
    assert "OWNER-ACTION 2" in findings[0].message
    assert "DISCOVERY RULE" in findings[0].message


def test_missing_ledger_flags_unrecorded(tmp_path):
    # No docs/CAPABILITIES.md at all — the wall is by definition unrecorded.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-wall-unrecorded"]


# ---------------------------------------------------------------------------
# owner-ask-capability-resolved — only the working side matches
# ---------------------------------------------------------------------------


def test_capability_only_match_flags_resolved(tmp_path):
    caps = (
        "- **rulesets via api.github.com**: reachable again since the proxy\n"
        "  allowlist change — 403-blocked no longer; verified 2026-07-10.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(caps=caps, walls="- **Branch deletion**: refused everywhere.\n"),
    )
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-capability-resolved"]
    assert "OWNER-ACTION 2" in findings[0].message
    assert "wall may have fallen" in findings[0].message


def test_wall_side_match_wins_over_capability_side(tmp_path):
    # Recorded as a wall AND echoed on the working side (e.g. a recipe
    # around it) → the wall is recorded; no finding.
    caps = "- **rulesets workaround**: api.github.com data via MCP mirror.\n"
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL, caps=caps))
    assert check_capability_xref(tmp_path) == []


# ---------------------------------------------------------------------------
# cmd_check integration — advisory NEVER touches the exit code
# ---------------------------------------------------------------------------


def test_cmd_check_strict_stays_green_on_unrecorded_wall(tmp_path, capsys):
    # No ledger file at all (the by-definition-unrecorded case) — strict
    # stays green because the cross-reference is advisory by contract.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    assert cmd_check(tmp_path, strict=True) == 0
    out = capsys.readouterr().out
    assert "owner-ask-wall-unrecorded" in out
    assert "never exit-affecting" in out


def test_cmd_check_status_only_lane_also_warns(tmp_path, capsys):
    # The asks live in the heartbeat files the control fast lane validates,
    # so the nag rides both lanes.
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    assert "owner-ask-wall-unrecorded" in capsys.readouterr().out


def test_cmd_check_quiet_when_xref_clean(tmp_path, capsys):
    # --status-only keeps the run scoped to the control-lane checkers (the
    # planted ledger fixture is deliberately minimal, not a full docs tree).
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=RULESET_WALL))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    out = capsys.readouterr().out
    assert "owner-ask-wall-unrecorded" not in out
    assert "owner-ask-capability-resolved" not in out

def test_verified_when_shorthand_also_parses(tmp_path):
    # #99 token alignment: check_owner_actions accepts VERIFIED-WHEN: as a
    # shorthand — the cross-reference reads the same token set.
    ask = (
        "⚑ OWNER-ACTION 3 — do a thing\n"
        "WHAT: One plain sentence.\n"
        "WHY: it matters.\n"
        "VERIFIED-WHEN: direct api.github.com HTTP is 403-blocked through "
        "the proxy; rulesets owner-only.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(ask))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(walls="- **Branch deletion**: refused everywhere.\n"),
    )
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["owner-ask-wall-unrecorded"]
    assert "OWNER-ACTION 3" in findings[0].message


# ---------------------------------------------------------------------------
# Slice-5 extensions (§4.2d): append-log grammar + staleness advisories
# ---------------------------------------------------------------------------

from datetime import date

from engine import grammar

TODAY = date(2026, 7, 12)


class _Cfg:
    """Duck-typed config carrier for the checker's config parameter."""

    def __init__(self, cadence=None, sessions_dir=".sessions"):
        self.cadence = cadence if cadence is not None else {"staleness_days": 14}
        self.sessions_dir = sessions_dir


def test_venue_scoped_wall_entry_feeds_the_wall_side(tmp_path):
    # WATCH-item pin: _ledger_sides reads the tag at fields[1] — the NEW
    # venue token at field 2 must not break tag-side attribution. A
    # venue-scoped wall entry still closes the xref loop.
    log = (
        "- 2026-07-10 · wall · routine-fired · api.github.com direct HTTP\n"
        "  403-blocked through the proxy; rulesets unreachable · exact error\n"
        "  captured · workaround: MCP tools only.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(RULESET_ASK))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    assert check_capability_xref(tmp_path) == []


def test_new_format_venue_line_is_grammar_clean(tmp_path):
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(log=grammar.capability_log_line_example()),
    )
    assert check_capability_xref(tmp_path) == []


def test_old_five_field_line_is_never_flagged(tmp_path):
    # Backward compatibility is a hard contract: a pre-venue line must not
    # become advisory noise.
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(log=grammar.capability_log_line_example(venue=None)),
    )
    assert check_capability_xref(tmp_path) == []


def test_unknown_venue_token_flags(tmp_path):
    log = (
        "- 2026-07-10 · wall · owner-lave · tag push refused · 403 ·\n"
        "  use workflow_dispatch.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["capability-log-venue-unknown"]
    assert "owner-lave" in findings[0].message
    assert "any" in findings[0].message  # the message lists the valid tokens


def test_undated_log_bullet_flags_malformed(tmp_path):
    log = "- wall · tag push refused · 403 · use workflow_dispatch.\n"
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["capability-log-malformed"]
    assert grammar.CAPABILITY_LOG_TAUGHT_FORMAT in findings[0].message


def test_untagged_log_entry_flags_malformed(tmp_path):
    log = "- 2026-07-10 · note · something happened · evidence · none.\n"
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    findings = check_capability_xref(tmp_path)
    assert [f.kind for f in findings] == ["capability-log-malformed"]
    assert "capability" in findings[0].message and "wall" in findings[0].message


def test_grammar_scan_is_scoped_to_the_append_log_section(tmp_path):
    # Walls-section bullets are seed rows, not append entries — never judged.
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(
        tmp_path,
        CAPABILITIES_RELPATH,
        _ledger(walls="- **Branch deletion**: refused everywhere.\n"),
    )
    assert check_capability_xref(tmp_path) == []


def _card(tmp_path, text, name="2026-07-12-current-session.md"):
    return _write(tmp_path, f".sessions/{name}", text)


def test_stale_cited_entry_flags(tmp_path):
    log = (
        "- 2026-06-01 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    _card(
        tmp_path,
        "# card\nRelying on the tag push wall: the git proxy 403 means the\n"
        "workflow_dispatch release path is the plan.\n",
    )
    findings = check_capability_xref(tmp_path, config=_Cfg(), today=TODAY)
    assert [f.kind for f in findings] == ["capability-entry-stale"]
    assert "2026-06-01" in findings[0].message
    assert "DISCOVERY RULE step 5" in findings[0].message


def test_fresh_cited_entry_is_clean(tmp_path):
    log = (
        "- 2026-07-10 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    _card(
        tmp_path,
        "# card\nRelying on the tag push wall: the git proxy 403 means the\n"
        "workflow_dispatch release path is the plan.\n",
    )
    assert check_capability_xref(tmp_path, config=_Cfg(), today=TODAY) == []


def test_stale_uncited_entry_is_clean(tmp_path):
    # Aging alone never nags — only an aged entry the current card leans on.
    log = (
        "- 2026-06-01 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    _card(tmp_path, "# card\nEntirely unrelated docs work this session.\n")
    assert check_capability_xref(tmp_path, config=_Cfg(), today=TODAY) == []


def test_stale_scan_reads_last_verified_seed_stamps(tmp_path):
    walls = (
        "- `any` · **Tag push via git**: refused everywhere — HTTP 403 from\n"
        "  the git proxy → use the workflow_dispatch release path.\n"
        "  — LAST-VERIFIED: 2026-06-01\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(walls=walls))
    _card(
        tmp_path,
        "# card\nRelying on the tag push wall: the git proxy 403 means the\n"
        "workflow_dispatch release path is the plan.\n",
    )
    findings = check_capability_xref(tmp_path, config=_Cfg(), today=TODAY)
    assert [f.kind for f in findings] == ["capability-entry-stale"]


def test_staleness_window_honors_the_config_knob(tmp_path):
    log = (
        "- 2026-06-20 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    _card(
        tmp_path,
        "# card\nRelying on the tag push wall: the git proxy 403 means the\n"
        "workflow_dispatch release path is the plan.\n",
    )
    # 22 days old: stale under the default 14 — clean under a 30-day window.
    wide = _Cfg(cadence={"staleness_days": 30})
    assert check_capability_xref(tmp_path, config=wide, today=TODAY) == []
    narrow = _Cfg(cadence={"staleness_days": 14})
    findings = check_capability_xref(tmp_path, config=narrow, today=TODAY)
    assert [f.kind for f in findings] == ["capability-entry-stale"]


def test_staleness_days_defaults_when_missing_from_cadence(tmp_path):
    # The triggers.py:100 house pattern: default-on-missing, never a KeyError.
    log = (
        "- 2026-06-01 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    _card(
        tmp_path,
        "# card\nRelying on the tag push wall: the git proxy 403 means the\n"
        "workflow_dispatch release path is the plan.\n",
    )
    findings = check_capability_xref(
        tmp_path, config=_Cfg(cadence={}), today=TODAY
    )
    assert [f.kind for f in findings] == ["capability-entry-stale"]


def test_no_session_card_no_staleness_verdict(tmp_path):
    log = (
        "- 2026-06-01 · wall · any · tag push via git refused everywhere ·\n"
        "  HTTP 403 from the git proxy · use the workflow_dispatch release\n"
        "  path.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    assert check_capability_xref(tmp_path, config=_Cfg(), today=TODAY) == []


def test_cmd_check_strict_stays_green_on_slice5_advisories(tmp_path, capsys):
    # Advisory by contract (§8 Q2=B): the new kinds are surfaced but never
    # exit-affecting, on both lanes.
    log = (
        "- 2026-07-10 · wall · owner-lave · tag push refused · 403 ·\n"
        "  use workflow_dispatch.\n"
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, _ledger(log=log))
    assert cmd_check(tmp_path, strict=True, status_only=True) == 0
    out = capsys.readouterr().out
    assert "capability-log-venue-unknown" in out
    assert "never exit-affecting" in out


def test_rendered_template_ledger_is_grammar_clean(tmp_path):
    # Dogfood: a fresh adopt's planted ledger (venue-scoped seeds, fence,
    # LAST-VERIFIED stamps, taught format line) yields zero slice-5 findings.
    from engine.render import load_templates, render

    rendered = render(
        load_templates()["CAPABILITIES.md.tmpl"],
        {"project_name": "demo"},
    )
    _write(tmp_path, STATUS_RELPATH, _status(""))
    _write(tmp_path, CAPABILITIES_RELPATH, rendered)
    assert check_capability_xref(tmp_path, config=_Cfg(), today=TODAY) == []
