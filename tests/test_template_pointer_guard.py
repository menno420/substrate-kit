"""Template pointer guard — no template ships a dead repo-local pointer.

The ORDER 015 dead-boot-pointer class, generalized into an ENFORCING test
(Q-0194 friction → guard). The kit's planted docs steer cold sessions almost
entirely through backtick path refs (`` `docs/x.md` ``), and as of kit HEAD
3d58a46 nothing enforced that those pointers land on files that actually
exist in an adopted repo:

1. ``engine.checks.check_docs.check_links`` validates only markdown
   ``[text](path)`` links; backtick refs — the templates' dominant pointer
   form — feed only the reachability walk, where a ref to a nonexistent file
   is SILENTLY DROPPED (the ``nxt.exists()`` filter in ``check_reachable``).
2. Pointers outside ``docs/`` (``control/*``, ``CONSTITUTION.md``,
   ``.session-journal.md``, ``scripts/env-setup.sh``) are checked by nothing.
3. No test asserted every template-emitted repo-local doc path is an
   ``ADOPT_PLAN`` destination or otherwise planted (partial coverage:
   ``test_adopt.py`` pins the ``agreement_home`` boot pointer only).

This guard extracts every repo-local path pointer emitted by each
``src/engine/templates/*.tmpl`` — both backtick and markdown-link forms —
and asserts each one resolves to a file an adopter will actually have (or is
explicitly, verifiably accounted for). Slot-bearing refs (``${...}``) are
skipped: the current templates only emit PURE-slot pointers
(``${agreement_home}``, ``${verify_command}``), and the agreement-home boot
pointer has its own dedicated pins (``test_adopt.py``
``test_orientation_boot_pointer_*``).

A kit-repo TEST rather than a ``check_docs`` extension, on purpose: the
invariant is a build-time property of the kit's templates, and folding it
into the adopter-facing checker would run it in repos where the templates do
not exist — risking new reds on green adopters for a kit-side concern.
"""

from __future__ import annotations

import re
from pathlib import Path

from engine.adopt import (
    ADOPT_PLAN,
    AUTOMERGE_ENABLER_RELPATH,
    LIVE_CI_RELPATH,
)
from engine.render import load_templates

KIT_ROOT = Path(__file__).resolve().parents[1]

# ── extraction ───────────────────────────────────────────────────────────────

_BACKTICK_RE = re.compile(r"`([^`\n]+)`")
_MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
# A path pointer: path-safe charset only — spaces, globs (*), angle-bracket
# placeholders (<lane>), quotes, and $ slots all disqualify a candidate.
_PATH_CHARS_RE = re.compile(r"^[A-Za-z0-9_./-]+$")
# A file extension: a dot followed by a letter-led short suffix ("v1.15.0"
# and bare version-ish tokens don't qualify).
_EXT_RE = re.compile(r"\.([a-z][a-z0-9]{0,5})$")
# Extension-shaped suffixes that mark a DOMAIN or bare-extension mention,
# not a repo file (`api.github.com`, `.mp4`).
_NON_FILE_EXTENSIONS = frozenset({"com", "org", "net", "io"})


def _pointer_candidates(text: str) -> set[str]:
    """Every repo-local path pointer in ``text`` (backtick + markdown link)."""
    raw: set[str] = set(_BACKTICK_RE.findall(text))
    for target in _MD_LINK_RE.findall(text):
        raw.add(target.split("#", 1)[0])
    pointers: set[str] = set()
    for cand in raw:
        cand = cand.strip()
        if not cand or cand.startswith(("http://", "https://", "mailto:", "#")):
            continue
        if "${" in cand:
            # Slot-bearing ref — not statically knowable here. Current
            # templates only emit pure-slot refs; the agreement_home boot
            # pointer is pinned by its own tests (see module docstring).
            continue
        if not _PATH_CHARS_RE.match(cand):
            continue
        ext = _EXT_RE.search(cand)
        if ext is None or ext.group(1) in _NON_FILE_EXTENSIONS:
            continue
        stem = Path(cand).name[: -len(ext.group(0))]
        if not stem:
            continue  # bare-extension mention like `.mp4`
        pointers.add(cand)
    return pointers


# ── resolution tables ────────────────────────────────────────────────────────

# 1) Files every default adopt plants.
_PLAN_DESTS = frozenset(dest for _, dest in ADOPT_PLAN)

