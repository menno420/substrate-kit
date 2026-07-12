"""Tests for the skills layer + the skill/stance precedence model (section 3c)."""

from engine import cli
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import find_placeholders
from engine.skills.skills import (
    SKILLS,
    action_permitted,
    get_skill,
    skill_capabilities,
    skill_document,
    skill_frontmatter,
    skill_names,
    skill_permits,
    skill_relpath,
    skills_index_table,
)
from engine.stances.stances import EDIT, READ, RUN


def _init(target):
    config = Config()
    save_config(target, config)
    state_path = target / config.state_dir / "state.json"
    backend = JsonStateBackend(state_path)
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return state_path


# ---------------------------------------------------------------------------
# Definitions
# ---------------------------------------------------------------------------


def test_starter_pack_present_and_ordered():
    assert skill_names() == [
        "session-close",
        "upgrade-distribution",
        "release",
        "quality-gate",
        "review",
        "repo-health",
        "deep-research",
        "question",
        "analysis",
    ]


def test_every_skill_is_well_formed():
    required = {"name", "description", "capabilities", "body", "grounds"}
    for skill in SKILLS:
        assert required <= set(skill), skill.get("name")
        assert skill["description"], skill["name"]
        assert skill["body"], skill["name"]
        assert isinstance(skill["grounds"], list), skill["name"]
        for ground in skill["grounds"]:
            assert isinstance(ground, str) and ground.strip(), skill["name"]


def test_get_skill_known_and_unknown():
    assert get_skill("quality-gate")["name"] == "quality-gate"
    assert get_skill("nope") is None


def test_skill_capabilities_include_implicit_read():
    assert skill_capabilities("session-close") == [READ, EDIT, RUN]
    assert skill_capabilities("question") == [READ]  # read-only skill
    assert skill_capabilities("unknown") == []


def test_skill_bodies_only_reference_known_bank_slots():
    bank = {q["slot"] for q in QUESTIONS}
    for skill in SKILLS:
        unknown = find_placeholders(skill["body"]) - bank
        assert not unknown, f"{skill['name']} references non-bank slots: {unknown}"


# ---------------------------------------------------------------------------
# Precedence — a skill's declared capability overrides the ambient stance
# ---------------------------------------------------------------------------


def test_skill_permits_declared_only():
    assert skill_permits("session-close", EDIT)
    assert not skill_permits("quality-gate", EDIT)  # quality-gate declares run, not edit


def test_skill_capability_overrides_stance():
    # The headline §3c rule: review stance forbids edits, but an invoked
    # session-close (which declares it edits) may write even so.
    assert action_permitted("review", EDIT) is False
    assert action_permitted("review", EDIT, "session-close") is True
    # A skill grants only what it declared — quality-gate (run-only) cannot edit.
    assert action_permitted("review", EDIT, "quality-gate") is False
    # With no skill, the stance's own tool-scope rules.
    assert action_permitted("debug", EDIT) is True


# ---------------------------------------------------------------------------
# Emission — native SKILL.md (metadata-first frontmatter + body)
# ---------------------------------------------------------------------------


def test_frontmatter_is_native_and_quoted():
    fm = skill_frontmatter(get_skill("review"))
    assert fm.startswith("---\nname: review\n")
    assert 'description: "' in fm and fm.rstrip().endswith("---")


def test_skill_relpath_shape():
    assert skill_relpath(get_skill("analysis")) == "skills/analysis/SKILL.md"


def test_skill_document_wraps_body():
    doc = skill_document(get_skill("question"), "BODY TEXT")
    assert doc.startswith("---\nname: question")
    assert "# question\n\nBODY TEXT\n" in doc


def test_session_close_carries_owner_ask_hygiene():
    # ORDER 008: the close procedure re-grades every ⚑ needs-owner ask
    # against the OWNER-ACTION fields (attempted-or-exact-wall) so unclear
    # or stale asks never survive a session close silently.
    body = get_skill("session-close")["body"]
    assert "OWNER-ACTION" in body
    assert "VERIFIED-NEEDED" in body
    assert "Withdraw stale asks" in body


def test_session_close_carries_capability_nudge():
    # ORDER 006: the close procedure asks the capability-delta question and
    # points at the planted manifest, so discoveries get appended same
    # session instead of being re-paid by the next one.
    body = get_skill("session-close")["body"]
    assert "Capability delta" in body
    assert "docs/CAPABILITIES.md" in body


# ---------------------------------------------------------------------------
# Grounds — the per-skill exact-command grounding (grounded-skills slice 2)
# ---------------------------------------------------------------------------

PLAYBOOK_SKILLS = ("session-close", "upgrade-distribution", "release")


def test_playbook_skills_ground_commands():
    # The three playbook skills MUST carry non-empty grounds — a playbook
    # with no exact commands is the checklist-prose gap slice 2 closes.
    for name in PLAYBOOK_SKILLS:
        assert get_skill(name)["grounds"], name


def test_grounds_entries_appear_verbatim_in_body():
    # Grounds are structured data, but they can never DRIFT from the body:
    # every entry must appear verbatim as a backticked span, so editing a
    # body command without updating grounds (or vice versa) fails here.
    for skill in SKILLS:
        for ground in skill["grounds"]:
            assert f"`{ground}`" in skill["body"], (
                f"{skill['name']}: ground {ground!r} not a backticked "
                "span in the body"
            )


