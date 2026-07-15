"""Tests for the `upgrade` verb (founding plan §4.3): archive-first, hash-based
doc diff, --apply-docs covenant, state backup + rollback, sha256 verification."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.adopt import (
    BACKUP_DIRNAME,
    DOC_HASHES_STATE_KEY,
    adopt,
    dist_version,
    doc_is_untouched,
)
from engine.lib.config import KIT_VERSION, Config, load_config
from engine.lib.state import JsonStateBackend, default_state
from engine.render import load_templates
from engine.upgrade import (
    CLASS_CONSUMER_EDITED,
    CLASS_DIVERGED,
    CLASS_IMPROVED,
    CLASS_MISSING,
    CLASS_UNCHANGED,
    UpgradeRefused,
    apply_doc_improvements,
    classify_planted_docs,
    find_vendored_bootstrap,
    load_old_templates,
    newest_banked_archive,
    run_apply_docs_posthoc,
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


def test_missing_skill_index_classifies_missing_and_replants(tmp_path):
    # Grounded-skills slice 1 accept criterion: an adopter installed before
    # the index existed has no docs/SKILLS.md — the upgrade doc diff
    # classifies it `missing` and the upgrade's adopt pass replants it.
    root, config, backend = _adopted(tmp_path)
    (root / "docs" / "SKILLS.md").unlink()
    rows = classify_planted_docs(root, config, backend, load_templates())
    row = next(r for r in rows if r["relpath"] == "docs/SKILLS.md")
    assert row["class"] == CLASS_MISSING
    assert "replants" in row["note"]
    # The adopt pass (what upgrade runs) replants the missing index.
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert "planted: docs/SKILLS.md" in lines
    assert (root / "docs" / "SKILLS.md").is_file()


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


def test_no_recorded_hashes_and_no_byte_match_stays_diverged(tmp_path):
    # No recorded hashes AND no byte-match to any known template render →
    # honestly diverged, nothing auto-applied. Self-heal (idea
    # upgrade-rollback-loses-doc-hash-records) only recovers a hash when the
    # doc byte-matches a render, so a doc matching nothing on record stays
    # diverged.
    root, config, backend = _adopted(tmp_path)
    backend.set(DOC_HASHES_STATE_KEY, {})
    # Diverge every NEW template render from what is on disk so no byte-match
    # can self-heal a hash back.
    new_templates = {
        name: text + "\nan unmatched new paragraph\n"
        for name, text in load_templates().items()
    }
    rows = classify_planted_docs(root, config, backend, None, new_templates)
    assert rows
    assert {r["class"] for r in rows} == {CLASS_DIVERGED}


def test_self_heal_recovers_a_lost_hash_on_new_template_byte_match(tmp_path):
    # `upgrade --rollback` restores the pre-upgrade state.json, discarding the
    # adopt-pass planted_doc_hashes; on the re-run a kit-written doc would carry
    # no hash and classify diverged, out of --apply-docs' reach (idea
    # upgrade-rollback-loses-doc-hash-records). A byte-match to the NEW template
    # render proves the doc is untouched kit-form, so classify records the hash
    # from ground truth and the doc reads unchanged — restoring the hash
    # coverage the first run achieved.
    root, config, backend = _adopted(tmp_path)
    # Simulate the rollback wiping every recorded hash.
    backend.set(DOC_HASHES_STATE_KEY, {})
    rows = classify_planted_docs(root, config, backend, load_templates())
    assert rows
    assert {r["class"] for r in rows} == {CLASS_UNCHANGED}
    # The hash coverage is back: every kept kit-form doc is untouched again.
    for row in rows:
        rel = row["relpath"]
        text = (root / rel).read_text(encoding="utf-8")
        assert doc_is_untouched(backend, rel, text), rel
    # A consumer-edited doc still never self-heals (it does not byte-match):
    # with no hashes and no old templates on record it stays honestly diverged.
    edited = root / "docs" / "architecture.md"
    edited.write_text(
        edited.read_text(encoding="utf-8") + "\nconsumer note\n",
        encoding="utf-8",
    )
    backend.set(DOC_HASHES_STATE_KEY, {})
    rows_edited = classify_planted_docs(root, config, backend, None)
    by_rel = {r["relpath"]: r for r in rows_edited}
    assert by_rel["docs/architecture.md"]["class"] == CLASS_DIVERGED
    assert not doc_is_untouched(
        backend,
        "docs/architecture.md",
        edited.read_text(encoding="utf-8"),
    )


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
    new_text = running.read_text(encoding="utf-8")
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
    # …the vendored file now IS the (new) file the flow ran from…
    assert old.read_text(encoding="utf-8") == new_text
    # …and the consumed .new input was cleaned up (default behavior).
    assert not running.exists()
    assert any("cleaned up: bootstrap.py.new" in line for line in lines)
    # …kit_version re-recorded, report written, sha note honest.
    assert load_config(root).kit_version == KIT_VERSION
    report = root / config.state_dir / "upgrade-report.md"
    assert report.is_file()
    assert f"v0.9.0 → v{KIT_VERSION}" in report.read_text(encoding="utf-8")
    assert any("sha256 verification skipped" in line for line in lines)


def test_upgrade_banks_only_the_pre_upgrade_dist(tmp_path):
    # Regression for the spurious-backup field bug (fleet-manager #35,
    # superbot-games #22, trading-strategy #38): upgrade's step-6 adopt pass
    # re-archived the vendored file AFTER the replace, banking a copy of the
    # NEW dist (`bootstrap-<new>.py`) next to the correct old-dist archive.
    # Harmless (last-upgrade.json named the right one) but wrong: an upgrade
    # run must bank EXACTLY ONE dist — the pre-upgrade one, under the OLD
    # version's name, byte-equal to the old vendored file.
    root, config, backend = _adopted(tmp_path)
    old = _fake_old_dist(root)
    old_text = old.read_text(encoding="utf-8")
    running = _fake_new_dist(tmp_path)
    config.kit_version = "0.9.0"
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    backup = root / config.state_dir / BACKUP_DIRNAME
    banked = sorted(p.name for p in backup.glob("bootstrap-*.py"))
    assert banked == ["bootstrap-0.9.0.py"]
    assert (backup / "bootstrap-0.9.0.py").read_text(encoding="utf-8") == old_text
    assert not (backup / f"bootstrap-{KIT_VERSION}.py").exists()


def test_upgrade_gate_regen_surfaces_carveouts_in_the_report(tmp_path):
    # The superbot-games #16 class: the repo's ONLY pytest CI job was
    # hand-added INSIDE the kit-owned substrate-gate.yml; a plain regen
    # would have silently deleted the repo's whole test gate. Upgrade must
    # (1) still regenerate the gate to kit form (kit-owned), (2) report the
    # host additions as carve-outs in upgrade-report.md, and (3) bank the
    # full pre-regen copy — never a silent drop.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _adopted(tmp_path)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    hand_edited = live_ci_workflow() + (
        "  pytest:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: host test suite\n"
        "        run: python3 -m pytest tests/ -q\n"
    )
    gate.write_text(hand_edited, encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert gate.read_text(encoding="utf-8") == live_ci_workflow()
    assert any("host-added job 'pytest'" in line for line in lines)
    banked = list(
        (root / config.state_dir / BACKUP_DIRNAME).glob(
            "substrate-gate.pre-regen-*.yml",
        )
    )
    assert len(banked) == 1
    assert banked[0].read_text(encoding="utf-8") == hand_edited
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Gate carve-outs" in report_text
    assert "host-added job 'pytest'" in report_text


def test_upgrade_pristine_gate_regen_stays_clean(tmp_path):
    # The other half of the carve-out contract: a pristine (already-current)
    # gate is kept, with NO carve-out warnings, NO banked pre-regen copy,
    # and NO carve-out section in the report.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _adopted(tmp_path)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text(live_ci_workflow(), encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert gate.read_text(encoding="utf-8") == live_ci_workflow()
    assert not any(line.startswith("carve-out:") for line in lines)
    assert not list(
        (root / config.state_dir / BACKUP_DIRNAME).glob(
            "substrate-gate.pre-regen-*.yml",
        )
    )
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Gate carve-outs" not in report_text


def test_upgrade_pin_bump_only_gate_reports_no_phantom_carveouts(tmp_path):
    # The v1.11.0-wave false positive end-to-end through the upgrade flow:
    # the live gate is byte-identical to the OLD template (recovered from
    # the pre-upgrade staged copy under <state_dir>/ci/), and the new
    # release only bumped a kit-side action pin — the upgrade report must
    # carry NO carve-out section, and nothing is banked.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _adopted(tmp_path)
    old_template = live_ci_workflow().replace(
        "uses: actions/checkout@v5",
        "uses: actions/checkout@v4",
    )
    assert old_template != live_ci_workflow()
    # Rewind the staged copy to what the OLD kit shipped (adopt in _adopted
    # staged the current render).
    staged = root / config.state_dir / "ci" / "substrate-gate.yml"
    staged.write_text(old_template, encoding="utf-8")
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text(old_template, encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert gate.read_text(encoding="utf-8") == live_ci_workflow()
    assert not any(line.startswith("carve-out:") for line in lines)
    assert not list(
        (root / config.state_dir / BACKUP_DIRNAME).glob(
            "substrate-gate.pre-regen-*.yml",
        )
    )
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Gate carve-outs" not in report_text
    assert (
        f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found (live matched "
        "the previous kit template byte-for-byte; the delta is kit-side "
        "template evolution)" in report_text
    )


def test_upgrade_enabler_regen_surfaces_carveouts_in_the_report(tmp_path):
    # EAP §6.10: the auto-merge enabler is kit-owned via the SAME mechanism
    # as the gate — an upgrade regenerates a hand-forked enabler in place,
    # reports host additions as carve-outs in upgrade-report.md, and banks
    # the full pre-regen copy.
    from engine.adopt import AUTOMERGE_ENABLER_RELPATH, automerge_enabler_workflow

    root, config, backend = _adopted(tmp_path)
    enabler = root / AUTOMERGE_ENABLER_RELPATH
    enabler.parent.mkdir(parents=True)
    hand_edited = automerge_enabler_workflow() + (
        "  notify:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: host notifier\n"
        "        run: echo merged\n"
    )
    enabler.write_text(hand_edited, encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert enabler.read_text(encoding="utf-8") == automerge_enabler_workflow()
    assert any("host-added job 'notify'" in line for line in lines)
    banked = list(
        (root / config.state_dir / BACKUP_DIRNAME).glob(
            "auto-merge-enabler.pre-regen-*.yml",
        )
    )
    assert len(banked) == 1
    assert banked[0].read_text(encoding="utf-8") == hand_edited
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Gate carve-outs" in report_text


def test_upgrade_sweep_regen_surfaces_carveouts_in_the_report(tmp_path):
    # ORDER 023: the scheduled branch sweep is kit-owned via the SAME
    # mechanism as the gate and the enabler — an upgrade regenerates a
    # hand-forked sweep in place, reports host additions as carve-outs in
    # upgrade-report.md, and banks the full pre-regen copy.
    from engine.adopt import BRANCH_SWEEP_RELPATH, branch_sweep_workflow

    root, config, backend = _adopted(tmp_path)
    sweep = root / BRANCH_SWEEP_RELPATH
    sweep.parent.mkdir(parents=True)
    hand_edited = branch_sweep_workflow() + (
        "  notify:\n"
        "    runs-on: ubuntu-latest\n"
        "    steps:\n"
        "      - name: host notifier\n"
        "        run: echo swept\n"
    )
    sweep.write_text(hand_edited, encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert sweep.read_text(encoding="utf-8") == branch_sweep_workflow()
    assert any("host-added job 'notify'" in line for line in lines)
    banked = list(
        (root / config.state_dir / BACKUP_DIRNAME).glob(
            "branch-sweep.pre-regen-*.yml",
        )
    )
    assert len(banked) == 1
    assert banked[0].read_text(encoding="utf-8") == hand_edited
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Gate carve-outs" in report_text
    assert "host-added job 'notify'" in report_text


def test_improved_note_names_the_posthoc_recovery_path(tmp_path, monkeypatch):
    # The apply window is single-shot (idea
    # upgrade-apply-docs-single-shot-window): after the transition a bare
    # re-run parses the already-new vendored templates and finds nothing. Now
    # that the full post-hoc mechanism exists, the skipped-apply note must name
    # THAT working recovery (`upgrade --apply-docs` applies post-hoc from the
    # banked archive, no rollback) — never the interim rollback dance and never
    # a bare "re-run with --apply-docs to take them" no-op.
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root, {"architecture.md.tmpl": "old ${project_name}"})
    running = _fake_new_dist(tmp_path)
    # Make the NEW architecture template improve on the planted (untouched)
    # doc so classify yields a template-improved row and the note fires.
    improved = dict(load_templates())
    improved["architecture.md.tmpl"] += "\nNew guidance paragraph.\n"
    monkeypatch.setattr("engine.upgrade.load_templates", lambda: improved)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
        apply_docs=False,
    )
    note = next(line for line in lines if "template improvements you" in line)
    assert "post-hoc" in note
    assert "--rollback" not in note  # the interim recovery is gone
    assert "re-run with --apply-docs to take them" not in note


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
# Post-hoc --apply-docs: recover the single-shot window from the banked archive
# (idea upgrade-apply-docs-single-shot-window — the full mechanism)
# ---------------------------------------------------------------------------


def _skipped_apply_upgrade(tmp_path, monkeypatch, *, extra_improved=()):
    """Drive an in-run upgrade that SKIPS --apply-docs, leaving the window
    closed: the vendored dist is now the new one, the pre-upgrade dist is
    banked, and the template-improved docs are still their old render on disk.
    Returns (root, config, backend) ready for a post-hoc apply."""
    root, config, backend = _adopted(tmp_path)
    # The banked OLD dist carries exactly the templates that planted the docs,
    # so post-hoc old_templates == what is on disk (untouched kit-form).
    _fake_old_dist(root, dict(load_templates()))
    config.kit_version = "0.9.0"
    running = _fake_new_dist(tmp_path)
    # The NEW kit templates improve one (or more) untouched planted docs.
    improved = dict(load_templates())
    improved["architecture.md.tmpl"] += "\nNew guidance paragraph.\n"
    for name in extra_improved:
        improved[name] += "\nNew guidance paragraph.\n"
    monkeypatch.setattr("engine.upgrade.load_templates", lambda: improved)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
        apply_docs=False,
    )
    # The window is closed: vendored is the new dist, the improvement unapplied.
    vendored = root / "bootstrap.py"
    assert dist_version(vendored.read_text(encoding="utf-8")) == KIT_VERSION
    arch = root / "docs" / "architecture.md"
    assert "New guidance paragraph." not in arch.read_text(encoding="utf-8")
    return root, config, backend


def test_newest_banked_archive_names_the_last_upgrades_dist(tmp_path, monkeypatch):
    root, config, backend = _skipped_apply_upgrade(tmp_path, monkeypatch)
    archived, from_version = newest_banked_archive(root, config)
    assert archived is not None
    assert archived.name == "bootstrap-0.9.0.py"
    assert from_version == "0.9.0"


def test_posthoc_apply_recovers_a_skipped_improvement(tmp_path, monkeypatch):
    # The done-when: an operator who skipped --apply-docs on the upgrade recovers
    # the same planted-doc coverage a rollback + re-run would — WITHOUT rollback.
    root, config, backend = _skipped_apply_upgrade(tmp_path, monkeypatch)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=root / "bootstrap.py",  # the now-new vendored file
        apply_docs=True,
    )
    arch = root / "docs" / "architecture.md"
    assert "New guidance paragraph." in arch.read_text(encoding="utf-8")
    assert any("applied: docs/architecture.md" in line for line in lines)
    # The applied doc is untouched kit-form again (hash re-recorded).
    assert doc_is_untouched(
        backend,
        "docs/architecture.md",
        arch.read_text(encoding="utf-8"),
    )
    # A report was written naming the recovered transition.
    report = root / config.state_dir / "upgrade-report.md"
    assert report.is_file()
    assert f"v0.9.0 → v{KIT_VERSION}" in report.read_text(encoding="utf-8")


def test_posthoc_apply_without_a_banked_archive_reports_cleanly(tmp_path):
    # No upgrade has banked anything yet: post-hoc --apply-docs must not crash
    # and must not recommend an impossible command — just say what is missing.
    root, config, backend = _adopted(tmp_path)
    vendored = root / "bootstrap.py"
    vendored.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED."""\n',
        encoding="utf-8",
    )
    arch = root / "docs" / "architecture.md"
    before = arch.read_text(encoding="utf-8")
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=vendored,
        apply_docs=True,
    )
    assert any("no banked pre-upgrade dist" in line for line in lines)
    assert not any("--rollback" in line for line in lines)
    # Nothing was written to any doc.
    assert arch.read_text(encoding="utf-8") == before


