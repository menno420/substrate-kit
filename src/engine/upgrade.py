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
        if doc_is_untouched(backend, rel, current):
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
) -> str:
    """Compose ``<state_dir>/upgrade-report.md``."""
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
    if applied:
        lines += ["", "## Applied (--apply-docs)", ""]
        lines += [f"- {line}" for line in applied]
    diffs = [r for r in rows if r["diff"]]
    if diffs:
        lines += ["", "## Template deltas for diverged docs", ""]
        for row in diffs:
            lines += [f"### {row['relpath']}", "", "```diff", row["diff"], "```", ""]
    return "\n".join(lines) + "\n"


def run_upgrade(
    root: Path,
    config: Config,
    backend: Any,
    *,
    kit_root: Path,
    running: Path,
    apply_docs: bool = False,
    release_json: Path | None = None,
) -> list[str]:
    """Execute the §4.3 upgrade flow; return the report lines.

    Raises :class:`UpgradeRefused` when release.json verification fails.
    """
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
    # The recorded config version (stamped at the OLD adopt) outranks the
    # vendored header: when the consumer already copied the new file over the
    # old one by hand, the header would misreport the new version as "from".
    old_version = (
        config.kit_version
        or (dist_version(old_text) if old_text else None)
        or "unknown"
    )
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
        report.append(
            f"note: {len(improved)} doc(s) have template improvements you "
            "never edited — re-run with --apply-docs to take them.",
        )

    # (5) Replace the vendored file with the running (new) one — only when the
    # running entry actually IS a stamped single-file bootstrap (in the
    # source/pip layouts there is no single file to install).
    running_is_dist = (
        running.is_file()
        and dist_version(running.read_text(encoding="utf-8")) is not None
    )
    if vendored is not None and running_is_dist and running.resolve() != vendored.resolve():
        atomic_write_text(vendored, running.read_text(encoding="utf-8"))
        report.append(
            f"replaced: {vendored.relative_to(root)} "
            f"(v{old_version} -> v{KIT_VERSION}; old copy archived)",
        )

    # (6) Staged regeneration: adopt is idempotent — staged artifacts always
    # regenerate, planted docs skip-if-exist, kit_version records new.
    report += adopt(root, config, backend, kit_root=kit_root)

    # (7) State migration (backup already banked above).
    backend.migrate(STATE_SCHEMA_VERSION)
    report.append(f"state: schema at v{STATE_SCHEMA_VERSION} (backup banked).")

    # (8) The report file (§9.2 names it as the upgrade PR's body evidence).
    report_rel = f"{config.state_dir}/{UPGRADE_REPORT_FILENAME}"
    atomic_write_text(
        root / report_rel,
        upgrade_report_text(old_version, rows, applied),
    )
    report.append(f"report: {report_rel}")
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
    if config.kit_version and config.kit_version != meta.get("from_version"):
        config.kit_version = str(meta.get("from_version") or "")
        save_config(root, config)
        report.append(f"restored: config kit_version -> {config.kit_version!r}.")
    report.append(
        "note: staged .substrate/ artifacts regenerate from the restored file "
        "(run: python3 bootstrap.py adopt); docs applied via --apply-docs are "
        "git-visible and were not reverted.",
    )
    return report
