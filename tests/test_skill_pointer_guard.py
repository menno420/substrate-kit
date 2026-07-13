"""Skill-body pointer guard — no shipped skill carries a dead path pointer.

Groom-forward of the 💡 idea on PR #334's session card
(``.sessions/2026-07-13-template-pointer-guard.md``): a dead pointer in an
installed ``SKILL.md`` misroutes a session exactly like a template one, so the
template pointer guard's extractor + resolution-table design extends to the
skill surface (Q-0194 friction → guard, generalized to the sibling surface).

Division of labor with ``check_skill_grounds`` (which already scans skill
bodies, with its zero-findings kit invariant pinned ENFORCING by
``test_check_skill_grounds.test_kit_skill_set_fully_grounded_at_kit_root`` /
``..._grounded_even_on_empty_target``): that scan is a *command*-grounding
advisory — it judges a backticked span by its FIRST TOKEN and deliberately
fails open on everything ambiguous. Verified blind spots for *doc pointers*
at kit HEAD 7c736fa (1 and 2 CLOSED in the checker itself on 2026-07-13 —
dot-led tokens are judged with a state-dir artifact classification, and
markdown-link targets feed the same ladder — so adopter-rendered docs now
inherit the coverage; this guard remains the kit-truth SKILLS floor and the
whitelist-classification pin):

1. **Dot-led paths are never judged** — ``_FIRST_TOKEN_RE`` requires an
   alnum/underscore first character, so ``.substrate/upgrade-report.md`` (a
   live pointer in the ``upgrade-distribution`` body) is skipped as prose;
   the state-dir skip rule would fail it open even if judged.
2. **Markdown-link pointers are never extracted** — ``_SPAN_RE`` matches
   backtick spans only. Zero live instances today; this guard's floor keeps
   the class covered when one appears.
3. **Whitelist rot** — ``_KIT_SHIPPED_PATHS`` entries have no existence pin:
   a kit-side rename (say ``docs/operations/release-runbook.md``) would ship
   dead skill-body pointers with every test green — the exact bypass class
   the template guard pins via ``test_kit_self_refs_exist_in_kit_tree``.

So this guard covers WHOLE-SPAN path pointers (backtick + markdown-link,
including dot-led) with the template guard's "an adopter will actually have
it" semantics, and pins the grounds checker's kit-path whitelist against rot.
Command spans (``python3 src/build_bootstrap.py`` …) stay the grounds
checker's domain — first-token resolution is the right semantics there.

NOT in scope, verified deliberately: the staged CLAUDE.md surface is already
guarded (``load_templates()`` globs every ``*.tmpl`` including
``CLAUDE.md.tmpl``, and the template guard iterates ``load_templates()``);
seat-digest / HANDOFF emissions compute their paths from live config and
files (self-grounded, no static pointer text); skill descriptions carry no
backtick spans.

Same posture as the template guard: a kit-repo TEST, zero ``src/engine``
changes, explicit commented accounting tables, loud failures naming the fix
path, a vacuity floor so a broken extractor cannot pass silently.
"""

from __future__ import annotations

from pathlib import Path

from engine.adopt import ADOPT_PLAN
from engine.checks.check_skill_grounds import (
    _ADOPTER_PLANTED_PATHS,
    _KIT_REPO_PATHS,
    _KIT_SHIPPED_PATHS,
    _WAVE_TRANSIENT_PATHS,
)
from engine.skills.skills import SKILLS

# One extractor, one source of truth: reuse the template guard's pointer
# extraction verbatim (tests/ is a package). A charset/extension fix there
# applies here automatically — duplicating the regexes is how the two guards
# would drift apart.
from tests.test_template_pointer_guard import _pointer_candidates

KIT_ROOT = Path(__file__).resolve().parents[1]

# ── resolution tables ────────────────────────────────────────────────────────

# 1) Files every default adopt plants — a pointer to a planted file is
#    grounded on any adopter.
_PLAN_DESTS = frozenset(dest for _, dest in ADOPT_PLAN)

# 2) Artifacts the kit writes OUTSIDE ADOPT_PLAN. Each entry names the
#    writer, so a dead pointer that lands here by mistake is auditable.
_GENERATED_BY_KIT: dict[str, str] = {
    # _vendor_bootstrap copies the running single-file dist to the repo root
    # (skip-if-exists) so the skills' `python3 bootstrap.py …` steps resolve.
    "bootstrap.py": "vendored to repo root by adopt (_vendor_bootstrap)",
    # engine.upgrade writes <state_dir>/UPGRADE_REPORT_FILENAME on every
    # upgrade; the upgrade-distribution body names the default state_dir
    # spelling. THE dot-led pointer check_skill_grounds never judges.
    ".substrate/upgrade-report.md": (
        "written by upgrade (engine.upgrade.UPGRADE_REPORT_FILENAME under "
        "the default state_dir)"
    ),
}

