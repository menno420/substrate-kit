"""Tests for tools/check_no_false_walls.py — the false merge-wall CI guard.

The checker fails when a FORWARD-BINDING surface (templates, skill bodies, live
docs, root constitution/capabilities) re-seeds the FALSE "agents cannot merge /
owner is the merge authority / classifier-denied" doctrine as a standing rule.
Merging a green PR is normal agent work; the checker must catch a re-seed while
leaving every corrected/dated/repudiated phrasing untouched.
"""

from __future__ import annotations

import sys
from pathlib import Path

_TOOLS = Path(__file__).resolve().parents[1] / "tools"
if str(_TOOLS) not in sys.path:
    sys.path.insert(0, str(_TOOLS))

import check_no_false_walls as cnfw  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parents[1]


def _write(tmp_path: Path, name: str, text: str) -> Path:
    """Write a doc under a synthetic repo tree and return the repo root."""
    docs = tmp_path / "docs"
    docs.mkdir(exist_ok=True)
    (docs / name).write_text(text, encoding="utf-8")
    return tmp_path


class TestLiveTreeClean:
    def test_current_tree_is_exit_zero(self):
        # The kit's own tree must satisfy its own checker — ZERO false
        # positives on main as it stands (the corrected merge doctrine, the
        # dated CAPABILITIES wall ledger, the NEXT-TASKS `FALSE "…"` flag).
        findings = cnfw.check_tree(REPO_ROOT)
        assert findings == [], [f"{x.path}:{x.line} [{x.rule}] {x.phrase}" for x in findings]

    def test_main_returns_zero_on_this_repo(self, capsys):
        assert cnfw.main(["--root", str(REPO_ROOT)]) == 0
        assert "OK" in capsys.readouterr().out


