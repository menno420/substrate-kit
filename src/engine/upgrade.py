"""The ``upgrade`` verb — move an install to this bootstrap's version (§4.3).

The consumer flow (``release.json.upgrade_steps`` says exactly this): download
the new release's ``bootstrap.py`` next to the vendored copy as
``bootstrap.py.new`` and run ``python3 bootstrap.py.new upgrade``. The verb
then, in order:

1. **Verifies itself** against ``release.json`` when one is supplied or sits
   next to the running file (sha256 + version) — refusing on mismatch, noting
   the skip when absent.
2. **Archives first** (the §4.3 ordering constraint): the OLD vendored dist is
   banked to ``<state_dir>/backup/bootstrap-<old-version>.py`` and
   ``state.json`` to ``<state_dir>/backup/state.json`` before anything is
   overwritten — together the ``--rollback`` path.
3. **Classifies every planted doc by hash, never by re-render** (template
   rendering stamps slots/banners/dates, so template@old never byte-matches
   even an untouched file): a doc whose current sha256 equals the recorded
   kit-written hash (``adopt``/``render --live`` record it) is
   *consumer-untouched*. Classes: ``unchanged`` ·
   ``template-improved`` (untouched + new template renders differently — safe
   to apply) · ``consumer-edited`` (template unchanged — consumer-owned,
   nothing to apply) · ``diverged`` (both moved, or no recorded hash — manual;
   the report shows the template@old→new delta rendered through the current
   slot context). Old templates are parsed out of the archived old dist's
   embedded ``_TEMPLATES`` (``ast.literal_eval`` — never executed).
4. **Applies template improvements only under ``--apply-docs`` and only to
   consumer-untouched docs** — consumer-owned stays consumer-owned. Installs
   predating the hash record have no hashes: every doc honestly classifies
   ``diverged``.
5. **Replaces the vendored file with itself**, re-runs adopt's staging
   (staged ``.substrate/`` artifacts always regenerate; missing planted docs
   replant), migrates state (backup already banked), records the new
   ``kit_version``, and writes ``<state_dir>/upgrade-report.md``.
6. **Cleans up its own inputs**: after the replace lands, the consumed
   ``bootstrap.py.new`` and the ``release.json`` next to it are removed
   (``--keep-inputs`` opts out) — the first field run (superbot-next#46)
   left both stranded at the repo root.

``upgrade --rollback`` restores the banked state.json + the archived dist
named by ``<state_dir>/backup/last-upgrade.json`` (staged artifacts regenerate
from the restored file; docs applied via ``--apply-docs`` are git-visible and
are not silently reverted). Pure stdlib; every write is atomic.
"""

from __future__ import annotations

import ast
import difflib
import hashlib
import json
from datetime import date
from pathlib import Path
from typing import Any

from engine.adopt import (
    ADOPT_PLAN,
    BACKUP_DIRNAME,
    _adopt_dest,
    adopt,
    archive_dist,
    dist_version,
    doc_is_untouched,
    record_doc_hash,
    with_unrendered_banner,
)
from engine.lib.atomicio import atomic_write_text
from engine.lib.config import KIT_VERSION, Config, save_config
from engine.lib.state import STATE_SCHEMA_VERSION
from engine.loop.telemetry import MODEL_LINE_NEEDLE
from engine.render import build_context, load_templates, render

LAST_UPGRADE_FILENAME = "last-upgrade.json"
UPGRADE_REPORT_FILENAME = "upgrade-report.md"
STATE_BACKUP_FILENAME = "state.json"

# Classification labels (the §4.3 report classes).
CLASS_UNCHANGED = "unchanged"
CLASS_IMPROVED = "template-improved"
CLASS_CONSUMER_EDITED = "consumer-edited"
CLASS_DIVERGED = "diverged"
CLASS_MISSING = "missing"


class UpgradeRefused(Exception):
    """Raised when the self-verification against release.json fails."""


