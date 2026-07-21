"""Tests for the no-false-walls ENGINE leg — the propagated `check --strict`
guard that reds EVERY adopter (not just substrate-kit) when a session
documents a FALSE agent-capability limitation into its own forward docs.

The grammar/blocklist/clearing logic lives once in
``engine.checks.check_no_false_walls`` (the standalone ``tools/`` wrapper
delegates to it — no duplicate logic). These tests cover the engine surfaces an
ADOPTER has (live ``docs/``, root ``CONSTITUTION.md`` / ``CAPABILITIES.md``,
live ``.claude/**``) and the exit-affecting wiring through ``cmd_check``. The
#449 must-fail / must-pass fixtures are re-exercised here on the adopter surface
so the shared core stays honest.
"""

from __future__ import annotations

from pathlib import Path

import pytest

pytest.importorskip("engine.hooks.settings")

from engine.checks.check_no_false_walls import (
    _UNKNOWN_RULE_CORRECTION,
    WALL_CORRECTIONS,
    check_no_false_walls,
    scan_text,
)
from engine.cli import cmd_check
from engine.lib.config import Config, save_config

# The #449 spread — each is a standing FALSE capability wall (owner directive
# 2026-07-18): subject-negated, owner-only, or platform-walled.
_MUST_FAIL = (
    "agents do NOT arm auto-merge — classifier-denied since 2026-07-15\n",
    "The owner is the merge authority for every session PR.\n",
    "A green PR is agent-unlandable; route it to the owner.\n",
    "Sessions may not self-merge their own PRs.\n",
    "agents cannot delete branches\n",
    "sessions are not allowed to update Railway variables\n",
    "branch deletion is owner-only\n",
    "deploying is classifier-denied for agent seats\n",
    "the owner must merge PRs\n",
    "merging is owner-gated\n",
    "the bot cannot push to protected branches\n",
)

# The phrasing we WANT adopters to keep — corrected doctrine, CODE rules,
# genuine dated walls, missing-input requests.
_MUST_PASS = (
    "merging is normal agent work; never route a mergeable green PR to the owner\n",
    "there are NO owner-imposed limitations\n",
    "services must not import views\n",
    "utils/ may not import services\n",
    "never call pool.execute directly outside utils/db\n",
    "needs a Stripe account from the owner\n",
    "session tokens cannot create repos (gen-1 wall)\n",
    "this repo's sessions cannot read fleet-manager directly\n",
)


def _plant(root: Path, rel: str, text: str) -> None:
    p = root / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


# ── The shared core stays honest on the #449 fixtures ─────────────────────────


class TestSharedCoreParity:
    def test_must_fail_lines_are_caught(self) -> None:
        for text in _MUST_FAIL:
            assert scan_text(text), f"shared core should catch: {text!r}"

    def test_must_pass_lines_are_cleared(self) -> None:
        for text in _MUST_PASS:
            assert scan_text(text) == [], f"shared core tripped on: {text!r}"


# ── The engine leg on each adopter surface ────────────────────────────────────