# 3) Kit-repo self-refs: the `release` / `upgrade-distribution` runbooks are
#    kit-repo-specific by declaration ("the commands below run in the kit
#    repo"), so their kit-source pointers must exist HERE — a kit-side rename
#    reds this guard until the skill bodies follow.
_KIT_SELF_REFS: dict[str, str] = {
    "dist/bootstrap.py": "the committed dist the sha256 three-way pins",
    "src/engine/lib/config.py": "KIT_VERSION home named by the release runbook",
    "pyproject.toml": "second version home named by the release runbook",
    "CHANGELOG.md": "release precondition named by the release runbook",
    "docs/adopters.md": "registry regenerated in the release aftermath step",
    "docs/operations/release-runbook.md": (
        "canonical prose the release skill cites as its source"
    ),
}

# 4) Release-wave transients: files that exist only mid-wave or as published
#    release assets — never in any committed tree. Named by the consumer flow
#    (release.json's own instructions) and the release workflow's assets.
_WAVE_TRANSIENTS: dict[str, str] = {
    "bootstrap.py.new": "mid-wave download name the consumer flow specifies",
    "bootstrap.py.sha256": "published release asset (release.yml)",
    "release.json": "published release asset carrying the sha256 field",
}

# 5) The explicit whitelist — (skill name, pointer) -> written reason. Empty
#    today; the escape hatch stays declared so the failure message's fix path
#    (e) has a real destination. An entry without a live reason is drift.
_WHITELIST: dict[tuple[str, str], str] = {}


def _skill_pointers() -> dict[str, set[str]]:
    """Skill name -> the repo-local path pointers its body emits."""
    return {skill["name"]: _pointer_candidates(skill["body"]) for skill in SKILLS}


def _resolves(skill_name: str, pointer: str) -> str | None:
    """Return None when ``pointer`` is accounted for, else the failure reason."""
    if pointer in _PLAN_DESTS:
        return None
    if pointer in _GENERATED_BY_KIT:
        return None
    if pointer in _KIT_SELF_REFS:
        return None
    if pointer in _WAVE_TRANSIENTS:
        return None
    if (skill_name, pointer) in _WHITELIST:
        return None
    return (
        f"skill `{skill_name}` points at `{pointer}`, which no adopter will "
        "have: it is not an ADOPT_PLAN destination, not a kit-generated "
        "artifact, not a kit-repo self-ref, and not a release-wave "
        "transient.\n"
        "Fix: (a) point at a planted file instead; (b) if adopt/upgrade "
        "really writes it, add it to _GENERATED_BY_KIT naming the writer; "
        "(c) if it names the KIT repo's own source, add it to _KIT_SELF_REFS "
        "(it must exist in this repo); (d) if it exists only mid-release-"
        "wave, add it to _WAVE_TRANSIENTS with the flow that names it; (e) "
        "as a last resort whitelist (skill, pointer) with a written reason "
        "in tests/test_skill_pointer_guard.py."
    )


# ── the guard ────────────────────────────────────────────────────────────────


def test_every_skill_pointer_resolves():
    failures: list[str] = []
    for skill_name, pointers in sorted(_skill_pointers().items()):
        for pointer in sorted(pointers):
            reason = _resolves(skill_name, pointer)
            if reason is not None:
                failures.append(reason)
    assert not failures, "dead skill-body pointer(s):\n\n" + "\n\n".join(failures)


def test_guard_extracts_a_meaningful_pointer_set():
    # Vacuity floor: the bodies carry 18 distinct pointers today — hold a
    # generous floor and pin known-load-bearing ones across the classes,
    # including the dot-led pointer check_skill_grounds cannot judge.
    all_pointers = set().union(*_skill_pointers().values())
    assert len(all_pointers) >= 12, sorted(all_pointers)
    assert ".substrate/upgrade-report.md" in all_pointers  # dot-led class
    assert "docs/CAPABILITIES.md" in all_pointers  # ADOPT_PLAN dest
    assert "CONSTITUTION.md" in all_pointers  # root-level dest
    assert "docs/operations/release-runbook.md" in all_pointers  # kit self-ref


def test_kit_self_refs_exist_in_kit_tree():
    # A skill citing the kit's own source must stay true when the kit
    # refactors: a rename reds here until the skill bodies follow.
    for pointer, reason in _KIT_SELF_REFS.items():
        assert (KIT_ROOT / pointer).is_file(), (
            f"_KIT_SELF_REFS names `{pointer}` ({reason}) but the file does "
            "not exist in the kit repo — update the skill bodies AND this "
            "table."
        )


