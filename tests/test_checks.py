"""Tests for the generic, config-driven hygiene checkers (the 1b tail port).

Covers the doc checker (badge / link / reachable) and the session-log marker
checker, plus a render->check integration that proves the kit's own rendered
templates pass its own ``check_docs`` (the plan's verification goal d).
"""

from pathlib import Path

from engine.checks.check_docs import (
    Finding,
    check_badges,
    check_links,
    check_reachable,
    run_doc_checks,
)
from engine.checks.check_session_log import (
    BORN_RED_HOLD_MESSAGE,
    NO_BADGE_MESSAGE,
    VALUELESS_BADGE_MESSAGE,
    check_added_card,
    check_log,
    has_status_badge,
    latest_session_log,
    missing_markers,
    status_in_progress,
)
from engine.interview.question_bank import QUESTIONS
from engine.lib.config import Config
from engine.render import (
    ENGINE_CONTEXT_KEYS,
    build_context,
    find_placeholders,
    load_templates,
    render,
)

_TOKENS = Config().badge_tokens
_READPATH = Config().readpath_docs
_MARKERS = Config().session_markers


def _write(p: Path, text: str) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ---------------------------------------------------------------------------
# Badges
# ---------------------------------------------------------------------------


def test_badge_valid_passes(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "ok.md", "# Title\n\n> **Status:** `binding`\n\nbody\n")
    assert check_badges(docs, _TOKENS) == []


def test_badge_missing_flagged(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "bare.md", "# Title\n\nbody only, no badge\n")
    viol = check_badges(docs, _TOKENS)
    assert len(viol) == 1
    assert viol[0].kind == "badge" and "missing" in viol[0].message


def test_badge_invalid_token_flagged(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "weird.md", "# Title\n\n> **Status:** `bogus`\n")
    viol = check_badges(docs, _TOKENS)
    assert len(viol) == 1 and "invalid badge token" in viol[0].message


def test_badge_custom_taxonomy_respected(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "x.md", "# X\n\n> **Status:** `bespoke`\n")
    assert check_badges(docs, ["bespoke"]) == []
    assert len(check_badges(docs, ["binding"])) == 1


def test_adr_is_exempt_from_badge(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "decisions" / "001-no-redis.md", "# ADR-001\n\n**Status:** Accepted\n")
    assert check_badges(docs, _TOKENS) == []


def test_badges_empty_when_docs_root_absent(tmp_path):
    assert check_badges(tmp_path / "nope", _TOKENS) == []


# ---------------------------------------------------------------------------
# Links
# ---------------------------------------------------------------------------


def test_links_dead_flagged_valid_and_external_ok(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "target.md", "# Target\n\n> **Status:** `reference`\n")
    _write(
        docs / "a.md",
        "# A\n\n> **Status:** `reference`\n\n"
        "[good](target.md) [dead](nope.md) "
        "[ext](https://example.com) [anchor](#x)\n",
    )
    viol = check_links(docs)
    assert len(viol) == 1
    assert viol[0].kind == "link" and "nope.md" in viol[0].message


# ---------------------------------------------------------------------------
# Reachability
# ---------------------------------------------------------------------------


def test_reachable_orphan_flagged_linked_ok(tmp_path):
    docs = tmp_path / "docs"
    # AGENT_ORIENTATION is a read-path root; it links good.md (markdown) and
    # sub.md (backtick `docs/...` ref). orphan.md is linked from nowhere.
    _write(
        docs / "AGENT_ORIENTATION.md",
        "# O\n\n> **Status:** `reference`\n\n[good](good.md) and `docs/sub.md`\n",
    )
    _write(docs / "good.md", "# Good\n\n> **Status:** `reference`\n")
    _write(docs / "sub.md", "# Sub\n\n> **Status:** `reference`\n")
    _write(docs / "orphan.md", "# Orphan\n\n> **Status:** `reference`\n")
    viol = check_reachable(docs, _READPATH)
    assert [v.path for v in viol] == ["orphan.md"]
    assert viol[0].kind == "reachable"