def load_old_templates(dist_text: str) -> dict[str, str] | None:
    """Parse the ``_TEMPLATES`` dict out of an old dist's text (never exec)."""
    try:
        tree = ast.parse(dist_text)
    except SyntaxError:
        return None
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if isinstance(target, ast.Name) and target.id == "_TEMPLATES":
                try:
                    value = ast.literal_eval(node.value)
                except (ValueError, SyntaxError):
                    return None
                if isinstance(value, dict):
                    return {str(k): str(v) for k, v in value.items()}
    return None


def find_vendored_bootstrap(root: Path) -> Path | None:
    """Return the install's vendored single-file bootstrap, if any.

    ``bootstrap.py`` at the repo root is the adopt mechanic's plant;
    ``dist/bootstrap.py`` is consumer #0 (the kit repo operating on itself).
    """
    for rel in ("bootstrap.py", "dist/bootstrap.py"):
        candidate = root / rel
        if candidate.is_file():
            return candidate
    return None


def verify_against_release_json(running: Path, release_json: Path) -> list[str]:
    """Return report lines; raise :class:`UpgradeRefused` on a mismatch."""
    payload = json.loads(release_json.read_text(encoding="utf-8"))
    digest = hashlib.sha256(running.read_bytes()).hexdigest()
    if payload.get("sha256") != digest:
        msg = (
            f"sha256 mismatch vs {release_json.name}: expected "
            f"{payload.get('sha256')}, this file is {digest} — corrupted or "
            "tampered download; re-download the release asset."
        )
        raise UpgradeRefused(msg)
    if payload.get("version") != KIT_VERSION:
        msg = (
            f"{release_json.name} names version {payload.get('version')!r} but "
            f"this bootstrap is v{KIT_VERSION} — mismatched release files."
        )
        raise UpgradeRefused(msg)
    return [f"verified: sha256 + version against {release_json.name}"]


def _upgrade_context(backend: Any) -> dict[str, str]:
    """Build the render context exactly the way adopt does."""
    context = build_context(backend.data)
    context.setdefault("integration_mode", str(backend.get("mode", "guided")))
    return context


def _render_planted(template_text: str, template_name: str, context: dict) -> str:
    """Render a template the way adopt plants it (banner; ledger date stamp)."""
    text = render(template_text, context)
    if template_name == "decisions.md.tmpl":
        text = text.replace("- date:\n", f"- date: {date.today().isoformat()}\n")
    return with_unrendered_banner(text)


def _normalize_dates(text: str) -> str:
    """Blank ledger date stamps so an adopt-day stamp is not template drift."""
    lines = text.split("\n")
    return "\n".join(
        "- date:" if line.startswith("- date: ") else line for line in lines
    )


def _doc_plan(root: Path, config: Config) -> list[tuple[str, str]]:
    """Return (template, planted relpath) pairs the diff report covers."""
    plan = [(tpl, _adopt_dest(rel, config)) for tpl, rel in ADOPT_PLAN]
    if (root / ".claude" / "CLAUDE.md").exists():
        plan.append(("CLAUDE.md.tmpl", ".claude/CLAUDE.md"))
    return plan