def test_no_stale_accounting_entries():
    # Table hygiene: an entry no skill emits anymore is drift — the tables
    # must shrink with the bodies, or they slowly become a bypass.
    by_skill = _skill_pointers()
    all_pointers = set().union(*by_skill.values())
    for table_name, table in (
        ("_GENERATED_BY_KIT", _GENERATED_BY_KIT),
        ("_KIT_SELF_REFS", _KIT_SELF_REFS),
        ("_WAVE_TRANSIENTS", _WAVE_TRANSIENTS),
    ):
        for pointer in table:
            assert pointer in all_pointers, (
                f"stale {table_name} entry: no skill body emits `{pointer}` "
                "anymore — delete the entry."
            )
    for (skill_name, pointer), reason in _WHITELIST.items():
        assert pointer in by_skill.get(skill_name, set()), (
            f"stale _WHITELIST entry: skill `{skill_name}` no longer emits "
            f"`{pointer}` ({reason}) — delete the entry."
        )


def test_skill_grounds_kit_path_whitelist_cannot_rot():
    # The rot pin (blind spot 3), now over the engine's OWN classification
    # tables (single source of truth — check_skill_grounds ships the classes;
    # this test pins them): every _KIT_SHIPPED_PATHS entry must be accounted
    # for — an ADOPT_PLAN destination (planted on every adopter), a named
    # release-wave transient, a kit-generated artifact, or a file that
    # actually exists in the kit tree. Without this, a kit-side rename
    # leaves a whitelist entry that resolves dead pointers forever.
    for entry in sorted(_KIT_SHIPPED_PATHS):
        if entry in _PLAN_DESTS:
            continue
        if entry in _WAVE_TRANSIENTS:
            continue
        if entry in _GENERATED_BY_KIT:
            continue
        assert (KIT_ROOT / entry).is_file(), (
            f"check_skill_grounds._KIT_SHIPPED_PATHS whitelists `{entry}`, "
            "but it is not planted by ADOPT_PLAN, not a known release-wave "
            "transient or kit-generated artifact, and does not exist in the "
            "kit tree — the whitelist entry is rot and now resolves dead "
            "pointers. Remove or fix the entry (or classify it in "
            "tests/test_skill_pointer_guard.py with a written reason)."
        )


def test_skill_grounds_whitelist_classes_disjoint_and_exhaustive():
    # The classes must partition the union: an entry in two classes has two
    # contradictory resolution stories; an entry in none is unclassified
    # (the derived-union definition makes "in none" unreachable today —
    # this pin keeps it that way if the union is ever hand-edited).
    classes = {
        "_KIT_REPO_PATHS": _KIT_REPO_PATHS,
        "_WAVE_TRANSIENT_PATHS": _WAVE_TRANSIENT_PATHS,
        "_ADOPTER_PLANTED_PATHS": _ADOPTER_PLANTED_PATHS,
    }
    names = sorted(classes)
    for i, a in enumerate(names):
        for b in names[i + 1 :]:
            overlap = classes[a] & classes[b]
            assert not overlap, (
                f"{a} and {b} both claim {sorted(overlap)} — a whitelist "
                "entry must have exactly one resolution story."
            )
    union = frozenset().union(*classes.values())
    assert union == _KIT_SHIPPED_PATHS, (
        "class union and _KIT_SHIPPED_PATHS diverge: "
        f"only-in-union={sorted(union - _KIT_SHIPPED_PATHS)}, "
        f"only-in-shipped={sorted(_KIT_SHIPPED_PATHS - union)}"
    )


def test_skill_grounds_kit_repo_class_pinned_to_kit_tree():
    # The existence pin the raw in-adopter check could never be (the
    # 2026-07-13 survey measured a raw existence pin at 14–15 FALSE findings
    # per adopter): kit-repo-class entries must exist HERE, in the kit tree.
    for entry in sorted(_KIT_REPO_PATHS):
        assert (KIT_ROOT / entry).is_file(), (
            f"check_skill_grounds._KIT_REPO_PATHS pins `{entry}` as a "
            "kit-repo file, but it does not exist in the kit tree — a "
            "kit-side rename must update the whitelist class AND the skill "
            "bodies that name it."
        )


def test_skill_grounds_transient_and_planted_classes_agree_with_tables():
    # Single source of truth both ways: the engine's wave-transient class
    # and this guard's reason-annotated _WAVE_TRANSIENTS table must name the
    # same set, and every adopter-planted entry needs a writer recorded in
    # _GENERATED_BY_KIT — an unexplained class entry is drift.
    assert set(_WAVE_TRANSIENTS) == set(_WAVE_TRANSIENT_PATHS), (
        "engine _WAVE_TRANSIENT_PATHS and the guard's _WAVE_TRANSIENTS "
        "reason table diverged: "
        f"engine-only={sorted(set(_WAVE_TRANSIENT_PATHS) - set(_WAVE_TRANSIENTS))}, "
        f"table-only={sorted(set(_WAVE_TRANSIENTS) - set(_WAVE_TRANSIENT_PATHS))}"
    )
    for entry in sorted(_ADOPTER_PLANTED_PATHS):
        assert entry in _GENERATED_BY_KIT, (
            f"check_skill_grounds._ADOPTER_PLANTED_PATHS names `{entry}` "
            "but _GENERATED_BY_KIT records no writer for it — name the "
            "adopt/upgrade code path that plants it."
        )
