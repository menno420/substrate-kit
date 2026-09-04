"""Tests for adoption profiles — the K1-K5 capability.

Structure, and why it is this shape:

- one section per K item, each with a POSITIVE test (the hub shape does the
  thing) and a NEGATIVE/mutant test (the same assertion applied to the default
  shape, or to a deliberately broken profile, must FAIL to hold) — so a
  regression that silently reverts one K item cannot pass by accident;
- a compatibility section pinning that the default shape is unchanged, that
  re-running adopt is idempotent and never clobbers, and that `upgrade` cannot
  undo a profile's sparseness;
- a cold-adoption section that drives the GENERATED `dist/bootstrap.py` through
  the same public interface a future hub seed will use, in a genuinely empty
  git repository, via subprocess. The source package passing proves the engine;
  only this proves the artifact anyone actually downloads.
"""

import json
import subprocess
import sys
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

import build_bootstrap
from engine.adopt import ADOPT_PLAN, adopt, adoption_plan
from engine.checks.check_engagement import scan_relpaths
from engine.checks.check_skill_grounds import _known_paths
from engine.checks.check_session_log import check_added_card
from engine.checks.check_status_current import check_status_current
from engine.lib.config import (
    Config,
    guard_fires_policy,
    load_config,
    new_config,
    owner_context_declaration,
    save_config,
)
from engine.lib.profiles import (
    DEFAULT_PROFILE,
    HUB_PROFILE,
    PROFILE_NAMES,
    AdoptionProfile,
    UnknownProfileError,
    profile_for_config,
    resolve_profile,
)
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.telemetry import (
    GUARD_FIRES_FILENAME,
    guard_fires_path,
    record_guard_fires,
)
from engine.render import agreement_boot_tail, boot_read_path, build_context, render

_KIT = Path(__file__).resolve().parents[1]


def _backend(root: Path, config: Config):
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return backend


def _adopt_into(tmp_path: Path, profile: str | None = None, **kwargs):
    """Adopt into a fresh subdir under ``tmp_path``; return (root, config, report)."""
    root = tmp_path / (profile or "default")
    config = new_config(profile)
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit", **kwargs)
    return root, config, lines


# --------------------------------------------------------------------------
# the profile records themselves
# --------------------------------------------------------------------------


def test_default_profile_omits_nothing_and_overrides_nothing():
    # The `default` profile IS the historical behavior. If this test ever needs
    # updating, every existing adopter's tree changed — which is what makes the
    # default a named record rather than an implicit else-branch.
    assert DEFAULT_PROFILE.omit_plan_dests == frozenset()
    assert DEFAULT_PROFILE.config_defaults == {}
    assert DEFAULT_PROFILE.plant_seat_digest is True


def test_unknown_profile_is_refused_loudly_not_defaulted():
    with pytest.raises(UnknownProfileError) as exc:
        resolve_profile("hubb")
    # The message must name what IS available — a refusal that does not tell you
    # the valid names is a refusal you fix by guessing.
    assert "hubb" in str(exc.value)
    for name in PROFILE_NAMES:
        assert name in str(exc.value)


def test_readers_degrade_to_default_where_writers_refuse():
    # Split posture: `new_config` (a writer, where a typo is still correctable)
    # raises; `profile_for_config` (a reader walking someone else's tree) must
    # never crash a checker on a config it did not write.
    with pytest.raises(UnknownProfileError):
        new_config("nonsense")
    stranger = Config(adoption_profile="nonsense")
    assert profile_for_config(stranger) is DEFAULT_PROFILE


def test_every_omitted_dest_is_a_real_plan_destination():
    # A typo'd omission would silently do nothing — the profile would look like
    # it omits a doc while adopt plants it. Pin the names against the plan.
    plan_dests = {dest for _tmpl, dest in ADOPT_PLAN}
    for profile in (DEFAULT_PROFILE, HUB_PROFILE):
        unknown = profile.omit_plan_dests - plan_dests
        assert not unknown, f"{profile.name} omits non-plan dests: {sorted(unknown)}"


def test_profile_config_defaults_name_real_config_fields():
    # Guards the other half of the same class: a default for a misspelled config
    # key. `new_config` raises rather than setting an attribute that nothing
    # reads and `save_config` would then drop.
    bad = AdoptionProfile(name="bad", summary="", config_defaults={"sessions": "x"})
    from engine.lib import profiles as profiles_mod

    profiles_mod.PROFILES["bad"] = bad
    try:
        with pytest.raises(UnknownProfileError):
            new_config("bad")
    finally:
        del profiles_mod.PROFILES["bad"]


# --------------------------------------------------------------------------
# K1 — no dead control/ room
# --------------------------------------------------------------------------


def test_k1_hub_plants_no_control_tree(tmp_path):
    root, _config, _lines = _adopt_into(tmp_path, "hub")
    assert not (root / "control").exists()


def test_k1_mutant_default_still_plants_the_control_bus(tmp_path):
    # The negative half: if the hub assertion above ever passes because adopt
    # stopped planting control/ FOR EVERYONE, this fails.
    root, _config, _lines = _adopt_into(tmp_path)
    for rel in (
        "control/README.md",
        "control/inbox.md",
        "control/status.md",
        "control/claims/README.md",
    ):
        assert (root / rel).is_file(), rel


def test_k1_status_gate_is_quiet_on_a_hub_and_red_on_a_fresh_default(tmp_path):
    # Omitting the bus must turn the bus gate off BY CONSTRUCTION (the checker's
    # own input-gating), never by an allowlist entry. And the same gate must
    # still hold a fresh default adopt red on its seed heartbeat — otherwise
    # "quiet" would mean the gate broke, not that it correctly did not engage.
    hub_root, hub_config, _ = _adopt_into(tmp_path, "hub")
    gate, advisories = check_status_current(
        hub_root,
        status_files=hub_config.heartbeat_files,
    )
    assert gate == []
    assert advisories == []
    assert not (hub_root / hub_config.state_dir / "check-exceptions.yml").exists()

    def_root, def_config, _ = _adopt_into(tmp_path)
    def_gate, _def_adv = check_status_current(
        def_root,
        status_files=def_config.heartbeat_files,
    )
    assert def_gate, "a fresh default adopt must stay red on its seed heartbeat"


def test_k1_lane_is_refused_on_a_bus_less_profile(tmp_path):
    root = tmp_path / "hub-lane"
    config = new_config("hub")
    with pytest.raises(ValueError) as exc:
        adopt(
            root,
            config,
            _backend(root, config),
            kit_root=tmp_path / "kit",
            lane="mining",
        )
    assert "--lane" in str(exc.value)
    # And nothing was planted before the refusal.
    assert not (root / "control").exists()


def test_k1_lane_still_works_on_the_default_profile(tmp_path):
    root = tmp_path / "def-lane"
    config = Config()
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit", lane="mining")
    assert (root / "control" / "status-mining.md").is_file()


# --------------------------------------------------------------------------
# K2 — no generic docs pile
# --------------------------------------------------------------------------


def test_k2_hub_plants_nothing_generic_under_docs(tmp_path):
    root, config, _lines = _adopt_into(tmp_path, "hub")
    docs = root / config.docs_root
    assert not docs.exists(), sorted(p.name for p in docs.rglob("*")) if docs.exists() else ""


def test_k2_mutant_default_still_plants_the_full_doc_set(tmp_path):
    root, config, _lines = _adopt_into(tmp_path)
    planted = {p.relative_to(root).as_posix() for p in (root / config.docs_root).rglob("*.md")}
    # The five the estate proposal named by name as the pile's signature, plus
    # the derived render that reads two of them.
    for rel in (
        "docs/seat-digest.md",
        "docs/ROUTINES.md",
        "docs/helper-policy.md",
        "docs/runtime_contracts.md",
        "docs/reading-path.md",
    ):
        assert rel in planted, rel


def test_k2_hub_plants_no_seat_digest_render(tmp_path):
    hub_root, _c, _l = _adopt_into(tmp_path, "hub")
    assert not (hub_root / "docs" / "seat-digest.md").exists()


def test_k2_hub_keeps_the_structural_root_plants(tmp_path):
    # "Intentionally sparse" is not "empty": the working agreement, the session
    # journal, the env-setup hook and the pack index are structural, not a docs
    # pile, and a hub with no working agreement has no boot file at all.
    root, _config, _lines = _adopt_into(tmp_path, "hub")
    for rel in (
        "CONSTITUTION.md",
        ".session-journal.md",
        "scripts/env-setup.sh",
        "project.index.json",
    ):
        assert (root / rel).is_file(), rel