def test_grounds_reference_only_known_bank_slots():
    bank = {q["slot"] for q in QUESTIONS}
    for skill in SKILLS:
        for ground in skill["grounds"]:
            unknown = find_placeholders(ground) - bank
            assert not unknown, f"{skill['name']}: {unknown}"


def test_session_close_is_the_landing_path_playbook():
    # The slice-2 upgrade: claim-first, born-red-first-commit, READY open,
    # flip-complete-last, designed-red reading, never-self-merge.
    body = get_skill("session-close")["body"]
    assert "Claim first" in body
    assert "FIRST commit" in body
    assert "READY (not\n   draft)" in body or "READY (not draft)" in body
    assert "NEVER arm auto-merge" in body
    assert "designed hold" in body
    assert "LAST step" in body
    assert "delete your own claim file" in body


def test_upgrade_distribution_is_the_wave_runbook():
    body = get_skill("upgrade-distribution")["body"]
    assert "git fetch origin main && git reset --hard origin/main" in body
    assert "sha256sum bootstrap.py.new" in body
    assert "python3 bootstrap.py.new upgrade" in body
    assert "three-way" in body
    assert "carve-out" in body.lower() or "Carve-out" in body
    assert "one outcome line per target repo" in body
    assert "git commit --allow-empty" in body  # the label-race cure (W-8)
    assert "~25-min" in body  # the stale-MCP-read gotcha


def test_release_is_the_cut_runbook():
    body = get_skill("release")["body"]
    assert "src/engine/lib/config.py" in body and "pyproject.toml" in body
    assert "SAME commit" in body
    assert "gh workflow run release.yml -f version=X.Y.Z" in body
    assert "git diff --exit-code dist/bootstrap.py" in body
    assert "gh release view vX.Y.Z" in body
    assert "python3 dist/bootstrap.py currency" in body
    assert "never deleted" in body


def test_playbook_bodies_have_no_multiline_command_spans():
    # The grounds-matching invariant relies on inline spans: a command
    # wrapped across lines silently escapes both the drift test above and
    # the check_skill_grounds scan.
    for name in PLAYBOOK_SKILLS:
        for ground in get_skill(name)["grounds"]:
            assert "\n" not in ground, name


# ---------------------------------------------------------------------------
# Skill index (grounded-skills plan §2 slice 1 — the docs/SKILLS.md table)
# ---------------------------------------------------------------------------


def test_skills_index_table_lists_every_skill():
    # One row per SKILLS entry, rendered from the same list that emits the
    # skills (the "render from ONE source" rule) — name backticked,
    # description verbatim as the when-to-reach-for-it line.
    table = skills_index_table()
    rows = table.split("\n")
    assert rows[0] == (
        "| Skill | When to reach for it | Capabilities | Grounds (exact commands) |"
    )
    assert rows[1] == "|---|---|---|---|"
    assert len(rows) == len(SKILLS) + 2
    for skill in SKILLS:
        assert f"| `{skill['name']}` |" in table
        assert skill["description"] in table


def test_skills_index_table_capabilities_match_declarations():
    # The capabilities column is skill_capabilities() truth: the implicit
    # read plus every declared capability, never hand-written prose.
    table = skills_index_table()
    for skill in SKILLS:
        row = next(
            line
            for line in table.split("\n")
            if line.startswith(f"| `{skill['name']}` |")
        )
        assert f"`{READ}`" in row
        for cap in skill["capabilities"]:
            assert f"`{cap}`" in row


def test_skills_index_table_grounds_column():
    # The grounds column is SKILLS truth: every ground appears (slot refs
    # display as <slot_name>, never raw ${...} — the re-banner trap), multi
    # grounds join with <br>, and a grounds-less skill shows an em dash.
    table = skills_index_table()
    assert "${" not in table  # raw slots would re-banner the planted index
    release_row = next(
        line for line in table.split("\n") if line.startswith("| `release` |")
    )
    assert "`python3 src/build_bootstrap.py`" in release_row
    assert "<br>" in release_row
    close_row = next(
        line for line in table.split("\n") if line.startswith("| `session-close` |")
    )
    assert "`<verify_command>`" in close_row  # unfilled slot display form
    question_row = next(
        line for line in table.split("\n") if line.startswith("| `question` |")
    )
    assert "| — |" in question_row


def test_skills_index_table_grounds_fill_from_context():
    # build_context passes the project's slot values INTO the table, so a
    # filled project's index shows its real verify command.
    table = skills_index_table({"verify_command": "python3 -m pytest -q"})
    assert "`python3 -m pytest -q`" in table
    assert "<verify_command>" not in table
    assert "${" not in table


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def test_cli_skills_list(tmp_path, capsys):
    rc = cli.cmd_skills(tmp_path, build=False)
    out = capsys.readouterr().out
    assert rc == 0
    for name in skill_names():
        assert name in out
    assert "capabilities" in out


def test_cli_skills_build_writes_native_files(tmp_path):
    _init(tmp_path)
    rc = cli.cmd_skills(tmp_path, build=True)
    assert rc == 0
    emitted = tmp_path / ".substrate" / "skills" / "session-close" / "SKILL.md"
    assert emitted.exists()
    text = emitted.read_text(encoding="utf-8")
    assert text.startswith("---\nname: session-close")
    assert "# session-close" in text


def test_cli_skills_build_via_parser(tmp_path):
    _init(tmp_path)
    rc = cli.main(["skills", "--build", "--target", str(tmp_path)])
    assert rc == 0
    assert (tmp_path / ".substrate" / "skills" / "analysis" / "SKILL.md").exists()