def test_posthoc_apply_leaves_a_consumer_edited_doc_diverged(tmp_path, monkeypatch):
    # A doc the consumer edited after the window closed stays consumer-owned:
    # post-hoc apply touches only the untouched improved class.
    root, config, backend = _skipped_apply_upgrade(
        tmp_path,
        monkeypatch,
        extra_improved=("ownership.md.tmpl",),
    )
    arch = root / "docs" / "architecture.md"
    consumer_text = arch.read_text(encoding="utf-8") + "\nconsumer note\n"
    arch.write_text(consumer_text, encoding="utf-8")
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=root / "bootstrap.py",
        apply_docs=True,
    )
    # The consumer-edited doc is untouched by apply…
    assert arch.read_text(encoding="utf-8") == consumer_text
    # …but the still-untouched improved doc took the improvement.
    own = root / "docs" / "ownership.md"
    assert "New guidance paragraph." in own.read_text(encoding="utf-8")


def test_posthoc_apply_is_idempotent(tmp_path, monkeypatch):
    root, config, backend = _skipped_apply_upgrade(tmp_path, monkeypatch)
    first = run_apply_docs_posthoc(root, config, backend)
    assert any("applied: docs/architecture.md" in line for line in first)
    # A second post-hoc apply finds everything already current — nothing written.
    second = run_apply_docs_posthoc(root, config, backend)
    assert not any(line.startswith("applied:") for line in second)
    assert any("no template-improved docs to apply" in line for line in second)


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