def test_k2_boot_read_path_names_no_unplanted_doc(tmp_path):
    # The dead-pointer class, at the one place the kit enforces it. A fixed
    # three-doc boot list planted into a tree that plants none of them is the
    # 2026-08-06 defect (0 of 11 adopters resolved) reproduced on purpose.
    hub = boot_read_path(new_config("hub"))
    for dead in ("docs/current-state.md", "docs/CAPABILITIES.md"):
        assert dead not in hub
    assert dead not in agreement_boot_tail(new_config("hub"))
    # Mutant: the default shape MUST still name them — it plants them, and the
    # reachability walk depends on the links.
    assert "docs/current-state.md" in boot_read_path(Config())
    assert "docs/CAPABILITIES.md" in boot_read_path(None)
    assert "docs/ROUTINES.md" in agreement_boot_tail(Config())


def test_k2_planted_agreement_carries_no_dead_doc_pointer(tmp_path):
    root, _config, _lines = _adopt_into(tmp_path, "hub")
    agreement = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    boot_section = agreement.split("## Boot read path", 1)[1].split("## ", 1)[0]
    for dead in ("docs/current-state.md", "docs/CAPABILITIES.md"):
        assert dead not in boot_section


def test_k2_profile_filtered_plan_is_what_every_consumer_reads(tmp_path):
    # The leakage class the fan-out found: `check_skill_grounds` folded EVERY
    # plan destination into its grounded-by-construction set unconditionally, so
    # a skill body naming a doc the hub never plants would have passed as
    # grounded — a false green in the checker whose whole job is dead pointers.
    hub = new_config("hub")
    assert "docs/ROUTINES.md" in _known_paths(Config())
    assert "docs/ROUTINES.md" not in _known_paths(hub)
    # ...and the engagement scan, and the plan accessor itself.
    assert "docs/ROUTINES.md" in scan_relpaths(Config())
    assert "docs/ROUTINES.md" not in scan_relpaths(hub)
    assert len(adoption_plan(hub)) < len(adoption_plan(Config())) == len(ADOPT_PLAN)


# --------------------------------------------------------------------------
# K3 — visible session directory
# --------------------------------------------------------------------------


def test_k3_hub_is_born_on_a_visible_sessions_dir(tmp_path):
    root, config, _lines = _adopt_into(tmp_path, "hub")
    assert config.sessions_dir == "sessions"
    assert (root / "sessions" / "README.md").is_file()
    assert not (root / ".sessions").exists()


def test_k3_mutant_default_keeps_the_hidden_dir(tmp_path):
    root, config, _lines = _adopt_into(tmp_path)
    assert config.sessions_dir == ".sessions"
    assert (root / ".sessions" / "README.md").is_file()
    assert not (root / "sessions").exists()


def test_k3_the_configured_dir_is_written_into_the_config_file(tmp_path):
    # Not merely implied by the profile name: an adopter opening
    # substrate.config.json must see its own truth without looking a name up.
    root = tmp_path / "repo"
    root.mkdir()
    save_config(root, new_config("hub"))
    raw = json.loads((root / "substrate.config.json").read_text(encoding="utf-8"))
    assert raw["sessions_dir"] == "sessions"
    assert raw["adoption_profile"] == "hub"


def test_k3_card_advice_names_the_configured_dir_not_a_hardcoded_one(tmp_path):
    # The advice half: a card rejected on a `sessions/` repo used to be told to
    # "see .sessions/README.md" — a path that does not exist there.
    card = tmp_path / "2026-01-01-x.md"
    card.write_text(
        "# x\n\n> **Status:** `complete`\n\n\N{ELECTRIC LIGHT BULB} idea\n"
        "previous-session review: n/a\n"
        "- **\N{BAR CHART} Model:** opus-5 \N{MIDDLE DOT} high "
        "\N{MIDDLE DOT} not-a-real-class\n",
        encoding="utf-8",
    )
    markers = Config().session_markers
    visible = check_added_card(card, markers, "sessions")
    hidden = check_added_card(card, markers, ".sessions")
    assert visible and hidden
    assert any("sessions/README.md" in m and ".sessions/README.md" not in m for m in visible)
    assert any(".sessions/README.md" in m for m in hidden)


def test_k3_the_generated_gate_gates_the_configured_dir(tmp_path):
    # The machinery half: the CI gate adopt stages must look for cards where
    # this install actually keeps them.
    hub_root, _c, _l = _adopt_into(tmp_path, "hub")
    gate = (hub_root / ".substrate" / "ci" / "substrate-gate.yml").read_text(encoding="utf-8")
    assert "sessions/*.md" in gate
    assert ".sessions/*.md" not in gate


# --------------------------------------------------------------------------
# K4 — owner-context pointer without duplicated owner truth
# --------------------------------------------------------------------------


def test_k4_undeclared_owner_context_renders_byte_identically(tmp_path):
    # The compatibility floor for K4: an install that declares nothing must get
    # exactly the pre-key document. Compared as bytes, against a render whose
    # context simply lacks the key.
    templates = build_bootstrap  # keep the import used; see load below
    from engine.render import load_templates

    tmpl = load_templates()["owner-profile.md.tmpl"]
    context = dict(build_context({}, Config()))
    with_key = render(tmpl, context)
    without_key = render(tmpl.replace("${owner_context_pointer}", ""), context)
    assert with_key == without_key
    assert templates is not None


def test_k4_declared_owner_context_renders_one_pointer_and_keeps_local_slots(tmp_path):
    config = new_config("hub")
    config.owner_context = {"canonical": "https://example.invalid/hub", "label": "the hub"}
    from engine.render import load_templates

    rendered = render(load_templates()["owner-profile.md.tmpl"], dict(build_context({}, config)))
    assert "Canonical owner context" in rendered
    assert "https://example.invalid/hub" in rendered
    assert "the hub" in rendered
    # The repo's own two slots survive — the pointer replaces DUPLICATION of the
    # broader profile, never the local answers.
    assert "## How the owner works" in rendered
    assert "## Review ritual" in rendered
    # Exactly one pointer, not one per section.
    assert rendered.count("Canonical owner context") == 1


def test_k4_a_label_without_a_canonical_is_not_a_pointer():
    # A dangling "the profile lives at " with nowhere to point is worse than no
    # pointer at all, so it degrades to nothing.
    config = Config()
    config.owner_context = {"label": "the hub"}
    assert owner_context_declaration(config) == ("", "")
    assert build_context({}, config)["owner_context_pointer"] == ""


# Repository/account references that must never appear in the PORTABLE surfaces
# below. The engine at large legitimately cites repo names in provenance
# comments ("field-reproduced on fleet-manager #35") and in the adopter scan
# roster; this rule is about the shape records and the owner-context mechanism,
# the two places a name would stop being a citation and become a hardcoded
# destination.
#
# `estate` is matched only in its IDENTIFIER forms — quoted, backticked, or as
# a path segment. The bare word is ordinary English for what a hub holds
# ("estate-level records") and banning it outright would be a rule about
# vocabulary rather than about portability. What must never appear is the kit
# treating a particular future repository as a name it knows.
_NON_PORTABLE_NAMES = (
    "fleet-manager",
    "menno420",
    '"estate"',
    "'estate'",
    "`estate`",
    "estate/",
)

# The files K4 and the profile abstraction are implemented in — the ones whose
# whole claim is that they are portable.
_PORTABLE_SURFACES = (
    "src/engine/lib/profiles.py",
    "src/engine/templates/owner-profile.md.tmpl",
)


def _name_hits(text: str) -> list[str]:
    return [n for n in _NON_PORTABLE_NAMES if n in text]


def test_the_name_scan_catches_a_planted_offender():
    # TRAP-003's positive control: an empty result proves the query RAN, not
    # that the world is empty. Prove the scan can fail — on every banned form —
    # before trusting the fact that it passed.
    assert _name_hits("owner context lives in the fleet-manager repo") == ["fleet-manager"]
    assert _name_hits("clone github.com/menno420/x") == ["menno420"]
    assert _name_hits('PROFILES["estate"] = ...') == ['"estate"']
    assert _name_hits("profile = 'estate'") == ["'estate'"]
    assert _name_hits("the `estate` profile") == ["`estate`"]
    assert _name_hits("plant into estate/state/") == ["estate/"]
    # ...and that the ordinary English word is NOT an offender, or the rule
    # would be about vocabulary rather than portability.
    assert _name_hits("holds estate-level records for the account") == []
    assert _name_hits("no names here at all") == []


def test_k4_the_portable_surfaces_hardcode_no_destination():
    # The portability rule: the kit ships the sentence, never its destination,
    # and a profile is a SHAPE — named for a role, never for a repository.
    offenders = []
    for rel in _PORTABLE_SURFACES:
        text = (_KIT / rel).read_text(encoding="utf-8")
        offenders += [f"{rel}: {name}" for name in _name_hits(text)]
    assert not offenders, offenders