def classify_planted_docs(
    root: Path,
    config: Config,
    backend: Any,
    old_templates: dict[str, str] | None,
    new_templates: dict[str, str] | None = None,
) -> list[dict[str, str]]:
    """Classify every planted doc for the upgrade report (§4.3 step 2).

    Returns rows ``{relpath, template, class, note, diff}`` (``diff`` only for
    diverged docs with old templates available — the template@old→new delta,
    both rendered through the *current* slot context for a readable diff).
    """
    context = _upgrade_context(backend)
    templates = new_templates if new_templates is not None else load_templates()
    rows: list[dict[str, str]] = []
    for template_name, rel in _doc_plan(root, config):
        path = root / rel
        row = {"relpath": rel, "template": template_name, "diff": ""}
        if not path.exists():
            row["class"] = CLASS_MISSING
            row["note"] = "absent — upgrade's adopt pass replants it"
            rows.append(row)
            continue
        current = path.read_text(encoding="utf-8")
        new_render = _render_planted(templates[template_name], template_name, context)
        old_render = None
        if old_templates and template_name in old_templates:
            old_render = _render_planted(
                old_templates[template_name],
                template_name,
                context,
            )
        untouched = doc_is_untouched(backend, rel, current)
        if not untouched and _normalize_dates(new_render) == _normalize_dates(
            current,
        ):
            # Self-heal a lost hash record (companion idea
            # upgrade-rollback-loses-doc-hash-records): `upgrade --rollback`
            # restores the pre-upgrade state.json, discarding every
            # planted_doc_hashes entry the upgrade's adopt pass recorded — so
            # on a re-run a doc the kit itself wrote carries no hash and would
            # classify diverged, taking it out of --apply-docs' reach. A
            # byte-match against the NEW template render (date-normalized)
            # *proves* the doc is untouched kit-form; recording the hash
            # recovers a lost record from ground truth, not a provenance lie. A
            # doc a consumer actually edited never byte-matches and stays
            # honestly diverged; and a byte-match to the new render only ever
            # yields `unchanged`, so nothing is auto-applied that would not be.
            record_doc_hash(backend, rel, current)
            untouched = True
        if untouched:
            if _normalize_dates(new_render) == _normalize_dates(current):
                row["class"] = CLASS_UNCHANGED
                row["note"] = "template identical across versions"
            else:
                row["class"] = CLASS_IMPROVED
                row["note"] = (
                    "consumer-untouched + template improved — "
                    "safe to apply with `upgrade --apply-docs`"
                )
        elif old_render is not None and _normalize_dates(
            old_render,
        ) == _normalize_dates(new_render):
            row["class"] = CLASS_CONSUMER_EDITED
            row["note"] = "template unchanged — consumer-owned, nothing to apply"
        else:
            row["class"] = CLASS_DIVERGED
            if old_render is None:
                row["note"] = (
                    "no recorded hash or old templates unavailable "
                    "(pre-1.0 install) — manual review"
                )
            else:
                row["note"] = "both the template and the doc moved — manual merge"
                row["diff"] = "\n".join(
                    difflib.unified_diff(
                        old_render.splitlines(),
                        new_render.splitlines(),
                        fromfile=f"{rel} (template@old, current slots)",
                        tofile=f"{rel} (template@new, current slots)",
                        lineterm="",
                    ),
                )
        rows.append(row)
    return rows


def apply_doc_improvements(
    root: Path,
    config: Config,
    backend: Any,
    rows: list[dict[str, str]],
    new_templates: dict[str, str] | None = None,
) -> list[str]:
    """Re-render + write every ``template-improved`` doc; re-record hashes.

    Only the consumer-untouched class is ever written (the §4.3 covenant:
    planted docs are never auto-edited without ``--apply-docs``, and never
    when the consumer diverged).
    """
    context = _upgrade_context(backend)
    templates = new_templates if new_templates is not None else load_templates()
    lines: list[str] = []
    for row in rows:
        if row["class"] != CLASS_IMPROVED:
            continue
        rel = row["relpath"]
        text = _render_planted(templates[row["template"]], row["template"], context)
        atomic_write_text(root / rel, text)
        record_doc_hash(backend, rel, text)
        lines.append(f"applied: {rel} (template@new, hash re-recorded)")
    return lines