def test_reachable_exempt_badges_and_adr_ok(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "AGENT_ORIENTATION.md", "# O\n\n> **Status:** `reference`\n")
    # Retired badges need no inbound link; ADRs are exempt.
    _write(docs / "old.md", "# Old\n\n> **Status:** `historical`\n")
    _write(docs / "gone.md", "# Gone\n\n> **Status:** `archive`\n")
    _write(docs / "decisions" / "009-x.md", "# ADR\n\n**Status:** Accepted\n")
    assert check_reachable(docs, _READPATH) == []


def test_reachable_readme_is_a_root(tmp_path):
    docs = tmp_path / "docs"
    # No read-path docs exist, but a README links the doc -> reachable.
    _write(docs / "sub" / "README.md", "# R\n\n> **Status:** `reference`\n\n[x](child.md)\n")
    _write(docs / "sub" / "child.md", "# C\n\n> **Status:** `reference`\n")
    assert check_reachable(docs, _READPATH) == []


# ---------------------------------------------------------------------------
# Aggregate
# ---------------------------------------------------------------------------


def test_run_doc_checks_combines_kinds(tmp_path):
    docs = tmp_path / "docs"
    _write(docs / "AGENT_ORIENTATION.md", "# O\n\n> **Status:** `reference`\n")
    _write(docs / "nobadge.md", "# N\n\nno badge, also an orphan\n")
    kinds = {f.kind for f in run_doc_checks(docs, _TOKENS, _READPATH)}
    assert kinds == {"badge", "reachable"}


def test_clean_tree_has_no_findings(tmp_path):
    docs = tmp_path / "docs"
    _write(
        docs / "AGENT_ORIENTATION.md",
        "# O\n\n> **Status:** `reference`\n\n[cs](current-state.md)\n",
    )
    _write(docs / "current-state.md", "# CS\n\n> **Status:** `living-ledger`\n")
    assert run_doc_checks(docs, _TOKENS, _READPATH) == []


# ---------------------------------------------------------------------------
# Session log
# ---------------------------------------------------------------------------


def test_missing_markers_complete_vs_incomplete():
    full = (
        "> **Status:** `reference`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n"
    )
    assert missing_markers(full, _MARKERS) == []
    bare = "nothing here\n"
    # A miss names the label AND the exact byte-form expected (the run-1
    # ON-arm false-red fix, idea model-line-checker-false-red-2026-07-09:
    # a bare "missing: Model line" against a card visibly carrying a Model
    # line told the agent nothing about which needle the scan wanted).
    assert missing_markers(bare, _MARKERS) == [
        f"{m['label']} (expected `{m['needle']}`)" for m in _MARKERS
    ]


def test_missing_markers_custom_set():
    markers = [{"label": "Sign-off", "needle": "signed-off-by"}]
    assert missing_markers("Signed-off-by: me", markers) == []
    assert missing_markers("no trailer", markers) == [
        "Sign-off (expected `signed-off-by`)"
    ]


def test_missing_markers_miss_names_the_model_line_byte_form():
    # The canonical run-1 ON-arm case: the card carries `> **Model:** …` but
    # not the configured `📊 Model:` needle — the red must name the expected
    # byte-form, never contradict what the agent can see on the card.
    card = (
        "> **Status:** `complete`\n\n💡 idea\n\nprevious-session review: ok\n\n"
        "> **Model:** claude-x\n"
    )
    assert missing_markers(card, _MARKERS) == ["Model line (expected `📊 Model:`)"]


def test_latest_session_log_picks_newest_skips_readme(tmp_path):
    sessions = tmp_path / ".sessions"
    sessions.mkdir()
    _write(sessions / "README.md", "convention doc\n")
    old = sessions / "2026-06-01-a.md"
    new = sessions / "2026-06-02-b.md"
    _write(old, "old\n")
    _write(new, "new\n")
    import os

    os.utime(old, (1000, 1000))
    os.utime(new, (2000, 2000))
    assert latest_session_log(sessions) == new


