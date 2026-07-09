"""Tests for the `upgrade` verb (founding plan §4.3): archive-first, hash-based
doc diff, --apply-docs covenant, state backup + rollback, sha256 verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import BACKUP_DIRNAME, DOC_HASHES_STATE_KEY, adopt
from engine.lib.config import KIT_VERSION, Config, load_config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import load_templates
from engine.upgrade import (
    CLASS_CONSUMER_EDITED,
    CLASS_DIVERGED,
    CLASS_IMPROVED,
    CLASS_UNCHANGED,
    UpgradeRefused,
    apply_doc_improvements,
    classify_planted_docs,
    find_vendored_bootstrap,
    load_old_templates,
    run_rollback,
    run_upgrade,
    verify_against_release_json,
)

_OLD_DIST_HEADER = '"""substrate-kit bootstrap v0.9.0 — GENERATED, DO NOT EDIT."""\n'


def _adopted(tmp_path: Path):
    root = tmp_path / "repo"
    config = Config()
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    adopt(root, config, backend, kit_root=tmp_path / "kit")
    return root, config, backend


def _fake_old_dist(root: Path, templates: dict[str, str] | None = None) -> Path:
    """Vendor a fake OLD single-file bootstrap (never executed by upgrade)."""
    body = _OLD_DIST_HEADER
    if templates is not None:
        body += f"\n_TEMPLATES = {templates!r}\n"
    path = root / "bootstrap.py"
    path.write_text(body, encoding="utf-8")
    return path


def _fake_new_dist(tmp_path: Path) -> Path:
    new = tmp_path / "bootstrap.py.new"
    new.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED, DO NOT EDIT."""\n',
        encoding="utf-8",
    )
    return new


# ---------------------------------------------------------------------------
# Old-dist parsing + vendored discovery
# ---------------------------------------------------------------------------


def test_load_old_templates_literal_eval():
    text = "x = 1\n_TEMPLATES = {'a.tmpl': 'hello ${name}'}\n"
    assert load_old_templates(text) == {"a.tmpl": "hello ${name}"}


def test_load_old_templates_absent_or_broken():
    assert load_old_templates("x = 1\n") is None
    assert load_old_templates("def broken(:\n") is None


def test_find_vendored_prefers_root_then_dist(tmp_path):
    root = tmp_path / "r"
    (root / "dist").mkdir(parents=True)
    dist = root / "dist" / "bootstrap.py"
    dist.write_text("d", encoding="utf-8")
    assert find_vendored_bootstrap(root) == dist
    at_root = root / "bootstrap.py"
    at_root.write_text("r", encoding="utf-8")
    assert find_vendored_bootstrap(root) == at_root


# ---------------------------------------------------------------------------
# sha256 verification against release.json
# ---------------------------------------------------------------------------


def _write_release_json(path: Path, *, sha256: str, version: str = KIT_VERSION):
    path.write_text(
        json.dumps({"version": version, "sha256": sha256}),
        encoding="utf-8",
    )


def test_verify_against_release_json_passes(tmp_path):
    running = _fake_new_dist(tmp_path)
    digest = hashlib.sha256(running.read_bytes()).hexdigest()
    rj = tmp_path / "release.json"
    _write_release_json(rj, sha256=digest)
    assert verify_against_release_json(running, rj)


def test_verify_refuses_sha_mismatch(tmp_path):
    running = _fake_new_dist(tmp_path)
    rj = tmp_path / "release.json"
    _write_release_json(rj, sha256="0" * 64)
    with pytest.raises(UpgradeRefused, match="sha256 mismatch"):
        verify_against_release_json(running, rj)


def test_verify_refuses_version_mismatch(tmp_path):
    running = _fake_new_dist(tmp_path)
    digest = hashlib.sha256(running.read_bytes()).hexdigest()
    rj = tmp_path / "release.json"
    _write_release_json(rj, sha256=digest, version="0.0.1")
    with pytest.raises(UpgradeRefused, match="mismatched release files"):
        verify_against_release_json(running, rj)