class TestAdopterSurfaces:
    def test_flags_false_wall_in_live_docs(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/current-state.md", _MUST_FAIL[0])
        findings = check_no_false_walls(tmp_path, Config())
        assert len(findings) == 1
        assert findings[0].kind.startswith("false-wall:")
        assert findings[0].path == "docs/current-state.md"

    def test_flags_false_wall_in_root_constitution(self, tmp_path: Path) -> None:
        _plant(tmp_path, "CONSTITUTION.md", _MUST_FAIL[1])
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == ["CONSTITUTION.md"]

    def test_flags_false_wall_in_live_claude_skill_body(self, tmp_path: Path) -> None:
        # An adopter's live .claude skill/rule body is a forward-binding surface.
        _plant(tmp_path, ".claude/skills/merge/SKILL.md", _MUST_FAIL[3])
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == [".claude/skills/merge/SKILL.md"]

    def test_every_must_fail_variant_reds(self, tmp_path: Path) -> None:
        for text in _MUST_FAIL:
            _plant(tmp_path, "docs/d.md", text)
            assert check_no_false_walls(tmp_path, Config()), f"missed: {text!r}"

    def test_every_must_pass_variant_is_silent(self, tmp_path: Path) -> None:
        for text in _MUST_PASS:
            _plant(tmp_path, "docs/d.md", text)
            assert check_no_false_walls(tmp_path, Config()) == [], f"tripped: {text!r}"


# ── Exclusions carried over from #449 ─────────────────────────────────────────


class TestExclusions:
    def test_historical_dir_is_skipped(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/retro/old.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_dated_filename_is_skipped(self, tmp_path: Path) -> None:
        _plant(tmp_path, "docs/2026-07-12-report.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_dated_ledger_bullet_is_cleared(self, tmp_path: Path) -> None:
        _plant(
            tmp_path,
            "docs/CAPABILITIES.md",
            "- 2026-07-16 · wall · An agent session cannot merge a SIBLING PR "
            "— the classifier denies it.\n",
        )
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_false_quote_repudiation_is_cleared(self, tmp_path: Path) -> None:
        _plant(
            tmp_path,
            "docs/d.md",
            '> FALSE "agents do NOT ready-flip / arm — classifier-denied"\n',
        )
        assert check_no_false_walls(tmp_path, Config()) == []


# ── Self-quiet + honors a non-default docs_root ───────────────────────────────


class TestSelfGating:
    def test_bare_tree_is_silent(self, tmp_path: Path) -> None:
        assert check_no_false_walls(tmp_path, Config()) == []

    def test_honors_configured_docs_root(self, tmp_path: Path) -> None:
        cfg = Config(docs_root="documentation")
        _plant(tmp_path, "documentation/d.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, cfg), "non-default docs_root missed"

    def test_skips_state_and_sessions_dirs(self, tmp_path: Path) -> None:
        # A false wall inside a dated session card / staged kit material is
        # history, not forward doctrine — never scanned.
        _plant(tmp_path, ".sessions/2026-07-18-x.md", _MUST_FAIL[0])
        _plant(tmp_path, ".substrate/claude/CLAUDE.md", _MUST_FAIL[0])
        assert check_no_false_walls(tmp_path, Config()) == []


# ── S6: the finding message inlines the rule's per-rule ground-truth correction ─


class TestFindingCarriesCorrection:
    def test_message_inlines_the_rule_specific_correction(self, tmp_path: Path) -> None:
        # Every must-fail line's finding message names its rule AND carries the
        # rule's WALL_CORRECTIONS sentence (or the unknown-rule fallback) inline —
        # not just the generic blurb — so the red gate states the specific truth.
        for text in _MUST_FAIL:
            _plant(tmp_path, "docs/d.md", text)
            findings = check_no_false_walls(tmp_path, Config())
            assert findings, f"expected a finding for: {text!r}"
            for f in findings:
                rule = f.kind.split("false-wall:", 1)[1]
                expected = WALL_CORRECTIONS.get(rule, _UNKNOWN_RULE_CORRECTION)
                assert expected in f.message, (
                    f"finding for rule {rule!r} must inline its correction; "
                    f"got: {f.message!r}"
                )
                # The rule name is still surfaced in the message for the reader.
                assert f"[{rule}]" in f.message
        # Belt-and-braces: no must-fail carries a stale generic-only message.
        assert "agents have no owner-imposed" not in "".join(
            f.message for f in check_no_false_walls(tmp_path, Config())
        )

    def test_every_rule_has_a_correction_so_no_fallback_ships(self) -> None:
        # The fallback is a safety net; every real blocklist rule should carry a
        # dedicated correction (mirrors tests/test_explain_wall.py coverage).
        from engine.checks.check_no_false_walls import all_rule_names

        missing = sorted(all_rule_names() - WALL_CORRECTIONS.keys())
        assert not missing, f"rules missing a WALL_CORRECTIONS entry: {missing}"


# ── Exit-affecting wiring through cmd_check (the propagation goal) ─────────────


class TestCmdCheckWiring:
    def test_strict_reds_and_names_the_leg(self, tmp_path: Path, capsys) -> None:
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/current-state.md", _MUST_FAIL[4])
        rc = cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert rc == 1
        assert "[false-wall:" in out
        # It rides the HARD finding block, not an advisory "never exit-affecting"
        # warning — the whole point of the propagation is a red gate.
        for line in out.splitlines():
            if "false-wall" in line:
                assert "never exit-affecting" not in line

    def test_clean_docs_leave_the_leg_silent(self, tmp_path: Path, capsys) -> None:
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/current-state.md", _MUST_PASS[0])
        cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert "false-wall" not in out


# ── Clearing-vocabulary regression: ATTACHMENT-BASED clearing (fm ORDER 048) ──
#
# v1.20.0 shipped the engine leg with too-narrow clearing vocabulary + a strict
# line-by-line scan, so on adopter idea-engine (branch claude/kit-upgrade-v1.20.0,
# sha 039b75b) it red-flagged lines that CORRECTLY repudiate a past false wall.
# The FIRST fix over-corrected: section-based (dated-heading) sheltering and a
# cross-line bullet window BLINDED the gate — a genuine STANDING wall under a
# dated heading, or beside an unrelated repudiation, went green. The tightened
# rule is ATTACHMENT-BASED: a wall clears ONLY when a repudiation/date is
# attached to the wall claim itself (same clause of the same physical line, or a
# `false "…"` quote whose content IS the wall), NEVER because it shares a dated
# section or sits near an unrelated cue. Safety wins over clearing a stray FP.

# The idea-engine false positives that clear SAFELY (repudiation attached to the
# wall on the wall's own physical line).
_FP_CLEAR = {
    # docs/CAPABILITIES.md:90-91 — the wall phrase ('self-merge classifier')
    # lands on the continuation line INSIDE a `false "self-merge classifier"`
    # quote, so it clears on its own line (quote names the wall). The bullet's
    # first line repudiates the SAME capability.
    "wrapped_repudiation_bullet": (
        "- `any` · **Merging own / sibling green PRs is NOT walled** "
        "(corrects a prior\n"
        '  false "self-merge classifier" entry): direct REST/MCP '
        "squash-on-green,\n"
        "  arming auto-merge, and draft→ready flips are verified working "
        "agent-side.\n"
    ),
    # docs/CAPABILITIES.md:133 — "do **not** establish that agents cannot merge":
    # the cue is in the SAME clause as the wall (emphasis stripped).
    "do_not_establish_bolded": (
        "> window — they do **not** establish that agents cannot merge or "
        "cannot arm\n> routines.\n"
    ),
    # docs/seat-digest.md:46 — single-line "is NOT walled (corrects a prior
    # false 'self-merge classifier' entry)": the false-quote names the wall.
    "single_line_not_walled": (
        "- `any` · **Merging own / sibling green PRs is NOT walled** "
        '(corrects a prior false "self-merge classifier" entry): direct '
        "REST/MCP squash-on-green, arming auto-merge,…\n"
    ),
    # P2 — SAME-capability wrapped repudiation still clears: the prev line's
    # trailing clause repudiates the SAME capability (self-merge) that the wall
    # on the continuation line names, so the tight lookback still bridges. (The
    # continuation line carries no clearing cue of its own, so this genuinely
    # exercises the wrap, not same-line clearing.)
    "p2_same_capability_wrap_clears": (
        "The self-merge claim no longer applies and\n"
        "self-merge classifier remains a worry for some readers.\n"
    ),
    # P3 — a LONE wall named by a repudiated `false "…"` quote still clears: the
    # quote spans the only wall match on the line, so position-aware clearing
    # fires (guards against the per-match change over-redding a genuine FP).
    "p3_lone_false_quote_wall_clears": (
        'This corrects a prior false "self-merge classifier" entry — nothing '
        "here is a standing wall.\n"
    ),
    # ── G2 (v1.20.2): same-clause repudiation-cue vocabulary ──
    # "never a standing '…' wall" (conventions.md style): the cue and the quoted
    # wall phrase share the clause.
    "g2_never_a_standing_wall": (
        'This was never a standing "agents cannot merge" wall.\n'
    ),
    # "does not reproduce": the correction phrasing on the SAME clause as the
    # quoted wall (the superbot-next:118 shape, reduced to one line).
    "g2_does_not_reproduce": (
        'The "classifier-denied" framing does not reproduce in the default env.\n'
    ),
    # "was a false standing wall": explicit past-tense repudiation, same clause.
    "g2_was_a_false_standing_wall": (
        'The old "self-merge classifier" note was a false standing wall.\n'
    ),
    # "false standing wall" + "superseded" (the two-signal conditional): the bare
    # phrase clears ONLY because a second repudiation signal accompanies it.
    "g2_false_standing_wall_superseded": (
        'The "agents cannot merge" claim is a false standing wall, superseded by '
        "later proof.\n"
    ),
    # ── G4 (v1.20.2): false/superseded characterisation AFTER the quote ──
    # '"…wall…" — superseded': the marker sits immediately after the closing
    # quote (only a dash between), and the wall phrase is INSIDE the quote.
    "g4_superseded_after_quote": (
        '"sessions may not self-merge" — superseded; agents merge green PRs.\n'
    ),
    # '"…wall…" was based on a false … wall': the "based on a false … wall"
    # marker follows the quote within the clause.
    "g4_based_on_false_after_quote": (
        '"self-merge classifier" was based on a false wall.\n'
    ),
    # ── G1 (v1.20.2): bounded, same-family lookforward ──
    # A `>` blockquote whose wall line is followed, in the SAME blockquote, by a
    # same-family (merge) repudiation that wraps onto the next line. The wall
    # line carries NO cue of its own — this genuinely exercises the lookforward.
    "g1_blockquote_forward_same_family": (
        '> Merging own PRs — the "self-merge classifier"\n'
        "> framing does not reproduce and is normal agent work.\n"
    ),
    # ── FIX C (v1.20.2): the EXACT multi-line dated-bullet-continuation shape ──
    # (i) the trigger (classifier-denied) and the "does not reproduce" cue on the
    # SAME continuation line of a `- 2026-07-17 — CORRECTION …` dated bullet →
    # clears via G2 same-clause. The wall is on the CONTINUATION line (not the
    # dated first line), so the date does NOT trivially clear it — the cue does.
    "c_dated_bullet_same_continuation_line_g2": (
        "- 2026-07-17 — CORRECTION to the classifier-wall note:\n"
        '  the "DB provisioning DDL is classifier-denied in agent auto-mode" '
        "framing does not reproduce in the project-default env.\n"
    ),
    # (ii) the trigger on one continuation line and the cue on the NEXT
    # continuation line within the SAME bullet → clears via G1 lookforward. This
    # is the verbatim superbot-next current-state.md:117-119 shape.
    "c_dated_bullet_next_continuation_line_g1": (
        "- 2026-07-17 — CORRECTION to the classifier-wall note above:\n"
        '  the "DB provisioning DDL is classifier-denied in agent\n'
        '  auto-mode" framing does not reproduce in the project-default env.\n'
    ),
}

# The adversarial-review MUST-RED set (fm ORDER 048): every genuine STANDING
# wall — even under a dated heading, even beside an unrelated repudiation — must
# stay flagged. Clearing a stray FP may NEVER blind the gate to one of these.
_MUST_STAY_RED = {
    # (a) KEY: a bare standing wall under a dated heading (no reset heading
    # after — the whole remainder must NOT be blinded).
    "a_bare_wall_under_dated_heading": (
        "### 2026-07-16 — notes\n\n"
        "Agents cannot delete branches — this is a hard wall.\n"
    ),
    # (a2) "never self-merge" under a dated heading.
    "a2_never_self_merge_under_dated_heading": (
        "## 2026-07-15 — session notes\n\n"
        "Sessions must not merge their own PRs; never self-merge.\n"
    ),
    # (a3) a classifier-denied STANDING wall under a dated heading.
    "a3_classifier_denied_standing_under_dated_heading": (
        "### 2026-07-16 — log\n\n"
        "Merging is classifier-denied for agent seats and stays owner-only.\n"
    ),
    # (b) a genuine wall as a CONTINUATION of a DATED bullet about a different
    # capability — the bullet's date must not bleed onto the continuation.
    "b_neighbor_bleed_dated_bullet_continuation": (
        "- 2026-07-16 · deploys work agent-side (verified)\n"
        "  but agents cannot merge their own PRs.\n"
    ),
    # (b2) first bullet line repudiates a DIFFERENT capability; the continuation
    # is a distinct merge wall — the block window must not clear it.
    "b2_neighbor_bleed_different_capability": (
        '- Pushing is NOT walled (corrects a prior false "push classifier" '
        "entry):\n"
        "  but agents cannot merge their own PRs and never self-merge.\n"
    ),
    # (c2) an unrelated `false "weather"` quote plus a bare wall on one line —
    # the false-quote must name the wall to clear it.
    "c2_unrelated_false_quote": (
        'A prior false "weather" note aside, sessions may not self-merge.\n'
    ),
    # (d) "not walled" used in a different clause than the real wall.
    "d_not_walled_different_clause": (
        'Nothing here is "not walled"; in truth agents cannot merge their own '
        "PRs.\n"
    ),
    # docs/SKILLS.md:22 — the genuine stale wall: bare "never self-merge", no
    # repudiation, no date.
    "skills_bare_never_self_merge": (
        "| `session-close` | Land the session — claim, born-red card first, "
        "READY PR, batched work, close-out docs, flip complete last; never "
        "self-merge. | `read`, `edit`, `run` | `python3 bootstrap.py check` |\n"
    ),
    # docs/CAPABILITIES.md:139 — a section-dated incident record with NO inline
    # date: SAFETY WINS, it stays red (needs a light inline-date rewording in
    # the adopter doc rather than a weakened gate).
    "cap139_dated_incident_no_inline_date": (
        "### 2026-07-16 — auto-mode-classifier denials (since 2026-07-15)\n\n"
        "The Claude Code auto-mode permission classifier denied several "
        "actions this window; recorded here per the discovery rule.\n"
    ),
    # docs/CAPABILITIES.md:149 — likewise, no inline date → stays red.
    "cap149_dated_incident_review_label_no_inline_date": (
        "### 2026-07-16 — auto-mode-classifier denials (since 2026-07-15)\n\n"
        "5. **First sim-lab worker dispatch** — **DENIED**, reported label "
        '"[Merge Without Review]", over merge-on-green wording in the '
        "dispatch prompt; re-dispatched with the worker taking zero merge "
        "actions.\n"
    ),
    # A bare "self-merge classifier" wall with NO repudiation — the false-quote
    # clearing must not fire without a quote that names this wall.
    "bare_self_merge_classifier": (
        "Every session hits the self-merge classifier and must route the PR "
        "to the owner.\n"
    ),
    # A wall AFTER a non-dated heading (the earlier dated heading must not
    # shelter it — belt-and-braces since sections never shelter now).
    "wall_after_reset_heading": (
        "### 2026-07-16 — auto-mode-classifier denials\n\n"
        "recorded a denial this window.\n\n"
        "## Standing policy\n\n"
        "agents cannot merge their own PRs.\n"
    ),
    # P2 (follow-up a) — the prev line's trailing clause repudiates a DIFFERENT
    # capability (push) than the wall that wraps onto the current line (merge).
    # The tight lookback must NOT bridge across capabilities: the merge wall
    # stays RED. Before the fix, "not walled"/"proven repeatedly" bled across
    # the wrap and cleared it (the punctuation-gated bleed).
    "p2_prev_line_repudiates_different_capability": (
        "Pushing is NOT walled (proven repeatedly), and\n"
        "agents cannot merge their own PRs.\n"
    ),
    # P3 (follow-up b) — one physical line carries BOTH a repudiated
    # `false "self-merge classifier"` quote AND a genuine standing self-merge
    # wall outside the quote. Grading only the first hit masked the genuine
    # wall; per-match, position-aware clearing reds it.
    "p3_genuine_wall_shares_line_with_false_quote": (
        'A prior false "self-merge classifier" note aside — the live self-merge '
        "classifier still blocks every session and routes the PR to the owner.\n"
    ),
    # ── G2 (v1.20.2) negatives: the trigger phrase alone never clears ──
    # "a standing wall" WITHOUT a "never/not" repudiation prefix stays red.
    "g2_bare_standing_wall_no_repudiation": (
        "The self-merge classifier is a standing wall for every session.\n"
    ),
    # "reproduces" without the negated "does not reproduce" stays red.
    "g2_reproduces_without_negation": (
        "The classifier-denied error reproduces every session.\n"
    ),
    # ── G4 (v1.20.2) negative: an unrelated quote characterised false does NOT
    # clear a bare wall elsewhere on the line (the wall must be INSIDE the
    # quote). ──
    "g4_unrelated_quote_then_superseded": (
        '"weather" is superseded, but sessions may not self-merge their PRs.\n'
    ),
    # ── G1 (v1.20.2) negatives ──
    # A forward repudiation of a DIFFERENT capability family (push) must NOT
    # bridge to clear a merge wall — the same-family gate holds.
    "g1_forward_different_capability": (
        'The "self-merge classifier" note here\n'
        "is not walled for pushing, which is proven repeatedly.\n"
    ),
    # A forward repudiation PAST a blank line does NOT clear (paragraph ended).
    "g1_forward_past_blank_line": (
        'The "self-merge classifier" note here\n'
        "\n"
        "is not walled, proven repeatedly.\n"
    ),
    # A forward repudiation on a NEW bullet does NOT clear (bullet boundary).
    "g1_forward_new_bullet": (
        'The "self-merge classifier" note\n'
        "- is not walled, proven repeatedly.\n"
    ),
    # ── Class (b) negative: a doc WITHOUT the render marker is still scanned. ──
    "b_no_render_marker_still_scanned": (
        "A normal project doc.\n\nagents cannot merge their own PRs.\n"
    ),
    # A wall OUTSIDE a digest fence still reds (only the fenced block is exempt).
    "b_wall_outside_fence_still_reds": (
        "<!-- substrate-kit:skills-digest BEGIN — derived render, never edit. -->\n"
        "fine rendered content\n"
        "<!-- substrate-kit:skills-digest END -->\n\n"
        "agents cannot merge their own PRs.\n"
    ),
    # ── Governance / launch-copy lines with no date/repudiation stay red. ──
    "owner_merges_on_green_governance": (
        "Governance: the owner merges on green.\n"
    ),
    "launch_copy_agent_unlandable_no_entry": (
        "Launch copy: the legacy bot was agent-unlandable.\n"
    ),
    "classifier_denied_agent_merge_owner_click": (
        "classifier denied agent merge — owner click needed.\n"
    ),
    # ── FIX A (v1.20.2): comma-bleed genuine-wall blind must STAY red ──
    # The capability-agnostic cue ("does not reproduce") sits before a
    # `, but`/`, and`/`, yet`/`, so` conjunction; the wall in the second half
    # must land in its own cue-less clause and RED. The comma+conjunction split
    # (not the family gate) is what closes this — an empty-family cue bypasses
    # the disjoint gate, so the split is load-bearing.
    "a_comma_but_does_not_reproduce_bleed": (
        "The bug does not reproduce now, but agents cannot merge PRs in prod.\n"
    ),
    "a_comma_and_never_standing_deploy_wall_bleed": (
        "That was never a standing deploy wall, and agents cannot merge here.\n"
    ),
    "a_comma_yet_false_standing_wall_bleed": (
        "The prior note was a false standing wall, yet agents cannot merge to "
        "main.\n"
    ),
    "a_comma_but_freeze_reproduce_bleed": (
        "The freeze does not reproduce, but agents cannot merge to main.\n"
    ),
    "a_comma_and_deploy_wall_arm_bleed": (
        "That was never a standing deploy wall, and seats can't arm auto-merge.\n"
    ),
    # Regression pin: a semicolon is ALREADY a separator — the wall in the
    # second clause stays red (confirms the existing split still holds).
    "a_semicolon_superseded_bleed": (
        "The classifier note is superseded; agents cannot self-merge on "
        "protected main.\n"
    ),
    # ── FIX A' (v1.20.2 follow-up): BARE (comma-less) conjunction bleed must
    # STAY red — one pinned variant per coordinating/contrast conjunction. A
    # whitespace-surrounded ` and/but/so/yet/… ` splits the cue's clause from
    # the wall's, so the wall lands cue-less → RED. ──
    "aprime_bare_and_reproduce_bleed": (
        "The freeze does not reproduce and agents cannot merge to main.\n"
    ),
    "aprime_bare_but_reproduce_bleed": (
        "The bug does not reproduce but agents cannot merge their own PRs.\n"
    ),
    "aprime_bare_so_reproduce_bleed": (
        "The note does not reproduce so agents cannot merge to main.\n"
    ),
    "aprime_bare_yet_reproduce_bleed": (
        "The freeze does not reproduce yet agents cannot merge to main.\n"
    ),
    "aprime_bare_and_deploy_wall_bleed": (
        "That was never a standing deploy wall and agents cannot merge here.\n"
    ),
    # ── FIX B (v1.20.2): render marker on a NON-render file does not exempt ──
    # A CAPABILITIES.md-shaped doc bearing the seat-digest render header marker
    # AND a genuine wall must still RED — the exemption is gated to the known
    # render path (docs/seat-digest.md), so an author cannot blanket-exempt a
    # real doc by pasting the marker. (Exercised via check_no_false_walls below,
    # which knows the path; scan_text with the default is_render_path=False also
    # reds it, so it belongs in the MUST-RED matrix.)
    "b_render_marker_on_capabilities_doc_still_reds": (
        "# capabilities\n\n"
        "> Generated by substrate-kit — a **derived render**.\n"
        "> NEVER edit this file: regenerate with `python3 bootstrap.py "
        "seat-digest`.\n\n"
        "agents cannot merge their own PRs.\n"
    ),
}

# Class (b) (v1.20.2): kit-generated derived-render files/blocks are exempt from
# wall-scanning because their SOURCE docs are scanned independently. Kept in a
# separate dict (they exercise scan_text like _FP_CLEAR, but the mechanism is
# file/block exemption, not clause clearing).
_RENDER_EXEMPT_CLEAR = {
    # Whole-file exemption via the seat-digest header marker.
    "b_header_marked_file": (
        "> Generated by substrate-kit — a **derived render**, never a copy.\n"
        "> NEVER edit this file: regenerate with `python3 bootstrap.py "
        "seat-digest`.\n\n"
        "agents cannot merge their own PRs.\n"
    ),
    # Block exemption via the digest fence (no whole-file header present).
    "b_fenced_block": (
        "# skill index\n\n"
        "<!-- substrate-kit:walls-digest BEGIN — derived render, kit-generated; "
        "never edit. -->\n"
        "agents cannot merge their own PRs.\n"
        "<!-- substrate-kit:walls-digest END -->\n"
    ),
}


class TestClearingVocabulary:
    def test_each_idea_engine_false_positive_clears(self) -> None:
        for name, text in _FP_CLEAR.items():
            assert scan_text(text) == [], (
                f"FALSE POSITIVE {name!r} must clear, got: "
                f"{[(h.line, h.rule, h.phrase) for h in scan_text(text)]}"
            )

    def test_every_genuine_standing_wall_stays_flagged(self) -> None:
        # The whole adversarial MUST-RED matrix: no section/neighbour/unrelated
        # cue may clear a genuine standing wall.
        for name, text in _MUST_STAY_RED.items():
            assert scan_text(text), f"genuine wall {name!r} must STAY red"

    def test_bare_skill_row_still_reds_via_the_engine_leg(self, tmp_path: Path) -> None:
        # The exact genuine finding, on a real adopter surface.
        _plant(tmp_path, "docs/SKILLS.md", _MUST_STAY_RED["skills_bare_never_self_merge"])
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == ["docs/SKILLS.md"]
        assert findings[0].kind == "false-wall:never-agent-side"

    def test_dated_heading_does_not_shelter_a_standing_wall(self, tmp_path: Path) -> None:
        # The blocker the first fix introduced: a standing wall under an
        # ISO-dated heading must red on the engine leg, not be section-cleared.
        _plant(
            tmp_path,
            "docs/current-state.md",
            _MUST_STAY_RED["a_bare_wall_under_dated_heading"],
        )
        assert check_no_false_walls(tmp_path, Config()), "dated heading blinded the gate"

    def test_p2_different_capability_wrap_stays_red_but_same_capability_clears(
        self,
    ) -> None:
        # Mutation guard for P2 (wrapped-lookback same-capability gate), both
        # directions from ONE assertion pair so a mutation to the gate breaks a
        # test: a prev-line repudiation of a DIFFERENT capability must NOT bridge
        # (stays red); the SAME-capability wrap must still bridge (clears).
        red = _MUST_STAY_RED["p2_prev_line_repudiates_different_capability"]
        clear = _FP_CLEAR["p2_same_capability_wrap_clears"]
        assert scan_text(red), "P2: different-capability wrap must stay RED"
        assert scan_text(clear) == [], "P2: same-capability wrap must still clear"

    def test_p3_genuine_wall_on_false_quote_line_reds_but_lone_quote_clears(
        self,
    ) -> None:
        # Mutation guard for P3 (per-match, position-aware clearing), both
        # directions: a genuine wall SHARING a line with a repudiated
        # `false "…"` quote must red (no longer masked by the first-hit grade);
        # a LONE wall the quote names must still clear.
        red = _MUST_STAY_RED["p3_genuine_wall_shares_line_with_false_quote"]
        clear = _FP_CLEAR["p3_lone_false_quote_wall_clears"]
        red_hits = scan_text(red)
        assert red_hits, "P3: genuine wall sharing a false-quote line must RED"
        assert red_hits[0].rule == "self-merge-classifier"
        assert scan_text(clear) == [], "P3: lone false-quoted wall must still clear"

    def test_p3_multi_wall_line_still_yields_at_most_one_finding(self) -> None:
        # The legacy count contract: even a line carrying two independent genuine
        # walls yields ≤1 finding per line (the first uncleared), so per-match
        # grading does not multiply findings on existing must-fail fixtures.
        two_walls = (
            "agents do NOT arm auto-merge — classifier-denied since 2026-07-15\n"
        )
        assert len(scan_text(two_walls)) == 1

    def test_safe_false_positives_clear_but_incident_records_stay_red(
        self, tmp_path: Path
    ) -> None:
        # The assembled CAPABILITIES.md shape: the two attach-clearable FPs go
        # silent; the two section-dated incident records (no inline date) stay
        # red by the safety-wins rule (they need an inline-date rewording).
        doc = (
            "## Append log — newest first\n\n"
            + _FP_CLEAR["wrapped_repudiation_bullet"]
            + "\n"
            + _FP_CLEAR["do_not_establish_bolded"]
            + "\n"
            + _MUST_STAY_RED["cap139_dated_incident_no_inline_date"]
        )
        _plant(tmp_path, "docs/CAPABILITIES.md", doc)
        findings = check_no_false_walls(tmp_path, Config())
        # Exactly the one incident-record line stays red.
        assert [f.kind for f in findings] == ["false-wall:classifier-denied-standing"]

    # ── G1 (v1.20.2) mutation guard: bounded, same-family lookforward ──
    def test_g1_lookforward_same_family_clears_but_different_family_stays_red(
        self,
    ) -> None:
        # Both directions from one pair: a same-family repudiation that wraps
        # onto the next line clears (the wall line carries no cue of its own);
        # a DIFFERENT-family forward repudiation must NOT bridge.
        assert scan_text(_FP_CLEAR["g1_blockquote_forward_same_family"]) == [], (
            "G1: same-family forward repudiation must clear"
        )
        assert scan_text(_MUST_STAY_RED["g1_forward_different_capability"]), (
            "G1: different-family forward repudiation must STAY red"
        )

    def test_g1_lookforward_stops_at_blank_line_and_new_bullet(self) -> None:
        # The paragraph/bullet boundary: a forward repudiation past a blank line
        # or on a new bullet is out of the wall's paragraph and must not clear.
        assert scan_text(_MUST_STAY_RED["g1_forward_past_blank_line"])
        assert scan_text(_MUST_STAY_RED["g1_forward_new_bullet"])

    # ── G2 (v1.20.2) mutation guard: cue vocabulary requires the context ──
    def test_g2_cues_clear_but_bare_trigger_phrase_stays_red(self) -> None:
        for name in (
            "g2_never_a_standing_wall",
            "g2_does_not_reproduce",
            "g2_was_a_false_standing_wall",
            "g2_false_standing_wall_superseded",
        ):
            assert scan_text(_FP_CLEAR[name]) == [], f"G2 {name!r} must clear"
        for name in (
            "g2_bare_standing_wall_no_repudiation",
            "g2_reproduces_without_negation",
        ):
            assert scan_text(_MUST_STAY_RED[name]), f"G2 {name!r} must STAY red"

    # ── G4 (v1.20.2) mutation guard: false/superseded AFTER the quote ──
    def test_g4_marker_after_quote_clears_but_unrelated_quote_stays_red(self) -> None:
        assert scan_text(_FP_CLEAR["g4_superseded_after_quote"]) == []
        assert scan_text(_FP_CLEAR["g4_based_on_false_after_quote"]) == []
        # The wall must be INSIDE the quote — an unrelated false-quote does not
        # clear a bare wall elsewhere on the line.
        assert scan_text(_MUST_STAY_RED["g4_unrelated_quote_then_superseded"])

    # ── FIX A' (v1.20.2 follow-up): bare (comma-less) conjunction split ──
    def test_bare_conjunction_splits_but_no_conjunction_clears(self) -> None:
        # Both directions: a BARE conjunction between a cue and a wall isolates
        # the wall in its own cue-less clause → RED (one per conjunction); the
        # intended clears (no bare cue↔wall conjunction) still CLEAR, and the
        # quote-covered G4 path — independent of clause splitting — is untouched.
        for name in (
            "aprime_bare_and_reproduce_bleed",
            "aprime_bare_but_reproduce_bleed",
            "aprime_bare_so_reproduce_bleed",
            "aprime_bare_yet_reproduce_bleed",
            "aprime_bare_and_deploy_wall_bleed",
        ):
            assert scan_text(_MUST_STAY_RED[name]), f"bare-conjunction {name!r} must RED"
        # Intended clears survive (no bare cue↔wall conjunction).
        assert scan_text(_FP_CLEAR["g2_never_a_standing_wall"]) == []
        assert scan_text(_FP_CLEAR["g2_does_not_reproduce"]) == []
        assert scan_text(_FP_CLEAR["g4_superseded_after_quote"]) == []
        assert scan_text(_FP_CLEAR["g1_blockquote_forward_same_family"]) == []

    # ── Class (b) (v1.20.2): kit-generated derived-render exemption ──
    def test_render_exempt_files_and_blocks_clear_on_the_render_path(self) -> None:
        # The exemption fires only for the KNOWN render path (FIX B) — modelled
        # by scan_text(..., is_render_path=True). Off the render path it does not.
        for name, text in _RENDER_EXEMPT_CLEAR.items():
            assert scan_text(text, is_render_path=True) == [], (
                f"render-exempt {name!r} must clear on the render path, got: "
                f"{[(h.line, h.rule) for h in scan_text(text, is_render_path=True)]}"
            )
            assert scan_text(text, is_render_path=False), (
                f"render-exempt {name!r} must STILL red off the render path"
            )

    def test_render_exemption_is_render_path_gated_not_marker_blanket(
        self, tmp_path: Path
    ) -> None:
        # FIX B: an author cannot blanket-exempt a real doc by pasting the render
        # marker. A CAPABILITIES.md-shaped file bearing the marker + a genuine
        # wall must still RED through the engine leg (it is NOT the render path);
        # the real docs/seat-digest.md (which IS the render path) clears.
        _plant(
            tmp_path,
            "docs/CAPABILITIES.md",
            _MUST_STAY_RED["b_render_marker_on_capabilities_doc_still_reds"],
        )
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.path for f in findings] == ["docs/CAPABILITIES.md"], (
            "render marker on a non-render doc must not exempt it"
        )
        # The same marker text, planted AT the render path, clears.
        (tmp_path / "docs" / "CAPABILITIES.md").unlink()
        _plant(
            tmp_path,
            "docs/seat-digest.md",
            _MUST_STAY_RED["b_render_marker_on_capabilities_doc_still_reds"],
        )
        assert check_no_false_walls(tmp_path, Config()) == [], (
            "the marker on the known render path (docs/seat-digest.md) exempts it"
        )

    def test_normal_doc_and_wall_outside_fence_still_red(self, tmp_path: Path) -> None:
        # A normal doc without the marker is scanned; a wall OUTSIDE a fence reds
        # even on the render path (only the fenced block is exempt).
        _plant(
            tmp_path, "docs/d.md", _MUST_STAY_RED["b_no_render_marker_still_scanned"]
        )
        assert check_no_false_walls(tmp_path, Config())
        assert scan_text(
            _MUST_STAY_RED["b_wall_outside_fence_still_reds"], is_render_path=True
        )


# ── FIX D (v1.20.2): false-wall findings ride the generic REASON-REQUIRED
# allowlist seam (engine.checks.allowlist), NOT a bespoke fail-open path ────────
#
# check_no_false_walls emits the finding unconditionally; cmd_check post-processes
# EVERY finding through load_allowlist + apply_allowlist. The product-copy
# allowlist is that generic seam: exact path+kind match WITH a non-empty reason
# suppresses; a reason-less entry suppresses nothing and surfaces as a
# `kind=allowlist` finding (fail-CLOSED, loud).


class TestFalseWallRidesGenericAllowlist:
    _WALL = "Launch copy: the legacy bot was agent-unlandable.\n"
    # The `agent-unlandable` phrase is emitted under the `standing-platform-wall`
    # rule (earlier in blocklist order) — the allowlist keys on the EXACT kind.
    _KIND = "false-wall:standing-platform-wall"
    _REASONED = (
        "- path: docs/launch.md\n"
        f"  kind: {_KIND}\n"
        "  reason: marketing copy describing the legacy bot\n"
        "  triaged: 2026-07-21\n"
        "  by: menno420\n"
        "  verdict: false_positive\n"
    )

    def _false_wall_finding(self, tmp_path: Path):
        _plant(tmp_path, "docs/launch.md", self._WALL)
        findings = check_no_false_walls(tmp_path, Config())
        assert [f.kind for f in findings] == [self._KIND], (
            "the leg must emit the finding; suppression is the allowlist's job"
        )
        return findings

    def test_reasoned_entry_suppresses_via_apply_allowlist(self, tmp_path: Path) -> None:
        from engine.checks.allowlist import apply_allowlist, parse_allowlist

        findings = self._false_wall_finding(tmp_path)
        entries, allow_findings = parse_allowlist(self._REASONED, ".substrate/x.yml")
        assert allow_findings == []  # a reasoned entry parses cleanly
        kept, suppressed = apply_allowlist(findings, entries)
        assert kept == [] and len(suppressed) == 1

    def test_reasonless_entry_does_not_clear_and_is_reported(
        self, tmp_path: Path
    ) -> None:
        from engine.checks.allowlist import apply_allowlist, parse_allowlist

        findings = self._false_wall_finding(tmp_path)
        reasonless = self._REASONED.replace(
            "  reason: marketing copy describing the legacy bot\n", ""
        )
        entries, allow_findings = parse_allowlist(reasonless, ".substrate/x.yml")
        # The reason-less entry suppresses nothing AND surfaces as an allowlist
        # finding — fail-closed and loud (not the old fail-open behaviour).
        assert entries == []
        assert [f.kind for f in allow_findings] == ["allowlist"]
        kept, suppressed = apply_allowlist(findings, entries)
        assert kept == findings and suppressed == []

    def test_wrong_kind_entry_does_not_clear(self, tmp_path: Path) -> None:
        from engine.checks.allowlist import apply_allowlist, parse_allowlist

        findings = self._false_wall_finding(tmp_path)
        entries, _ = parse_allowlist(
            self._REASONED.replace(self._KIND, "false-wall:the-owner-merges"),
            ".substrate/x.yml",
        )
        kept, suppressed = apply_allowlist(findings, entries)
        assert kept == findings and suppressed == []

    def test_end_to_end_reasoned_entry_suppresses_through_cmd_check(
        self, tmp_path: Path, capsys
    ) -> None:
        # Proof the false-wall finding actually flows through cmd_check's
        # allowlist pass: with a reasoned entry, the false-wall line is gone.
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/launch.md", self._WALL)
        _plant(tmp_path, ".substrate/check-exceptions.yml", self._REASONED)
        cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert "false-wall" not in out, "reasoned allowlist entry must suppress it"

    def test_end_to_end_no_allowlist_leaves_false_wall_red(
        self, tmp_path: Path, capsys
    ) -> None:
        save_config(tmp_path, Config())
        _plant(tmp_path, "docs/launch.md", self._WALL)
        rc = cmd_check(tmp_path, strict=True)
        out = capsys.readouterr().out
        assert rc == 1 and "[false-wall:" in out