def test_k4_the_rendered_pointer_quotes_only_what_the_host_declared():
    # The behavioral half of the same rule, which no file scan can give: the
    # rendered sentence must contain the host's string and no destination of
    # the kit's own invention.
    from engine.render import load_templates

    config = Config()
    config.owner_context = {"canonical": "https://example.invalid/x", "label": "L"}
    rendered = render(load_templates()["owner-profile.md.tmpl"], dict(build_context({}, config)))
    pointer = [line for line in rendered.splitlines() if "Canonical owner context" in line]
    assert len(pointer) == 1
    assert "https://example.invalid/x" in "".join(
        rendered.split("Canonical owner context", 1)[1].splitlines()[:3],
    )
    assert not _name_hits(rendered)


def test_k4_owner_context_survives_a_config_round_trip(tmp_path):
    # `Config.from_dict` drops unknown keys, so a bare JSON key would be
    # stripped on the next load->save cycle. Pin that it is a declared field.
    root = tmp_path / "repo"
    root.mkdir()
    config = new_config("hub")
    config.owner_context = {"canonical": "docs/owner/", "label": "owner workbench"}
    save_config(root, config)
    save_config(root, load_config(root))
    reloaded = load_config(root)
    assert reloaded.owner_context == {"canonical": "docs/owner/", "label": "owner workbench"}
    assert reloaded.adoption_profile == "hub"


# --------------------------------------------------------------------------
# K5 — telemetry must not create an unbounded tracked ledger
# --------------------------------------------------------------------------


def test_k5_default_policy_is_the_historical_kf11_shape():
    policy = guard_fires_policy(Config())
    assert policy == {"enabled": True, "path": "", "tracked": True, "max_records": 0}


def test_k5_hub_policy_is_untracked_and_capped():
    policy = guard_fires_policy(new_config("hub"))
    assert policy["tracked"] is False
    assert policy["max_records"] > 0
    # Untracked must not mean unrecorded — the estate requirement is USEFUL
    # telemetry without an unbounded tracked ledger, not "delete telemetry".
    assert policy["enabled"] is True


def test_k5_a_partial_declaration_keeps_the_other_axes(tmp_path):
    config = Config()
    config.telemetry = {"guard_fires": {"tracked": False}}
    policy = guard_fires_policy(config)
    assert policy["tracked"] is False
    assert policy["enabled"] is True
    assert policy["max_records"] == 0


def test_k5_hand_edited_garbage_fails_open_to_a_usable_policy():
    config = Config()
    config.telemetry = {"guard_fires": {"max_records": "lots", "tracked": "yes"}}
    policy = guard_fires_policy(config)
    assert policy["max_records"] == 0
    assert policy["tracked"] is True


def test_k5_hub_adopt_plants_the_ignore_entry(tmp_path):
    root, config, lines = _adopt_into(tmp_path, "hub")
    ignored = (root / ".gitignore").read_text(encoding="utf-8")
    assert f"/{config.state_dir}/{GUARD_FIRES_FILENAME}" in ignored
    assert any(".gitignore" in line for line in lines)


def test_k5_mutant_default_adopt_plants_no_ignore_entry(tmp_path):
    # The tracked default is a deliberate design (KF-11: committed, never
    # gitignored). If this ever fails, the change silently untracked every
    # existing adopter's ledger.
    root, _config, _lines = _adopt_into(tmp_path)
    if (root / ".gitignore").exists():
        assert GUARD_FIRES_FILENAME not in (root / ".gitignore").read_text(encoding="utf-8")


def test_k5_the_ignore_merge_never_clobbers_host_content(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text("# host policy\n*.log\n", encoding="utf-8")
    config = new_config("hub")
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    text = (root / ".gitignore").read_text(encoding="utf-8")
    assert "# host policy" in text
    assert "*.log" in text
    assert f"/{config.state_dir}/{GUARD_FIRES_FILENAME}" in text


def test_k5_a_capped_ledger_cannot_grow_without_bound(tmp_path):
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    policy = {"enabled": True, "path": "", "tracked": False, "max_records": 10}
    for i in range(600):
        record_guard_fires(
            root,
            ".substrate",
            cmd="check",
            surface="check",
            posture="advisory",
            findings=[_finding(f"p{i}", "kind", f"message {i}")],
            verdict="false_positive",
            reason="fixture",
            policy=policy,
        )
    lines = guard_fires_path(root, ".substrate", policy).read_text(encoding="utf-8").splitlines()
    # Bounded by cap + the rewrite slack, and never at the unbounded 600.
    assert 10 <= len(lines) < 600
    # The NEWEST records survive a trim — a cap that dropped the newest would be
    # a data-loss bug wearing a size-limit label.
    assert json.loads(lines[-1])["finding"]["path"] == "p599"


def test_k5_mutant_uncapped_ledger_still_grows(tmp_path):
    # The negative control for the test above: with the default policy the feed
    # is strictly append-only, so a passing cap test cannot be an artifact of
    # writes silently failing.
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    policy = guard_fires_policy(Config())
    for i in range(300):
        record_guard_fires(
            root,
            ".substrate",
            cmd="check",
            surface="check",
            posture="advisory",
            findings=[_finding(f"p{i}", "kind", f"message {i}")],
            verdict="false_positive",
            reason="fixture",
            policy=policy,
        )
    lines = guard_fires_path(root, ".substrate", policy).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 300


def test_k5_disabled_telemetry_writes_nothing(tmp_path):
    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    policy = {"enabled": False, "path": "", "tracked": False, "max_records": 0}
    written = record_guard_fires(
        root,
        ".substrate",
        cmd="check",
        surface="check",
        posture="advisory",
        findings=[_finding("p", "kind", "m")],
        verdict="v",
        reason="r",
        policy=policy,
    )
    assert written == 0
    assert not guard_fires_path(root, ".substrate", policy).exists()


def test_k5_the_path_axis_cannot_escape_the_repo(tmp_path):
    root = tmp_path / "repo"
    for escape in ("../outside.jsonl", "/etc/passwd", "a/../../b.jsonl"):
        policy = {"enabled": True, "path": escape, "tracked": False, "max_records": 0}
        resolved = guard_fires_path(root, ".substrate", policy)
        assert resolved == root / ".substrate" / GUARD_FIRES_FILENAME, escape
    inside = {"enabled": True, "path": "telemetry/fires.jsonl", "tracked": False, "max_records": 0}
    assert guard_fires_path(root, ".substrate", inside) == root / "telemetry" / "fires.jsonl"


def _finding(path, kind, message):
    from engine.checks.check_docs import Finding

    return Finding(path, kind, message)


# --------------------------------------------------------------------------
# compatibility — the default shape, idempotence, and upgrade
# --------------------------------------------------------------------------


def test_default_adopt_plants_exactly_the_full_plan(tmp_path):
    root, config, _lines = _adopt_into(tmp_path)
    from engine.adopt import _adopt_dest

    for _tmpl, plan_rel in ADOPT_PLAN:
        assert (root / _adopt_dest(plan_rel, config)).is_file(), plan_rel


def test_config_without_the_new_keys_loads_as_the_default_shape(tmp_path):
    # The upgrade path for every install that predates this change: its
    # substrate.config.json has no adoption_profile / telemetry / owner_context.
    root = tmp_path / "legacy"
    root.mkdir()
    (root / "substrate.config.json").write_text(
        json.dumps({"project_id": "abc123", "sessions_dir": ".sessions"}),
        encoding="utf-8",
    )
    config = load_config(root)
    assert config.adoption_profile == "default"
    assert profile_for_config(config) is DEFAULT_PROFILE
    assert guard_fires_policy(config)["tracked"] is True
    assert adoption_plan(config) == list(ADOPT_PLAN)


def test_re_adopting_a_hub_is_idempotent_and_keeps_user_material(tmp_path):
    root, config, _first = _adopt_into(tmp_path, "hub")
    edited = root / "CONSTITUTION.md"
    edited.write_text("# hand-written by the host\n", encoding="utf-8")
    (root / "sessions" / "2026-01-01-card.md").write_text("# card\n", encoding="utf-8")
    before = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and ".substrate" not in p.parts
    }
    second = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    after = {
        p.relative_to(root).as_posix()
        for p in root.rglob("*")
        if p.is_file() and ".substrate" not in p.parts
    }
    assert before == after
    assert edited.read_text(encoding="utf-8") == "# hand-written by the host\n"
    assert (root / "sessions" / "2026-01-01-card.md").is_file()
    assert not (root / "control").exists()
    assert any(line.startswith("kept: CONSTITUTION.md") for line in second)


