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