def test_latest_session_log_none_when_absent_or_empty(tmp_path):
    assert latest_session_log(tmp_path / "nope") is None
    empty = tmp_path / ".sessions"
    empty.mkdir()
    assert latest_session_log(empty) is None


def test_check_log_unreadable_returns_all_labels(tmp_path):
    missing = check_log(tmp_path / "does-not-exist.md", _MARKERS)
    assert missing == [
        f"{m['label']} (expected `{m['needle']}`)" for m in _MARKERS
    ]


def test_in_progress_status_keeps_the_card_incomplete(tmp_path):
    # The KL-1 PR #9 lesson: a card can carry every marker needle (inherited
    # from an earlier PR on a shared card) while its Status badge still says
    # in-progress — presence-only checking read born-red as green and
    # auto-merge landed the PR without its close-out. The status VALUE is
    # part of completeness.
    card = tmp_path / "2026-07-09-x.md"
    _write(
        card,
        "# x\n\n> **Status:** `in-progress`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    missing = check_log(card, _MARKERS)
    assert missing == ["a completed Status (badge still says in-progress)"]
    # Flipping the badge (everything else unchanged) opens the door.
    _write(
        card,
        "# x\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_log(card, _MARKERS) == []


def test_check_log_valueless_badge_is_a_grammar_finding_not_a_release(tmp_path):
    # The #426 card's filed 💡, graduated: a MODIFIED card whose badge LINE
    # carries no VALUE makes `status_in_progress` False (no value → not
    # in-progress), so before this branch a valueless card carrying every
    # marker passed `check_log` clean — the symmetric false-green PR #426
    # closed only on the added-card lane. A valueless badge is a grammar
    # finding on the modified-card lane too.
    card = tmp_path / "2026-07-16-vl.md"
    _write(
        card,
        "# vl\n\n> **Status:**\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    missing = check_log(card, _MARKERS)
    assert VALUELESS_BADGE_MESSAGE in missing
    assert "Status badge VALUE" in missing[0]
    assert missing != []
    # Whitespace-only remainder parses valueless too.
    _write(
        card,
        "# vl\n\n> **Status:**   \n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    missing = check_log(card, _MARKERS)
    assert VALUELESS_BADGE_MESSAGE in missing
    assert "Status badge VALUE" in missing[0]


def test_check_log_valueless_branch_leaves_real_values_alone(tmp_path):
    # The neighbouring states are untouched on the modified-card lane: an
    # in-progress badge still yields the completeness miss (not the valueless
    # one), and a `complete` badge with all markers passes clean.
    card = tmp_path / "2026-07-16-vr.md"
    _write(
        card,
        "# vr\n\n> **Status:** `in-progress`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_log(card, _MARKERS) == [
        "a completed Status (badge still says in-progress)"
    ]
    _write(
        card,
        "# vr\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_log(card, _MARKERS) == []


def test_check_log_without_any_badge_is_a_grammar_finding(tmp_path):
    card = tmp_path / "2026-07-16-c.md"
    _write(card, "# c\n\nnotes, no Status badge line at all\n")
    findings = check_log(card, _MARKERS)
    assert NO_BADGE_MESSAGE in findings


def test_both_card_lanes_flag_a_missing_badge_identically(tmp_path):
    body = "# x\n\n## Session idea\nfree-form, no badge\n"
    added = tmp_path / "2026-07-16-added.md"
    modified = tmp_path / "2026-07-16-modified.md"
    _write(added, body)
    _write(modified, body)
    assert NO_BADGE_MESSAGE in check_added_card(added, _MARKERS)
    assert NO_BADGE_MESSAGE in check_log(modified, _MARKERS)


def test_status_in_progress_token_variants():
    assert status_in_progress("> **Status:** `WIP`\n")
    assert status_in_progress("> **Status:** in progress\n")
    assert status_in_progress("> **Status:** `hold` — waiting\n")
    assert not status_in_progress("> **Status:** `complete`\n")
    assert not status_in_progress("no badge at all\n")


# The auto-drafted badge prose, verbatim from ``draft_card`` — the badge
# line's parenthetical says "auto-drafted", which CONTAINS the hold token
# "drafted". Only the VALUE decides the state.
_AUTO_DRAFT_BADGE = (
    "# card\n\n"
    "> **Status:** `{value}` *(auto-drafted by substrate-kit — edit the\n"
    "> close-out, resolve every slot, then flip this badge to\n"
    "> `complete`.)*\n\n"
)


def test_status_in_progress_judges_the_value_not_the_line_prose():
    # The false-hold regression (the #420 card's filed bug): the old
    # substring scan matched "drafted" inside the badge prose "auto-drafted"
    # and held a card whose VALUE reads `complete`. The value decides:
    # `in-progress` with that prose HOLDS; `complete` with the SAME prose
    # RELEASES.
    assert status_in_progress(_AUTO_DRAFT_BADGE.format(value="in-progress"))
    assert not status_in_progress(_AUTO_DRAFT_BADGE.format(value="complete"))


def test_status_in_progress_value_boundaries():
    # Tokens count only at the value's start, on a word boundary.
    assert not status_in_progress("> **Status:** `holding`\n")  # not `hold`
    assert status_in_progress("> **Status:** `in-progress · slice 1`\n")
    # A bare (unbackticked) value with trailing prose that merely MENTIONS a
    # hold token releases — the value is `complete`, the prose is commentary.
    assert not status_in_progress("> **Status:** complete — drafted skeleton adopted\n")
    # A badge line with no value at all is not in-progress.
    assert not status_in_progress("> **Status:**\n")


def test_added_card_with_auto_draft_prose_releases_on_complete(tmp_path):
    # End-to-end through the gate's added-card lane: a card that flipped its
    # VALUE to `complete` but kept the auto-draft parenthetical on the badge
    # line must get the full completeness check (and pass with its markers),
    # not the born-red HOLD the substring scan produced.
    card = tmp_path / "2026-07-16-c.md"
    _write(
        card,
        _AUTO_DRAFT_BADGE.format(value="complete")
        + "💡 idea\n\nprevious-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_added_card(card, _MARKERS) == []
    # Same prose, value still in-progress: the designed HOLD stands.
    _write(card, _AUTO_DRAFT_BADGE.format(value="in-progress"))
    assert check_added_card(card, _MARKERS) == [BORN_RED_HOLD_MESSAGE]


def test_has_status_badge_detects_presence_not_value():
    assert has_status_badge("> **Status:** `in-progress`\n")
    assert has_status_badge("> **Status:** `complete`\n")
    assert not has_status_badge("# card with no badge at all\n💡 idea\n")


def test_added_card_born_red_is_the_hold(tmp_path):
    # The superbot-games #40 loophole fix: an ADDED card that declares
    # in-progress is the born-red HOLD — one designed-state finding, never
    # green (the old full exemption let a card-only born-red PR with
    # auto-merge pre-armed merge in 24 s) and never a completeness grade
    # (mid-flight incompleteness stays unjudged; no marker findings).
    card = tmp_path / "2026-07-11-a.md"
    _write(card, "# a\n\n> **Status:** `in-progress`\n\nabout to do X\n")
    assert check_added_card(card, _MARKERS) == [BORN_RED_HOLD_MESSAGE]


def test_added_card_drafted_is_the_hold_too(tmp_path):
    # `drafted` is an in-progress value (KL-5): an auto-drafted added card
    # holds exactly like born-red.
    card = tmp_path / "2026-07-11-e.md"
    _write(card, "# e\n\n> **Status:** `drafted`\n")
    assert check_added_card(card, _MARKERS) == [BORN_RED_HOLD_MESSAGE]


def test_added_card_without_any_badge_is_a_grammar_finding(tmp_path):
    # Born-red exempts the badge's VALUE, never its presence: a card with no
    # parseable Status badge is malformed from its first commit.
    card = tmp_path / "2026-07-11-b.md"
    _write(card, "# b\n\n## Session idea\nfree-form, no badge\n")
    misses = check_added_card(card, _MARKERS)
    assert len(misses) == 1
    assert NO_BADGE_MESSAGE in misses


def test_added_card_valueless_badge_is_a_grammar_finding_not_a_release(tmp_path):
    # The #422 card's filed 💡: a badge LINE with no VALUE used to fall
    # through to the completeness check as if it had declared `complete` —
    # a card carrying every marker then RELEASED the gate while declaring
    # nothing. A valueless badge is a grammar finding that HOLDS.
    card = tmp_path / "2026-07-16-v.md"
    _write(
        card,
        "# v\n\n> **Status:**\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    misses = check_added_card(card, _MARKERS)
    assert len(misses) == 1
    assert "Status badge VALUE" in misses[0]
    assert misses != [BORN_RED_HOLD_MESSAGE]
    # Whitespace-only remainder parses valueless too.
    _write(card, "# v\n\n> **Status:**   \n")
    misses = check_added_card(card, _MARKERS)
    assert len(misses) == 1
    assert "Status badge VALUE" in misses[0]


def test_added_card_valueless_branch_leaves_real_values_alone(tmp_path):
    # The neighbouring states are untouched: in-progress still HOLDs with
    # the designed born-red message, complete still gets the full check.
    card = tmp_path / "2026-07-16-w.md"
    _write(card, "# w\n\n> **Status:** `in-progress`\n")
    assert check_added_card(card, _MARKERS) == [BORN_RED_HOLD_MESSAGE]
    _write(
        card,
        "# w\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_added_card(card, _MARKERS) == []


def test_added_card_claiming_complete_gets_the_full_check(tmp_path):
    # The venture-lab #15 false-green class: an ADDED card declaring
    # `complete` while missing its grammar tokens (💡 / 📊 Model:) merged
    # green under the old full exemption and pre-reddened every later bare
    # `check --strict` run. Declared-complete → judged as complete.
    card = tmp_path / "2026-07-11-c.md"
    _write(
        card,
        "# c\n\n> **Status:** `complete`\n\n## Session idea\nno needle\n"
        "\n## Model\nCoordinator seat: opus-x\n",
    )
    misses = check_added_card(card, _MARKERS)
    assert misses == check_log(card, _MARKERS)
    assert any("Model line" in m for m in misses)
    assert any("Session idea" in m for m in misses)


def test_added_card_complete_and_well_formed_is_clean(tmp_path):
    card = tmp_path / "2026-07-11-d.md"
    _write(
        card,
        "# d\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n📊 Model: m · e · docs-only\n",
    )
    assert check_added_card(card, _MARKERS) == []


def test_added_card_unreadable_is_named_honestly(tmp_path):
    misses = check_added_card(tmp_path / "absent.md", _MARKERS)
    assert misses == ["an unreadable added card (cannot grammar-check)"]


# ── R13: exit-affecting PL-004 task-class gate on the PR's OWN added card ────
# The fleet-wide `check_model_line` advisory is windowed + never exit-affecting,
# so an off-taxonomy class on a NEW card merges green. `check_added_card` folds
# the same rule in EXIT-AFFECTING, scoped to the single added card: an
# off-taxonomy class on the PR's own complete card reds like an unflipped badge,
# a VALID class passes, and a card with NO `📊 Model:` line is fail-open.


def test_added_card_valid_task_class_yields_no_task_class_finding(tmp_path):
    # Direction 1 (passes): an otherwise-complete card whose `📊 Model:`
    # task-class IS one of the 9 PL-004 classes gets no task-class finding.
    card = tmp_path / "2026-07-19-tc-ok.md"
    _write(
        card,
        "# ok\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n"
        "- **📊 Model:** opus-4.8 · high · feature build\n",
    )
    assert check_added_card(card, _MARKERS) == []


def test_added_card_off_taxonomy_task_class_reds(tmp_path):
    # Direction 2 (reds): the SAME card with only the task-class changed to an
    # off-taxonomy value (`kit-feature`) gains exactly one task-class finding
    # (and nothing else — every marker is present).
    card = tmp_path / "2026-07-19-tc-bad.md"
    _write(
        card,
        "# bad\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n"
        "- **📊 Model:** opus-4.8 · high · kit-feature\n",
    )
    misses = check_added_card(card, _MARKERS)
    assert len(misses) == 1
    assert "off-taxonomy" in misses[0]
    assert "'kit-feature'" in misses[0]
    assert "feature build" in misses[0]  # the 9 valid classes are listed


def test_added_card_missing_model_line_is_fail_open_for_task_class(tmp_path):
    # Fail-open: a complete card with NO `📊 Model:` needle gains no NEW
    # task-class finding — the missing-line case is the marker checks' job
    # (`check_log`), never a double-red here. The card still reds on the
    # missing Model-line MARKER, so `check_added_card` == `check_log` exactly.
    card = tmp_path / "2026-07-19-tc-none.md"
    _write(
        card,
        "# none\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n",  # no 📊 Model: line at all
    )
    misses = check_added_card(card, _MARKERS)
    assert misses == check_log(card, _MARKERS)  # no extra task-class finding
    assert not any("off-taxonomy" in m for m in misses)
    assert any("Model line" in m for m in misses)  # marker miss still reds


def test_added_card_decorated_valid_task_class_passes(tmp_path):
    # Prefix-match on purpose: a decorated valid class (`feature build (...)`)
    # is a valid report — the same tail the repo's real cards carry — not drift.
    card = tmp_path / "2026-07-19-tc-decorated.md"
    _write(
        card,
        "# dec\n\n> **Status:** `complete`\n\n💡 idea\n\n"
        "previous-session review: ok\n\n"
        "- **📊 Model:** Opus 4.8 · high · feature build (the gate + tests)\n",
    )
    assert check_added_card(card, _MARKERS) == []


# ---------------------------------------------------------------------------
# Integration — the kit's own rendered templates pass its own check_docs
# ---------------------------------------------------------------------------


def test_rendered_templates_are_badge_and_link_clean(tmp_path):
    """Verification goal (d): generated docs pass the engine's own check_docs.

    Render every template with a fully-filled context into a flat docs tree and
    assert zero badge + link findings. (Reachability is host-layout dependent —
    a host files CLAUDE.md under .claude/, the journal at the root — so it is
    exercised by the synthetic-tree tests above, not this flat render.)
    """
    docs = tmp_path / "docs"
    context = {q["slot"]: f"v-{q['slot']}" for q in QUESTIONS}
    # Engine-computed keys (build_context injects them on every live path).
    context.update({key: f"v-{key}" for key in ENGINE_CONTEXT_KEYS})
    for name, text in load_templates().items():
        rendered = render(text, context)
        assert find_placeholders(rendered) == set(), f"{name} left placeholders"
        out_name = name[:-5] if name.endswith(".tmpl") else name
        if out_name in ("control-inbox.md", "control-status.md"):
            # The two protocol skeletons are message-bus files, not docs:
            # their format is fixed by the control/ contract (KL-8) and they
            # are planted outside docs_root, so the badge rule never applies.
            continue
        _write(docs / out_name, rendered)
    assert check_badges(docs, _TOKENS) == []
    assert check_links(docs) == []


def test_finding_is_a_named_triple():
    f = Finding("p.md", "badge", "msg")
    assert (f.path, f.kind, f.message) == ("p.md", "badge", "msg")