# ---------------------------------------------------------------------------
# KL-4 field fixes (superbot-next#46): from-version truth + input cleanup
# ---------------------------------------------------------------------------


def test_pin_before_upgrade_reports_unknown_not_the_pin(tmp_path):
    """The exact field scenario: kit_version pinned in config BEFORE the first
    real upgrade (the D2 order), while the vendored file is an unstamped
    pre-release bootstrap. from_version must agree with the archive
    (bootstrap-unknown.py), not echo the aspirational pin."""
    root, config, backend = _adopted(tmp_path)
    old = root / "bootstrap.py"
    old.write_text(
        '"""hand-written pre-release bootstrap — no version stamp."""\n',
        encoding="utf-8",
    )
    config.kit_version = KIT_VERSION  # the D2 pin, recorded ahead of the fact
    running = _fake_new_dist(tmp_path)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    backup = root / config.state_dir / BACKUP_DIRNAME
    assert (backup / "bootstrap-unknown.py").is_file()
    meta = json.loads((backup / "last-upgrade.json").read_text(encoding="utf-8"))
    assert meta["from_version"] == "unknown"  # was: the pin ("1.0.0")
    # Rollback restores the honest unrecorded sentinel, never "unknown"/"1.0.0".
    run_rollback(root, load_config(root))
    assert load_config(root).kit_version == ""


