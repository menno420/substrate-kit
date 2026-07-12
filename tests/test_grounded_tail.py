"""Grounded-skills program §7 tail — the three graduation-map ❌ rows.

Pins the closing slice of the grounded-skills program
(``docs/planning/2026-07-12-grounded-skills-program.md`` §6 rows + §7 tail;
map: ``docs/reports/2026-07-12-prompt-template-hardening-input.md`` §(b)):

1. **Routine / wake-chain doctrine** — the new ``routines.md.tmpl`` planted
   to ``docs/ROUTINES.md`` (ADOPT_PLAN), routed from orientation so the
   plant never orphans an adopter's ``check --strict``.
2. **Verify-don't-trust Evidence block** — the ``CONSTITUTION.md.tmpl``
   working-agreement bullet (probe-not-record · tree-over-self-report ·
   job-log-over-check-name · stale-read cross-check · false-green = a bug
   in the CHECK, PL-006 · cite commit/PR/tag/run).
3. **Preflight fetch + hard-reset** — the explicit FIRST orientation step
   (rule in ``CLAUDE.md.tmpl``, mechanics in ``AGENT_ORIENTATION.md.tmpl``).

Phrases are pinned directly against the templates (not ``engine.grammar``):
the slice-2/3/4/5/8 grammar rule homes a phrase only when BOTH a writer
(template) and an enforcer (checker) consume it — no checker consumes these
doctrine sentences; the only enforcer in play is the generic reachability
walk (``check_docs.check_reachable``), which consumes the backtick path
``docs/ROUTINES.md``, exercised end-to-end below.

Doctrine provenance: ``docs/reports/2026-07-12-trigger-forensics.md`` (H1
fresh-session cron 0-for-2 vs 100% self-bound; H2 env-id mismatch
load-bearing; the no-tombstone vanish; the manual-fire ``last_fired_at``
trap) and the hardening report §a.1/a.3/a.5 — portably worded, no fleet ids.
"""

from __future__ import annotations

import pytest

pytest.importorskip("engine.adopt")

from engine.adopt import ADOPT_PLAN, adopt
from engine.checks.check_docs import run_doc_checks
from engine.lib.config import Config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import build_context, load_templates, render


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


# ── row 1: routines.md.tmpl — the wake-chain doctrine ────────────────────────


def test_routines_template_in_adopt_plan():
    assert ("routines.md.tmpl", "docs/ROUTINES.md") in ADOPT_PLAN


# The doctrine's load-bearing sentences (whitespace-insensitive). Each maps
# to an incident in the trigger-forensics / hardening reports.
_ROUTINES_DOCTRINE_PINS = (
    # binding choice — self-bind lifetime + cutover re-arm (report §a.1)
    "A self-bound trigger dies with its session.",
    "re-arm it at every seat cutover",
    # fresh-session rationale PLUS the verified platform caveat (forensics H1)
    "fresh-session-per-fire",
    "0-for-2 on fresh-session cron fires vs 100% on self-bound",
    "UNVERIFIED-BROKEN until a scheduled fire is proven in your environment",
    "choose the binding by lifetime rationale, then **verify the first scheduled delivery",
    # env-id portability caveat (forensics H2 — load-bearing, not cosmetic)
    "Never hardcode environment or session ids",
    # verbatim create-call records (report §a.1)
    "id, cron, binding, next-fire",
    # re-verify at every wake — probe-not-record (report §a.3)
    "A record is a claim; the live registry is the proof.",
    "ABSENCE claim requires walking the registry **to exhaustion**",
    "Deleted triggers may vanish with no tombstone.",
    "total absence means hard deletion, actor unknown",
    # scheduler health (forensics §a items 6/7 + recommendation 4)
    "enabled ∧ next_run_at < now − 15min",
    "advances `next_run_at` after each fire",
    "never read `last_fired_at` alone as scheduler health",
    # pacing (retro W-6)
    "sequentially, one write at a time",
    "pacemaker for a live seat only",
    "the cron failsafe is the dead-man backstop, not the pacer",
    # failsafe blind-window check (forensics §d.5, recommendation 3)
    "verify the standing loop's last slot actually delivered",
)


def test_routines_template_carries_the_doctrine():
    tmpl = _flat(_template("routines.md.tmpl"))
    for phrase in _ROUTINES_DOCTRINE_PINS:
        assert phrase in tmpl, phrase


def test_routines_template_is_portably_worded():
    # No fleet-specific ids: trigger/env/session ids belong in dated records,
    # never in a planted template (the forensics H2 env-id-mismatch lesson —
    # a hardcoded id is wrong somewhere by construction).
    tmpl = _template("routines.md.tmpl")
    for needle in ("trig_", "env_0", "session_0", "cse_", "menno420"):
        assert needle not in tmpl, needle