def test_upgrade_does_not_replant_what_the_profile_omits(tmp_path):
    # The regression that would quietly undo K1/K2 three weeks after the seed:
    # `upgrade` re-runs `adopt` with the LOADED config, so the profile has to
    # travel in the config file, not in an adopt-time flag.
    from engine.upgrade import run_upgrade

    from engine.lib.config import KIT_VERSION

    root, config, _lines = _adopt_into(tmp_path, "hub")
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    running = tmp_path / "bootstrap.py.new"
    running.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED, DO NOT EDIT."""\n',
        encoding="utf-8",
    )
    run_upgrade(root, config, backend, kit_root=tmp_path / "kit", running=running)
    assert not (root / "control").exists()
    assert not (root / "docs").exists()
    assert (root / "sessions" / "README.md").is_file()
    assert load_config(root).adoption_profile == "hub"


def test_render_live_does_not_replant_what_the_profile_omits(tmp_path):
    from engine.cli import cmd_render

    root, config, _lines = _adopt_into(tmp_path, "hub")
    save_config(root, config)
    assert cmd_render(root, live=True) == 0
    assert not (root / "control").exists()
    assert not (root / "docs").exists()


# --------------------------------------------------------------------------
# cold adoption through the GENERATED artifact
# --------------------------------------------------------------------------


def _cold_repo(tmp_path: Path) -> Path:
    """Return a genuinely empty git repo carrying only the built dist."""
    root = tmp_path / "cold"
    root.mkdir()
    (root / "bootstrap.py").write_text(build_bootstrap.build(), encoding="utf-8")
    subprocess.run(["git", "init", "-q", "."], cwd=root, check=True)
    return root


def _run(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "bootstrap.py", *args],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )


def test_cold_hub_adoption_through_the_generated_dist(tmp_path):
    """The whole capability, end to end, through the artifact a seed downloads.

    The source package passing proves the engine; only this proves the single
    file. They have diverged before: an engine module missing from MODULE_ORDER
    builds a dist whose checker crashes with NameError at runtime while every
    source test stays green (tests/test_bootstrap.py's own module-order note).
    """
    root = _cold_repo(tmp_path)
    adopted = _run(root, "adopt", "--profile", "hub")
    assert adopted.returncode == 0, adopted.stderr or adopted.stdout
    assert "adoption profile 'hub'" in adopted.stdout

    # K1 + K2 — the tree is born without the dead rooms.
    assert not (root / "control").exists()
    assert not (root / "docs").exists()
    # K3 — visible, and only visible.
    assert (root / "sessions" / "README.md").is_file()
    assert not (root / ".sessions").exists()
    # K5 — the ignore entry exists from birth.
    assert "/.substrate/guard-fires.jsonl" in (root / ".gitignore").read_text(encoding="utf-8")
    # ...and the config states its own shape.
    raw = json.loads((root / "substrate.config.json").read_text(encoding="utf-8"))
    assert raw["adoption_profile"] == "hub"
    assert raw["sessions_dir"] == "sessions"
    assert raw["telemetry"]["guard_fires"]["tracked"] is False

    # Born red, and for the RIGHT three reasons — no control/ or docs/ finding
    # among them, which is what "quiet by construction" has to mean in practice.
    assert "NOT ENGAGED" in adopted.stdout
    checked = _run(root, "check", "--strict")
    assert checked.returncode == 1, checked.stdout
    assert "boot-path-unresolved" not in checked.stdout
    for absent in ("control/status.md", "docs/current-state.md", "docs/CAPABILITIES.md"):
        assert absent not in checked.stdout, absent
    # K5's advice half: a session on this install is not told to commit a delta
    # that its own .gitignore guarantees does not exist.
    assert "policy INTENDS it untracked" in checked.stdout
    assert "commit the delta with your session" not in checked.stdout
    # It must not assert an unchecked git fact in EITHER direction: it says so
    # out loud, and names the remedy for an install that committed the ledger
    # before the policy changed (adopt never touches git's index).
    assert "claims nothing about your working tree" in checked.stdout
    assert "git rm --cached" in checked.stdout
    # ...and the ledger really is ignored by git, not merely named in a file.
    status = subprocess.run(
        ["git", "status", "--porcelain", "--ignored=no"],
        cwd=root,
        capture_output=True,
        text=True,
        check=True,
    )
    assert "guard-fires.jsonl" not in status.stdout

    # Re-adopting is idempotent and keeps host material.
    (root / "CONSTITUTION.md").write_text("# host-owned\n", encoding="utf-8")
    again = _run(root, "adopt", "--profile", "hub")
    assert again.returncode == 0, again.stderr
    assert (root / "CONSTITUTION.md").read_text(encoding="utf-8") == "# host-owned\n"
    assert not (root / "control").exists()


def test_cold_default_adoption_through_the_generated_dist_is_unchanged(tmp_path):
    # The compatibility control for the test above, in the same venue: the
    # artifact must still produce the historical tree with no flag.
    root = _cold_repo(tmp_path)
    adopted = _run(root, "adopt")
    assert adopted.returncode == 0, adopted.stderr
    assert "adoption profile" not in adopted.stdout
    assert (root / "control" / "status.md").is_file()
    assert (root / "docs" / "current-state.md").is_file()
    assert (root / "docs" / "seat-digest.md").is_file()
    assert (root / ".sessions" / "README.md").is_file()
    if (root / ".gitignore").exists():
        assert "guard-fires" not in (root / ".gitignore").read_text(encoding="utf-8")


def test_cold_dist_refuses_an_unknown_profile(tmp_path):
    root = _cold_repo(tmp_path)
    result = _run(root, "adopt", "--profile", "estate")
    assert result.returncode != 0
    assert not (root / "substrate.config.json").exists()


def test_cold_dist_refuses_to_reshape_an_adopted_tree(tmp_path):
    # Idempotence has a boundary: re-running with a DIFFERENT profile would mean
    # unplanting files the host may have edited. That is a migration, not an
    # adopt, and the kit refuses rather than doing half of one.
    root = _cold_repo(tmp_path)
    assert _run(root, "adopt", "--profile", "hub").returncode == 0
    reshape = _run(root, "adopt")
    assert reshape.returncode == 0, "no --profile keeps the recorded shape"
    assert not (root / "docs").exists()
    reshape2 = _run(root, "adopt", "--profile", "default")
    assert reshape2.returncode == 2
    assert "REFUSED" in reshape2.stdout
    assert not (root / "docs").exists()


# --------------------------------------------------------------------------
# Codex round 1 (PR #590) — one regression test per finding
# --------------------------------------------------------------------------


def test_codex_p1_a_writer_refuses_an_unknown_persisted_profile(tmp_path):
    # The reader/writer split was stated in the design and then violated in the
    # one place it mattered: `adopt` called the READER, so a hand-edited or
    # future-version config naming a shape this kit does not ship would plant
    # the FULL default tree into a repo that asked for a sparse one.
    root = tmp_path / "repo"
    config = Config(adoption_profile="hubb")
    with pytest.raises(UnknownProfileError):
        adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    assert not (root / "control").exists()
    assert not (root / "docs").exists()
    # The READER stays lenient — a checker walking that same tree must not crash.
    assert profile_for_config(config) is DEFAULT_PROFILE
    assert adoption_plan(config) == list(ADOPT_PLAN)


def test_codex_p2_a_non_dict_telemetry_key_does_not_crash_the_command():
    # `telemetry` is host input and the policy is resolved OUTSIDE
    # record_guard_fires' fail-open boundary, so an unguarded .get crashed
    # `check` itself rather than degrading to the documented defaults.
    for garbage in ("yes", 7, [1, 2], True):
        config = Config()
        config.telemetry = garbage
        assert guard_fires_policy(config) == {
            "enabled": True,
            "path": "",
            "tracked": True,
            "max_records": 0,
        }, garbage


def test_codex_p2_the_upgrade_doc_plan_follows_the_profile(tmp_path):
    # _doc_plan iterated the raw plan, so every hub upgrade would report the
    # intentionally-omitted destinations as `missing` with a note promising a
    # replant that correctly never happens — a permanent untrue report line.
    from engine.upgrade import _doc_plan

    hub = new_config("hub")
    hub_dests = {rel for _tmpl, rel in _doc_plan(tmp_path, hub)}
    default_dests = {rel for _tmpl, rel in _doc_plan(tmp_path, Config())}
    assert "docs/current-state.md" in default_dests
    assert "docs/current-state.md" not in hub_dests
    assert "control/status.md" in default_dests
    assert "control/status.md" not in hub_dests


def test_codex_p2_model_line_advice_follows_the_configured_dir():
    from engine.checks.check_model_line import model_line_findings

    card = (
        "# c\n\n> **Status:** `complete`\n\n"
        "- **\N{BAR CHART} Model:** opus-5 \N{MIDDLE DOT} high "
        "\N{MIDDLE DOT} not-a-real-class\n"
    )
    visible = model_line_findings(card, "sessions")
    hidden = model_line_findings(card, ".sessions")
    assert visible and hidden
    assert all("sessions/README.md" in m and ".sessions/README" not in m for _k, m in visible)
    assert all(".sessions/README.md" in m for _k, m in hidden)


def test_codex_p2_ungroomed_ideas_reads_the_configured_dir(tmp_path):
    # It accepted `config` for signature parity and ignored it, so on any
    # install whose cards are not in the historical hidden location the probe
    # found no directory, gated itself off, and reported "no pending ideas"
    # for a repo full of them — a silent false negative.
    from engine.checks.check_ungroomed_ideas import check_ungroomed_ideas

    root = tmp_path / "repo"
    (root / "sessions").mkdir(parents=True)
    (root / "docs" / "planning").mkdir(parents=True)
    (root / "docs" / "planning" / "2026-01-01-groom.md").write_text("# groom\n", encoding="utf-8")
    (root / "sessions" / "2026-02-01-card.md").write_text(
        "# card\n\n\N{ELECTRIC LIGHT BULB} an idea worth grooming\n", encoding="utf-8",
    )
    hub = new_config("hub")
    assert check_ungroomed_ideas(root, hub), "the advisory must SEE cards in sessions/"
    # ...and the historical layout is unchanged.
    assert check_ungroomed_ideas(root, Config()) == []


def test_codex_p1_gitignore_patterns_are_escaped_to_literals(tmp_path):
    # A path is a NAME; a gitignore line is a PATTERN. `path: "*"` planted the
    # line "/*", which makes git ignore every root-level file in the repo —
    # including everything adopt had just planted.
    from engine.adopt import _gitignore_literal

    assert _gitignore_literal(".substrate/guard-fires.jsonl") == "/.substrate/guard-fires.jsonl"
    assert _gitignore_literal("*") == "/\\*"
    assert _gitignore_literal("a b/c?.jsonl") == "/a\\ b/c\\?.jsonl"
    assert _gitignore_literal("#x[1].jsonl") == "/\\#x\\[1\\].jsonl"
    assert _gitignore_literal("trailing ") == "/trailing\\ "

    root = tmp_path / "repo"
    config = new_config("hub")
    config.telemetry = {"guard_fires": {"enabled": True, "path": "*", "tracked": False, "max_records": 0}}
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    ignored = (root / ".gitignore").read_text(encoding="utf-8")
    assert "/\\*" in ignored
    assert "\n/*\n" not in ignored


def test_codex_p2_a_stale_telemetry_ignore_entry_is_reported(tmp_path):
    # Append-only means a policy change leaves the old line: git would keep
    # ignoring a ledger `check` has started telling the session to commit.
    root = tmp_path / "repo"
    config = new_config("hub")
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    assert GUARD_FIRES_FILENAME in (root / ".gitignore").read_text(encoding="utf-8")
    # Flip the policy to tracked and re-adopt: the leftover must be NAMED.
    config.telemetry = {"guard_fires": {"enabled": True, "path": "", "tracked": True, "max_records": 0}}
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    stale = [ln for ln in lines if ln.startswith("telemetry: .gitignore still carries")]
    assert stale, lines
    assert GUARD_FIRES_FILENAME in stale[0]
    # Reporting, never editing — a .gitignore line is host policy.
    assert GUARD_FIRES_FILENAME in (root / ".gitignore").read_text(encoding="utf-8")


def test_codex_p2_a_capped_ledger_serialises_appends_against_trims(tmp_path):
    # The lost-update race: a trim reads, another writer appends, the trim then
    # replaces the file with its stale snapshot. Run real concurrent processes
    # over a capped ledger and assert no acknowledged record vanishes.
    import multiprocessing

    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    policy = {"enabled": True, "path": "", "tracked": False, "max_records": 40}

    def worker(tag):
        import sys as _sys

        _sys.path.insert(0, str(_KIT / "src"))
        from engine.checks.check_docs import Finding as F
        from engine.loop.telemetry import record_guard_fires as rec

        for i in range(120):
            rec(
                root, ".substrate", cmd="check", surface="check", posture="advisory",
                findings=[F(f"{tag}-{i}", "kind", f"m{tag}{i}")],
                verdict="false_positive", reason="fixture", policy=policy,
            )

    procs = [multiprocessing.Process(target=worker, args=(t,)) for t in ("a", "b", "c")]
    for pr in procs:
        pr.start()
    for pr in procs:
        pr.join(120)
    for pr in procs:
        assert pr.exitcode == 0, pr.exitcode

    path = guard_fires_path(root, ".substrate", policy)
    lines = path.read_text(encoding="utf-8").splitlines()
    # Every line is intact JSON — a torn write from an unserialised rewrite
    # would show up here first.
    for line in lines:
        json.loads(line)
    # The cap held under concurrency, and the file is not empty.
    assert 0 < len(lines) <= 40 + 128
    # An uncapped ledger creates NO lock file: the mechanism is confined to
    # installs that opted into a cap, so no existing adopter gains a file.
    from engine.loop.telemetry import guard_fires_lock_path

    assert guard_fires_lock_path(path).exists()
    plain = tmp_path / "plain"
    (plain / ".substrate").mkdir(parents=True)
    default_policy = guard_fires_policy(Config())
    record_guard_fires(
        plain, ".substrate", cmd="c", surface="s", posture="p",
        findings=[_finding("p", "k", "m")], verdict="v", reason="r", policy=default_policy,
    )
    assert not guard_fires_lock_path(guard_fires_path(plain, ".substrate", default_policy)).exists()


def test_codex_p1_surviving_dead_routes_are_reported_not_discovered(tmp_path):
    # The kit does not fork its doctrine prose per shape, but it must not let
    # the residue be found one dead pointer at a time weeks later.
    root, _config, lines = _adopt_into(tmp_path, "hub", include_claude=True)
    routed = [ln for ln in lines if ln.startswith("profile 'hub':")]
    assert routed, lines
    named = " ".join(routed)
    assert "CONSTITUTION.md" in named
    assert ".claude/CLAUDE.md" in named
    for dead in ("docs/SKILLS.md", "docs/CAPABILITIES.md", "control/README.md"):
        assert dead in named, dead
    # A default adopt has no omitted destinations, so it reports nothing.
    _droot, _dconfig, dlines = _adopt_into(tmp_path)
    assert not [ln for ln in dlines if ln.startswith("profile ")]


def test_codex_p1_the_session_journal_names_the_configured_card_dir(tmp_path):
    # It hardcoded `.sessions/`, which was wrong for ANY install that moved
    # sessions_dir — not only the hub.
    hub_root, _c, _l = _adopt_into(tmp_path, "hub")
    journal = (hub_root / ".session-journal.md").read_text(encoding="utf-8")
    assert "`sessions/<date>-<slug>.md`" in journal
    assert ".sessions/" not in journal
    def_root, _dc, _dl = _adopt_into(tmp_path)
    assert "`.sessions/<date>-<slug>.md`" in (def_root / ".session-journal.md").read_text(encoding="utf-8")


def test_codex_p1_the_boot_section_intro_names_no_omitted_doc(tmp_path):
    # The list was parameterised and the INTRO one paragraph above it was not,
    # so it still routed to docs/AGENT_ORIENTATION.md on a shape that omits it.
    root, _config, _lines = _adopt_into(tmp_path, "hub")
    agreement = (root / "CONSTITUTION.md").read_text(encoding="utf-8")
    section = agreement.split("## Boot read path", 1)[1].split("\n## ", 1)[0]
    assert "docs/AGENT_ORIENTATION.md" not in section
    assert "docs/current-state.md" not in section
    # Mutant: the default shape still carries the router sentence.
    def_root, _dc, _dl = _adopt_into(tmp_path)
    def_section = (def_root / "CONSTITUTION.md").read_text(encoding="utf-8")
    def_section = def_section.split("## Boot read path", 1)[1].split("\n## ", 1)[0]
    assert "docs/AGENT_ORIENTATION.md" in def_section


def test_codex_p1_the_hub_skill_pack_gap_is_pinned_not_hidden(tmp_path):
    """The kit's SHARED skill bodies name docs a sparse shape does not plant.

    Codex round 1 on PR #590 raised this as blocking: a fresh hub adoption emits
    skill-ground advisories naming documents its own profile omits, so the shape
    ships procedures that cannot run against the tree it produces.

    The finding is correct and the advisories are NOT the defect — they are this
    change working. Before the profile filter reached
    ``check_skill_grounds._known_paths``, every one of these paths was
    "grounded by construction" and passed silently: a false green in the checker
    whose entire job is dead pointers. Making them visible is the fix; what
    remains is that the hub has no skill pack of its own.

    That is the skills channel — K6/K7 in the estate plan — which the accepted
    build order defers until after the first cold test. So this test does not
    assert zero. It PINS the gap: the count and the exact set of paths, so the
    residue is a tracked number rather than a thing someone rediscovers, and so
    the day a hub-compatible skill set lands this test is its acceptance
    criterion (the assertion below should then be updated to an empty set, in
    the PR that closes the gap).
    """
    from engine.checks.check_skill_grounds import check_skill_grounds

    root, config, _lines = _adopt_into(tmp_path, "hub")
    findings = check_skill_grounds(root, state_dir=config.state_dir, config=config)
    named = set()
    for f in findings:
        for word in f.message.replace("`", " ").split():
            if word.startswith(("docs/", "control/")):
                named.add(word)
    # Every path named is one the hub profile genuinely omits — an advisory
    # naming something else would be a bug in the filter, not a known gap.
    omitted = set(HUB_PROFILE.omit_plan_dests)
    assert named, "the gap is real; an empty result means the filter stopped working"
    assert named <= omitted, sorted(named - omitted)
    # And the DEFAULT shape has no such gap: it plants what its skills name.
    def_root, def_config, _ = _adopt_into(tmp_path)
    def_findings = check_skill_grounds(
        def_root, state_dir=def_config.state_dir, config=def_config,
    )
    def_named = {
        w
        for f in def_findings
        for w in f.message.replace("`", " ").split()
        if w.startswith(("docs/", "control/"))
    }
    assert not def_named, sorted(def_named)


# --------------------------------------------------------------------------
# Adversarial review (43 agents, 37 findings, 14 survived refutation)
# --------------------------------------------------------------------------


def test_adv_a_hub_that_writes_its_own_state_doc_does_not_red(tmp_path):
    """The finding that overturned an earlier judgement of mine.

    I had left ``readpath_docs`` at the shipped default because a hub plants no
    docs, so nothing engages. That is true only while the hub stays EMPTY. The
    moment it writes its own state document — exactly what "declare your own
    folders" tells it to do — ``check_orientation_budget`` engages on the doc
    that exists and reds, EXIT-AFFECTING, on the one the shape guarantees it
    will never plant.
    """
    hub = new_config("hub")
    assert hub.readpath_docs == ["current-state.md"]
    assert "docs/AGENT_ORIENTATION.md" in HUB_PROFILE.omit_plan_dests

    # Exercised END TO END through the built artifact, not by calling the
    # checker directly: `cmd_check` engages it only when at least one
    # CONFIGURED boot doc exists, and that gate is half the behaviour. A direct
    # call bypasses it and measures the wrong thing (it did, on the first
    # draft of this test).
    root = _cold_repo(tmp_path)
    assert _run(root, "adopt", "--profile", "hub").returncode == 0
    bare = _run(root, "check", "--strict")
    assert "orientation-missing" not in bare.stdout, bare.stdout

    (root / "docs").mkdir(exist_ok=True)
    (root / "docs" / "current-state.md").write_text(
        "# now\n\n> **Status:** `living-ledger`\n\nstate.\n", encoding="utf-8",
    )
    written = _run(root, "check", "--strict")
    assert "orientation-missing" not in written.stdout, written.stdout

    # Mutant: the SHIPPED DEFAULT boot pair — what this profile carried before
    # the fix — reds exit-affecting on the doc the shape never plants.
    raw = json.loads((root / "substrate.config.json").read_text(encoding="utf-8"))
    raw["readpath_docs"] = ["AGENT_ORIENTATION.md", "current-state.md"]
    (root / "substrate.config.json").write_text(json.dumps(raw, indent=2), encoding="utf-8")
    stale = _run(root, "check", "--strict")
    assert "orientation-missing" in stale.stdout
    assert "AGENT_ORIENTATION" in stale.stdout


def test_adv_the_hubs_own_docs_are_still_reachability_checked(tmp_path):
    """The other half of the same decision, and why the value is not ``[]``.

    With no read-path roots at all the hub's own state document becomes an
    ORPHAN instead — one false red traded for another. Naming the one entry a
    hub plausibly writes keeps orphan detection working.
    """
    from engine.checks.check_docs import check_reachable

    root, config, _lines = _adopt_into(tmp_path, "hub")
    docs = root / "docs"
    docs.mkdir(exist_ok=True)
    (docs / "current-state.md").write_text(
        "# now\n\n> **Status:** `living-ledger`\n\nstate.\n", encoding="utf-8",
    )
    assert check_reachable(docs, config.readpath_docs) == []
    (docs / "stray.md").write_text(
        "# stray\n\n> **Status:** `reference`\n\nunlinked.\n", encoding="utf-8",
    )
    orphans = [f.path for f in check_reachable(docs, config.readpath_docs)]
    assert orphans == ["stray.md"], orphans


def test_adv_the_seat_digest_verb_cannot_undo_the_profile(tmp_path, capsys):
    # `adopt` gated the digest on the profile; the on-demand verb did not, so
    # one `bootstrap.py seat-digest` re-created the doc a sparse shape exists
    # to not have — a profile undone by a verb.
    from engine.cli import cmd_seat_digest

    root, config, _lines = _adopt_into(tmp_path, "hub")
    save_config(root, config)
    assert cmd_seat_digest(root) == 2
    assert "refused" in capsys.readouterr().out
    assert not (root / "docs" / "seat-digest.md").exists()
    # Mutant: the default shape still writes it on demand.
    def_root, def_config, _ = _adopt_into(tmp_path)
    save_config(def_root, def_config)
    assert cmd_seat_digest(def_root) == 0
    assert (def_root / "docs" / "seat-digest.md").is_file()


def test_adv_the_stance_route_names_no_omitted_doc():
    # The stance briefing is injected at SessionStart, so a dead route there is
    # the first thing a booting session is told to read.
    from engine.stances.stances import stance_briefing

    default_text = stance_briefing("analysis")
    assert "AGENT_ORIENTATION.md" in default_text
    hub_text = stance_briefing("analysis", HUB_PROFILE.omit_plan_dests)
    for dead in ("AGENT_ORIENTATION.md", "architecture.md", "ownership.md"):
        assert dead not in hub_text, dead
    assert "plants no generic doc set" in hub_text


def test_adv_the_stale_scan_reads_only_below_the_marker(tmp_path):
    # It promised "only lines under the marker" and comprehended over the whole
    # file, so a host's own unrelated ignore line could be reported as the
    # kit's stale leftover.
    from engine.adopt import TELEMETRY_IGNORE_MARKER

    root = tmp_path / "repo"
    root.mkdir()
    (root / ".gitignore").write_text(
        "# host policy\n/vendor/guard-fires.jsonl\n", encoding="utf-8",
    )
    config = new_config("hub")
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    stale = [ln for ln in lines if ln.startswith("telemetry: .gitignore still carries")]
    assert not stale, stale
    text = (root / ".gitignore").read_text(encoding="utf-8")
    assert "/vendor/guard-fires.jsonl" in text
    assert TELEMETRY_IGNORE_MARKER in text


def test_adv_the_stale_scan_matches_a_moved_ledger_path(tmp_path):
    # It matched on the DEFAULT filename, so it missed every install that had
    # moved the ledger via the `path` axis — the case a stale entry is most
    # likely to arise from.
    root = tmp_path / "repo"
    config = new_config("hub")
    config.telemetry = {"guard_fires": {"enabled": True, "path": "telemetry/fires.jsonl", "tracked": False, "max_records": 0}}
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    assert "/telemetry/fires.jsonl" in (root / ".gitignore").read_text(encoding="utf-8")
    # Move the path: the previous entry is now stale and must be NAMED.
    config.telemetry = {"guard_fires": {"enabled": True, "path": "telemetry/other.jsonl", "tracked": False, "max_records": 0}}
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    stale = [ln for ln in lines if "still carries" in ln]
    assert stale, lines
    assert "/telemetry/fires.jsonl" in stale[0]


def test_adv_the_lock_is_ignored_on_the_max_records_axis(tmp_path):
    # The two artifacts ride different axes. Conflating them left a
    # tracked+capped install with an unignored lock file in `git status`.
    from engine.loop.telemetry import LOCK_SUFFIX

    root = tmp_path / "repo"
    config = Config()  # DEFAULT profile: tracked ledger...
    config.telemetry = {"guard_fires": {"enabled": True, "path": "", "tracked": True, "max_records": 500}}
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    ignored = (root / ".gitignore").read_text(encoding="utf-8")
    # ...the ledger is NOT ignored (tracked), but its lock is (it is machine
    # state, never worth committing under any policy).
    assert f"/.substrate/{GUARD_FIRES_FILENAME}{LOCK_SUFFIX}" in ignored
    assert f"/.substrate/{GUARD_FIRES_FILENAME}\n" not in ignored
    # And an UNCAPPED default plants neither — no lock file is ever created.
    plain = tmp_path / "plain"
    pconfig = Config()
    adopt(plain, pconfig, _backend(plain, pconfig), kit_root=tmp_path / "kit")
    if (plain / ".gitignore").exists():
        assert GUARD_FIRES_FILENAME not in (plain / ".gitignore").read_text(encoding="utf-8")


def test_adv_the_trim_counts_records_not_splitlines_units(tmp_path):
    # json.dumps(ensure_ascii=False) leaves U+2028/U+2029/U+0085 raw inside
    # string values; str.splitlines() breaks on all of them, so one record
    # carrying one in a message would be read as two — the cap counting the
    # wrong unit, and a trim slicing at that boundary writing back half a
    # record.
    from engine.loop.telemetry import _records

    assert _records('{"a": "x y"}\n') == ['{"a": "x y"}']
    assert len('{"a": "x y"}'.splitlines()) == 2  # the trap, pinned

    root = tmp_path / "repo"
    (root / ".substrate").mkdir(parents=True)
    policy = {"enabled": True, "path": "", "tracked": False, "max_records": 5}
    for i in range(400):
        record_guard_fires(
            root, ".substrate", cmd="check", surface="check", posture="advisory",
            findings=[_finding(f"p{i}", "kind", f"line break {i}")],
            verdict="false_positive", reason="fixture", policy=policy,
        )
    path = guard_fires_path(root, ".substrate", policy)
    for line in _records(path.read_text(encoding="utf-8")):
        json.loads(line)  # every record survives the trim intact


def test_adv_an_unusable_telemetry_path_falls_back(tmp_path):
    # A newline cannot be escaped in a gitignore line and would split every
    # downstream consumer's idea of "one path" in half.
    root = tmp_path / "repo"
    for bad in ("a\nb.jsonl", "a\rb.jsonl", "\n"):
        policy = {"enabled": True, "path": bad, "tracked": False, "max_records": 0}
        assert guard_fires_path(root, ".substrate", policy) == (
            root / ".substrate" / GUARD_FIRES_FILENAME
        ), bad


# --------------------------------------------------------------------------
# Codex round 2 (PR #590, head 7b07c1d) — five P2 findings, one test each
# --------------------------------------------------------------------------


def test_codex_r2_the_staged_agreement_is_scanned_for_dead_routes(tmp_path):
    # On the NORMAL path (no --include-claude) the only working agreement
    # produced is the STAGED one, and the scan added only the live copy — so
    # the report said nothing in exactly the case a host most needs told, and
    # installing the staged agreement installed dead pointers silently.
    root, config, lines = _adopt_into(tmp_path, "hub")
    assert not (root / ".claude" / "CLAUDE.md").exists()
    staged = root / config.state_dir / "claude" / "CLAUDE.md"
    assert staged.is_file()
    body = staged.read_text(encoding="utf-8")
    assert "`docs/SKILLS.md`" in body, "precondition: the staged agreement has dead routes"
    # Assert the STAGED PATH is itself named. Asserting only that some report
    # mentions docs/SKILLS.md passes via CONSTITUTION.md, which routes there
    # too — the first draft of this test did exactly that and a mutation
    # removing the staged scan survived it.
    staged_rel = f"{config.state_dir}/claude/CLAUDE.md"
    staged_reports = [
        ln for ln in lines
        if ln.startswith("profile 'hub':") and staged_rel in ln
    ]
    assert staged_reports, lines
    assert "docs/SKILLS.md" in staged_reports[0], staged_reports
    # Live + staged are the same render; one problem must not print twice.
    both_root, _bc, both_lines = _adopt_into(tmp_path, "hub", include_claude=True)
    assert both_root  # adopted
    agreement_reports = [
        ln for ln in both_lines
        if ln.startswith("profile 'hub':") and "CLAUDE.md" in ln
    ]
    assert len(agreement_reports) == 1, agreement_reports


def test_codex_r2_no_digest_advisory_on_a_shape_that_plants_no_digest(tmp_path):
    # A repo that KEPT docs/seat-digest.md while moving to a sparse profile was
    # told `seat-digest-stale` forever, and the fix that advisory names is the
    # one command the profile gate refuses with exit 2.
    from engine.cli import cmd_check

    root, config, _lines = _adopt_into(tmp_path)
    digest = root / "docs" / "seat-digest.md"
    assert digest.is_file()
    digest.write_text("# stale\n", encoding="utf-8")
    # Move the install to the sparse shape the way cmd_init's refusal suggests.
    config.adoption_profile = "hub"
    save_config(root, config)
    from engine.checks.check_seat_digest import check_seat_digest

    # The checker itself still fires — the gate is in cmd_check, which is what
    # decides whether a session ever sees advice it cannot act on.
    assert check_seat_digest(root, config, context={}), "precondition"

    def _advisory_lines(where):
        import engine.cli as cli_mod

        out = []
        original = cli_mod._emit
        cli_mod._emit = out.append
        try:
            # advisories=True is the surface the finding is ON: without it the
            # heuristic tail is summarised as a count, so grepping the default
            # output tests nothing (the first draft of this test did, and a
            # mutation removing the gate survived it).
            cmd_check(where, strict=False, advisories=True)
        finally:
            cli_mod._emit = original
        return out

    # Match the CHECKER's own finding kinds, not the substring "seat-digest":
    # a hand-written fixture file also draws an unrelated `[badge]` finding
    # naming the same path, which would make this assertion fail for the wrong
    # reason (it did).
    kinds = ("seat-digest-stale", "seat-digest-over-budget")

    def _digest_findings(where):
        return [ln for ln in _advisory_lines(where) if any(k in ln for k in kinds)]

    assert not _digest_findings(root), "hub"
    # Mutant: the DEFAULT shape still gets the advisory it can act on.
    def_root, def_config, _ = _adopt_into(tmp_path)
    (def_root / "docs" / "seat-digest.md").write_text(
        "# stale\n\n> **Status:** `reference`\n", encoding="utf-8",
    )
    save_config(def_root, def_config)
    assert _digest_findings(def_root), "default"


def test_codex_r2_a_root_level_state_doc_does_not_red_the_hub(tmp_path):
    # The third state I had not measured: cmd_check's own predicate counted a
    # ROOT-level match, which the readpath fallback never resolves to, so a
    # repo whose state document sits at the root engaged the checker and was
    # then red for a docs/ path it deliberately never created.
    root = _cold_repo(tmp_path)
    assert _run(root, "adopt", "--profile", "hub").returncode == 0
    (root / "current-state.md").write_text(
        "# now\n\n> **Status:** `living-ledger`\n\nstate.\n", encoding="utf-8",
    )
    result = _run(root, "check", "--strict")
    assert "orientation-missing" not in result.stdout, result.stdout


def test_codex_r2_the_engagement_predicate_is_the_resolver(tmp_path):
    # The root cause of the finding above, pinned directly: one function, one
    # answer. Any predicate that is not this resolver can disagree with it.
    from engine.checks.check_orientation_budget import orientation_boot_paths

    config = new_config("hub")
    resolved = orientation_boot_paths(tmp_path, config)
    assert resolved == [tmp_path / "docs" / "current-state.md"]
    # An explicit boot_docs entry carrying "/" resolves from the root — the
    # supported way to name a root-level document.
    rooted = new_config("hub")
    rooted.orientation = dict(rooted.orientation, boot_docs=["./current-state.md"])
    assert orientation_boot_paths(tmp_path, rooted) == [tmp_path / "./current-state.md"]


def test_codex_r2_the_announcement_asserts_no_git_fact(tmp_path):
    # It said "no delta to commit" before acknowledging the exact case where
    # there IS one — still asserting the unchecked git fact the rewrite was
    # meant to remove.
    from engine.cli import cmd_check

    root, config, _lines = _adopt_into(tmp_path, "hub")
    save_config(root, config)
    import engine.cli as cli_mod

    out = []
    original = cli_mod._emit
    cli_mod._emit = out.append
    try:
        cmd_check(root, strict=False)
    finally:
        cli_mod._emit = original
    announced = [line for line in out if "guard-fire record(s) appended" in line]
    assert announced, out
    line = announced[0]
    assert "no delta to commit" not in line
    assert "nothing to commit" not in line
    assert "claims nothing about your working tree" in line
    assert "git rm --cached" in line


def test_codex_r2_a_host_line_below_the_fence_is_not_claimed(tmp_path):
    # Without a closing fence, "the kit's lines" had no end: every
    # root-anchored rule a host added LATER fell inside the claimed region and
    # was reported as a stale telemetry leftover on every pass, forever.
    from engine.adopt import TELEMETRY_IGNORE_END, TELEMETRY_IGNORE_MARKER

    root = tmp_path / "repo"
    config = new_config("hub")
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    text = (root / ".gitignore").read_text(encoding="utf-8")
    assert TELEMETRY_IGNORE_MARKER in text
    assert TELEMETRY_IGNORE_END in text
    # A host rule appended BELOW the block is host-owned and must stay unclaimed.
    (root / ".gitignore").write_text(text + "/vendor/\n", encoding="utf-8")
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    assert not [ln for ln in lines if "still carries" in ln], lines
    # ...while a genuinely stale entry INSIDE the block is still named.
    inside = (root / ".gitignore").read_text(encoding="utf-8").replace(
        TELEMETRY_IGNORE_END, "/.substrate/old-fires.jsonl\n" + TELEMETRY_IGNORE_END,
    )
    (root / ".gitignore").write_text(inside, encoding="utf-8")
    lines = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    stale = [ln for ln in lines if "still carries" in ln]
    assert stale and "old-fires.jsonl" in stale[0], lines
    assert "/vendor/" not in " ".join(stale)


# --------------------------------------------------------------------------
# Codex round 3 (PR #590, head 19d70ee) — the last round the cap allows
# --------------------------------------------------------------------------


def test_codex_r3_upgrade_refuses_an_unknown_profile_before_any_write(tmp_path):
    # `adopt` resolved strictly, but `run_upgrade` only reaches it at step 6 —
    # after archiving state, applying doc changes, refreshing derived files and
    # replacing the vendored bootstrap. The refusal then arrived as an uncaught
    # exception over a PARTIALLY UPGRADED repository. A refusal is only safe
    # where nothing has happened yet.
    from engine.lib.config import KIT_VERSION
    from engine.upgrade import UpgradeRefused, run_upgrade

    root, config, _lines = _adopt_into(tmp_path, "hub")
    config.adoption_profile = "hubb"
    save_config(root, config)
    before = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    running = tmp_path / "bootstrap.py.new"
    running.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED, DO NOT EDIT."""\n',
        encoding="utf-8",
    )
    with pytest.raises(UpgradeRefused) as exc:
        run_upgrade(root, config, backend, kit_root=tmp_path / "kit", running=running)
    assert "hubb" in str(exc.value)
    assert "before any write" in str(exc.value)
    after = sorted(p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file())
    assert before == after, "the refusal must leave the tree untouched"


