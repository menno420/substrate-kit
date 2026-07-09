"""Tests for the one-step adopt flow (Lane B8).

Covers: every ADOPT_PLAN target planted; re-adopt keeps (never clobbers)
hand-edited files; the .claude/ opt-in gate; the staged <state_dir> tree;
the planted ledger parsing through ``engine.ledger``; the guardrail refusal;
badge-cleanliness of the freshly planted doc tree; and the CI snippet.

``engine.adopt`` imports ``engine.hooks.settings`` (built by lane B7 in
parallel); until that module lands these tests skip rather than red the suite.
"""

import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import (
    ADOPT_PLAN,
    DOC_HASHES_STATE_KEY,
    LIVE_CI_RELPATH,
    UNRENDERED_BANNER_FIRST_LINE,
    adopt,
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


def test_wire_enforcement_does_not_clobber_an_existing_workflow(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = _make_backend(root, config)
    workflow = root / LIVE_CI_RELPATH
    workflow.parent.mkdir(parents=True)
    workflow.write_text("name: mine\n", encoding="utf-8")
    lines = adopt(
        root, config, backend, kit_root=tmp_path / "kit", wire_enforcement=True
    )
    assert workflow.read_text(encoding="utf-8") == "name: mine\n"
    assert f"kept: {LIVE_CI_RELPATH}" in lines


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
    # No card in the diff -> the argument is omitted (the engine falls back).
    assert '${card:+--session-log "$card"}' in text
    # A custom sessions_dir threads through, README excluded from selection.
    custom = live_ci_workflow(sessions_dir="journal")
    assert "'journal/*.md'" in custom
    assert ":!journal/README.md" in custom


def test_sessions_readme_carries_the_guard_recipe_convention(tmp_path):
    root, config, _ = _adopt_into(tmp_path)
    text = (root / config.sessions_dir / "README.md").read_text(encoding="utf-8")
    # Friction->guard entries name their code anchors, not just the symptom.
    assert "Guard recipes" in text
    assert "function + file" in text
