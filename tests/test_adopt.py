"""Tests for the one-step adopt flow (Lane B8).

Covers: every ADOPT_PLAN target planted; re-adopt keeps (never clobbers)
hand-edited files; the .claude/ opt-in gate; the staged <state_dir> tree;
the planted ledger parsing through ``engine.ledger``; the guardrail refusal;
badge-cleanliness of the freshly planted doc tree; and the CI snippet.

``engine.adopt`` imports ``engine.hooks.settings`` (built by lane B7 in
parallel); until that module lands these tests skip rather than red the suite.
"""

import json
import subprocess
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import (
    ADOPT_PLAN,
    AUTOMERGE_CARVEOUT_LABEL,
    AUTOMERGE_ENABLER_RELPATH,
    DOC_HASHES_STATE_KEY,
    LIVE_CI_RELPATH,
    UNRENDERED_BANNER_FIRST_LINE,
    adopt,
    archive_dist,
    automerge_enabler_workflow,
    ci_snippet,
    dist_version,
    doc_is_untouched,
    live_ci_workflow,
    strip_unrendered_banner,
    with_unrendered_banner,
)
from engine.agents.agents import AGENTS
from engine.checks.check_docs import run_doc_checks
from engine.ledger import parse_ledger
from engine.lib.config import KIT_VERSION, Config, load_config
from engine.lib.guardrail import UnsafeTargetError
from engine.lib.state import JsonStateBackend, default_state
from engine.skills.skills import SKILLS


def _make_backend(root: Path, config: Config, answers: dict | None = None):
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
        for slot, value in (answers or {}).items():
            slots = backend.get("slots", {})
            slots[slot] = "filled"
            backend.set("slots", slots)
            values = backend.get("slot_values", {})
            values[slot] = {"value": value, "status": "confirmed"}
            backend.set("slot_values", values)
    return backend


def _adopt_into(tmp_path: Path, *, include_claude: bool = False, config=None):
    root = tmp_path / "repo"
    config = config or Config()
    backend = _make_backend(root, config)
    lines = adopt(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        include_claude=include_claude,
    )
    return root, config, lines


# ---------------------------------------------------------------------------
# Planting
# ---------------------------------------------------------------------------


def test_every_plan_target_planted(tmp_path):
    root, _, lines = _adopt_into(tmp_path)
    for _, rel in ADOPT_PLAN:
        assert (root / rel).is_file(), rel
        assert f"planted: {rel}" in lines
    assert (root / ".sessions" / "README.md").is_file()
    assert (root / "project.index.json").is_file()


def test_claude_md_is_staged_not_planted(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    assert not (root / "CLAUDE.md").exists()
    assert (root / config.state_dir / "claude" / "CLAUDE.md").is_file()
    assert "CLAUDE.md.tmpl" not in {name for name, _ in ADOPT_PLAN}


def test_unfilled_placeholders_stay_visible_under_banner(tmp_path):
    root, _, _ = _adopt_into(tmp_path)
    text = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    # ${project_name} is derived from the root dir name at adopt time…
    assert "${project_name}" not in text
    assert "repo" in text
    # …while a genuinely un-derivable slot stays visible, under the banner.
    assert "${drift_resolution}" in text
    assert text.startswith(UNRENDERED_BANNER_FIRST_LINE)


def test_capability_manifest_planted_with_discovery_rule(tmp_path):
    # ORDER 006: the capability manifest plants at docs/CAPABILITIES.md,
    # fully rendered (its only slot is the derivable project_name), carrying
    # the discovery rule + the seeded fleet walls, and the orientation
    # templates route sessions through it at start.
    root, _, lines = _adopt_into(tmp_path)
    manifest = root / "docs" / "CAPABILITIES.md"
    assert manifest.is_file()
    assert "planted: docs/CAPABILITIES.md" in lines
    text = manifest.read_text(encoding="utf-8")
    assert "${" not in text  # project_name derives → no banner, no leftovers
    assert not text.startswith(UNRENDERED_BANNER_FIRST_LINE)
    assert "THE DISCOVERY RULE" in text
    assert "ffmpeg" in text
    assert "printenv" in text
    assert "workflow_dispatch" in text.lower() or "workflow_dispatch" in text
    # Orientation wiring: constitution + orientation router name the manifest.
    constitution = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    assert "docs/CAPABILITIES.md" in constitution
    orientation = (root / "docs" / "AGENT_ORIENTATION.md").read_text(
        encoding="utf-8"
    )
    assert "docs/CAPABILITIES.md" in orientation


def test_order_claim_convention_planted(tmp_path):
    # ORDER 007: the planted control/README.md carries the order-claiming
    # convention — claim FIRST on your own status orders line (landed on
    # main before build), re-read after merge, stale claims expire — so no
    # two lanes ever execute the same `new` order (the #50/#51 root cause).
    root, _, _ = _adopt_into(tmp_path)
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    assert "Claiming an order" in readme
    assert "claimed-by:" in readme
    assert "claim it first" in readme.lower()
    assert "Claims expire" in readme
    # The status-format block advertises the claim annotation.
    assert "[claimed-by: <ids> <lane-or-session> <ISO8601>]" in readme


def test_work_claim_convention_planted(tmp_path):
    # EAP §6.4: the kit-owned work-claim convention plants at
    # control/claims/README.md (one file per claim — the measured
    # 0%-conflict layout), and the planted control/README.md routes to it.
    root, _, lines = _adopt_into(tmp_path)
    claims_readme = root / "control" / "claims" / "README.md"
    assert claims_readme.is_file()
    assert "planted: control/claims/README.md" in lines
    text = claims_readme.read_text(encoding="utf-8")
    assert "one file per claim" in text
    assert "0%" in text and "98%" in text  # the measured evidence travels
    assert "Delete your own claim file" in text
    assert "claims-legacy-location" in text
    assert "claims_dir" in text
    # Routed from the control protocol contract.
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    assert "control/claims/" in readme
    assert "Claiming work" in readme


def test_owner_action_format_planted_and_wired(tmp_path):
    # ORDER 008: the planted control/README.md carries the OWNER-ACTION item
    # format (six REQUIRED fields, attempted-or-exact-wall), and the
    # constitution + collaboration model carry the routing doctrine.
    root, _, _ = _adopt_into(tmp_path)
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    assert "OWNER-ACTION" in readme
    for field in ("WHAT:", "WHERE:", "HOW:", "WHY-IT-MATTERS:", "UNBLOCKS:", "VERIFIED-NEEDED:"):
        assert field in readme
    assert "assumption-based ask" in readme
    constitution = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    assert "OWNER-ACTION" in constitution
    assert "VERIFIED-NEEDED" in constitution
    collab = (root / "docs" / "collaboration-model.md").read_text(encoding="utf-8")
    assert "Routing work to the owner" in collab
    assert "VERIFIED-NEEDED" in collab


def test_derived_slots_render_and_stay_provisional(tmp_path):
    root, config, lines = _adopt_into(tmp_path)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    slots = backend.get("slots", {})
    values = backend.get("slot_values", {})
    assert slots.get("project_name") == "provisional"
    assert values["project_name"]["value"] == "repo"
    assert values["project_name"]["source"] == "derived"
    assert any(line.startswith("derived: project_name") for line in lines)
    # A doc whose only slot is project_name is now fully rendered: no banner.
    ledger = (root / "docs" / "decisions.md").read_text(encoding="utf-8")
    assert "${" not in ledger
    assert not ledger.startswith(UNRENDERED_BANNER_FIRST_LINE)


def test_derivation_never_overwrites_an_existing_answer(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config, {"project_name": "demobot"})
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    values = backend.get("slot_values", {})
    assert values["project_name"]["value"] == "demobot"


def test_python_project_derives_language_and_verify_command(tmp_path):
    root = tmp_path / "repo"
    root.mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        '[project]\nname = "x"\nrequires-python = ">=3.10"\n', encoding="utf-8"
    )
    (root / "tests").mkdir()
    config = Config()
    backend = _make_backend(root, config)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    values = backend.get("slot_values", {})
    assert values["primary_language"]["value"] == "Python >=3.10"
    assert values["verify_command"]["value"] == "python3 -m pytest"
    staged = (root / config.state_dir / "claude" / "CLAUDE.md").read_text(
        encoding="utf-8"
    )
    assert "python3 -m pytest" in staged
    assert "${verify_command}" not in staged