# ---------------------------------------------------------------------------
# Doc classification (the §4.3 classes)
# ---------------------------------------------------------------------------


def test_untouched_docs_with_identical_templates_are_unchanged(tmp_path):
    root, config, backend = _adopted(tmp_path)
    rows = classify_planted_docs(root, config, backend, load_templates())
    assert rows
    assert {r["class"] for r in rows} == {CLASS_UNCHANGED}


def test_template_improvement_on_untouched_doc_is_apply_safe(tmp_path):
    root, config, backend = _adopted(tmp_path)
    new_templates = dict(load_templates())
    new_templates["architecture.md.tmpl"] += "\nNew guidance paragraph.\n"
    rows = classify_planted_docs(
        root,
        config,
        backend,
        load_templates(),
        new_templates,
    )
    by_rel = {r["relpath"]: r for r in rows}
    assert by_rel["docs/architecture.md"]["class"] == CLASS_IMPROVED


def test_consumer_edit_with_unchanged_template_is_consumer_owned(tmp_path):
    root, config, backend = _adopted(tmp_path)
    doc = root / "docs" / "architecture.md"
    doc.write_text(
        doc.read_text(encoding="utf-8") + "\nconsumer note\n",
        encoding="utf-8",
    )
    rows = classify_planted_docs(root, config, backend, load_templates())
    by_rel = {r["relpath"]: r for r in rows}
    assert by_rel["docs/architecture.md"]["class"] == CLASS_CONSUMER_EDITED


def test_both_moved_is_diverged_with_a_template_delta(tmp_path):
    root, config, backend = _adopted(tmp_path)
    doc = root / "docs" / "architecture.md"
    doc.write_text(
        doc.read_text(encoding="utf-8") + "\nconsumer note\n",
        encoding="utf-8",
    )
    new_templates = dict(load_templates())
    new_templates["architecture.md.tmpl"] += "\nNew guidance paragraph.\n"
    rows = classify_planted_docs(
        root,
        config,
        backend,
        load_templates(),
        new_templates,
    )
    by_rel = {r["relpath"]: r for r in rows}
    row = by_rel["docs/architecture.md"]
    assert row["class"] == CLASS_DIVERGED
    assert "New guidance paragraph." in row["diff"]


def test_no_recorded_hashes_means_everything_diverges(tmp_path):
    # Pre-1.0 installs have no recorded hashes: honest and safe — nothing is
    # ever auto-applied.
    root, config, backend = _adopted(tmp_path)
    backend.set(DOC_HASHES_STATE_KEY, {})
    rows = classify_planted_docs(root, config, backend, None)
    assert {r["class"] for r in rows} == {CLASS_DIVERGED}


def test_apply_docs_touches_only_the_improved_untouched_class(tmp_path):
    root, config, backend = _adopted(tmp_path)
    edited = root / "docs" / "ownership.md"
    consumer_text = edited.read_text(encoding="utf-8") + "\nconsumer note\n"
    edited.write_text(consumer_text, encoding="utf-8")
    new_templates = dict(load_templates())
    new_templates["architecture.md.tmpl"] += "\nNew guidance paragraph.\n"
    new_templates["ownership.md.tmpl"] += "\nNew guidance paragraph.\n"
    rows = classify_planted_docs(
        root,
        config,
        backend,
        load_templates(),
        new_templates,
    )
    applied = apply_doc_improvements(root, config, backend, rows, new_templates)
    # The untouched doc took the improvement…
    arch = (root / "docs" / "architecture.md").read_text(encoding="utf-8")
    assert "New guidance paragraph." in arch
    assert any("docs/architecture.md" in line for line in applied)
    # …the consumer-diverged doc was NOT touched (the §4.3 covenant).
    assert edited.read_text(encoding="utf-8") == consumer_text
    # And the applied doc's hash was re-recorded (still "untouched").
    rows_after = classify_planted_docs(
        root,
        config,
        backend,
        new_templates,
        new_templates,
    )
    by_rel = {r["relpath"]: r for r in rows_after}
    assert by_rel["docs/architecture.md"]["class"] == CLASS_UNCHANGED