# 2) Artifacts adopt/upgrade (or the session loop) writes OUTSIDE ADOPT_PLAN.
#    Each entry names the writer, so a future dead pointer that lands here by
#    mistake is auditable.
_GENERATED_BY_KIT: dict[str, str] = {
    # adopt() persists the config via save_config on every run.
    "substrate.config.json": "written by adopt (engine.lib.config.save_config)",
    # _vendor_bootstrap copies the running single-file dist to the repo root
    # (skip-if-exists) so staged hook commands resolve.
    "bootstrap.py": "vendored to repo root by adopt (_vendor_bootstrap)",
    # Planted by adopt outside ADOPT_PLAN — a derived render, hash-classified
    # differently (engine.seatdigest.seat_digest_relpath, default docs root).
    "docs/seat-digest.md": "planted by adopt (seat_digest_relpath)",
    # Regenerated at every session boot by engine.loop.handoff_pointer;
    # untracked by design ('when present' in every template that names it).
    "HANDOFF.md": "regenerated by engine.loop.handoff_pointer (conditional)",
    # Installed by `adopt --wire-enforcement`; kit-owned, regenerated in place.
    LIVE_CI_RELPATH: "installed by adopt --wire-enforcement (kit-owned gate)",
    AUTOMERGE_ENABLER_RELPATH: "installed by adopt --wire-enforcement",
}

# 3) Per-lane heartbeats: `adopt --lane <name>` plants control/status-<lane>.md
#    (engine.adopt.lane_status_relpath; charset per _LANE_NAME_RE). Templates
#    name concrete example lanes (mining / exploration) when documenting the
#    multi-Project extension.
_LANE_HEARTBEAT_RE = re.compile(r"control/status-[A-Za-z0-9][A-Za-z0-9_-]*\.md")

# 4) Kit-repo self-refs: templates that cite the KIT's own source as the
#    grammar/skills source of truth ("kit-owned constants in the kit's
#    `src/engine/grammar.py`"). These are pointers into THIS repo, not the
#    adopter — so the guard asserts they exist HERE (a kit-side rename must
#    fail this test until the templates are updated too).
_KIT_SELF_REFS: dict[str, str] = {
    "src/engine/grammar.py": "grammar source of truth named by control templates",
    "tests/test_grammar.py": "grammar agreement pin named by control templates",
    "tests/test_owner_assist.py": "owner-assist grammar pin named by control-README",
    "src/engine/skills/skills.py": "skills source of truth named by SKILLS-index",
    "docs/program/rulings.md": "the [PL-NNN] register named by CONSTITUTION/collab",
    "docs/program/collaboration-model.md": "program doctrine named by collab template",
    "docs/adopters.md": "kit-generated adopter registry named by control templates",
}

# 5) Cross-repo refs: pointers into ANOTHER fleet repo, always introduced with
#    the owning repo's name in the same template. pointer -> (owner marker
#    that must appear in every referencing template, reason).
_EXTERNAL_REPO_REFS: dict[str, tuple[str, str]] = {
    # (fleet-manager's master capability ledger was `docs/capabilities.md`
    # here until INC-29 / fm plan B2 — the real fleet-master file is uppercase
    # `docs/CAPABILITIES.md`, so the lowercase pointer was a dead link. Fixed
    # at CAPABILITIES.md.tmpl:8; the corrected uppercase pointer now resolves
    # via _PLAN_DESTS as an ADOPT_PLAN destination — no cross-repo entry
    # needed, and CAPABILITIES.md.tmpl still names `menno420/fleet-manager`
    # next to it.)
    "docs/planning/fleet-coordination-protocol-2026-07-09.md": (
        "superbot",
        "canonical control-protocol spec — control-README.md.tmpl names "
        "`menno420/superbot` as its home",
    ),
    "tools/sim/claim_layout_sim.py": (
        "superbot",
        "claim-layout simulation — control templates attribute it to superbot",
    ),
}

# 6) The explicit whitelist — (template name, pointer) -> written reason.
#    Keep every entry commented: an entry without a live reason is drift.
_WHITELIST: dict[tuple[str, str], str] = {
    # "`CLAUDE.md`-level rules, hooks, settings" — a concept mention of the
    # agreement file, which the default adopt only STAGES
    # (<state_dir>/claude/CLAUDE.md; live at .claude/CLAUDE.md only with the
    # include_claude opt-in). Not a boot pointer — those render via the
    # engine-computed ${agreement_home}.
    ("CONSTITUTION.md.tmpl", "CLAUDE.md"): (
        "concept mention of the staged agreement file (adopt stages it; "
        "boot pointers use ${agreement_home})"
    ),
    # Bare basename of the kit-owned CI gate (LIVE_CI_RELPATH =
    # .github/workflows/substrate-gate.yml), named when explaining the
    # control fast lane. Conditional: installed by adopt --wire-enforcement.
    ("control-README.md.tmpl", "substrate-gate.yml"): (
        "basename of LIVE_CI_RELPATH, installed by adopt --wire-enforcement"
    ),
}


def _planted_dirs() -> dict[str, str]:
    """Template filename -> directory its planted copy lives in.

    Bare (slash-less) refs like `` `inbox.md` `` inside control-README.md are
    sibling refs — resolve them relative to the template's own planted home.
    CLAUDE.md.tmpl is deliberately absent from ADOPT_PLAN (staged only); its
    live opt-in home is ``.claude/``.
    """
    dirs = {}
    for tmpl, dest in ADOPT_PLAN:
        parent = str(Path(dest).parent)
        dirs[tmpl] = "" if parent == "." else parent
    dirs["CLAUDE.md.tmpl"] = ".claude"
    return dirs