def test_header_outranks_a_disagreeing_config_pin(tmp_path):
    """A stamped old dist whose header disagrees with the pin: the header
    states what is actually installed and wins."""
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)  # header says v0.9.0
    config.kit_version = "0.8.0"  # a stale/wrong pin
    running = _fake_new_dist(tmp_path)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    backup = root / config.state_dir / BACKUP_DIRNAME
    meta = json.loads((backup / "last-upgrade.json").read_text(encoding="utf-8"))
    assert meta["from_version"] == "0.9.0"
    assert (backup / "bootstrap-0.9.0.py").is_file()


def test_hand_copied_new_dist_still_trusts_the_pin(tmp_path):
    """The one header that cannot name the true "from" is KIT_VERSION itself —
    the consumer hand-copied the new file over the old one — so the recorded
    pin wins there (the pre-fix behavior, preserved)."""
    root, config, backend = _adopted(tmp_path)
    old = root / "bootstrap.py"
    old.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED."""\n',
        encoding="utf-8",
    )
    config.kit_version = "0.9.0"  # what the old adopt recorded
    running = _fake_new_dist(tmp_path)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    backup = root / config.state_dir / BACKUP_DIRNAME
    meta = json.loads((backup / "last-upgrade.json").read_text(encoding="utf-8"))
    assert meta["from_version"] == "0.9.0"


def test_cleanup_also_removes_the_adjacent_release_json(tmp_path):
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    digest = hashlib.sha256(running.read_bytes()).hexdigest()
    rj = tmp_path / "release.json"
    _write_release_json(rj, sha256=digest)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert not running.exists()
    assert not rj.exists()
    assert any("cleaned up: release.json" in line for line in lines)


def test_keep_inputs_opts_out_of_cleanup(tmp_path):
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
        cleanup_inputs=False,
    )
    assert running.is_file()
    assert not any("cleaned up" in line for line in lines)


def test_no_cleanup_when_nothing_was_replaced(tmp_path):
    """Consumer #0 shape: the running file IS the vendored file — the flow
    must never delete the install's own bootstrap."""
    root, config, backend = _adopted(tmp_path)
    vendored = _fake_old_dist(root)
    vendored.write_text(
        f'"""substrate-kit bootstrap v{KIT_VERSION} — GENERATED."""\n',
        encoding="utf-8",
    )
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=vendored,
    )
    assert vendored.is_file()
    assert not any("cleaned up" in line for line in lines)


# ---------------------------------------------------------------------------
# Kit-owned live gate regeneration on upgrade (EAP program review §6.1)
# ---------------------------------------------------------------------------


def test_upgrade_regenerates_a_stale_live_gate(tmp_path):
    # The whole point of declaring the gate kit-owned: an adopter carrying a
    # stale or hand-forked substrate-gate.yml (gba-homebrew's live-fire fix
    # was exactly this) gets the current template on `bootstrap.py upgrade` —
    # no hand-porting of gate patches ever again.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _adopted(tmp_path)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text("# stale hand-forked gate\nname: substrate-gate\n", encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert gate.read_text(encoding="utf-8") == live_ci_workflow()
    assert any(
        line.startswith(f"regenerated: {LIVE_CI_RELPATH}") for line in lines
    )


def test_upgrade_never_creates_a_live_gate_that_was_not_installed(tmp_path):
    # The safety doctrine survives the kit-owned declaration: an install that
    # never wired enforcement has no live gate, and upgrade must not sneak
    # one in — existence is the opt-in signal, absence stays respected.
    from engine.adopt import LIVE_CI_RELPATH

    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert not (root / LIVE_CI_RELPATH).exists()