def test_routines_template_points_at_agreement_and_capabilities():
    # Pointers ride the engine-computed key, never a hardcoded agreement
    # filename (the ORDER 015 dead-boot-pointer lesson); trigger capability
    # findings route to the ledger, not a second home.
    tmpl = _template("routines.md.tmpl")
    assert "${agreement_home}" in tmpl
    assert "docs/CAPABILITIES.md" in tmpl


def test_routines_template_renders_slot_free_in_fresh_adopt_context():
    context = dict(build_context({}))
    context.setdefault("agreement_home", "CONSTITUTION.md")
    context.setdefault("project_name", "example")
    rendered = render(_template("routines.md.tmpl"), context)
    assert "${" not in rendered
    for phrase in _ROUTINES_DOCTRINE_PINS:
        assert phrase in _flat(rendered), phrase


def test_orientation_routes_the_routines_doc():
    # Reachability wiring (the orphan-doc rule: a planted doc must be linked
    # from orientation or it reds check --strict on adopters): the planted-doc
    # list carries the backtick path the reachability walk follows, plus a
    # routed when-to-open pointer — mirroring the SKILLS/CAPABILITIES pattern.
    orientation = _template("AGENT_ORIENTATION.md.tmpl")
    assert "`docs/ROUTINES.md`" in orientation
    assert "trigger/routine" in _flat(orientation)
    claude = _template("CLAUDE.md.tmpl")
    assert "`docs/ROUTINES.md`" in claude


def test_planted_routines_doc_is_reachable(tmp_path):
    # End-to-end against the real enforcer: a fresh adopt plants
    # docs/ROUTINES.md and the reachability walk reaches it (no orphan
    # finding) — the exact red the v1.13.0 orphan-doc lesson is about.
    root, config = _adopt_into(tmp_path)
    planted = root / "docs" / "ROUTINES.md"
    assert planted.is_file()
    findings = run_doc_checks(
        root / config.docs_root,
        config.badge_tokens,
        config.readpath_docs,
    )
    orphans = [f for f in findings if f.kind == "reachable"]
    assert "ROUTINES.md" not in {f.path for f in orphans}, orphans


# ── row 2: CONSTITUTION.md.tmpl — the Evidence block ─────────────────────────

_EVIDENCE_PINS = (
    "Evidence — verify, don't trust.",
    # probe-not-record (report §a.3 wording)
    "A record is a claim; the live surface is the proof",
    "probe-not-record",
    # tree over registry/heartbeat (adopter kit: lines lag 1–3 releases)
    "tree wins over a self-report",
    "lag the target repo's tree by 1–3 releases",
    # job-log over check-name (alias/designed-red reading)
    "judged by its job log, never its name",
    # stale-read cross-check (~25 min stale MCP PR reads)
    "~25 min stale",
    # false-green ruling (PL-006)
    "a bug in the CHECK, not a clearance",
    "PL-006",
    # citation discipline
    "Every load-bearing claim cites a commit / PR / tag / run",
)


def test_constitution_evidence_block_carries_every_pin():
    tmpl = _flat(_template("CONSTITUTION.md.tmpl"))
    for phrase in _EVIDENCE_PINS:
        assert phrase in tmpl, phrase


def test_constitution_evidence_block_sits_in_the_working_agreement():
    tmpl = _template("CONSTITUTION.md.tmpl")
    agreement = tmpl.split("## Working agreement", 1)[1].split("\n## ", 1)[0]
    assert "Evidence — verify, don't trust." in agreement


# ── row 3: preflight fetch + hard-reset — the first orientation step ─────────

_PREFLIGHT_COMMAND = "git fetch origin main && git reset --hard origin/main"


def test_claude_orientation_starts_with_the_preflight_step():
    # The rule is step 0 — BEFORE "1. This file": land on origin's HEAD
    # before reading anything else (the warm-clone-behind-origin class; a
    # stale clone reads stale orders).
    tmpl = _template("CLAUDE.md.tmpl")
    orientation = tmpl.split("## Orientation — read first, in order", 1)[1]
    step0 = orientation.index("0. **Preflight")
    step1 = orientation.index("1. This file")
    assert step0 < step1
    assert _PREFLIGHT_COMMAND in orientation
    # mechanics are routed, not duplicated
    assert "docs/AGENT_ORIENTATION.md" in orientation.split("1. This file")[0]


def test_orientation_carries_the_preflight_mechanics():
    tmpl = _template("AGENT_ORIENTATION.md.tmpl")
    section = tmpl.split("## Start every session", 1)[1].split("\n## ", 1)[0]
    assert _PREFLIGHT_COMMAND in section
    # verify HEAD against the remote, and never reset over unexplained work
    assert "git ls-remote origin main" in section
    assert "git rev-parse HEAD" in section
    assert "stop and report it" in _flat(section)