def upgrade_report_text(
    old_version: str,
    rows: list[dict[str, str]],
    applied: list[str],
    carveouts: list[str] | None = None,
) -> str:
    """Compose ``<state_dir>/upgrade-report.md``.

    ``carveouts`` — the ``carve-out:`` lines adopt's kit-owned gate regen
    emitted (host-added jobs/steps the regen could not keep; the full
    pre-regen gate is banked under ``<state_dir>/backup/``). They get their
    own loud section: the report file is the upgrade PR's body evidence, and
    a host whose only CI job lived inside the kit gate (superbot-games #16)
    must see the relocation instruction there, not only in stdout.
    """
    counts: dict[str, int] = {}
    for row in rows:
        counts[row["class"]] = counts.get(row["class"], 0) + 1
    summary = " · ".join(f"{k}: {v}" for k, v in sorted(counts.items()))
    lines = [
        f"# substrate-kit upgrade report — v{old_version} → v{KIT_VERSION}",
        "",
        f"> Generated {date.today().isoformat()} by `bootstrap.py upgrade`. "
        f"Rollback: `python3 bootstrap.py upgrade --rollback`.",
        "",
        f"**Docs:** {summary}",
        "",
        "| planted doc | class | note |",
        "|---|---|---|",
    ]
    lines += [f"| {r['relpath']} | {r['class']} | {r['note']} |" for r in rows]
    if carveouts:
        lines += [
            "",
            "## ⚠️ Gate carve-outs (host additions the kit-owned regen "
            "could not keep)",
            "",
        ]
        lines += [f"- {line}" for line in carveouts]
    if applied:
        lines += ["", "## Applied (--apply-docs)", ""]
        lines += [f"- {line}" for line in applied]
    diffs = [r for r in rows if r["diff"]]
    if diffs:
        lines += ["", "## Template deltas for diverged docs", ""]
        for row in diffs:
            lines += [f"### {row['relpath']}", "", "```diff", row["diff"], "```", ""]
    return "\n".join(lines) + "\n"


def newest_banked_archive(
    root: Path,
    config: Config,
) -> tuple[Path | None, str | None]:
    """Return ``(path, from_version)`` of the newest banked pre-upgrade dist.

    The archive-first covenant banks the OLD dist under
    ``<state_dir>/backup/bootstrap-<old-version>.py`` and records the exact one
    the last upgrade banked in ``last-upgrade.json`` (``archived_dist`` +
    ``from_version``). That marker names the newest banked pre-upgrade dist —
    the templates the single-shot apply window closed over. Returns
    ``(None, None)`` when no upgrade has banked one (nothing to apply post-hoc
    from).
    """
    marker = root / config.state_dir / BACKUP_DIRNAME / LAST_UPGRADE_FILENAME
    if not marker.is_file():
        return None, None
    try:
        meta = json.loads(marker.read_text(encoding="utf-8"))
    except (ValueError, OSError):
        return None, None
    archived_rel = meta.get("archived_dist")
    if not archived_rel:
        return None, None
    archived = root / archived_rel
    if not archived.is_file():
        return None, None
    return archived, meta.get("from_version")


def run_apply_docs_posthoc(
    root: Path,
    config: Config,
    backend: Any,
) -> list[str]:
    """Apply template improvements *after* the single-shot window has closed.

    (Idea ``upgrade-apply-docs-single-shot-window``.) Once an upgrade replaced
    the vendored dist, a bare re-run parses new==new templates and can never
    yield a ``template-improved`` row again — the apply window was single-shot.
    But the pre-upgrade dist was banked (archive-first), so its templates
    survive on disk. Load them as ``old_templates`` and run the SAME
    classify/apply the in-run path uses, so an operator who skipped
    ``--apply-docs`` recovers the improvements WITHOUT a rollback. The covenant
    is unchanged: only consumer-untouched kit-form docs are ever written
    (consumer-edited docs stay diverged), hashes are re-recorded, and a re-run
    is idempotent (everything already current). No archive banked yet → a clean,
    actionable message and nothing written (never a crash, never an impossible
    command).
    """
    report: list[str] = []
    archived, from_version = newest_banked_archive(root, config)
    if archived is None:
        report.append(
            "apply-docs: no banked pre-upgrade dist to apply from — post-hoc "
            "--apply-docs needs the archive the last upgrade banked "
            f"({config.state_dir}/{BACKUP_DIRNAME}/bootstrap-<old>.py, named by "
            f"{LAST_UPGRADE_FILENAME}). Nothing applied.",
        )
        return report
    old_templates = load_old_templates(archived.read_text(encoding="utf-8"))
    rows = classify_planted_docs(root, config, backend, old_templates)
    applied = apply_doc_improvements(root, config, backend, rows)
    report += applied
    if not applied:
        report.append(
            "apply-docs: no template-improved docs to apply — every planted "
            "doc is already current or consumer-owned.",
        )
    report_rel = f"{config.state_dir}/{UPGRADE_REPORT_FILENAME}"
    atomic_write_text(
        root / report_rel,
        upgrade_report_text(
            from_version or config.kit_version or "unknown",
            rows,
            applied,
        ),
    )
    report.append(f"report: {report_rel}")
    return report


