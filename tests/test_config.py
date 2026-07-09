"""Tests for the substrate-kit config (the two-interpreter schema)."""

import json
from pathlib import Path

from engine.lib.config import (
    KIT_VERSION,
    Config,
    config_path,
    load_config,
    save_config,
)


def test_defaults_have_two_interpreters():
    c = Config()
    assert c.interpreter  # defaults to the running interpreter
    assert c.interpreter_for_checks is None  # host sets this (e.g. python3.10)
    assert c.state_dir == ".substrate"
    assert len(c.project_id) == 12
    # 30, not 20: the founding plan §3.4 drift fix (the origin repo's Q-0134).
    assert c.cadence["reconciliation_prs"] == 30


def test_project_id_is_unique_per_install():
    assert Config().project_id != Config().project_id


def test_from_dict_ignores_unknown_keys():
    c = Config.from_dict({"project_id": "abc", "not_a_field": 1})
    assert c.project_id == "abc"


def test_save_and_load_roundtrip(tmp_path: Path):
    original = Config(project_id="proj12345678", interpreter_for_checks="python3.10")
    save_config(tmp_path, original)
    assert config_path(tmp_path).exists()
    loaded = load_config(tmp_path)
    assert loaded.project_id == "proj12345678"
    assert loaded.interpreter_for_checks == "python3.10"


def test_load_missing_returns_defaults(tmp_path: Path):
    assert load_config(tmp_path).state_dir == ".substrate"


def test_kit_version_is_semver():
    assert len(KIT_VERSION.split(".")) == 3


def test_kit_version_field_defaults_unrecorded():
    # "" until adopt/upgrade records it — a pre-release install must not
    # claim a version it never adopted.
    assert Config().kit_version == ""


def test_kit_version_survives_from_dict_roundtrip(tmp_path: Path):
    # The founding plan §4.1 warning made real: kit_version MUST be a declared
    # dataclass field — from_dict drops unknown keys and save_config
    # serialises only fields, so a bare JSON key would be stripped on the
    # next load→save round-trip.
    c = Config.from_dict({"kit_version": "1.0.0"})
    assert c.kit_version == "1.0.0"
    save_config(tmp_path, c)
    assert load_config(tmp_path).kit_version == "1.0.0"
    assert json.loads(c.to_json())["kit_version"] == "1.0.0"