def test_banner_strips_when_placeholders_fill():
    bannered = with_unrendered_banner("# Doc\n\n${architecture_layers}\n")
    assert bannered.startswith(UNRENDERED_BANNER_FIRST_LINE)
    filled = bannered.replace("${architecture_layers}", "layered")
    assert strip_unrendered_banner(filled) == "# Doc\n\nlayered\n"
    # A fully-rendered doc never gains a banner, and stripping is a no-op.
    assert with_unrendered_banner("# Clean\n") == "# Clean\n"
    assert strip_unrendered_banner("# Clean\n") == "# Clean\n"


def test_adopt_as_single_file_vendors_bootstrap(tmp_path, monkeypatch):
    fake_bootstrap = tmp_path / "dist" / "bootstrap.py"
    fake_bootstrap.parent.mkdir(parents=True)
    fake_bootstrap.write_text("# fake single-file bootstrap\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", [str(fake_bootstrap), "adopt"])
    root, config, lines = _adopt_into(tmp_path)
    assert "planted: bootstrap.py" in lines
    assert (root / "bootstrap.py").read_text(encoding="utf-8") == (
        "# fake single-file bootstrap\n"
    )
    settings = (root / config.state_dir / "hooks" / "settings.template.json").read_text(
        encoding="utf-8"
    )
    # Hook commands reference the vendored root copy, not a path outside the repo.
    assert "bootstrap.py hook" in settings
    assert str(fake_bootstrap) not in settings


def test_adopt_skips_vendoring_when_target_ships_generating_dist(
    tmp_path, monkeypatch
):
    # KL-0 friction guard (2026-07-09): adopting the kit repo itself
    # (consumer #0, §3.3) via its own dist/bootstrap.py must not vendor a
    # root duplicate that would silently drift from the CI-byte-pinned dist
    # file. Hook commands point at the dist copy instead.
    root = tmp_path / "repo"
    dist = root / "dist" / "bootstrap.py"
    dist.parent.mkdir(parents=True)
    dist.write_text("# generating single-file bootstrap\n", encoding="utf-8")
    monkeypatch.setattr("sys.argv", [str(dist), "adopt"])
    _, config, lines = _adopt_into(tmp_path)
    assert not (root / "bootstrap.py").exists()
    assert "planted: bootstrap.py" not in lines
    settings = (root / config.state_dir / "hooks" / "settings.template.json").read_text(
        encoding="utf-8"
    )
    assert "dist/bootstrap.py hook" in settings
    assert str(dist) not in settings


def test_filled_slot_renders_into_planted_doc(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config, {"project_name": "demobot"})
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    text = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    assert "demobot" in text
    assert "${project_name}" not in text