class TestCatchesReseed:
    def test_synthetic_bad_string_is_caught(self, tmp_path):
        # The exact regression three sessions hand-removed.
        root = _write(
            tmp_path,
            "doctrine.md",
            "# Doctrine\n\nagents do NOT arm auto-merge — classifier-denied since 2026-07-15\n",
        )
        findings = cnfw.check_tree(root)
        assert findings, "the re-seeded false wall must be caught"
        assert findings[0].path == "docs/doctrine.md"

    def test_main_returns_nonzero_on_bad_tree(self, tmp_path, capsys):
        root = _write(
            tmp_path,
            "doctrine.md",
            "agents do NOT arm auto-merge — classifier-denied since 2026-07-15\n",
        )
        assert cnfw.main(["--root", str(root)]) == 1
        assert "false merge-wall phrasing" in capsys.readouterr().out

    def test_other_false_walls_are_caught(self, tmp_path):
        # A spread across the curated blocklist — each is a standing false wall.
        for text in (
            "The owner is the merge authority for every session PR.\n",
            "A green PR is agent-unlandable; route it to the owner.\n",
            "Sessions may not self-merge their own PRs.\n",
            "NEVER arm auto-merge — the classifier denies it.\n",
            "Always route owner-gated PRs to the owner; agents cannot merge them.\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root), f"should have caught: {text!r}"


class TestCorrectedPhrasingPasses:
    def test_corrected_line_passes(self, tmp_path):
        # The synthetic CORRECTED string from the task brief.
        root = _write(
            tmp_path,
            "doctrine.md",
            "merging is normal agent work; never route a mergeable green PR to the owner\n",
        )
        assert cnfw.check_tree(root) == []

    def test_all_corrected_variants_pass(self, tmp_path):
        for text in (
            "Merging works agent-side — NOT a wall\n",
            'no standing "classifier-denied" merge wall; do not invent one\n',
            "merging is a normal agent action\n",
            "never route a mergeable green PR to the owner\n",
            "Land your own green PR\n",
            "The old owner-gated-merge note no longer applies; land your own green PR.\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root) == [], f"corrected phrasing must pass: {text!r}"


class TestGeneralizedCapabilityWalls:
    """The check reds ANY false agent-capability limitation, not just merge
    (owner directive 2026-07-18): a subject-negated capability, an owner-only
    capability action, or a standing platform wall."""

    def test_generalized_false_walls_are_caught(self, tmp_path):
        # MUST-FAIL fixtures from the brief + semantic-class spread. Each is a
        # forward-binding surface asserting an agent CANNOT do a capability, or
        # that a capability is owner-only / platform-walled.
        for text in (
            "agents cannot delete branches\n",
            "sessions are not allowed to update Railway variables\n",
            "branch deletion is owner-only\n",
            "deploying is classifier-denied for agent seats\n",
            "the owner must merge PRs\n",
            "workers are unable to deploy the service\n",
            "you may not arm auto-merge on any PR\n",
            "merging is owner-gated\n",
            "only the owner can deploy to Railway\n",
            "deploying is blocked for agents\n",
            "the bot cannot push to protected branches\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root), f"should have caught: {text!r}"

    def test_code_and_architecture_rules_never_trip(self, tmp_path):
        # The failure mode: a CODE rule ("must not"/"never"/"cannot" over a code
        # noun) must NEVER be read as an agent-capability wall.
        for text in (
            "services must not import views\n",
            "utils/ may not import services\n",
            "Never define a utility function in views/ that other layers need.\n",
            "never call pool.execute directly outside utils/db\n",
            "the core layer cannot import cogs\n",
            "views must not reach into the cogs package\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root) == [], f"code rule tripped: {text!r}"

    def test_corrected_capability_text_passes(self, tmp_path):
        # Today's corrected capability doctrine — the phrasing we WANT to keep.
        for text in (
            "merging is normal agent work\n",
            "never route a mergeable green PR to the owner\n",
            "there are NO owner-imposed limitations\n",
            "attempt it before assuming it is walled\n",
            "do not document limitations; record capabilities\n",
            "no standing merge wall — deploying works agent-side too\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root) == [], f"corrected text tripped: {text!r}"

    def test_missing_credential_owner_input_is_not_a_wall(self, tmp_path):
        # A missing external credential framed as an owner INPUT request is a
        # missing input, not a capability wall.
        for text in (
            "needs a Stripe account from the owner\n",
            "needs a PayPal account from the owner\n",
            "the deploy needs a RAILWAY_TOKEN provided by the owner\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root) == [], f"missing-input tripped: {text!r}"

    def test_genuine_dated_walls_still_pass(self, tmp_path):
        # Walls that genuinely stand are recorded as DATED / LAST-VERIFIED
        # capability-ledger rows (they carry their own expiry) — never flagged.
        for text in (
            "- `any` · **Branch deletion**: 403 on every path → owner deletes "
            "by hand. — LAST-VERIFIED: 2026-07-10\n",
            "session tokens cannot create repos (gen-1 wall)\n",
            "this repo's sessions cannot read fleet-manager directly\n",
            "repo settings / rulesets / secrets / env vars / host provisioning "
            "remain owner-only\n",
        ):
            root = _write(tmp_path, "d.md", text)
            assert cnfw.check_tree(root) == [], f"genuine wall tripped: {text!r}"


class TestExclusions:
    def test_dated_ledger_record_is_ignored(self, tmp_path):
        # A dated `- YYYY-MM-DD · wall · …` bullet is history, not doctrine.
        root = _write(
            tmp_path,
            "CAPABILITIES.md",
            "- 2026-07-16 · wall · An agent session cannot merge OR arm-auto-merge "
            "a SIBLING session's PR — the classifier denies it.\n",
        )
        assert cnfw.check_tree(root) == []

    def test_dated_report_filename_is_skipped(self, tmp_path):
        # Report files carry an ISO date in the basename — dated records.
        root = _write(
            tmp_path,
            "2026-07-12-report.md",
            "Rule: agents do NOT merge their own PR — classifier-denied since 2026-07-15.\n",
        )
        assert cnfw.check_tree(root) == []

    def test_historical_heading_section_is_skipped(self, tmp_path):
        root = _write(
            tmp_path,
            "d.md",
            "# doc\n\n## Append log\n\nagents do NOT arm auto-merge — classifier-denied since 2026.\n",
        )
        assert cnfw.check_tree(root) == []

    def test_false_quote_repudiation_is_skipped(self, tmp_path):
        # The repo's `FALSE "…"` convention quotes the wall to repudiate it.
        root = _write(
            tmp_path,
            "d.md",
            '> FALSE "agents do NOT ready-flip / arm / REST-merge — classifier-denied"\n',
        )
        assert cnfw.check_tree(root) == []

    def test_historical_dir_is_skipped(self, tmp_path):
        retro = tmp_path / "docs" / "retro"
        retro.mkdir(parents=True)
        (retro / "old.md").write_text(
            "agents do NOT arm auto-merge — classifier-denied since 2026-07-15\n",
            encoding="utf-8",
        )
        assert cnfw.check_tree(tmp_path) == []
