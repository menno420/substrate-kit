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
    assert "UNTRACKED by this install's policy" in checked.stdout
    assert "commit the delta" not in checked.stdout
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