def test_upgrade_report_states_clean_carveout_scan_explicitly(tmp_path):
    # Queued fix 1 (fleet-manager #40 finding): a clean scan was SILENT in
    # upgrade-report.md — indistinguishable from "the detector never ran".
    # A pristine kit-owned gate now yields an explicit scan section naming
    # the file scanned with 0 found.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _adopted(tmp_path)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text(live_ci_workflow(), encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in lines
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "## Carve-out scan" in report_text
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in report_text
    assert "Gate carve-outs" not in report_text


def test_carveout_scan_honors_the_confirmed_verify_command(tmp_path):
    # The #403 follow-on's writer/scanner symmetry: an installed gate whose
    # test step runs the CONFIRMED verify_command must scan clean — without
    # gate_test_command in the rescan's expectation, kit-owned verify-step
    # bytes would misreport as a host carve-out (and the regen would flap
    # between the two forms).
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    command = "python3 -m pytest tests/ -q && python3 bootstrap.py check --strict"
    root, config, backend = _adopted(tmp_path)
    with backend.transaction():
        slots = dict(backend.get("slots", {}))
        slots["verify_command"] = "filled"
        backend.set("slots", slots)
        values = dict(backend.get("slot_values", {}))
        values["verify_command"] = {"value": command, "source": "user"}
        backend.set("slot_values", values)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text(live_ci_workflow(test_command=command), encoding="utf-8")
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in lines
    assert not any(line.startswith("carve-out: ") for line in lines)
    # The regen keeps the verify-command form (adopt reads the same state).
    text = gate.read_text(encoding="utf-8")
    assert "- name: verify suite" in text
    assert f"          {command}\n" in text


def test_scan_gate_carveouts_reads_the_verify_command_slot(tmp_path):
    # The post-hoc --apply-docs rescan is read-only (no adopt pass, no
    # backend in scope): it must load state.json itself and expect the same
    # verify-command gate the writer produced, or a clean kit-owned gate
    # would rescan as a phantom carve-out.
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow
    from engine.upgrade import scan_gate_carveouts

    command = "python3 -m pytest -q; python3 bootstrap.py check --strict"
    root, config, backend = _adopted(tmp_path)
    with backend.transaction():
        slots = dict(backend.get("slots", {}))
        slots["verify_command"] = "filled"
        backend.set("slots", slots)
        values = dict(backend.get("slot_values", {}))
        values["verify_command"] = {"value": command, "source": "user"}
        backend.set("slot_values", values)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True)
    gate.write_text(live_ci_workflow(test_command=command), encoding="utf-8")
    lines = scan_gate_carveouts(root, config)
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in lines
    assert not any(line.startswith("carve-out: ") for line in lines)


def test_upgrade_report_names_nothing_to_scan_when_no_live_workflow(tmp_path):
    # No kit-owned live workflow installed → the report still states scan
    # status: ran, nothing to scan (absence of the section would read as
    # "never ran").
    root, config, backend = _adopted(tmp_path)
    _fake_old_dist(root)
    running = _fake_new_dist(tmp_path)
    run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "## Carve-out scan" in report_text
    assert "no kit-owned live workflow installed, nothing to scan" in report_text


# ---------------------------------------------------------------------------
# Post-hoc --apply-docs keeps the carve-out section (websites, v1.9.0 wave:
# the report rewrite passed carveouts=None and DROPPED the section — it had
# to be hand-restored)
# ---------------------------------------------------------------------------


def test_posthoc_apply_report_reemits_the_carveout_section(tmp_path, monkeypatch):
    from engine.adopt import LIVE_CI_RELPATH, live_ci_workflow

    root, config, backend = _skipped_apply_upgrade(tmp_path, monkeypatch)
    gate = root / LIVE_CI_RELPATH
    gate.parent.mkdir(parents=True, exist_ok=True)
    gate.write_text(
        live_ci_workflow(
            config.interpreter_for_checks or "python3",
            sessions_dir=config.sessions_dir,
        ),
        encoding="utf-8",
    )
    run_apply_docs_posthoc(root, config, backend)
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    # The rewrite carries an honest carve-out section again: the read-only
    # rescan ran and states its clean result explicitly.
    assert "## Carve-out scan" in report_text
    assert f"carve-out scan: {LIVE_CI_RELPATH} — ran, 0 found" in report_text


def test_posthoc_apply_report_carries_prior_carveout_hits(tmp_path, monkeypatch):
    from engine.upgrade import CARRIED_CARVEOUT_SUFFIX

    root, config, backend = _skipped_apply_upgrade(tmp_path, monkeypatch)
    report_path = root / config.state_dir / "upgrade-report.md"
    report_path.write_text(
        "# substrate-kit upgrade report — v0.9.0 → vX\n\n"
        "## ⚠️ Gate carve-outs (host additions the kit-owned regen "
        "could not keep)\n\n"
        "- carve-out: .github/workflows/substrate-gate.yml — host-added "
        "job 'pytest' (run tests)\n",
        encoding="utf-8",
    )
    run_apply_docs_posthoc(root, config, backend)
    report_text = report_path.read_text(encoding="utf-8")
    # The historical detection survives the rewrite, marked as carried —
    # post-regen the live file matches the template again, so the rescan
    # alone would have erased the hit the host may still need to act on.
    assert "host-added job 'pytest'" in report_text
    assert CARRIED_CARVEOUT_SUFFIX in report_text
    assert "Gate carve-outs" in report_text
    # Idempotent: a second post-hoc rewrite never stacks suffixes or
    # duplicates the hit.
    run_apply_docs_posthoc(root, config, backend)
    report_text = report_path.read_text(encoding="utf-8")
    assert report_text.count("host-added job 'pytest'") == 1
    assert report_text.count(CARRIED_CARVEOUT_SUFFIX) == 1


# ---------------------------------------------------------------------------
# Retroactive model doctrine (v1.9.0 wave: the PR #170 render was
# fresh-plant-only; 4 adopters needed manual regen/hand-merge)
# ---------------------------------------------------------------------------