def test_codex_r3_the_ledger_cannot_escape_the_repo_through_a_symlink(tmp_path):
    # Rejecting absolute paths and literal ".." is a guess about the STRING and
    # says nothing about the filesystem. Measured before the fix: a `telemetry`
    # symlink pointing outside the repo plus path "telemetry/fires.jsonl" had
    # `check` appending the ledger into the external directory.
    root = tmp_path / "repo"
    outside = tmp_path / "outside"
    root.mkdir()
    outside.mkdir()
    (root / ".substrate").mkdir()
    (root / "telemetry").symlink_to(outside, target_is_directory=True)

    default = root / ".substrate" / GUARD_FIRES_FILENAME
    for escape in ("telemetry/fires.jsonl", ".", "..", "/etc/x.jsonl", "a/../../b.jsonl"):
        policy = {"enabled": True, "path": escape, "tracked": False, "max_records": 0}
        assert guard_fires_path(root, ".substrate", policy) == default, escape
    # A path naming an existing DIRECTORY is not a ledger either — the append
    # would fail and, under a cap, the sidecar lock would be created beside it.
    (root / "docs").mkdir()
    d = {"enabled": True, "path": "docs", "tracked": False, "max_records": 0}
    assert guard_fires_path(root, ".substrate", d) == default
    # A genuine in-repo file path is still honoured.
    ok = {"enabled": True, "path": "state/fires.jsonl", "tracked": False, "max_records": 0}
    assert guard_fires_path(root, ".substrate", ok) == root / "state" / "fires.jsonl"

    # End to end: nothing may land outside the tree.
    policy = {"enabled": True, "path": "telemetry/fires.jsonl", "tracked": False, "max_records": 5}
    for i in range(10):
        record_guard_fires(
            root, ".substrate", cmd="check", surface="check", posture="advisory",
            findings=[_finding(f"p{i}", "k", f"m{i}")], verdict="v", reason="r",
            policy=policy,
        )
    assert list(outside.iterdir()) == [], sorted(p.name for p in outside.iterdir())
    assert default.is_file()
    assert not (tmp_path / "repo.lock").exists()