def _resolves(template: str, pointer: str, planted_dir: str) -> str | None:
    """Return None when ``pointer`` is accounted for, else the failure reason."""
    candidates = [pointer]
    if "/" not in pointer and planted_dir:
        # Sibling ref: try the template's planted directory first.
        candidates.insert(0, f"{planted_dir}/{pointer}")
    for cand in candidates:
        if cand in _PLAN_DESTS:
            return None
        if cand in _GENERATED_BY_KIT:
            return None
        if _LANE_HEARTBEAT_RE.fullmatch(cand):
            return None
    if pointer in _KIT_SELF_REFS:
        return None
    if pointer in _EXTERNAL_REPO_REFS:
        return None
    if (template, pointer) in _WHITELIST:
        return None
    return (
        f"{template} points at `{pointer}`, which no adopter will have: it is "
        "not an ADOPT_PLAN destination, not a kit-generated artifact, not a "
        "lane heartbeat, and not whitelisted.\n"
        "Fix: (a) point at a planted file instead; (b) if adopt/upgrade "
        "really writes it, add it to _GENERATED_BY_KIT naming the writer; "
        "(c) if it names the KIT repo's own source, add it to _KIT_SELF_REFS "
        "(it must exist in this repo); (d) if it names ANOTHER fleet repo, "
        "add it to _EXTERNAL_REPO_REFS with the owning repo's marker; (e) as "
        "a last resort whitelist (template, pointer) with a written reason "
        "in tests/test_template_pointer_guard.py."
    )


def _template_pointers() -> dict[str, set[str]]:
    """Template filename -> the repo-local path pointers it emits."""
    return {
        name: _pointer_candidates(text)
        for name, text in load_templates().items()
    }


# ── the guard ────────────────────────────────────────────────────────────────


def test_every_template_pointer_resolves():
    planted_dirs = _planted_dirs()
    failures: list[str] = []
    for template, pointers in sorted(_template_pointers().items()):
        planted_dir = planted_dirs.get(template, "")
        for pointer in sorted(pointers):
            reason = _resolves(template, pointer, planted_dir)
            if reason is not None:
                failures.append(reason)
    assert not failures, "dead template pointer(s):\n\n" + "\n\n".join(failures)


def test_guard_extracts_a_meaningful_pointer_set():
    # Self-check on the extractor: if a regex/filter regression silently
    # dropped the pointer population, the main test would pass vacuously.
    # The templates carry ~45 distinct pointers today; hold a generous floor
    # and pin a few known-load-bearing ones across both categories.
    all_pointers = set().union(*_template_pointers().values())
    assert len(all_pointers) >= 30, sorted(all_pointers)
    assert "control/README.md" in all_pointers  # dominant backtick form
    assert "docs/CAPABILITIES.md" in all_pointers  # ADOPT_PLAN dest
    assert "CONSTITUTION.md" in all_pointers  # root-level, outside docs/
    assert ".session-journal.md" in all_pointers  # dotfile, outside docs/


def test_kit_self_refs_exist_in_kit_tree():
    # A template citing the kit's own source must stay true when the kit
    # refactors: a rename reds here until the templates follow.
    for pointer, reason in _KIT_SELF_REFS.items():
        assert (KIT_ROOT / pointer).is_file(), (
            f"_KIT_SELF_REFS names `{pointer}` ({reason}) but the file does "
            "not exist in the kit repo — update the templates AND this table."
        )


def test_no_stale_accounting_entries():
    # Whitelist hygiene: an entry nothing references anymore is drift — the
    # table must shrink with the templates, or it slowly becomes a bypass.
    by_template = _template_pointers()
    for (template, pointer), reason in _WHITELIST.items():
        assert pointer in by_template.get(template, set()), (
            f"stale _WHITELIST entry: {template} no longer emits `{pointer}` "
            f"({reason}) — delete the entry."
        )
    all_pointers = set().union(*by_template.values())
    for pointer in _KIT_SELF_REFS:
        assert pointer in all_pointers, (
            f"stale _KIT_SELF_REFS entry: no template emits `{pointer}` "
            "anymore — delete the entry."
        )
    for pointer, (owner, _) in _EXTERNAL_REPO_REFS.items():
        referencing = [t for t, ps in by_template.items() if pointer in ps]
        assert referencing, (
            f"stale _EXTERNAL_REPO_REFS entry: no template emits `{pointer}` "
            "anymore — delete the entry."
        )
        for template in referencing:
            assert owner in load_templates()[template], (
                f"{template} emits the cross-repo pointer `{pointer}` but "
                f"never names its owning repo ({owner!r}) — an unattributed "
                "cross-repo path reads as a dead local pointer to a cold "
                "session; name the repo next to the ref."
            )
