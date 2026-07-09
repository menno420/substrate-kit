"""Tests for the KL-1 version surface: the `--version` flag + render --live hashes."""

from __future__ import annotations

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import DOC_HASHES_STATE_KEY, adopt, doc_is_untouched
from engine.cli import cmd_render, main
from engine.lib.config import KIT_VERSION, Config
from engine.lib.state import JsonStateBackend, default_state


def test_version_flag_prints_kit_version(capsys):
    with pytest.raises(SystemExit) as excinfo:
        main(["--version"])
    assert excinfo.value.code == 0
    assert f"substrate-kit {KIT_VERSION}" in capsys.readouterr().out


def _adopted(tmp_path):
    root = tmp_path / "repo"
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    return root, config


def test_render_live_rerecords_the_doc_hash(tmp_path):
    # §4.3: a `render --live` rewrite is kit-written content — the recorded
    # hash must follow it, or every slot-fill would masquerade as a consumer
    # edit and block --apply-docs forever.
    root, config = _adopted(tmp_path)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    values = backend.get("slot_values", {})
    # A slot adopt could NOT derive (so its placeholder survived planting).
    values["drift_resolution"] = {"value": "source wins", "status": "confirmed"}
    backend.set("slot_values", values)
    assert cmd_render(root, live=True) == 0
    fresh = JsonStateBackend(root / config.state_dir / "state.json")
    hashes = fresh.get(DOC_HASHES_STATE_KEY)
    rel = "CONSTITUTION.md"
    text = (root / rel).read_text(encoding="utf-8")
    assert "source wins" in text
    assert "${drift_resolution}" not in text
    assert hashes[rel]
    assert doc_is_untouched(fresh, rel, text)