def test_codex_r3_the_upgrade_digest_refresh_honours_the_profile(tmp_path):
    # Third call site of the same declaration. A default install that moved to
    # a sparse profile had its retained digest REGENERATED on the next upgrade,
    # or was told to run the one command the profile gate refuses.
    from engine.upgrade import refresh_seat_digest

    root, config, _lines = _adopt_into(tmp_path)
    digest = root / "docs" / "seat-digest.md"
    assert digest.is_file()
    digest.unlink()
    config.adoption_profile = "hub"
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    lines = refresh_seat_digest(root, config, backend)
    assert any("skipped" in line for line in lines), lines
    assert not digest.exists()
    # Mutant: the default shape still refreshes.
    def_root, def_config, _ = _adopt_into(tmp_path)
    def_backend = JsonStateBackend(def_root / def_config.state_dir / "state.json")
    def_lines = refresh_seat_digest(def_root, def_config, def_backend)
    assert not any("skipped" in line for line in def_lines), def_lines


def test_codex_r3_new_entries_land_inside_the_existing_fence(tmp_path):
    # Appending at EOF put new entries BELOW the closing marker, where the
    # stale-reconciliation scan can no longer see them — so a later policy
    # change reported the old in-fence rules and silently left the new ledger
    # ignored forever. A managed block only stays managed if everything the kit
    # writes lands in it.
    from engine.adopt import TELEMETRY_IGNORE_END, TELEMETRY_IGNORE_MARKER

    root = tmp_path / "repo"
    config = new_config("hub")
    config.telemetry = {"guard_fires": {"enabled": True, "path": "", "tracked": False, "max_records": 0}}
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    # Move the ledger: the new entry must land INSIDE the fence.
    config.telemetry = {"guard_fires": {"enabled": True, "path": "state/new.jsonl", "tracked": False, "max_records": 0}}
    adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    lines = [ln.strip() for ln in (root / ".gitignore").read_text(encoding="utf-8").splitlines()]
    start = lines.index(TELEMETRY_IGNORE_MARKER)
    end = lines.index(TELEMETRY_IGNORE_END)
    inside = lines[start + 1 : end]
    assert "/state/new.jsonl" in inside, lines
    assert not [ln for ln in lines[end + 1 :] if ln.startswith("/")], lines
    # ...and reconciliation can therefore still see and name it.
    config.telemetry = {"guard_fires": {"enabled": True, "path": "", "tracked": True, "max_records": 0}}
    report = adopt(root, config, _backend(root, config), kit_root=tmp_path / "kit")
    stale = " ".join(ln for ln in report if "still carries" in ln)
    assert "/state/new.jsonl" in stale, report