# ---------------------------------------------------------------------------
# The full flow: archive-first, replace, state backup, report, rollback
# ---------------------------------------------------------------------------


def test_run_upgrade_archives_replaces_and_reports(tmp_path):
    root, config, backend = _adopted(tmp_path)
    old = _fake_old_dist(root, {"architecture.md.tmpl": "old ${project_name}"})
    old_text = old.read_text(encoding="utf-8")
    running = _fake_new_dist(tmp_path)
    config.kit_version = "0.9.0"  # what the old adopt recorded
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
        apply_docs=False,
    )
    backup = root / config.state_dir / BACKUP_DIRNAME
    # Archive-first: the OLD dist is banked under its version name…
    archived = backup / "bootstrap-0.9.0.py"
    assert archived.is_file()
    assert archived.read_text(encoding="utf-8") == old_text
    # …state.json banked, the last-upgrade marker written…
    assert (backup / "state.json").is_file()
    meta = json.loads((backup / "last-upgrade.json").read_text(encoding="utf-8"))
    assert meta["from_version"] == "0.9.0"
    assert meta["to_version"] == KIT_VERSION
    # …the vendored file now IS the running (new) file…
    assert old.read_text(encoding="utf-8") == running.read_text(encoding="utf-8")
    # …kit_version re-recorded, report written, sha note honest.
    assert load_config(root).kit_version == KIT_VERSION
    report = root / config.state_dir / "upgrade-report.md"
    assert report.is_file()
    assert f"v0.9.0 → v{KIT_VERSION}" in report.read_text(encoding="utf-8")
    assert any("sha256 verification skipped" in line for line in lines)


def test_run_upgrade_verifies_release_json_when_present(tmp_path):
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    rj = tmp_path / "release.json"
    _write_release_json(rj, sha256="0" * 64)
    with pytest.raises(UpgradeRefused):
        run_upgrade(
            root,
            config,
            backend,
            kit_root=tmp_path / "kit",
            running=running,
            release_json=rj,
        )


def test_rollback_restores_state_and_dist(tmp_path):
    root, config, backend = _adopted(tmp_path)
    old = _fake_old_dist(root)
    old_text = old.read_text(encoding="utf-8")
    state_path = root / config.state_dir / "state.json"
    state_before = state_path.read_text(encoding="utf-8")
    running = _fake_new_dist(tmp_path)
    config.kit_version = "0.9.0"
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert old.read_text(encoding="utf-8") != old_text  # replaced
    lines = run_rollback(root, load_config(root))
    assert old.read_text(encoding="utf-8") == old_text  # restored
    assert state_path.read_text(encoding="utf-8") == state_before
    assert load_config(root).kit_version == "0.9.0"
    assert any("restored" in line for line in lines)


def test_rollback_without_marker_is_a_noop(tmp_path):
    root, config, _ = _adopted(tmp_path)
    lines = run_rollback(root, config)
    assert any("nothing to roll back" in line for line in lines)


# ---------------------------------------------------------------------------
# KL-3: the 📊 Model needle joins the gate at upgrade time
# ---------------------------------------------------------------------------


def test_upgrade_adds_model_line_needle_to_pre_kl3_install(tmp_path):
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root, {"architecture.md.tmpl": "old ${project_name}"})
    running = _fake_new_dist(tmp_path)
    # Simulate a pre-KL-3 install: its saved markers lack the Model line.
    config.session_markers = [
        m for m in config.session_markers if m.get("label") != "Model line"
    ]
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert any("Model line needle" in line for line in lines)
    saved = load_config(root)
    assert any(m.get("label") == "Model line" for m in saved.session_markers)
    # Idempotent: a re-run neither duplicates the marker nor re-reports.
    lines = run_upgrade(
        root,
        saved,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert not any("Model line needle" in line for line in lines)
    markers = [
        m for m in load_config(root).session_markers if m.get("label") == "Model line"
    ]
    assert len(markers) == 1