def test_upgrade_merges_model_doctrine_into_preexisting_readme(tmp_path):
    from engine.adopt import MODEL_DOCTRINE_MARKER

    root, config, backend = _adopted(tmp_path)
    # Simulate a pre-doctrine planted README (skip-if-exists keeps it).
    readme = root / config.sessions_dir / "README.md"
    old_text = "# Session logs\n\nOld planted README without the doctrine.\n"
    readme.write_text(old_text, encoding="utf-8")
    # Pre-KL-3 install: markers lack the Model line; the upgrade adds the
    # needle at step 6b and must merge the doctrine in the SAME run (the
    # adopt pass in step 6 ran before the needle existed).
    config.session_markers = [
        m for m in config.session_markers if m.get("label") != "Model line"
    ]
    _fake_old_dist(root, {"architecture.md.tmpl": "old ${project_name}"})
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    text = readme.read_text(encoding="utf-8")
    # Host content preserved byte-for-byte; doctrine appended under the
    # provenance marker (the search-hygiene plant pattern).
    assert text.startswith(old_text)
    assert MODEL_DOCTRINE_MARKER in text
    assert "family-level model name your own harness/environment reports" in text
    assert any("model-attribution doctrine appended" in line for line in lines)
    # Idempotent: a re-run appends nothing (the detection phrase is present).
    lines = run_upgrade(
        root,
        load_config(root),
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert readme.read_text(encoding="utf-8") == text
    assert not any("model-attribution doctrine appended" in line for line in lines)


def test_fresh_plant_readme_needs_no_doctrine_merge(tmp_path):
    from engine.adopt import MODEL_DOCTRINE_MARKER

    # A fresh v1.9.0+ plant renders the doctrine inline — the retroactive
    # merge must recognise it as present (shared detection phrase) and
    # never double-append.
    root, config, backend = _adopted(tmp_path)
    readme = root / config.sessions_dir / "README.md"
    text = readme.read_text(encoding="utf-8")
    assert (
        text.count("family-level model name your own harness/environment reports")
        == 1
    )
    assert MODEL_DOCTRINE_MARKER not in text
    lines = adopt(root, config, backend, kit_root=tmp_path / "kit")
    assert readme.read_text(encoding="utf-8") == text
    assert not any("model-attribution doctrine appended" in line for line in lines)


def test_doctrine_merge_noop_when_markers_lack_the_needle(tmp_path):
    from engine.adopt import _merge_model_doctrine

    root, config, backend = _adopted(tmp_path)
    readme = root / config.sessions_dir / "README.md"
    old_text = "# Session logs\n\nno doctrine, and no Model needle either\n"
    readme.write_text(old_text, encoding="utf-8")
    config.session_markers = [
        m for m in config.session_markers if m.get("label") != "Model line"
    ]
    report: list[str] = []
    _merge_model_doctrine(root, config, report)
    # Doctrine without the needle would be noise — nothing written.
    assert readme.read_text(encoding="utf-8") == old_text
    assert report == []


def test_doctrine_merge_detects_emphasis_variant_phrase(tmp_path):
    # The v1.10.0-wave defect (websites #105): a hand-merged doctrine carried
    # Markdown emphasis INSIDE the detection phrase, the exact-substring test
    # missed it, and a harmless near-duplicate paragraph was appended. The
    # presence check is now emphasis-blind (strip * _ ` + collapse
    # whitespace) — an emphasis-variant existing phrase means NO append.
    from engine.adopt import MODEL_DOCTRINE_MARKER, _merge_model_doctrine

    root, config, backend = _adopted(tmp_path)
    readme = root / config.sessions_dir / "README.md"
    # The exact websites shape: emphasis opens mid-phrase.
    starred = (
        "# Session logs\n\nThe model segment is the family-level model name "
        "**your own harness/environment reports this session** — hand-merged "
        "pre-retroactively.\n"
    )
    readme.write_text(starred, encoding="utf-8")
    report: list[str] = []
    _merge_model_doctrine(root, config, report)
    assert readme.read_text(encoding="utf-8") == starred
    assert MODEL_DOCTRINE_MARKER not in starred
    assert report == []
    # Underscore emphasis + a reflowed line break inside the phrase — still
    # the same doctrine, still no duplicate append.
    underscored = (
        "# Session logs\n\nUse the _family-level model name_ your own\n"
        "harness/environment reports for the card's model segment.\n"
    )
    readme.write_text(underscored, encoding="utf-8")
    report = []
    _merge_model_doctrine(root, config, report)
    assert readme.read_text(encoding="utf-8") == underscored
    assert report == []


# ---------------------------------------------------------------------------
# Grounded-skills slice 5 (§4.2c): the capability-ledger fenced-seed refresh
# ---------------------------------------------------------------------------

from engine import grammar  # noqa: E402  (slice-5 block import, kept local)
from engine.upgrade import (  # noqa: E402
    CAPABILITY_POSTURE_COLLAPSE_NOTE,
    _capability_fence,
    _render_planted,
    _upgrade_context,
    refresh_capability_seed,
)

_LEDGER_REL = "docs/CAPABILITIES.md"

# A pre-slice-5 (fence-less) CAPABILITIES template, shaped like the shipped
# v1.13.0 one: seed region = discovery rule + Capabilities/Walls, no markers.
_LEGACY_CAPABILITIES_TMPL = """# ${project_name} — session capabilities & walls

> **Status:** `living-ledger`

## Why this file exists

This ledger makes capability knowledge durable across sessions.

## THE DISCOVERY RULE

1. **Check this file** — the capability or wall may already be recorded.
2. **Attempt once** — capture the exact error text.

## Capabilities — verified working

- **Release cutting despite the tag wall**: workflow_dispatch creates the tag.

## Walls — verified blocked (use the workaround; don't rediscover)

- **Tag push / release create via git**: HTTP 403 — use workflow_dispatch.

## Append log — newest first

Format: `- YYYY-MM-DD · capability|wall · finding · evidence · workaround`.

(Hand-filled by sessions, per the discovery rule.)
"""


def _seed_variant(extra_row: str) -> dict[str, str]:
    """Return a template set whose CAPABILITIES fence carries ``extra_row``."""
    templates = dict(load_templates())
    templates["CAPABILITIES.md.tmpl"] = templates["CAPABILITIES.md.tmpl"].replace(
        grammar.CAPABILITY_SEED_END,
        extra_row + "\n\n" + grammar.CAPABILITY_SEED_END,
    )
    return templates


_NEW_SEED_ROW = (
    "- `any` · **New fleet-wide seed row**: proven at the next wave. "
    "— LAST-VERIFIED: 2026-08-01"
)


def test_capability_seed_refreshes_fence_and_preserves_consumer_text(tmp_path):
    # The §7.5 accept criterion: upgrade on a consumer-edited ledger
    # refreshes ONLY the fenced seed block; the append log + all consumer
    # text survive byte-for-byte.
    root, config, backend = _adopted(tmp_path)
    ledger = root / _LEDGER_REL
    appended = grammar.capability_log_line_example()
    before = ledger.read_text(encoding="utf-8") + appended
    ledger.write_text(before, encoding="utf-8")
    old_templates = dict(load_templates())
    new_templates = _seed_variant(_NEW_SEED_ROW)
    rows = classify_planted_docs(root, config, backend, old_templates, new_templates)
    row = next(r for r in rows if r["relpath"] == _LEDGER_REL)
    assert row["class"] == CLASS_DIVERGED  # consumer appended + template moved
    lines = refresh_capability_seed(
        root, config, backend, rows, old_templates, new_templates
    )
    assert any("refreshed the kit-owned fenced seed block" in ln for ln in lines)
    after = ledger.read_text(encoding="utf-8")
    assert "New fleet-wide seed row" in after
    assert appended in after  # the consumer append survives
    # Byte-for-byte preservation outside the fence.
    fence_before = _capability_fence(before)
    fence_after = _capability_fence(after)
    assert fence_before is not None and fence_after is not None
    assert before.replace(fence_before, "", 1) == after.replace(fence_after, "", 1)
    # The file stays consumer-owned: no hash was re-recorded.
    assert not doc_is_untouched(backend, _LEDGER_REL, after)


def test_capability_seed_modified_fence_downgrades_to_report_line(tmp_path):
    # The covenant's other half: a consumer edit INSIDE the fence is never
    # clobbered — the refresh downgrades to an instruction line.
    root, config, backend = _adopted(tmp_path)
    ledger = root / _LEDGER_REL
    edited = ledger.read_text(encoding="utf-8").replace(
        "Media is readable", "Media is unreadable here"
    )
    assert "Media is unreadable here" in edited
    ledger.write_text(edited, encoding="utf-8")
    old_templates = dict(load_templates())
    new_templates = _seed_variant(_NEW_SEED_ROW)
    rows = classify_planted_docs(root, config, backend, old_templates, new_templates)
    lines = refresh_capability_seed(
        root, config, backend, rows, old_templates, new_templates
    )
    assert any("NOT refreshed" in ln for ln in lines)
    assert ledger.read_text(encoding="utf-8") == edited  # nothing written
    assert "New fleet-wide seed row" not in edited


def test_capability_seed_adopts_fence_on_pre_fence_ledger(tmp_path):
    # Transition case: a pre-slice-5 ledger has no markers. When its kit
    # seed region still matches the OLD template verbatim (the designed
    # append-only edit pattern), the fence is adopted automatically.
    root, config, backend = _adopted(tmp_path)
    old_templates = dict(load_templates())
    old_templates["CAPABILITIES.md.tmpl"] = _LEGACY_CAPABILITIES_TMPL
    context = _upgrade_context(root, backend)
    legacy_render = _render_planted(
        _LEGACY_CAPABILITIES_TMPL, "CAPABILITIES.md.tmpl", context
    )
    appended = grammar.capability_log_line_example(venue=None)  # legacy form
    ledger = root / _LEDGER_REL
    ledger.write_text(legacy_render + appended, encoding="utf-8")
    rows = classify_planted_docs(root, config, backend, old_templates)
    lines = refresh_capability_seed(root, config, backend, rows, old_templates)
    assert any("adopted the marker fence" in ln for ln in lines)
    after = ledger.read_text(encoding="utf-8")
    assert grammar.CAPABILITY_SEED_BEGIN in after
    assert grammar.CAPABILITY_SEED_END in after
    assert appended in after  # the consumer append survives
    headings = [ln for ln in after.splitlines() if ln.startswith("## Append log")]
    assert len(headings) == 1  # one heading (the fence warning names it mid-line)
    assert "workflow_dispatch creates the tag" not in after  # old seed replaced


def test_capability_seed_pre_fence_ledger_with_edited_seed_downgrades(tmp_path):
    # A fence-less ledger whose seed region no longer matches the old
    # template cannot be auto-adopted — report line, nothing written.
    root, config, backend = _adopted(tmp_path)
    old_templates = dict(load_templates())
    old_templates["CAPABILITIES.md.tmpl"] = _LEGACY_CAPABILITIES_TMPL
    context = _upgrade_context(root, backend)
    legacy_render = _render_planted(
        _LEGACY_CAPABILITIES_TMPL, "CAPABILITIES.md.tmpl", context
    )
    edited = legacy_render.replace("HTTP 403", "HTTP 403 (site note)")
    ledger = root / _LEDGER_REL
    ledger.write_text(edited, encoding="utf-8")
    rows = classify_planted_docs(root, config, backend, old_templates)
    lines = refresh_capability_seed(root, config, backend, rows, old_templates)
    assert any("hand-adopt once" in ln for ln in lines)
    assert ledger.read_text(encoding="utf-8") == edited


def test_capability_seed_already_current_fence_is_a_noop(tmp_path):
    # Consumer appended below the fence, template unchanged: the fence is
    # already at kit form — nothing to write, an honest "already current".
    root, config, backend = _adopted(tmp_path)
    ledger = root / _LEDGER_REL
    text = ledger.read_text(encoding="utf-8") + grammar.capability_log_line_example()
    ledger.write_text(text, encoding="utf-8")
    old_templates = dict(load_templates())
    rows = classify_planted_docs(root, config, backend, old_templates)
    row = next(r for r in rows if r["relpath"] == _LEDGER_REL)
    assert row["class"] == CLASS_CONSUMER_EDITED
    lines = refresh_capability_seed(root, config, backend, rows, old_templates)
    assert any("already current" in ln for ln in lines)
    assert ledger.read_text(encoding="utf-8") == text


def test_capability_seed_untouched_ledger_points_at_apply_docs(tmp_path):
    # A consumer-untouched improved ledger is the --apply-docs channel's job;
    # the fence step only leaves the pointer line.
    root, config, backend = _adopted(tmp_path)
    old_templates = dict(load_templates())
    new_templates = _seed_variant(_NEW_SEED_ROW)
    rows = classify_planted_docs(root, config, backend, old_templates, new_templates)
    row = next(r for r in rows if r["relpath"] == _LEDGER_REL)
    assert row["class"] == CLASS_IMPROVED
    before = (root / _LEDGER_REL).read_text(encoding="utf-8")
    lines = refresh_capability_seed(
        root, config, backend, rows, old_templates, new_templates
    )
    assert any("--apply-docs" in ln for ln in lines)
    assert (root / _LEDGER_REL).read_text(encoding="utf-8") == before


def test_run_upgrade_refreshes_seed_and_reports_q0270_collapse(tmp_path):
    # End-to-end through run_upgrade: the doc on disk is the OLD render
    # (fence at old form) + a consumer append; the running engine's template
    # is newer inside the fence. The upgrade refreshes the fence and the
    # report carries the seed section + the Q-0270 collapse wording.
    root, config, backend = _adopted(tmp_path)
    current = load_templates()["CAPABILITIES.md.tmpl"]
    old_capabilities = current.replace(
        "- `any` · **GraphQL API quota**: tight — batch queries and prefer the\n"
        "  REST-backed MCP tools for bulk reads. — LAST-VERIFIED: 2026-07-10\n",
        "",
    )
    assert old_capabilities != current  # the removal really happened
    old_templates = dict(load_templates())
    old_templates["CAPABILITIES.md.tmpl"] = old_capabilities
    context = _upgrade_context(root, backend)
    old_render = _render_planted(old_capabilities, "CAPABILITIES.md.tmpl", context)
    appended = grammar.capability_log_line_example()
    ledger = root / _LEDGER_REL
    ledger.write_text(old_render + appended, encoding="utf-8")
    _fake_old_dist(root, old_templates)
    running = _fake_new_dist(tmp_path)
    lines = run_upgrade(
        root,
        config,
        backend,
        kit_root=tmp_path / "kit",
        running=running,
    )
    assert any("refreshed the kit-owned fenced seed block" in ln for ln in lines)
    after = ledger.read_text(encoding="utf-8")
    assert "GraphQL API quota" in after  # the new seed row arrived
    assert appended in after
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Capability-ledger seed refresh" in report_text
    assert CAPABILITY_POSTURE_COLLAPSE_NOTE in report_text
    assert "superseded by docs/CAPABILITIES.md's posture rule" in report_text


def test_posthoc_apply_docs_mirrors_the_seed_refresh(tmp_path):
    # The decide-and-flag mirror: a same-version `upgrade --apply-docs`
    # (post-hoc, from the banked archive) also refreshes the fence, and its
    # report rewrite carries the seed section.
    root, config, backend = _adopted(tmp_path)
    current = load_templates()["CAPABILITIES.md.tmpl"]
    old_capabilities = current.replace(
        "- `any` · **GraphQL API quota**: tight — batch queries and prefer the\n"
        "  REST-backed MCP tools for bulk reads. — LAST-VERIFIED: 2026-07-10\n",
        "",
    )
    old_templates = dict(load_templates())
    old_templates["CAPABILITIES.md.tmpl"] = old_capabilities
    context = _upgrade_context(root, backend)
    old_render = _render_planted(old_capabilities, "CAPABILITIES.md.tmpl", context)
    appended = grammar.capability_log_line_example()
    ledger = root / _LEDGER_REL
    ledger.write_text(old_render + appended, encoding="utf-8")
    # Bank the old dist the way an upgrade would have (archive-first), with
    # the vendored file already AT the running version (the post-hoc state).
    backup = root / config.state_dir / BACKUP_DIRNAME
    backup.mkdir(parents=True, exist_ok=True)
    archived = backup / "bootstrap-0.9.0.py"
    archived.write_text(
        _OLD_DIST_HEADER + f"\n_TEMPLATES = {old_templates!r}\n",
        encoding="utf-8",
    )
    (backup / "last-upgrade.json").write_text(
        json.dumps(
            {
                "from_version": "0.9.0",
                "to_version": KIT_VERSION,
                "archived_dist": str(archived.relative_to(root)),
                "vendored": "bootstrap.py",
            },
        ),
        encoding="utf-8",
    )
    lines = run_apply_docs_posthoc(root, config, backend)
    assert any("refreshed the kit-owned fenced seed block" in ln for ln in lines)
    after = ledger.read_text(encoding="utf-8")
    assert "GraphQL API quota" in after
    assert appended in after
    report_text = (root / config.state_dir / "upgrade-report.md").read_text(
        encoding="utf-8",
    )
    assert "Capability-ledger seed refresh" in report_text
    assert CAPABILITY_POSTURE_COLLAPSE_NOTE in report_text
    # Idempotent: a re-run finds the fence already current, writes nothing.
    again = run_apply_docs_posthoc(root, config, backend)
    assert any("already current" in ln for ln in again)
    assert ledger.read_text(encoding="utf-8") == after