def test_codex_r3_the_route_dedupe_keys_on_document_content(tmp_path):
    # The key was the route LIST, shared across every scanned document, so two
    # distinct documents citing the same omitted destinations collapsed to one
    # report naming only the first path — while each still needs its own edit.
    from engine.adopt import _report_omitted_routes

    # Build the COLLISION the routes-only key could not distinguish: two
    # different documents citing the same omitted destination. Asserting only
    # that CONSTITUTION.md appears does not test this — its route set differs
    # from the agreements', so it is never the one suppressed (the first draft
    # of this test asserted exactly that, and the mutation survived it).
    root, config, _lines = _adopt_into(tmp_path, "hub")
    (root / "CONSTITUTION.md").write_text(
        "# one\n\nsee `docs/SKILLS.md` for the index.\n", encoding="utf-8",
    )
    (root / ".session-journal.md").write_text(
        "# two — a DIFFERENT document, same citation\n\n`docs/SKILLS.md`\n",
        encoding="utf-8",
    )
    report: list[str] = []
    _report_omitted_routes(root, config, HUB_PROFILE, report)
    paths = {ln.split(": ", 1)[1].split(" ", 1)[0] for ln in report}
    assert "CONSTITUTION.md" in paths, report
    assert ".session-journal.md" in paths, report

    # ...while the staged and live agreements, which ARE the same render,
    # still collapse to one report.
    both, bconfig, blines = _adopt_into(tmp_path, "hub", include_claude=True)
    assert both
    agreements = [
        ln for ln in blines
        if ln.startswith("profile 'hub':") and "CLAUDE.md" in ln
    ]
    assert len(agreements) == 1, agreements


def test_codex_r3_ungroomed_ideas_reports_the_configured_path(tmp_path):
    # The scan was fixed and the finding's PATH was not, so a real finding
    # discovered under sessions/ was printed — and recorded in guard telemetry,
    # and fingerprinted for the allowlist — against a path that does not exist.
    from engine.checks.check_ungroomed_ideas import check_ungroomed_ideas

    root = tmp_path / "repo"
    (root / "sessions").mkdir(parents=True)
    (root / "docs" / "planning").mkdir(parents=True)
    (root / "docs" / "planning" / "2026-01-01-groom.md").write_text("# g\n", encoding="utf-8")
    (root / "sessions" / "2026-02-01-c.md").write_text(
        "# c\n\n\N{ELECTRIC LIGHT BULB} an idea\n", encoding="utf-8",
    )
    findings = check_ungroomed_ideas(root, new_config("hub"))
    assert findings
    assert findings[0].path == "sessions/", findings[0].path