def test_readopt_reports_kept_and_does_not_clobber(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    edited = root / "docs" / "architecture.md"
    edited.write_text("# hand-edited\nkeep me\n", encoding="utf-8")
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert "kept: docs/architecture.md" in lines
    assert edited.read_text(encoding="utf-8") == "# hand-edited\nkeep me\n"
    for _, rel in ADOPT_PLAN:
        assert f"kept: {rel}" in lines
        assert f"planted: {rel}" not in lines


def test_docs_root_remap(tmp_path):
    root = tmp_path / "repo"
    config = Config(docs_root="documentation")
    backend = _make_backend(root, config)
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert (root / "documentation" / "decisions.md").is_file()
    assert not (root / "docs").exists()
    assert "planted: documentation/decisions.md" in lines


# ---------------------------------------------------------------------------
# .claude/ opt-in gate
# ---------------------------------------------------------------------------


def test_claude_tree_not_written_without_opt_in(tmp_path):
    root, _, _ = _adopt_into(tmp_path)
    assert not (root / ".claude").exists()


def test_include_claude_writes_live_tree_skip_if_exists(tmp_path):
    root, _, lines = _adopt_into(tmp_path, include_claude=True)
    assert (root / ".claude" / "CLAUDE.md").is_file()
    assert (root / ".claude" / "settings.json").is_file()
    assert "planted: .claude/CLAUDE.md" in lines
    json.loads((root / ".claude" / "settings.json").read_text(encoding="utf-8"))
    # Re-adopt keeps a hand-edited live file.
    (root / ".claude" / "CLAUDE.md").write_text("mine\n", encoding="utf-8")
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit", include_claude=True)
    assert "kept: .claude/CLAUDE.md" in lines
    assert (root / ".claude" / "CLAUDE.md").read_text(encoding="utf-8") == "mine\n"


# ---------------------------------------------------------------------------
# Staged tree
# ---------------------------------------------------------------------------


def test_staged_tree_contains_all_packs(tmp_path):
    root, config, lines = _adopt_into(tmp_path)
    state = root / config.state_dir
    assert (state / "claude" / "CLAUDE.md").is_file()
    assert len(list(state.glob("skills/*/SKILL.md"))) == len(SKILLS)
    assert len(list(state.glob("agents/*.md"))) == len(AGENTS)
    assert (state / "hooks" / "settings.template.json").is_file()
    assert (state / "hooks" / "README.md").is_file()
    assert (state / "ci" / "quality.yml.example").is_file()
    staged = [line for line in lines if line.startswith("staged: ")]
    assert f"staged: {config.state_dir}/claude/CLAUDE.md" in staged
    assert f"staged: {config.state_dir}/ci/quality.yml.example" in staged
    settings_text = (state / "hooks" / "settings.template.json").read_text(
        encoding="utf-8"
    )
    json.loads(settings_text)


def test_report_ends_with_next_steps(tmp_path):
    _, _, lines = _adopt_into(tmp_path)
    assert lines[-1].startswith("next steps:")
    assert "bootstrap ask" in lines[-1]
    assert "mode" in lines[-1]


# ---------------------------------------------------------------------------
# Planted content quality
# ---------------------------------------------------------------------------


def test_planted_decisions_ledger_parses_with_an_entry(tmp_path):
    root, _, _ = _adopt_into(tmp_path)
    text = (root / "docs" / "decisions.md").read_text(encoding="utf-8")
    entries = parse_ledger(text)
    assert len(entries) >= 1
    assert entries[0]["id"] == "D-0001"


def test_planted_docs_have_no_badge_findings(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    findings = run_doc_checks(
        root / config.docs_root,
        config.badge_tokens,
        config.readpath_docs,
    )
    badge = [f for f in findings if f.kind == "badge"]
    assert badge == [], badge


def test_sessions_readme_names_convention_and_markers(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    text = (root / config.sessions_dir / "README.md").read_text(encoding="utf-8")
    assert "born-red" in text
    for marker in config.session_markers:
        assert marker["label"] in text


def test_sessions_readme_plants_each_marker_byte_form(tmp_path):
    # The run-1 ON-arm false-red guard (idea
    # model-line-checker-false-red-2026-07-09): the planted README must carry
    # each configured NEEDLE (the byte-form the checker scans for), not just
    # the label — an arm session that reads only this doc must be able to
    # write a card the needle scan accepts (`📊 Model:` included).
    root, config, _ = _adopt_into(tmp_path)
    text = (root / config.sessions_dir / "README.md").read_text(encoding="utf-8")
    for marker in config.session_markers:
        assert marker["needle"] in text, marker
        assert f"{marker['label']} (`{marker['needle']}`)" in text, marker


def test_sessions_readme_teaches_family_level_model_attribution(tmp_path):
    # ORDER 012 (fleet standing rule, fm model matrix 2026-07): the model
    # segment is the family-level name the session's OWN harness reports —
    # the committed card's self-report is the attribution ground truth;
    # external surfaces (schedule/Routines screens) are evidenced to
    # misattribute, and full dated model IDs are banned from attribution.
    root, config, _ = _adopt_into(tmp_path)
    text = (root / config.sessions_dir / "README.md").read_text(encoding="utf-8")
    assert "family-level model name your own harness" in text
    assert "attribution ground truth" in text
    assert "`fable-5`" in text
    assert "family-level names only" in text


def test_sessions_readme_model_doctrine_only_with_model_marker(tmp_path):
    # A host whose markers don't require the Model line gets no model
    # doctrine paragraph — the sentence is keyed to the configured needle.
    from engine.adopt import _adopt_sessions_readme

    without = _adopt_sessions_readme([{"label": "Status badge", "needle": "**Status:**"}])
    assert "attribution ground truth" not in without
    with_model = _adopt_sessions_readme(
        [{"label": "Model line", "needle": "\N{BAR CHART} Model:"}],
    )
    assert "attribution ground truth" in with_model
    assert "family-level names only" in with_model


def test_planted_index_skeleton_is_valid_json(tmp_path):
    root, _, _ = _adopt_into(tmp_path)
    data = json.loads((root / "project.index.json").read_text(encoding="utf-8"))
    assert data["areas"][0]["name"] == "example-area"


# ---------------------------------------------------------------------------
# Guardrail
# ---------------------------------------------------------------------------


def test_adopt_refuses_the_kits_own_tree():
    kit_root = Path("/srv/substrate-kit")
    config = Config()
    backend = JsonStateBackend(kit_root / config.state_dir / "state.json")
    with pytest.raises(UnsafeTargetError):
        adopt(kit_root, config, backend, kit_root=kit_root)


# ---------------------------------------------------------------------------
# ci_snippet
# ---------------------------------------------------------------------------


def test_ci_snippet_is_fully_commented_and_runs_strict_check():
    text = ci_snippet()
    assert "bootstrap.py check --strict" in text
    needles = ("docs", "session-log", "namespace", "seam", "orientation", "ledger")
    for needle in needles:
        assert needle in text, needle
    assert all(line.startswith("#") for line in text.splitlines() if line.strip())


# ---------------------------------------------------------------------------
# Enforcement wiring (the forcing functions)
# ---------------------------------------------------------------------------


def test_live_ci_workflow_is_uncommented_and_gates_on_the_session_log():
    text = live_ci_workflow()
    # Real workflow, not a commented example: the YAML keys are live.
    assert "\nname: substrate-gate\n" in text
    assert "on:\n" in text and "jobs:\n" in text
    # The locked door: the required check fails without a session log.
    assert "check --strict --require-session-log" in text
    # A custom interpreter threads through (the config's check interpreter).
    assert "python3.10 bootstrap.py" in live_ci_workflow("python3.10")


def test_wire_enforcement_plants_live_ci_and_live_claude(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    # The locked door: a live CI workflow running the gate.
    workflow = root / LIVE_CI_RELPATH
    assert workflow.is_file()
    assert "check --strict --require-session-log" in workflow.read_text(
        encoding="utf-8"
    )
    assert f"planted: {LIVE_CI_RELPATH}" in lines
    # The nag: wire_enforcement implies include_claude → live hooks.
    assert (root / ".claude" / "settings.json").is_file()
    settings = json.loads(
        (root / ".claude" / "settings.json").read_text(encoding="utf-8")
    )
    stop_cmd = settings["hooks"]["Stop"][0]["hooks"][0]["command"]
    assert "hook stopcheck" in stop_cmd


def test_default_adopt_never_installs_live_ci(tmp_path):
    root, _, _ = _adopt_into(tmp_path)
    # Safety default preserved: no live CI, no live .claude, without opt-in.
    assert not (root / LIVE_CI_RELPATH).exists()
    assert not (root / ".claude").exists()


def test_live_gate_is_kit_owned_and_regenerated_in_place(tmp_path):
    # EAP program review §6.1: the live gate is KIT-OWNED — an existing file
    # (a stale template, a hand-forked fix like gba-homebrew's) is regenerated
    # on every adopt/upgrade pass, so upstream gate fixes reach installed
    # gates instead of stranding as hand-forked patches. (This inverts the
    # old never-clobber test on purpose — that behavior is what stranded the
    # gba-homebrew fix outside the kit.)
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / LIVE_CI_RELPATH
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: mine\n", encoding="utf-8")
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    assert workflow.read_text(encoding="utf-8") == live_ci_workflow()
    assert any(
        line.startswith(f"regenerated: {LIVE_CI_RELPATH}") for line in lines
    )


def test_default_adopt_regenerates_an_existing_live_gate(tmp_path):
    # Existence is the opt-in signal after the first install: even WITHOUT
    # --wire-enforcement (the upgrade verb's adopt pass runs exactly this
    # shape), an existing gate is refreshed to the current template — but a
    # default adopt still never CREATES one (the safety doctrine, covered by
    # test_default_adopt_never_installs_live_ci above).
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / LIVE_CI_RELPATH
    workflow.parent.mkdir(parents=True)
    workflow.write_text(
        "# stale hand-forked gate\nname: substrate-gate\n", encoding="utf-8"
    )
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert workflow.read_text(encoding="utf-8") == live_ci_workflow()
    assert any(
        line.startswith(f"regenerated: {LIVE_CI_RELPATH}") for line in lines
    )
    # Idempotent second pass: already current -> kept, byte-identical.
    lines2 = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert workflow.read_text(encoding="utf-8") == live_ci_workflow()
    assert f"kept: {LIVE_CI_RELPATH} (kit-owned, already current)" in lines2


def test_live_ci_workflow_declares_kit_ownership():
    # The overwrite-on-upgrade contract must be visible in the file itself:
    # the generated header says KIT-OWNED and routes host customizations to
    # a separate workflow file.
    text = live_ci_workflow()
    assert "KIT-OWNED" in text
    assert "SEPARATE workflow" in text
    assert "NOTE: the INSTALLED .github/workflows/substrate-gate.yml" in ci_snippet()


# ---------------------------------------------------------------------------
# Version + planted-doc hash recording (KL-1, founding plan §4.1/§4.3)
# ---------------------------------------------------------------------------


def test_adopt_records_kit_version_in_config_and_state(tmp_path):
    root, config, lines = _adopt_into(tmp_path)
    assert config.kit_version == KIT_VERSION
    # Persisted (not just in-memory): reload both from disk.
    assert load_config(root).kit_version == KIT_VERSION
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    assert backend.get("kit_version") == KIT_VERSION
    assert f"recorded: kit_version {KIT_VERSION}" in lines


def test_adopt_records_a_hash_per_planted_doc(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    hashes = backend.get(DOC_HASHES_STATE_KEY)
    for _, rel in ADOPT_PLAN:
        assert rel in hashes, rel
        # The recorded hash matches the on-disk bytes → doc_is_untouched.
        text = (root / rel).read_text(encoding="utf-8")
        assert doc_is_untouched(backend, rel, text), rel


def test_kept_docs_get_no_hash_recorded(tmp_path):
    # A pre-existing (consumer-owned) file is never claimed as kit-written:
    # no recorded hash → the upgrade diff honestly treats it as diverged.
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    theirs = root / "CONSTITUTION.md"
    theirs.parent.mkdir(parents=True, exist_ok=True)
    theirs.write_text("consumer-owned\n", encoding="utf-8")
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    hashes = (
        JsonStateBackend(root / config.state_dir / "state.json").get(
            DOC_HASHES_STATE_KEY,
        )
        or {}
    )
    assert "CONSTITUTION.md" not in hashes
    assert not doc_is_untouched(backend, "CONSTITUTION.md", "consumer-owned\n")


def test_hand_edit_breaks_untouched(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    rel = "docs/architecture.md"
    edited = (root / rel).read_text(encoding="utf-8") + "\nconsumer note\n"
    assert not doc_is_untouched(backend, rel, edited)


def test_adopt_archives_the_running_dist(tmp_path, monkeypatch):
    # §4.3 ordering constraint: the archive must exist BEFORE any future
    # overwrite, so adopt (not just upgrade) banks the running single file
    # under <state_dir>/backup/bootstrap-<version>.py.
    fake = tmp_path / "downloads" / "bootstrap.py"
    fake.parent.mkdir(parents=True)
    fake.write_text(
        '"""substrate-kit bootstrap v0.9.9 — GENERATED, DO NOT EDIT."""\n',
        encoding="utf-8",
    )
    monkeypatch.setattr("sys.argv", [str(fake), "adopt"])
    root, config, lines = _adopt_into(tmp_path)
    archived = root / config.state_dir / "backup" / "bootstrap-0.9.9.py"
    assert archived.is_file()
    assert archived.read_text(encoding="utf-8") == fake.read_text(encoding="utf-8")
    assert f"archived: {config.state_dir}/backup/bootstrap-0.9.9.py" in lines


def test_archive_dist_reports_already_banked_on_the_idempotent_path(tmp_path):
    # The idempotent early return must never be silent (idea
    # upgrade-archive-report-line-gap): an upgrade whose OLD dist was already
    # banked would otherwise print no `archived:` line for it, leaving the
    # report's only such line naming the NEW version — three field reads of the
    # same doubt. The second archive still accounts for the old dist explicitly.
    root = tmp_path / "repo"
    config = Config()
    dist_file = root / "bootstrap.py"
    dist_file.parent.mkdir(parents=True, exist_ok=True)
    dist_file.write_text(
        '"""substrate-kit bootstrap v0.9.0 — GENERATED, DO NOT EDIT."""\n',
        encoding="utf-8",
    )
    rel = f"{config.state_dir}/backup/bootstrap-0.9.0.py"

    first: list[str] = []
    archive_dist(root, config, dist_file, first)
    assert first == [f"archived: {rel}"]

    second: list[str] = []
    archive_dist(root, config, dist_file, second)
    assert second == [f"archived: {rel} (already banked)"]


def test_dist_version_parses_the_header_stamp():
    header = '"""substrate-kit bootstrap v1.2.3 — GENERATED, DO NOT EDIT.\nrest'
    assert dist_version(header) == "1.2.3"
    assert dist_version('"""no stamp here"""') is None


# ---------------------------------------------------------------------------
# Diff-aware gate selection + guard-recipe convention (groomed-ideas-1)
# ---------------------------------------------------------------------------


def test_live_ci_workflow_selects_the_card_from_the_diff():
    text = live_ci_workflow()
    # The gate step derives the card from what the PR/push diff touches and
    # passes it explicitly — a fresh checkout flattens mtimes, so the engine's
    # newest-by-mtime guess is unreliable in CI (the mtime-restore-shim trap).
    assert "--session-log" in text
    assert "git diff --name-only" in text
    assert "'.sessions/*.md'" in text
    # No card in the diff -> an explicitly named ABSENT sentinel (advisory per
    # the engine contract), never the bare mtime fallback: on a fresh checkout
    # the fallback latches onto the mid-session in-progress card and reds
    # every unrelated PR (adopter live-fire, gba-homebrew PR #3, 2026-07-10).
    assert "--session-log .sessions/__no-card-in-diff__.md" in text
    assert '${card:+--session-log "$card"}' not in text
    # A custom sessions_dir threads through, README excluded from selection.
    custom = live_ci_workflow(sessions_dir="journal")
    assert "'journal/*.md'" in custom
    assert ":!journal/README.md" in custom
    assert "--session-log journal/__no-card-in-diff__.md" in custom
    assert "--session-log journal/__born-red-card-added__.md" in custom


def test_live_ci_workflow_gates_added_cards_by_declared_status():
    text = live_ci_workflow()
    # EVERY card ADDED by the PR is a born-red heartbeat (first-commit
    # conventions REQUIRE an in-progress card at birth); each gates via the
    # absent sentinel + --added-card, whose declared-status tiering HOLDs an
    # in-progress card red until it flips complete (the superbot-games #40
    # card-only loophole fix) while never grading mid-flight completeness
    # (gba-homebrew PR #2). Sibling cards modified in the same diff are
    # advisory-only; a modified-only diff keeps the full
    # --require-session-log locked door on each modified card.
    assert "--diff-filter=A" in text
    assert "--session-log .sessions/__born-red-card-added__.md" in text
    # The multi-card loop replaced the tail-1 single-card pick (venture-lab
    # #33 shadowing loophole): added/changed card lists are no longer
    # tail-1-truncated, and every added card walks the added-card lane.
    assert 'done <<< "$added"' in text
    assert "| tail -1)\"\n          added=" not in text
    assert "modified sibling card (advisory" in text
    # The locked door still exists — on the modified-only branch.
    assert 'check --strict --require-session-log --session-log "$card"' in text
    # The gate-regen locked-door branch also self-tests the added-card lane
    # (--simulate-added-card), so the lane stays observable on the very PRs
    # that ship gate changes.
    assert '--simulate-added-card "$card"' in text
    # The interpreter threads through all four branches (locked door with
    # simulate, added-card hold lane, modified-card locked door, no-card
    # sentinel).
    custom = live_ci_workflow("python3.10")
    assert custom.count("python3.10 bootstrap.py check --strict") == 4


def test_sessions_readme_carries_the_guard_recipe_convention(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    text = (root / config.sessions_dir / "README.md").read_text(encoding="utf-8")
    # Friction->guard entries name their code anchors, not just the symptom.
    assert "Guard recipes" in text
    assert "function + file" in text


# ---------------------------------------------------------------------------
# The control/ coordination scaffold + CI control fast lane (band KL-8)
# ---------------------------------------------------------------------------


def test_adopt_plants_the_control_bus(tmp_path):
    root, _, lines = _adopt_into(tmp_path)
    for rel in ("control/README.md", "control/inbox.md", "control/status.md"):
        assert (root / rel).is_file(), rel
        assert f"planted: {rel}" in lines
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    # The contract's load-bearing lines travel: one writer per file, the two
    # formats, and both 2026-07-09 CI lessons (fast lane over paths-ignore;
    # API-authored PRs may carry zero check runs).
    assert "One writer per file" in readme
    assert "status.md" in readme and "inbox.md" in readme
    assert "paths-ignore" in readme
    assert "API-authored PRs may not trigger CI" in readme
    # project_name derived at adopt: the local copy names its own repo.
    assert "repo" in readme


def test_control_status_seed_has_no_fake_heartbeat(tmp_path):
    from engine.checks.check_status_current import parse_heartbeat

    root, _, _ = _adopt_into(tmp_path)
    seed = (root / "control" / "status.md").read_text(encoding="utf-8")
    # Honest seed: no parseable heartbeat until the Project writes a real
    # one — check gates strict RED on this state (status-no-heartbeat).
    assert parse_heartbeat(seed) is None
    assert "SOLE writer" in seed
    inbox = (root / "control" / "inbox.md").read_text(encoding="utf-8")
    assert "ONE writer: the manager" in inbox


def test_control_status_seed_carries_the_kit_self_report_line(tmp_path):
    # ORDER 003 (adopter-visibility band): the seed self-reports the REAL
    # planted kit version — no stranded ${kit_version} placeholder — with the
    # honest born-red starting values, and the planted contract documents the
    # line's format so every adopter knows to keep it current.
    root, _, _ = _adopt_into(tmp_path)
    seed = (root / "control" / "status.md").read_text(encoding="utf-8")
    assert f"kit: v{KIT_VERSION} · check: red · engaged: no" in seed
    assert "${kit_version}" not in seed
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    assert "kit: v<X.Y.Z> · check: green|red · engaged: yes|no" in readme


def test_control_files_are_never_clobbered_on_readopt(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    status = root / "control" / "status.md"
    status.write_text("# mine\nupdated: 2026-07-09T12:00Z\n", encoding="utf-8")
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert status.read_text(encoding="utf-8") == "# mine\nupdated: 2026-07-09T12:00Z\n"
    assert "kept: control/status.md" in lines


def test_live_ci_workflow_carries_the_control_fast_lane():
    text = live_ci_workflow()
    # The lane detects a control/**-only diff and short-circuits IN-JOB —
    # the required context always reports (paths-ignore would leave it
    # pending and jam heartbeat auto-merge, the 2026-07-09 lesson).
    assert "id: lane" in text
    assert "grep -v '^control/'" in text
    assert 'control_only=$control_only" >> "$GITHUB_OUTPUT"' in text
    # Every heavy step is conditioned on the lane verdict.
    assert text.count("if: steps.lane.outputs.control_only != 'true'") == 2
    # And no live paths-ignore key anywhere — the short-circuit IS the skip
    # (the word appears only in the warning comment).
    assert "paths-ignore:" not in text


def test_live_ci_workflow_fast_lane_still_gates_the_heartbeat():
    text = live_ci_workflow()
    # Fleet adoption review fix (2026-07-09): the lane must still run the
    # scoped status gate — a control-only diff edits exactly the files
    # check_status_current validates, so a checker-free lane let a
    # heartbeat-deleting control PR merge green (red deferred onto the next
    # unrelated PR). Plain system python3: setup-python is skipped on the
    # lane, and the engine is stdlib-only by contract.
    assert "python3 bootstrap.py check --strict --status-only" in text
    step = text.split("- name: control-status gate", 1)
    assert len(step) == 2, "planted gate misses the fast-lane status step"
    body = step[1].split("- name:", 1)[0]
    assert "if: steps.lane.outputs.control_only == 'true'" in body


def test_live_ci_workflow_wires_the_inbox_base_gate():
    # The v1.7.0 distribution-wave finding: the generated gate never wired
    # --inbox-base, so inbox pure-append enforcement (issue #36 report 2)
    # was LATENT on every adopter — only the kit's own ci.yml ran it. The
    # planted gate must (1) carry the step, (2) run it on BOTH lanes (no
    # lane condition — an inbox append rides the fast lane, a mixed PR the
    # full one), (3) extract the merge-base blob in bash and hand it in via
    # --inbox-base (the engine never shells out to git), (4) self-skip when
    # the inbox is untouched.
    text = live_ci_workflow()
    step = text.split("- name: inbox append-only gate", 1)
    assert len(step) == 2, "planted gate misses the inbox append-only step"
    body = step[1].split("- uses: actions/setup-python@v6", 1)[0]
    assert "if: steps.lane.outputs" not in body  # both lanes
    assert "git merge-base" in body
    assert "git show" in body
    assert "control/inbox.md not in diff" in body  # self-skip
    assert (
        'python3 bootstrap.py check --strict --status-only '
        '--inbox-base "$basefile"' in body
    )


def test_gate_carveouts_detects_host_added_job_and_step():
    from engine.adopt import gate_carveouts

    expected = live_ci_workflow()
    # Identical gate: nothing host-added.
    assert gate_carveouts(expected, expected) == []
    # A host-added step inside a kit job (and kit steps are never flagged).
    live = expected.replace(
        "      - uses: actions/setup-python@v6\n",
        "      - name: host coverage upload\n"
        "        run: echo host step\n"
        "      - uses: actions/setup-python@v6\n",
    )
    assert gate_carveouts(live, expected) == [
        "host-added step 'host coverage upload' in job 'substrate-gate'",
    ]
    # A whole host-added job (the superbot-games #16 shape: the repo's ONLY
    # pytest job hand-added inside the kit-owned gate).
    live = expected + (
        "  pytest:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - uses: actions/checkout@v5\n"
        "      - name: host test suite\n"
        "        run: python3 -m pytest tests/ -q\n"
    )
    (line,) = gate_carveouts(live, expected)
    assert line.startswith("host-added job 'pytest'")
    assert "host test suite" in line
    # Kit content the host merely edited/removed is NOT a carve-out (the
    # regen restores it by design).
    stale = expected.replace(
        "      - uses: actions/setup-python@v6\n"
        "        if: steps.lane.outputs.control_only != 'true'\n"
        "        with:\n"
        '          python-version: "3.x"\n',
        "",
    )
    assert gate_carveouts(stale, expected) == []


def test_adopt_gate_regen_banks_and_reports_carveouts(tmp_path):
    # The regen path itself (adopt step 6b): a live gate carrying a
    # host-added job is still regenerated to kit form, but the additions are
    # reported as carve-outs and the FULL pre-regen copy is banked under
    # <state_dir>/backup/ — never a silent drop (superbot-games #16 class).
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / LIVE_CI_RELPATH
    workflow.parent.mkdir(parents=True)
    hand_edited = live_ci_workflow() + (
        "  pytest:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: host test suite\n"
        "        run: python3 -m pytest tests/ -q\n"
    )
    workflow.write_text(hand_edited, encoding="utf-8")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert workflow.read_text(encoding="utf-8") == live_ci_workflow()
    assert any(
        line.startswith(f"carve-out: {LIVE_CI_RELPATH} — host-added job 'pytest'")
        for line in lines
    )
    banked = list(
        (root / config.state_dir / "backup").glob("substrate-gate.pre-regen-*.yml")
    )
    assert len(banked) == 1
    assert banked[0].read_text(encoding="utf-8") == hand_edited
    # And a stale-but-addition-free gate regens CLEAN: no carve-out lines,
    # no banked copy beyond the one above (fresh root to prove zero).
    root2 = tmp_path / "repo2"
    backend2 = _make_backend(root2, Config())
    workflow2 = root2 / LIVE_CI_RELPATH
    workflow2.parent.mkdir(parents=True)
    workflow2.write_text(
        "# stale hand-forked gate\nname: substrate-gate\n", encoding="utf-8"
    )
    lines2 = adopt(root2, Config(), backend2, kit_root=tmp_path / "kit")
    assert not any(line.startswith("carve-out:") for line in lines2)
    assert not list(
        (root2 / Config().state_dir / "backup").glob("substrate-gate.pre-regen-*.yml")
    )


# ---------------------------------------------------------------------------
# Auto-merge enabler planted by the kit (EAP program review §6.10)
# ---------------------------------------------------------------------------


def test_automerge_enabler_workflow_shape():
    text = automerge_enabler_workflow()
    # A real live workflow, not a commented example.
    assert "\nname: auto-merge-enabler\n" in text
    assert "on:\n" in text and "jobs:\n" in text
    # Arms only agent branches (default claude/*), same-repo PRs, non-draft.
    assert "startsWith(github.head_ref, 'claude/')" in text
    assert (
        "github.event.pull_request.head.repo.full_name == github.repository"
        in text
    )
    assert "github.event.pull_request.draft == false" in text
    # The refuse-to-arm guard counts required CONTEXTS on the base branch
    # (the KL-0/KL-1 instant-merge footgun).
    assert "rules/branches/${{ github.base_ref }}" in text
    assert "required_status_checks" in text
    # The label carve-out: job-level skip AND the fresh API re-read race
    # guard both travel into the planted file.
    assert (
        "!contains(github.event.pull_request.labels.*.name, "
        f"'{AUTOMERGE_CARVEOUT_LABEL}')" in text
    )
    assert f"Re-check the {AUTOMERGE_CARVEOUT_LABEL} label FRESH" in text
    # `synchronize` re-arms after a branch update (the behind-stall fix).
    assert "types: [opened, reopened, ready_for_review, synchronize]" in text
    # Kit ownership is declared in the file itself, routing host edits away.
    assert "KIT-OWNED" in text
    assert "SEPARATE workflow" in text


def test_automerge_enabler_workflow_parameterization():
    # Custom patterns render as prefix/exact matches; the context name
    # threads into the log lines.
    text = automerge_enabler_workflow(
        ["bot/*", "release-please"], required_context="quality"
    )
    assert "startsWith(github.head_ref, 'bot/')" in text
    assert "github.head_ref == 'release-please'" in text
    assert "startsWith(github.head_ref, 'claude/')" not in text
    assert "'quality' is green" in text
    # Fallback-on-empty (the heartbeat_files doctrine): [] / blank / a bare
    # "*" must not silently widen arming to every branch.
    for degenerate in ([], [""], ["*"], ["  "]):
        text = automerge_enabler_workflow(degenerate)
        assert "startsWith(github.head_ref, 'claude/')" in text


def test_adopt_stages_the_enabler_and_never_installs_it_by_default(tmp_path):
    root, config, lines = _adopt_into(tmp_path)
    # Staged always, right next to the gate (the one-copy install).
    staged = root / config.state_dir / "ci" / "auto-merge-enabler.yml"
    assert staged.is_file()
    assert staged.read_text(encoding="utf-8") == automerge_enabler_workflow()
    # Safety doctrine unchanged: a default adopt never creates live CI —
    # and without a live enabler there is no repo-settings checklist.
    assert not (root / AUTOMERGE_ENABLER_RELPATH).exists()
    assert not any("repo-settings checklist" in line for line in lines)


def test_wire_enforcement_plants_live_enabler_and_repo_settings_checklist(
    tmp_path,
):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    workflow = root / AUTOMERGE_ENABLER_RELPATH
    assert workflow.is_file()
    assert workflow.read_text(encoding="utf-8") == automerge_enabler_workflow()
    assert f"planted: {AUTOMERGE_ENABLER_RELPATH}" in lines
    # The §6.10 second half: the one-time owner-UI checklist rides the
    # adopt report (a planted workflow cannot flip repo settings — the
    # trading-strategy Allow-auto-merge-OFF boundary).
    assert any("repo-settings checklist" in line for line in lines)
    assert any('"Allow auto-merge" = ON' in line for line in lines)
    assert any("'substrate-gate' status check" in line for line in lines)


def test_default_adopt_regenerates_an_existing_live_enabler(tmp_path):
    # Existence is the opt-in signal (the gate's exact lifecycle): a
    # hand-forked enabler at the kit path falls under kit ownership on the
    # next adopt/upgrade pass — parameterized from the host's own config.
    root = tmp_path / "repo"
    config = Config()
    config.automerge = {
        "branch_patterns": ["agent/*"],
        "required_context": "quality",
    }
    backend = _make_backend(root, config)
    workflow = root / AUTOMERGE_ENABLER_RELPATH
    workflow.parent.mkdir(parents=True)
    workflow.write_text(
        "# hand-forked enabler\nname: auto-merge-enabler\n", encoding="utf-8"
    )
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    expected = automerge_enabler_workflow(["agent/*"], required_context="quality")
    assert workflow.read_text(encoding="utf-8") == expected
    assert any(
        line.startswith(f"regenerated: {AUTOMERGE_ENABLER_RELPATH}")
        for line in lines
    )
    # Idempotent second pass: already current -> kept, byte-identical.
    lines2 = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert workflow.read_text(encoding="utf-8") == expected
    assert (
        f"kept: {AUTOMERGE_ENABLER_RELPATH} (kit-owned, already current)"
        in lines2
    )


def test_adopt_enabler_regen_banks_and_reports_carveouts(tmp_path):
    # The #137 carve-out protection applies to the enabler identically: a
    # host-added job inside the kit-owned file is banked + reported, never
    # silently dropped — and the regen still restores kit form.
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / AUTOMERGE_ENABLER_RELPATH
    workflow.parent.mkdir(parents=True)
    hand_edited = automerge_enabler_workflow() + (
        "  notify:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: host notifier\n"
        "        run: echo merged\n"
    )
    workflow.write_text(hand_edited, encoding="utf-8")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert workflow.read_text(encoding="utf-8") == automerge_enabler_workflow()
    assert any(
        line.startswith(
            f"carve-out: {AUTOMERGE_ENABLER_RELPATH} — host-added job 'notify'"
        )
        for line in lines
    )
    banked = list(
        (root / config.state_dir / "backup").glob(
            "auto-merge-enabler.pre-regen-*.yml"
        )
    )
    assert len(banked) == 1
    assert banked[0].read_text(encoding="utf-8") == hand_edited


# ---------------------------------------------------------------------------
# Lane-aware adopt (`adopt --lane` — queue item 11, the G1 double-adoption fix)
# ---------------------------------------------------------------------------


def _adopt_with_lane(tmp_path, lane, *, root=None, config=None, backend=None):
    root = root or tmp_path / "repo"
    config = config or Config()
    backend = backend or _make_backend(root, config)
    lines = adopt(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        lane=lane,
    )
    return root, config, backend, lines


def test_adopt_lane_plants_lane_heartbeat_not_the_singular(tmp_path):
    root, config, _, lines = _adopt_with_lane(tmp_path, "mining")
    # The heartbeat is the ONE per-Project file on the bus: it plants
    # parametrized, and the singular control/status.md is never created.
    assert (root / "control" / "status-mining.md").is_file()
    assert "planted: control/status-mining.md" in lines
    assert not (root / "control" / "status.md").exists()
    # The shared bus still plants (single inbox, single README).
    assert (root / "control" / "inbox.md").is_file()
    assert (root / "control" / "README.md").is_file()
    # Lane-shaped from the start: the lane REPLACES the untouched default —
    # the gate must not hold strict RED on a singular file no Project owns.
    assert config.heartbeat_files == ["control/status-mining.md"]
    # Persisted, not just in-memory (the checker reads the config from disk).
    assert load_config(root).heartbeat_files == ["control/status-mining.md"]


def test_adopt_lane_joins_an_existing_install(tmp_path):
    # A second Project joining an adopted repo: its heartbeat is ADDED, the
    # first Project's files (singular heartbeat included) are never touched.
    root, config, _ = _adopt_into(tmp_path)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    _, config, _, lines = _adopt_with_lane(
        tmp_path, "exploration", root=root, config=config, backend=backend
    )
    assert (root / "control" / "status-exploration.md").is_file()
    assert "planted: control/status-exploration.md" in lines
    assert "kept: control/inbox.md" in lines
    assert "kept: control/README.md" in lines
    assert config.heartbeat_files == [
        "control/status.md",
        "control/status-exploration.md",
    ]
    assert load_config(root).heartbeat_files == config.heartbeat_files


def test_adopt_lane_is_idempotent(tmp_path):
    root, config, backend, _ = _adopt_with_lane(tmp_path, "mining")
    seed = root / "control" / "status-mining.md"
    seed.write_text("# mine\nupdated: 2026-07-10T00:00:00Z\n", encoding="utf-8")
    _, config, _, lines = _adopt_with_lane(
        tmp_path, "mining", root=root, config=config, backend=backend
    )
    # Re-adopt keeps the lane's own heartbeat and never duplicates the entry.
    assert seed.read_text(encoding="utf-8").startswith("# mine")
    assert "kept: control/status-mining.md" in lines
    assert config.heartbeat_files == ["control/status-mining.md"]
    assert (
        "lane: mining — heartbeat already declared (control/status-mining.md)"
        in lines
    )


def test_adopt_lane_never_drops_a_sibling_lane(tmp_path):
    # Two lanes adopting in sequence into one shared repo: the second lane
    # APPENDS to heartbeat_files — splitting the heartbeat, never sharing or
    # clobbering it (the superbot-games shape, end-to-end via --lane).
    root, config, backend, _ = _adopt_with_lane(tmp_path, "mining")
    _, config, _, _ = _adopt_with_lane(
        tmp_path, "exploration", root=root, config=config, backend=backend
    )
    assert config.heartbeat_files == [
        "control/status-mining.md",
        "control/status-exploration.md",
    ]
    assert load_config(root).heartbeat_files == config.heartbeat_files
    assert (root / "control" / "status-mining.md").is_file()
    assert (root / "control" / "status-exploration.md").is_file()


def test_adopt_lane_records_doc_hash_under_the_lane_relpath(tmp_path):
    root, _, backend, _ = _adopt_with_lane(tmp_path, "mining")
    rel = "control/status-mining.md"
    text = (root / rel).read_text(encoding="utf-8")
    assert doc_is_untouched(backend, rel, text)
    hashes = backend.get(DOC_HASHES_STATE_KEY)
    # Provenance follows what was actually written: no phantom hash for the
    # never-planted singular heartbeat.
    assert "control/status.md" not in hashes


def test_adopt_lane_seed_is_a_real_seed(tmp_path):
    from engine.checks.check_status_current import parse_heartbeat

    root, _, _, _ = _adopt_with_lane(tmp_path, "mining")
    seed = (root / "control" / "status-mining.md").read_text(encoding="utf-8")
    # Same honest-seed contract as the singular file: no parseable heartbeat
    # until the lane writes a real one; check gates strict RED until then.
    assert parse_heartbeat(seed) is None
    assert "SOLE writer" in seed


@pytest.mark.parametrize(
    "bad",
    ["../evil", "a/b", "", ".hidden", "sp ace", "-lead", "dot.dot"],
)
def test_adopt_lane_refuses_unsafe_names(tmp_path, bad):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    with pytest.raises(ValueError):
        adopt(root, config, backend, kit_root=tmp_path / "kit", lane=bad)
    # Refused BEFORE any write: nothing planted.
    assert not (root / "control").exists()
    assert config.heartbeat_files == ["control/status.md"]


def test_cmd_adopt_lane_end_to_end_and_refusal(tmp_path, capsys):
    from engine.cli import cmd_adopt

    root = tmp_path / "repo"
    assert cmd_adopt(root, include_claude=False, lane="mining") == 0
    out = capsys.readouterr().out
    assert "planted: control/status-mining.md" in out
    # The engagement checklist gates the LANE heartbeat (config read in the
    # same pass — the adopt output already points at the lane's seed).
    assert "status-no-heartbeat" in out
    assert "control/status-mining.md" in out
    assert load_config(root).heartbeat_files == ["control/status-mining.md"]
    # An unsafe lane name refuses loudly with the CLI's refusal exit code.
    assert cmd_adopt(tmp_path / "other", include_claude=False, lane="../up") == 2
    out = capsys.readouterr().out
    assert "adopt: REFUSED" in out
    assert "invalid lane name" in out


def test_planted_readme_documents_the_one_command_lane_shape(tmp_path):
    # The planted contract advertises the scaffold, not just the convention:
    # a second Project reads ONE command instead of three hand-edits.
    root, _, _ = _adopt_into(tmp_path)
    readme = (root / "control" / "README.md").read_text(encoding="utf-8")
    assert "adopt --lane <name>" in readme
    assert "control/status-<name>.md" in readme


# ---------------------------------------------------------------------------
# Queued kit fixes batch (2026-07-11): explicit-when-clean carve-out scan ·
# archive hash-verify + dedup · mid-PR gate-regen born-red hold
# ---------------------------------------------------------------------------


def test_kit_owned_regen_reports_explicit_clean_scan(tmp_path):
    # Queued fix 1 (fleet-manager #40 finding): a clean scan says so out
    # loud — silence was indistinguishable from "the detector never ran".
    # Covers both clean shapes: kept-already-current and regenerated-clean.
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / LIVE_CI_RELPATH
    workflow.parent.mkdir(parents=True)
    workflow.write_text(live_ci_workflow(), encoding="utf-8")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in lines

    root2 = tmp_path / "repo2"
    backend2 = _make_backend(root2, Config())
    workflow2 = root2 / LIVE_CI_RELPATH
    workflow2.parent.mkdir(parents=True)
    workflow2.write_text(
        "# stale hand-forked gate\nname: substrate-gate\n", encoding="utf-8"
    )
    lines2 = adopt(root2, Config(), backend2, kit_root=tmp_path / "kit")
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in lines2
    # A dirty regen reports its carve-outs INSTEAD of the clean-scan line.
    root3 = tmp_path / "repo3"
    backend3 = _make_backend(root3, Config())
    workflow3 = root3 / LIVE_CI_RELPATH
    workflow3.parent.mkdir(parents=True)
    workflow3.write_text(
        live_ci_workflow()
        + "  pytest:\n    runs-on: ubuntu-latest\n    steps:\n"
        "      - name: host suite\n        run: pytest\n",
        encoding="utf-8",
    )
    lines3 = adopt(root3, Config(), backend3, kit_root=tmp_path / "kit")
    assert not any(line.startswith("carve-out scan:") for line in lines3)
    assert any(line.startswith("carve-out:") for line in lines3)


def test_archive_dist_never_overwrites_a_differing_bank(tmp_path):
    # Queued fix 2 (wave B' verification): a pre-existing archive at the
    # target name with DIFFERENT bytes is a rollback source — never
    # overwritten, never silently accepted. The new bytes bank under a
    # content-hash dedup name and the collision is reported.
    root = tmp_path / "repo"
    config = Config()
    dist_file = root / "bootstrap.py"
    dist_file.parent.mkdir(parents=True, exist_ok=True)
    dist_file.write_text(
        '"""substrate-kit bootstrap v0.9.0 — GENERATED, DO NOT EDIT."""\n# A\n',
        encoding="utf-8",
    )
    rel = f"{config.state_dir}/backup/bootstrap-0.9.0.py"
    first: list[str] = []
    banked = archive_dist(root, config, dist_file, first)
    assert first == [f"archived: {rel}"]
    original_bytes = banked.read_text(encoding="utf-8")

    # Same version stamp, different content (the bootstrap-unknown.py /
    # re-tagged-dist collision class).
    dist_file.write_text(
        '"""substrate-kit bootstrap v0.9.0 — GENERATED, DO NOT EDIT."""\n# B\n',
        encoding="utf-8",
    )
    second: list[str] = []
    dedup = archive_dist(root, config, dist_file, second)
    assert dedup != banked
    assert dedup.name.startswith("bootstrap-0.9.0.") and dedup.name.endswith(".py")
    assert dedup.read_text(encoding="utf-8") == dist_file.read_text(encoding="utf-8")
    # The pre-existing bank is byte-untouched and the collision is loud.
    assert banked.read_text(encoding="utf-8") == original_bytes
    assert len(second) == 1
    assert "NOT overwritten" in second[0]
    assert "name collision" in second[0]

    # Idempotent on the dedup path too.
    third: list[str] = []
    again = archive_dist(root, config, dist_file, third)
    assert again == dedup
    assert third == [
        f"archived: {config.state_dir}/backup/{dedup.name} (already banked)"
    ]


def test_gate_holds_added_card_to_locked_door_when_pr_regenerates_the_gate():
    # Queued fix 3 (venture-lab #14): a PR that both ADDS a session card and
    # touches the gate workflow itself runs the NEW gate mid-PR — the added
    # card must keep the FULL locked door, so hold semantics can only
    # tighten, never loosen, inside the PR that changes them.
    text = live_ci_workflow()
    assert f"'{LIVE_CI_RELPATH}'" in text
    assert 'gate_regen="$(git diff --name-only "$range" -- ' in text
    # Inside the added-card loop, a gate-touching PR routes EVERY added card
    # through the full locked door (+ the advisory simulate), not the
    # added-card lane.
    assert 'if [ -n "$gate_regen" ]; then' in text
    assert (
        '--require-session-log --session-log "$card"'
        ' --simulate-added-card "$card" || fail=1' in text
    )
    # The plain added-card advisory path survives for ordinary PRs.
    assert "__born-red-card-added__.md" in text


# ---------------------------------------------------------------------------
# Queued kit fixes batch 2 (2026-07-11)
# ---------------------------------------------------------------------------


def test_live_ci_workflow_grammar_checks_added_cards():
    # Fix 1 (venture-lab #15 false-green class): the added-card lane still
    # passes the absent sentinel as --session-log but grades the added card
    # via --added-card (in-progress → HOLD, grammar misses → red).
    text = live_ci_workflow()
    assert '--session-log .sessions/__born-red-card-added__.md --added-card "$card"' in text
    assert "in-progress HOLDs until the card flips complete" in text
    custom = live_ci_workflow(sessions_dir="journal")
    assert '--session-log journal/__born-red-card-added__.md --added-card "$card"' in custom


def test_workflow_context_names_reads_job_ids_and_display_names(tmp_path):
    from engine.adopt import _workflow_context_names

    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "ci.yml").write_text(
        "name: CI\non: [push]\njobs:\n  quality:\n    name: quality-display\n"
        "    runs-on: ubuntu-latest\n    steps:\n      - run: echo hi\n",
        encoding="utf-8",
    )
    names = _workflow_context_names(tmp_path)
    assert "quality" in names
    assert "quality-display" in names
    # No workflows dir → nothing judgeable.
    assert _workflow_context_names(tmp_path / "elsewhere") == set()


def test_required_context_advisory_fires_on_the_websites_shape(tmp_path):
    # Fix 3: config says 'substrate-gate' while the repo's own workflows only
    # produce a 'quality' context — one advisory line naming the override.
    from engine.adopt import _required_context_advisory

    wf = tmp_path / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "quality.yml").write_text(
        "name: Q\non: [push]\njobs:\n  quality:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: echo hi\n",
        encoding="utf-8",
    )
    line = _required_context_advisory(tmp_path, "substrate-gate")
    assert line is not None
    assert "'quality'" in line
    assert "required_context" in line
    # Matching context (job id) → silence.
    assert _required_context_advisory(tmp_path, "quality") is None
    # Nothing judgeable (no workflows) → silence, never a guess.
    assert _required_context_advisory(tmp_path / "empty", "substrate-gate") is None


def test_adopt_reports_required_context_mismatch(tmp_path):
    # Adopt-level: a host with pre-existing CI whose contexts don't include
    # the configured required_context gets the advisory in the report.
    root = tmp_path / "repo"
    wf = root / ".github" / "workflows"
    wf.mkdir(parents=True)
    (wf / "quality.yml").write_text(
        "name: Q\non: [push]\njobs:\n  quality:\n    runs-on: ubuntu-latest\n"
        "    steps:\n      - run: echo hi\n",
        encoding="utf-8",
    )
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert any("matches no job in .github/workflows/" in ln for ln in lines)


def test_wire_enforcement_adopt_has_no_context_mismatch(tmp_path):
    # The installed live gate itself produces the default 'substrate-gate'
    # context, so a --wire-enforcement adopt must stay silent.
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    assert not any("matches no job" in ln for ln in lines)


def test_adopt_plants_search_hygiene_surfaces(tmp_path):
    # Fix 5 (bench run-5 judge limitation 5, mechanical half): adopt plants
    # root-anchored .ignore + .gitattributes entries for the vendored dist
    # and the backup bank.
    root, config, lines = _adopt_into(tmp_path)
    ignore = (root / ".ignore").read_text(encoding="utf-8")
    assert "/bootstrap.py" in ignore
    assert f"/{config.state_dir.strip('/')}/backup/" in ignore
    attrs = (root / ".gitattributes").read_text(encoding="utf-8")
    assert "/bootstrap.py linguist-generated=true" in attrs
    assert (
        f"/{config.state_dir.strip('/')}/backup/** linguist-generated=true"
        in attrs
    )
    assert any(".ignore" in ln and "search-hygiene" in ln for ln in lines)


def test_search_hygiene_merges_never_clobbers(tmp_path):
    # A host .ignore/.gitattributes carries host policy: existing lines must
    # survive byte-for-byte; the kit only appends what is missing.
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".ignore").write_text("node_modules/\n", encoding="utf-8")
    (root / ".gitattributes").write_text(
        "*.png binary\n/bootstrap.py linguist-generated=true\n",
        encoding="utf-8",
    )
    config = Config()
    backend = _make_backend(root, config)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    ignore = (root / ".ignore").read_text(encoding="utf-8")
    assert ignore.startswith("node_modules/\n")
    assert "/bootstrap.py" in ignore
    attrs = (root / ".gitattributes").read_text(encoding="utf-8")
    assert attrs.startswith("*.png binary\n")
    # The already-present entry is not duplicated.
    assert attrs.count("/bootstrap.py linguist-generated=true") == 1


def test_search_hygiene_is_idempotent_across_passes(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    before_ignore = (root / ".ignore").read_text(encoding="utf-8")
    before_attrs = (root / ".gitattributes").read_text(encoding="utf-8")
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert (root / ".ignore").read_text(encoding="utf-8") == before_ignore
    assert (root / ".gitattributes").read_text(encoding="utf-8") == before_attrs
    assert any("already present" in ln for ln in lines)


# ---------------------------------------------------------------------------
# Gate multi-card grading — the tail-1 shadowing loophole (v1.10.1 payload)
#
# These tests EXECUTE the generated gate's actual bash run-block in a scratch
# git repo, with the engine replaced by a stub that models its graded-card
# contract (in-progress card -> exit 1, anything else -> exit 0) and logs
# every invocation. The engine's real grading is pinned separately by
# tests/test_cli_gate.py; the seam these tests pin is the SHELL side — which
# cards reach the engine, through which lane, and how verdicts combine. The
# old `tail -1` picker graded only the last-sorted card of the diff, so a PR
# that ADDED an in-progress card and MODIFIED a later-sorting sibling shipped
# the in-progress card GREEN (venture-lab #33 head 798a3d0, run 29144734514).
# ---------------------------------------------------------------------------

_STUB_ENGINE = """\
#!/usr/bin/env python3
import os, sys

args = sys.argv[1:]
with open(os.environ["STUB_LOG"], "a", encoding="utf-8") as f:
    f.write(" ".join(args) + "\\n")
target = None
if "--added-card" in args:
    target = args[args.index("--added-card") + 1]
elif "--session-log" in args:
    target = args[args.index("--session-log") + 1]
if target and os.path.exists(target):
    with open(target, encoding="utf-8") as f:
        if "in-progress" in f.read():
            sys.exit(1)
sys.exit(0)
"""

_COMPLETE_CARD = "# card\n\n> **Status:** `complete`\n\nall done\n"
_IN_PROGRESS_CARD = "# card\n\n> **Status:** `in-progress`\n\nborn red\n"


def _extract_run_block(text: str, step_marker: str) -> str:
    """Pull a step's ``run: |`` script out of a workflow's YAML text."""
    start = text.index(step_marker)
    run_at = text.index("run: |\n", start)
    body_indent = None
    lines = []
    for line in text[run_at:].split("\n")[1:]:
        if body_indent is None:
            body_indent = len(line) - len(line.lstrip(" "))
        if line.strip() == "" or not line.startswith(" " * body_indent):
            break
        lines.append(line[body_indent:])
    return "\n".join(lines) + "\n"


def _gate_script(tmp_path: Path, workflow_text: str, step_marker: str) -> Path:
    """Materialize a runnable gate script (GitHub expressions resolved)."""
    script = _extract_run_block(workflow_text, step_marker)
    script = script.replace("${{ github.base_ref }}", "main")
    script = script.replace("${{ github.event.before }}", "")
    script = script.replace("${{ github.sha }}", "HEAD")
    path = tmp_path / "gate.sh"
    path.write_text(script, encoding="utf-8")
    return path


def _git(repo: Path, *args: str) -> None:
    subprocess.run(
        ["git", "-c", "user.email=t@t", "-c", "user.name=t", *args],
        cwd=repo,
        check=True,
        capture_output=True,
    )


def _gate_repo(tmp_path: Path) -> Path:
    """Scratch repo: main carries a complete sibling card; a `pr` branch is
    checked out ready for the shape under test."""
    repo = tmp_path / "repo"
    (repo / ".sessions").mkdir(parents=True)
    _git(repo, "init", "-b", "main")
    (repo / ".sessions" / "README.md").write_text("# convention\n", encoding="utf-8")
    (repo / ".sessions" / "session-001.md").write_text(
        _COMPLETE_CARD, encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "baseline")
    _git(repo, "update-ref", "refs/remotes/origin/main", "main")
    _git(repo, "checkout", "-b", "pr")
    return repo


def _run_gate(tmp_path: Path, repo: Path, script: Path) -> tuple[int, str, str]:
    stub = tmp_path / "stub-engine"
    stub.write_text(_STUB_ENGINE, encoding="utf-8")
    stub.chmod(0o755)
    log = tmp_path / "stub.log"
    log.write_text("", encoding="utf-8")
    proc = subprocess.run(
        ["bash", "-e", str(script)],
        cwd=repo,
        capture_output=True,
        text=True,
        env={"PATH": "/usr/bin:/bin", "STUB_LOG": str(log)},
    )
    return proc.returncode, proc.stdout, log.read_text(encoding="utf-8")


def _generated_gate_script(tmp_path: Path) -> Path:
    stub = tmp_path / "stub-engine"
    text = live_ci_workflow(interpreter=str(stub))
    return _gate_script(
        tmp_path, text, "- name: substrate gate (docs + session-log required)"
    )


def test_gate_script_holds_the_shadowed_added_in_progress_card(tmp_path):
    # THE regression shape (venture-lab #33): the PR ADDS an in-progress card
    # AND MODIFIES a sibling card that sorts later alphabetically
    # (".sessions/session-001.md" > ".sessions/2026-...md"). The old picker
    # graded only the sibling and went GREEN; the gate must HOLD.
    repo = _gate_repo(tmp_path)
    (repo / ".sessions" / "2026-07-11-new.md").write_text(
        _IN_PROGRESS_CARD, encoding="utf-8"
    )
    sibling = repo / ".sessions" / "session-001.md"
    sibling.write_text(
        _COMPLETE_CARD + "\nprovenance-marked grammar backfill\n", encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "shadowing shape")
    rc, out, log = _run_gate(tmp_path, repo, _generated_gate_script(tmp_path))
    assert rc != 0, out
    # The added card reached the added-card lane.
    assert "--added-card .sessions/2026-07-11-new.md" in log
    # The modified sibling is advisory-only: logged, never graded.
    assert "modified sibling card (advisory" in out
    assert ".sessions/session-001.md" in out
    assert "session-001" not in log


def test_gate_script_passes_a_single_added_complete_card(tmp_path):
    repo = _gate_repo(tmp_path)
    (repo / ".sessions" / "2026-07-11-new.md").write_text(
        _COMPLETE_CARD, encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "single complete added card")
    rc, out, log = _run_gate(tmp_path, repo, _generated_gate_script(tmp_path))
    assert rc == 0, out
    assert "--added-card .sessions/2026-07-11-new.md" in log


def test_gate_script_holds_when_any_of_several_added_cards_is_in_progress(
    tmp_path,
):
    # Multiple ADDED cards: every one is graded; one in-progress card holds
    # the whole step even though a later-sorting added card is complete.
    repo = _gate_repo(tmp_path)
    (repo / ".sessions" / "2026-07-11-a.md").write_text(
        _IN_PROGRESS_CARD, encoding="utf-8"
    )
    (repo / ".sessions" / "2026-07-11-b.md").write_text(
        _COMPLETE_CARD, encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "two added cards, one in-progress")
    rc, out, log = _run_gate(tmp_path, repo, _generated_gate_script(tmp_path))
    assert rc != 0, out
    assert "--added-card .sessions/2026-07-11-a.md" in log
    assert "--added-card .sessions/2026-07-11-b.md" in log


def test_gate_script_modified_only_diff_keeps_the_locked_door(tmp_path):
    # No added card: the existing modified-card semantics — the full
    # --require-session-log locked door engages on the modified card.
    repo = _gate_repo(tmp_path)
    sibling = repo / ".sessions" / "session-001.md"
    sibling.write_text(_COMPLETE_CARD + "\nclose-out detail\n", encoding="utf-8")
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "modified-only diff")
    rc, out, log = _run_gate(tmp_path, repo, _generated_gate_script(tmp_path))
    assert rc == 0, out
    assert "--require-session-log --session-log .sessions/session-001.md" in log
    assert "--added-card" not in log


def test_kit_ci_gate_script_holds_the_shadowed_added_in_progress_card(tmp_path):
    # The kit's OWN .github/workflows/ci.yml had the same tail-1 picker; its
    # (single-lane) gate must also grade every diff card, so the shadowing
    # shape holds red via the engine's in-progress hold.
    ci_text = (
        Path(__file__).resolve().parents[1] / ".github" / "workflows" / "ci.yml"
    ).read_text(encoding="utf-8")
    stub = tmp_path / "stub-engine"
    ci_text = ci_text.replace("python3 dist/bootstrap.py", str(stub))
    script = _gate_script(
        tmp_path, ci_text, "- name: Session gate (§3.2 item 5"
    )
    repo = _gate_repo(tmp_path)
    (repo / ".sessions" / "2026-07-11-new.md").write_text(
        _IN_PROGRESS_CARD, encoding="utf-8"
    )
    (repo / ".sessions" / "session-001.md").write_text(
        _COMPLETE_CARD + "\nbackfill\n", encoding="utf-8"
    )
    _git(repo, "add", "-A")
    _git(repo, "commit", "-m", "shadowing shape")
    rc, out, log = _run_gate(tmp_path, repo, script)
    assert rc != 0, out
    # Both diff cards were graded through the locked door.
    assert "--session-log .sessions/2026-07-11-new.md" in log
    assert "--session-log .sessions/session-001.md" in log