def run_upgrade(
    root: Path,
    config: Config,
    backend: Any,
    *,
    kit_root: Path,
    running: Path,
    apply_docs: bool = False,
    release_json: Path | None = None,
    cleanup_inputs: bool = True,
) -> list[str]:
    """Execute the §4.3 upgrade flow; return the report lines.

    Raises :class:`UpgradeRefused` when release.json verification fails.
    """
    # Post-hoc --apply-docs (idea upgrade-apply-docs-single-shot-window): when
    # the vendored dist is ALREADY at the running version there is no pending
    # transition, but a prior upgrade that skipped --apply-docs banked the
    # pre-upgrade dist (archive-first covenant). Loading old_templates from that
    # newest banked archive and running the SAME classify/apply the in-run path
    # uses recovers the single-shot window without a rollback. Guarded by
    # apply_docs so a bare same-version re-run keeps its existing no-op shape,
    # and the in-run path (vendored OLDER than KIT_VERSION) is UNCHANGED.
    posthoc_vendored = find_vendored_bootstrap(root)
    if apply_docs and posthoc_vendored is not None:
        vendored_text = posthoc_vendored.read_text(encoding="utf-8")
        if dist_version(vendored_text) == KIT_VERSION:
            return run_apply_docs_posthoc(root, config, backend)

    report: list[str] = []

    # (1) Self-verification (sha256 + version) when release.json is findable.
    candidate = release_json or running.parent / "release.json"
    if candidate.is_file():
        report += verify_against_release_json(running, candidate)
    else:
        report.append(
            "note: no release.json found — sha256 verification skipped "
            "(download it next to the new bootstrap to enable it).",
        )

    # (2) Archive FIRST (§4.3): old dist + state.json, before any overwrite.
    vendored = find_vendored_bootstrap(root)
    old_text = vendored.read_text(encoding="utf-8") if vendored else None
    # From-version: the vendored header states what is actually installed and
    # OUTRANKS the config pin when they disagree — a consumer may record its
    # pin BEFORE the first real upgrade (the D2 order), leaving the pin
    # aspirational while the file on disk is older or unstamped. The field
    # case (superbot-next#46): pin said 1.0.0, the archive honestly said
    # bootstrap-unknown.py, and a rollback would have restored the wrong pin.
    # The one header that cannot name the true "from" is KIT_VERSION itself —
    # the hand-copied-new-dist-over-old case — where the recorded pin wins
    # (distinguishable exactly because the header equals KIT_VERSION).
    header_version = dist_version(old_text) if old_text else None
    if old_text is not None and header_version != KIT_VERSION:
        old_version = header_version or "unknown"
    else:
        old_version = config.kit_version or header_version or "unknown"
    backup_dir = root / config.state_dir / BACKUP_DIRNAME
    archived = None
    if vendored is not None:
        archived = archive_dist(root, config, vendored, report)
    state_path = root / config.state_dir / "state.json"
    if state_path.exists():
        atomic_write_text(
            backup_dir / STATE_BACKUP_FILENAME,
            state_path.read_text(encoding="utf-8"),
        )
        report.append(
            f"backed up: state.json -> "
            f"{config.state_dir}/{BACKUP_DIRNAME}/{STATE_BACKUP_FILENAME}",
        )
    atomic_write_text(
        backup_dir / LAST_UPGRADE_FILENAME,
        json.dumps(
            {
                "from_version": old_version,
                "to_version": KIT_VERSION,
                "date": date.today().isoformat(),
                "vendored": (
                    str(vendored.relative_to(root)) if vendored is not None else None
                ),
                "archived_dist": (
                    str(archived.relative_to(root)) if archived is not None else None
                ),
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
    )

    # (3) Hash-based planted-doc diff report (§4.3 step 2), computed BEFORE
    # the adopt pass replants anything.
    old_templates = load_old_templates(old_text) if old_text else None
    rows = classify_planted_docs(root, config, backend, old_templates)

    # (4) --apply-docs: template improvements land on untouched docs only.
    applied = apply_doc_improvements(root, config, backend, rows) if apply_docs else []
    for line in applied:
        report.append(line)
    improved = [r for r in rows if r["class"] == CLASS_IMPROVED]
    if improved and not apply_docs:
        # A bare re-run parses the already-new vendored templates and can never
        # yield a template-improved row again (idea
        # upgrade-apply-docs-single-shot-window) — but the pre-upgrade dist was
        # banked (archive-first), so a same-version `upgrade --apply-docs` now
        # applies these POST-HOC from that archive. Name that working recovery
        # (no rollback needed), never a bare "re-run to take them" no-op.
        report.append(
            f"note: {len(improved)} doc(s) have template improvements you "
            "never edited — take them now by re-running with --apply-docs, or "
            "any time later with `upgrade --apply-docs`: it applies them "
            "post-hoc from the banked pre-upgrade archive (no rollback needed).",
        )

    # (5) Replace the vendored file with the running (new) one — only when the
    # running entry actually IS a stamped single-file bootstrap (in the
    # source/pip layouts there is no single file to install).
    running_is_dist = (
        running.is_file()
        and dist_version(running.read_text(encoding="utf-8")) is not None
    )
    replaced = False
    if vendored is not None and running_is_dist and running.resolve() != vendored.resolve():
        atomic_write_text(vendored, running.read_text(encoding="utf-8"))
        replaced = True
        report.append(
            f"replaced: {vendored.relative_to(root)} "
            f"(v{old_version} -> v{KIT_VERSION}; old copy archived)",
        )

    # (6) Staged regeneration: adopt is idempotent — staged artifacts always
    # regenerate, planted docs skip-if-exist, kit_version records new.
    # ``archive_running=False``: the archive-first covenant was honored in
    # step (2) with the OLD dist; by now the vendored file IS the new dist,
    # and adopt's own banking pass would archive a spurious
    # ``bootstrap-<new>.py`` next to it (field-reproduced on fleet-manager
    # #35, superbot-games #22, trading-strategy #38). An upgrade banks
    # exactly one dist: the pre-upgrade one.
    adopt_lines = adopt(
        root,
        config,
        backend,
        kit_root=kit_root,
        archive_running=False,
    )
    report += adopt_lines
    # Gate carve-outs (superbot-games #16 class): adopt's kit-owned gate
    # regen reports host additions it could not keep as ``carve-out:`` lines
    # — surface them in upgrade-report.md too (the report is the upgrade PR's
    # body evidence; a stdout-only warning is too easy to lose).
    gate_carveout_lines = [
        line for line in adopt_lines if line.startswith("carve-out:")
    ]

    # (6b) KL-3: the 📊 Model needle joins session_markers at upgrade time —
    # a consumer's gate only tightens when it upgrades, never mid-version
    # (founding plan §5.2); the report says so out loud.
    if not any(
        m.get("needle") == MODEL_LINE_NEEDLE for m in config.session_markers
    ):
        config.session_markers.append(
            {"label": "Model line", "needle": MODEL_LINE_NEEDLE},
        )
        save_config(root, config)
        report.append(
            "session_markers: added the \N{BAR CHART} Model line needle "
            "(KL-3 telemetry) — session logs must now carry "
            "`- **\N{BAR CHART} Model:** <model> \N{MIDDLE DOT} <effort> "
            "\N{MIDDLE DOT} <task-class>`; session-close harvests it into "
            "telemetry/model-usage.jsonl.",
        )

    # (7) State migration (backup already banked above).
    backend.migrate(STATE_SCHEMA_VERSION)
    report.append(f"state: schema at v{STATE_SCHEMA_VERSION} (backup banked).")

    # (8) The report file (§9.2 names it as the upgrade PR's body evidence).
    report_rel = f"{config.state_dir}/{UPGRADE_REPORT_FILENAME}"
    atomic_write_text(
        root / report_rel,
        upgrade_report_text(old_version, rows, applied, gate_carveout_lines),
    )
    report.append(f"report: {report_rel}")

    # (9) Self-cleanup of the upgrade inputs: the consumer flow downloads
    # ``bootstrap.py.new`` (+ its ``release.json``) next to the vendored file,
    # and once the replace has landed both are strays the first field run
    # (superbot-next#46) left behind. Only the files the flow itself consumed
    # are touched — the running .new file that was just installed and the
    # release.json sitting NEXT TO it (an explicit --release-json elsewhere is
    # left alone). ``--keep-inputs`` opts out; a cleanup error never fails a
    # completed upgrade (fail-open, like every non-essential step).
    if cleanup_inputs and replaced:
        for leftover in (running, candidate):
            if leftover.parent != running.parent or not leftover.is_file():
                continue
            try:
                leftover.unlink()
                report.append(
                    f"cleaned up: {leftover.name} "
                    "(upgrade input; pass --keep-inputs to retain)",
                )
            except OSError:
                report.append(
                    f"note: could not remove {leftover.name} — "
                    "delete it by hand.",
                )
    return report


def run_rollback(root: Path, config: Config) -> list[str]:
    """Restore the banked state.json + archived dist from the last upgrade."""
    backup_dir = root / config.state_dir / BACKUP_DIRNAME
    marker = backup_dir / LAST_UPGRADE_FILENAME
    if not marker.is_file():
        return [f"rollback: nothing to roll back (no {LAST_UPGRADE_FILENAME})."]
    meta = json.loads(marker.read_text(encoding="utf-8"))
    report: list[str] = []
    state_backup = backup_dir / STATE_BACKUP_FILENAME
    if state_backup.is_file():
        atomic_write_text(
            root / config.state_dir / "state.json",
            state_backup.read_text(encoding="utf-8"),
        )
        report.append("restored: state.json from backup.")
    archived_rel = meta.get("archived_dist")
    vendored_rel = meta.get("vendored")
    if archived_rel and vendored_rel:
        archived = root / archived_rel
        if archived.is_file():
            atomic_write_text(
                root / vendored_rel,
                archived.read_text(encoding="utf-8"),
            )
            report.append(
                f"restored: {vendored_rel} from {archived_rel} "
                f"(back to v{meta.get('from_version')}).",
            )
    recorded = str(meta.get("from_version") or "")
    # "unknown" names an unstamped pre-release dist (the archive is
    # bootstrap-unknown.py) — the honest config value for that state is the
    # unrecorded sentinel "", never the literal string "unknown".
    restored_pin = "" if recorded == "unknown" else recorded
    if config.kit_version and config.kit_version != restored_pin:
        config.kit_version = restored_pin
        save_config(root, config)
        report.append(f"restored: config kit_version -> {config.kit_version!r}.")
    report.append(
        "note: staged .substrate/ artifacts regenerate from the restored file "
        "(run: python3 bootstrap.py adopt); docs applied via --apply-docs are "
        "git-visible and were not reverted.",
    )
    return report
