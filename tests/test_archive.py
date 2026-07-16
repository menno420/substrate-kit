"""Tests for the archive-ready note drafter (archive-ready close-out plan §5 S2+S3)."""

import re
from datetime import date

import pytest

from engine.checks.check_session_log import DRAFT_FILL_TOKEN
from engine.lib.config import Config, save_config
from engine.lib.state import JsonStateBackend, default_state
from engine.loop.archive import (
    ARCHIVE_EVIDENCE_HINTS,
    ARCHIVE_TEMPLATE_NAME,
    REQUIRES_PROBE_TOKEN,
    archive_note_path,
    draft_archive_note,
    ensure_archive_draft,
    probe_slot_residue,
)
from engine.loop.handoff import DRAFT_MARKER
from engine.render import load_templates

TODAY = date.today().isoformat()
_RETRO_DIR_NAME = "retro"


def _init(root):
    config = Config()
    save_config(root, config)
    backend = JsonStateBackend(root / config.state_dir / "state.json")
    with backend.transaction():
        for key, value in default_state(config.project_id).items():
            backend.set(key, value)
    return config, backend


def _seed_evidence(root, config):
    """Plant the tree evidence the drafter harvests (plan §3)."""
    claims = root / config.claims_dir
    claims.mkdir(parents=True)
    (claims / "README.md").write_text("# claims\n", encoding="utf-8")
    (claims / "claude-live-work.md").write_text(
        "- `claude/live-work` · scope · files · 2026-07-16\n",
        encoding="utf-8",
    )
    control = root / "control"
    (control / "status.md").write_text(
        "# seat heartbeat\n"
        "updated: 2026-07-16T00:00Z\n\n"
        "\N{BLACK FLAG} P10 required-check swap\n"
        "WHAT: swap the required checks.\n\n"
        "- \N{BLACK FLAG} FOR OWNER REVIEW: failsafe discrepancy\n",
        encoding="utf-8",
    )
    (root / "CHANGELOG.md").write_text(
        "# Changelog\n\n## [Unreleased]\n\n### Added\n"
        "- archive-prep draft verb (S2).\n\n## [1.17.0] - 2026-07-14\n\n- old.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# Drafting — evidence fills what the tree proves
# ---------------------------------------------------------------------------


def test_draft_creates_note_with_evidence(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    note = archive_note_path(tmp_path, config)
    assert note.is_file()
    text = note.read_text(encoding="utf-8")
    assert DRAFT_MARKER in text
    # Title slot: date filled from evidence, chat identity stays a slot.
    assert TODAY in text.splitlines()[0]
    # Claims evidence: the live claim is named; README.md is not a claim.
    assert "`claude-live-work.md`" in text
    assert "README.md" not in text.split("Claims:")[1].split("\n")[0]
    # Heartbeat ⚑ extraction: both flag lines carried, names only.
    assert "\N{BLACK FLAG} P10 required-check swap" in text
    assert "\N{BLACK FLAG} FOR OWNER REVIEW: failsafe discrepancy" in text
    # CHANGELOG [Unreleased] park.
    assert "archive-prep draft verb (S2)." in text
    # Judgment stays with the session: unresolved slots remain.
    assert DRAFT_FILL_TOKEN in text


def test_requires_probe_and_confirmation_never_prefilled(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    text = archive_note_path(tmp_path, config).read_text(encoding="utf-8")
    # The routine-state slot survives verbatim as an unresolved REQUIRES-PROBE
    # slot — a record-shaped default is the realized failure (plan §4.2).
    assert f"{DRAFT_FILL_TOKEN} {REQUIRES_PROBE_TOKEN}" in text
    assert "list triggers/routines LIVE" in text
    # The confirmation slot is never drafted as complete.
    assert "never drafted as complete" in text
    assert "writing it IS the final check]]" in text


def test_draft_with_no_evidence_fails_soft(tmp_path):
    config, _ = _init(tmp_path)  # no claims dir, no heartbeat, no CHANGELOG
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    text = archive_note_path(tmp_path, config).read_text(encoding="utf-8")
    assert "none at draft time" in text  # claims
    assert "none open" in text  # ⚑ items
    assert "nothing parked at draft time" in text  # payload


# ---------------------------------------------------------------------------
# Re-run — report, never redraft; complete notes are never touched
# ---------------------------------------------------------------------------


def test_rerun_reports_unresolved_slots_and_touches_nothing(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    before = note.read_text(encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("still unresolved" in line for line in lines)
    assert note.read_text(encoding="utf-8") == before
    # No second note was drafted.
    assert len(list(note.parent.glob("archive-ready-*.md"))) == 1


def test_complete_note_never_touched(tmp_path):
    config, _ = _init(tmp_path)
    note = archive_note_path(tmp_path, config)
    note.parent.mkdir(parents=True)
    complete = "# Archive-ready note — done\n\nAll slots resolved.\n"
    note.write_text(complete, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("never touched" in line for line in lines)
    assert note.read_text(encoding="utf-8") == complete


def test_prior_complete_note_drafts_todays(tmp_path):
    # A completed note from an earlier archive event does not block a new one.
    config, _ = _init(tmp_path)
    old = archive_note_path(tmp_path, config, day="2026-01-01")
    old.parent.mkdir(parents=True)
    old.write_text("# Archive-ready note — old\n\nResolved.\n", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("drafted" in line for line in lines)
    assert archive_note_path(tmp_path, config).is_file()
    assert old.read_text(encoding="utf-8").endswith("Resolved.\n")


def test_prior_unresolved_note_blocks_new_draft(tmp_path):
    # An unresolved note (any date) is reported, never superseded silently.
    config, _ = _init(tmp_path)
    old = archive_note_path(tmp_path, config, day="2026-01-01")
    old.parent.mkdir(parents=True)
    old.write_text(f"# note\n\n{DRAFT_FILL_TOKEN} pending]]\n", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("1 [[fill:]] slot(s) still unresolved" in line for line in lines)
    assert not archive_note_path(tmp_path, config).is_file()


# ---------------------------------------------------------------------------
# S3 — REQUIRES-PROBE resolve semantics: no templated default survives
# ---------------------------------------------------------------------------

_SLOT_STRIP_RE = re.compile(r"\[\[fill:(.*?)\]\]", re.DOTALL)

_GENUINE_PROBE = (
    "Probed live at 2026-07-16T01:20Z via list_triggers (2 pages, exhaustive): "
    "trig_01ABC · cron `0 */2 * * *` · ENABLED · next fire 02:00Z. "
    "All other ids verified deleted; nothing armed beyond the failsafe."
)
_GENUINE_CONFIRMATION = (
    "Attested after resolving every section above: lessons in docs/retro/, "
    "routine record in this note, owner-action list in control/status.md, "
    "unreleased payload in CHANGELOG.md. Nothing remains chat-only."
)


def _sham_resolve(text):
    """Strip every [[fill:]] marker pair but keep the templated default text.

    The exact sham S3 exists to catch: zero slots remain, yet nothing was
    actually replaced — a record-shaped default that *looks* done.
    """
    return _SLOT_STRIP_RE.sub(lambda m: m.group(1), text)


def _wholesale_resolve(text):
    """Replace every [[fill:]] slot wholesale with plausible live output."""

    def replacement(match):
        body = match.group(1)
        if REQUIRES_PROBE_TOKEN in body:
            return _GENUINE_PROBE
        if "never drafted as complete" in body:
            return _GENUINE_CONFIRMATION
        return "resolved with live facts this session."

    return _SLOT_STRIP_RE.sub(replacement, text)


def test_sham_resolution_templated_default_cannot_pass(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    sham = _sham_resolve(note.read_text(encoding="utf-8"))
    assert DRAFT_FILL_TOKEN not in sham  # zero slots — the old "complete"
    note.write_text(sham, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    joined = "\n".join(lines)
    assert "NOT complete" in joined
    assert f"routine-state ({REQUIRES_PROBE_TOKEN})" in joined
    assert "chat-only confirmation" in joined
    assert not any("never touched" in line for line in lines)
    # Touches nothing: the sham note survives byte-identical, no new draft.
    assert note.read_text(encoding="utf-8") == sham
    assert len(list(note.parent.glob("archive-ready-*.md"))) == 1


def test_wholesale_replacement_passes(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    resolved = _wholesale_resolve(note.read_text(encoding="utf-8"))
    note.write_text(resolved, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    # The template preamble (which quotes the doctrine) survives in a genuine
    # resolution and must not trip the residue guard.
    assert any("never touched" in line for line in lines)
    assert note.read_text(encoding="utf-8") == resolved


def test_partial_sham_names_only_the_guilty_slot(tmp_path):
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    text = note.read_text(encoding="utf-8")

    def replacement(match):
        body = match.group(1)
        if REQUIRES_PROBE_TOKEN in body:
            return _GENUINE_PROBE  # genuinely replaced
        return body  # everything else sham-resolved (markers stripped)

    note.write_text(_SLOT_STRIP_RE.sub(replacement, text), encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    joined = "\n".join(lines)
    assert "chat-only confirmation" in joined
    assert f"routine-state ({REQUIRES_PROBE_TOKEN})" not in joined


def test_rewrapped_default_still_detected(tmp_path):
    # Re-flowing the default text to a different line width is still residue:
    # fingerprints are whitespace-normalized word runs.
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    sham = _sham_resolve(note.read_text(encoding="utf-8"))
    rewrapped_lines = []
    for line in sham.splitlines():
        words = line.split(" ")
        if len(words) > 4:
            rewrapped_lines.append(" ".join(words[:4]))
            rewrapped_lines.append(" ".join(words[4:]))
        else:
            rewrapped_lines.append(line)
    note.write_text("\n".join(rewrapped_lines) + "\n", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("NOT complete" in line for line in lines)


def test_prior_sham_note_blocks_new_draft(tmp_path):
    # A sham-resolved note from an earlier date is reported, never silently
    # superseded by a fresh draft (masking would defeat the guard).
    config, _ = _init(tmp_path)
    old = archive_note_path(tmp_path, config, day="2026-01-01")
    old.parent.mkdir(parents=True)
    old.write_text(
        _sham_resolve(draft_archive_note(tmp_path, config, day="2026-01-01")),
        encoding="utf-8",
    )
    lines = ensure_archive_draft(tmp_path, config)
    assert any("NOT complete" in line for line in lines)
    assert not archive_note_path(tmp_path, config).is_file()


def test_probe_slot_residue_clean_on_unresolved_draft(tmp_path):
    # Marker-carrying guarded slots are "unresolved", not residue — the
    # [[fill:]] count owns that report; residue is marker-stripped default.
    config, _ = _init(tmp_path)
    text = draft_archive_note(tmp_path, config)
    assert probe_slot_residue(text) == []


def test_probe_slot_residue_direct():
    template = load_templates()[ARCHIVE_TEMPLATE_NAME]
    findings = probe_slot_residue(_sham_resolve(template), template=template)
    assert len(findings) == 2
    assert all("wholesale replacement" in f for f in findings)
    assert probe_slot_residue(_wholesale_resolve(template), template=template) == []


# ---------------------------------------------------------------------------
# S2 evidence-judgment hints are guarded too (KL-5 surface sweep, baton 2b)
# ---------------------------------------------------------------------------


def test_draft_injects_canonical_evidence_hints(tmp_path):
    # The drafter renders its judgment slots FROM the canonical constants
    # (the CARD_GUARDED_HINTS one-source pattern): every hint appears in a
    # real evidence-seeded draft as an intact [[fill:]] slot — and an
    # intact slot is UNRESOLVED, never residue.
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    text = draft_archive_note(tmp_path, config)
    for _, body in ARCHIVE_EVIDENCE_HINTS:
        assert f"{DRAFT_FILL_TOKEN} {body}]]" in text
    assert probe_slot_residue(text) == []


def test_evidence_hint_residue_detected(tmp_path):
    # The deliberate red fixture for the S2 evidence-hint surface: the two
    # doctrine slots genuinely replaced, the three drafter-injected
    # judgment hints marker-stripped but kept — the note reads zero-slot
    # yet each surviving hint is named, and the doctrine slots are not.
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    text = note.read_text(encoding="utf-8")

    def replacement(match):
        body = match.group(1)
        if REQUIRES_PROBE_TOKEN in body:
            return _GENUINE_PROBE
        if "never drafted as complete" in body:
            return _GENUINE_CONFIRMATION
        return body  # judgment hints sham-resolved (markers stripped)

    sham = _SLOT_STRIP_RE.sub(replacement, text)
    assert DRAFT_FILL_TOKEN not in sham
    note.write_text(sham, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    joined = "\n".join(lines)
    assert "NOT complete" in joined
    assert "claims disposition" in joined
    assert "\N{BLACK FLAG} verification" in joined
    assert "payload park" in joined
    assert f"routine-state ({REQUIRES_PROBE_TOKEN})" not in joined
    assert "chat-only confirmation" not in joined
    # Touches nothing, same contract as every residue report.
    assert note.read_text(encoding="utf-8") == sham


def test_evidence_hint_wholesale_resolution_stays_silent(tmp_path):
    # Genuine judgment text in the evidence slots leaves no residue — the
    # guard fires on surviving drafted hints, not on the slot existing.
    config, _ = _init(tmp_path)
    _seed_evidence(tmp_path, config)
    ensure_archive_draft(tmp_path, config)
    note = archive_note_path(tmp_path, config)
    resolved = _wholesale_resolve(note.read_text(encoding="utf-8"))
    note.write_text(resolved, encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("never touched" in line for line in lines)


# ---------------------------------------------------------------------------
# Fail-open + the CLI verb
# ---------------------------------------------------------------------------


def test_fail_open_returns_hand_copy_advisory(tmp_path):
    config, _ = _init(tmp_path)
    # docs/retro exists as a FILE: the draft write must fail, and the verb
    # must fail open with the hand-copy fallback instead of raising.
    (tmp_path / config.docs_root).mkdir(parents=True, exist_ok=True)
    (tmp_path / config.docs_root / "retro").write_text("not a dir", encoding="utf-8")
    lines = ensure_archive_draft(tmp_path, config)
    assert any("failed open" in line for line in lines)
    assert any("archive-ready.md.tmpl" in line for line in lines)


def test_draft_archive_note_composes_from_template(tmp_path):
    config, _ = _init(tmp_path)
    text = draft_archive_note(tmp_path, config, day="2026-02-03")
    assert text.startswith("# Archive-ready note — 2026-02-03")
    assert DRAFT_MARKER in text
    assert REQUIRES_PROBE_TOKEN in text


@pytest.fixture()
def wired(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    config, backend = _init(tmp_path)
    return tmp_path, config, backend


def test_archive_prep_verb(wired, capsys):
    from engine.cli import cmd_archive_prep

    root, config, _ = wired
    assert cmd_archive_prep(root) == 0
    out = capsys.readouterr().out
    assert "archive-prep: drafted" in out
    assert archive_note_path(root, config).is_file()
    # Second run: reports the unresolved slots, exits 0.
    assert cmd_archive_prep(root) == 0
    assert "still unresolved" in capsys.readouterr().out


def test_archive_prep_verb_requires_state(tmp_path, monkeypatch, capsys):
    from engine.cli import cmd_archive_prep

    monkeypatch.chdir(tmp_path)
    assert cmd_archive_prep(tmp_path) == 1
    assert "no state" in capsys.readouterr().out


def test_dist_flat_namespace_does_not_shadow_archive_symbols(tmp_path):
    """The single-file build must substitute evidence exactly like src does.

    Regression: the dist concatenates every module into ONE namespace, so a
    later module's same-named top-level symbol silently replaces an earlier
    one at runtime. First hit: ``check_template_sync._SLOT_RE`` (a ``${}``
    matcher, concatenated after ``loop/archive.py``) shadowed archive's
    ``[[fill:]]`` slot regex — src tests were green while the shipped dist
    drafted a note with ZERO evidence substituted. Drive the dist artifact
    end-to-end and assert the one behavior the shadowing killed.
    """
    import subprocess
    import sys

    import build_bootstrap

    boot = tmp_path / "bootstrap.py"
    boot.write_text(build_bootstrap.build(), encoding="utf-8")
    repo = tmp_path / "repo"
    repo.mkdir()
    init = subprocess.run(
        [sys.executable, str(boot), "init", "--target", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert init.returncode == 0, init.stderr
    result = subprocess.run(
        [sys.executable, str(boot), "archive-prep", "--target", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "drafted" in result.stdout
    note = repo / "docs" / _RETRO_DIR_NAME / f"archive-ready-{TODAY}.md"
    text = note.read_text(encoding="utf-8")
    # Evidence substitution happened: the title slot carries today's date...
    assert text.splitlines()[0] == (
        f"# Archive-ready note — {TODAY} \N{MIDDLE DOT} "
        "[[fill: which chat/session is being archived]]"
    )
    # ...and the doctrine-guarded slots survive untouched.
    assert f"{DRAFT_FILL_TOKEN} {REQUIRES_PROBE_TOKEN}" in text
    assert "never drafted as complete" in text
    # S3 through the same artifact: sham-resolve the note (strip markers,
    # keep the templated defaults) and re-run — the dist must detect residue,
    # not report complete (guards the residue seam against dist shadowing).
    note.write_text(_sham_resolve(text), encoding="utf-8")
    rerun = subprocess.run(
        [sys.executable, str(boot), "archive-prep", "--target", str(repo)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert rerun.returncode == 0, rerun.stderr
    assert "NOT complete" in rerun.stdout
    assert "wholesale replacement" in rerun.stdout
