"""Skill sources + the skill/stance precedence model (plan section 3c).

A *skill* is an invokable procedure emitted as a native ``.claude/skills/<name>/
SKILL.md`` (YAML frontmatter for metadata-first loading + a readable body). Unlike
a stance (an ambient posture), a skill is invoked for a specific job and **declares
the capabilities it needs** — so a skill's declared capability **takes precedence
over the ambient stance** (a ``session-close`` that declares it edits can write the
session log even while the active stance is ``review``). Stances stay advisory for
anything a skill has not declared.

Like the question bank and the stances, the set ships as a Python module — embeds
in the stdlib-only bootstrap with no YAML parser, identical in ``src`` and ``dist``.
Bodies use ``${slot}`` placeholders filled from the interview at build time, so a
skill is project-aware (e.g. ``quality-gate`` runs the project's own verify command).
"""

from __future__ import annotations

import re

from engine.stances.stances import COMMENT, EDIT, READ, RUN, action_allowed

_SESSION_CLOSE_BODY = """\
Land ${project_name}'s session correctly — the full landing path, claim to
merged-on-green. Playbook-grade: a session reading this executes without
improvising (grounded-skills plan §7.2).

## What this does

Drives the session's work to a terminal, verified state on two rails:
the born-red gate (card first, flip last) and never-self-merge (the repo's
server-side auto-merge-enabler arms; GitHub lands the PR on green required
checks). Everything else is ordered steps.

## Instructions

1. Claim first (session start — verify it happened) — one file per claim,
   `control/claims/<branch-or-scope>.md`, a single bullet: backticked
   branch/scope token · **scope** — one-line detail · expected files/area ·
   ISO date (the shape `check_claims` parses). Land the claim on main fast,
   then re-read `control/claims/` at HEAD before building.
2. Born-red card as the FIRST commit — `.sessions/<date>-<slug>.md` whose
   Status badge line declares `in-progress` (the born-red hold token), plus
   a one-line "what is about to happen". Push, then open the PR READY (not
   draft) immediately: the open PR + the claim are the in-flight signal
   parallel sessions collide without.
3. NEVER arm auto-merge on, or merge, your own PR — author self-arm/
   self-merge is refused terminally (deny-wins; never retry it). The
   enabler workflow arms server-side at open; green required checks merge
   it with no action from you. Read a red on a born-red head as the
   designed hold, not a CI failure: verify any red against the job log
   before diagnosing — alias/mirror jobs echo the required check without
   running anything (kit repo example: the two legacy jobs mirroring
   `kit-quality`), and "HOLD (by design)" means nothing to investigate.
4. Batch the work — push when a batch is meaningfully complete, never every
   commit (superseded CI runs are the dominant Actions cost).
5. Close-out docs, into the SAME card: what shipped (paths + commits);
   Capability delta — new capability or wall discovered? Append it to
   `docs/CAPABILITIES.md` (dated, exact error or proof, workaround); every
   ⚑ needs-owner ask carries the OWNER-ACTION fields (WHAT / WHERE / HOW /
   WHY-IT-MATTERS / UNBLOCKS / VERIFIED-NEEDED — attempted, or the exact
   wall; see `control/README.md`) — Withdraw stale asks; groom one idea
   forward; add one new 💡 idea you genuinely believe in; write the ⟲
   previous-session review.
6. Verify — `${verify_command}` and `python3 bootstrap.py check --strict`.
   The only acceptable pre-flip red is the designed born-red hold naming
   this session's own card.
7. Flip as the deliberate LAST step — flip the card badge to `complete`,
   delete your own claim file, push. Green then merges server-side; a
   flipped-early card merges a partial PR (the failure the gate exists
   for), and an unpushed flip leaves the PR red forever.

## Report format (card close-out)

- Shipped: one line per artifact, with paths + commit SHAs.
- Verify: each command + its tail, verbatim.
- ⚑ decide-and-flag lines · 💡 session idea · ⟲ previous-session review.
- PR: #<n> + terminal state, probed against the tree/checks — not a stale
  PR read.

Declared capabilities: edit (the log + docs), run (the checks + git)."""

_UPGRADE_DISTRIBUTION_BODY = """\
Roll a substrate-kit release out to ${project_name} — one target repo of the
distribution wave. Playbook-grade wave runbook (grounded-skills plan §7.2).

## What this does

Moves the target's vendored `bootstrap.py` to the released version with the
sha256 three-way proof, the banked rollback path, a carve-out scan for local
modifications, and a born-red PR — then verifies MERGED MAIN against the
tree, never a registry line or a PR read.

## Instructions

1. Preflight — sync the clone before reading anything:
   `git fetch origin main && git reset --hard origin/main`. A stale clone
   reads stale orders and re-executes finished work.
2. Download the release next to the vendored copy:
   `gh release download vX.Y.Z --repo menno420/substrate-kit --pattern 'bootstrap.py*' --pattern 'release.json'`
   then move the downloaded dist to `bootstrap.py.new` (the consumer flow
   `release.json` names).
3. sha256 three-way compare (never skip) — `sha256sum bootstrap.py.new`
   must equal BOTH the `sha256` field in `release.json` AND the kit repo's
   committed `dist/bootstrap.py` at the release's bump SHA. Any mismatch:
   stop and report; do not upgrade.
4. Born-red PR first — claim file + `.sessions/` card declaring
   `in-progress` as the first commit on the wave branch; open the PR READY;
   never self-arm/self-merge (the session-close rails apply verbatim).
5. Upgrade — `python3 bootstrap.py.new upgrade`. It banks the OLD dist to
   `.substrate/backup/` (verify the banked `bootstrap-<old-version>.py`
   exists — that is the rollback path) and consumes its own inputs.
6. Carve-out scan — read `.substrate/upgrade-report.md`: `consumer-edited`
   and `diverged` docs are LOCAL MODIFICATIONS the upgrade must not
   clobber; list them verbatim in the PR body. `template-improved` applies
   only under `--apply-docs` and only to consumer-untouched docs.
7. Verify + flip — `${verify_command}` and
   `python3 bootstrap.py check --strict` green (own card's designed hold
   excepted); flip the card `complete`, delete the claim, push.
8. Verify merged main afterward — TREE over registries:
   `git fetch origin main && git log -1 --oneline origin/main` and read the
   vendored dist's version header at origin/main. Never trust an MCP PR
   read alone for merge/CI state (~25-min-stale data) — cross-check the
   tree or the Actions runs.

## Report format — one outcome line per target repo

`<repo>: vOLD → vNEW · sha256 3-way ✔ · bank ✔ · carve-outs: <n or none> · PR #<n> merged @ <sha> · tree-verified ✔`

Known failure modes + fixes:

- A `do-not-automerge` label applied seconds after MCP PR-create misses the
  opened-event label snapshot and reds the first CI round — cure with one
  empty commit (`git commit --allow-empty`) to re-fire the enabler.
- MCP PR reads can serve ~25-minute-stale merge/CI state — probe the tree,
  not the PR object.
- A born-red head red-pings "failed checks"; job-log truth is the designed
  hold plus alias jobs that mirror the required check — verify against the
  job log, don't chase.

Declared capabilities: edit (the vendored dist + docs), run (git + gh + the
checks)."""

_RELEASE_BODY = """\
Cut and publish a substrate-kit release — the kit cut runbook, executable
(canonical prose: `docs/operations/release-runbook.md`). Kit-repo-specific
by nature: the commands below run in the kit repo, the source of the
releases ${project_name} consumes.

## What this does

Takes `CHANGELOG.md` `[Unreleased]` to a published GitHub Release with
byte-verified assets: version bump PR (born-red), workflow_dispatch publish,
three-way post-release verification, then adopter notification via
distribution PRs.

## Instructions

1. Preconditions — every shipped PR has its entry under `[Unreleased]` in
   `CHANGELOG.md`; decide the semver class (MAJOR = planted-doc / state /
   config / CLI break · MINOR = new capability · PATCH = fixes).
2. Claim, then bump PR born-red — claim `control/claims/` (one file, e.g.
   release-vX.Y.Z.md) on main first; cut the bump branch from post-claim
   main; born-red card as first commit; open the PR READY; never
   self-arm/self-merge.
3. Version bump, one commit set — BOTH version homes in the SAME commit:
   `src/engine/lib/config.py` (`KIT_VERSION`) and `pyproject.toml`
   (`version`). CHANGELOG: rename `[Unreleased]` to the new `[X.Y.Z]`
   dated section, add a fresh empty `[Unreleased]` above it, and keep the
   machine comment (breaking / state_migration / min_upgrade_from)
   accurate — the release workflow refuses a version with no CHANGELOG
   section.
4. Dist regen + byte-pin — `python3 src/build_bootstrap.py`, then
   `git diff --exit-code dist/bootstrap.py` must be clean; commit the
   regenerated dist (CI rebuilds and byte-compares).
5. Verify locally, then flip — `python3 -m pytest tests/ -q` green ·
   `python3 -m ruff check src/engine/` clean ·
   `python3 src/build_release_json.py --version X.Y.Z --verify-only`
   reports preconditions green ·
   `python3 dist/bootstrap.py check --strict` (only acceptable red = own
   card's designed hold). Flip the card `complete` as the last commit; the
   server-side enabler merges on green.
6. Publish — dispatch the release workflow on main at the bump-merge SHA:
   `gh workflow run release.yml -f version=X.Y.Z`. The run creates the
   annotated tag `vX.Y.Z` in-Actions and publishes the Release with three
   assets: `bootstrap.py`, `bootstrap.py.sha256`, `release.json`.
7. Post-release verification (never skip) — the tag exists:
   `git fetch --tags && git tag -l vX.Y.Z`; the assets are published:
   `gh release view vX.Y.Z`; independently download the released
   `bootstrap.py` and its sha256 must equal BOTH the `sha256` field in
   `release.json` AND the committed `dist/bootstrap.py` at the bump SHA
   (three-way, byte-identical). Record run id, tag, commit SHA, and hash
   in the release record.
8. Aftermath — adopter notification via distribution PRs: run the
   `upgrade-distribution` skill per adopter (one born-red PR each);
   registry regen `python3 dist/bootstrap.py currency` refreshes
   `docs/adopters.md`; write the `control/status.md` release record;
   delete the claim.

## Report format (release record)

`vX.Y.Z · bump PR #<n> merged @ <sha> · release run <id> · tag vX.Y.Z @ <sha> · sha256 <hash> (3-way ✔) · adopters: <one outcome line per repo>`

Known failure modes + fixes:

- Tag pushes can 403 where branch pushes work — the workflow_dispatch path
  creates the tag in-Actions; never hand-push a tag first.
- The workflow refuses when `KIT_VERSION` / dist header / CHANGELOG
  disagree — fix the version homes, never the guard.
- Published releases are never deleted — supersede a bad cut with a fixed
  one whose `release.json` carries the yank note.

Declared capabilities: edit (version homes + CHANGELOG + docs), run (build +
git + gh)."""

_INTAKE_BODY = """\
Turn a fragmented owner ask about ${project_name} into a verified fuller
picture before building. Executable wrapper around the understand-and-reflect
doctrine (`CONSTITUTION.md` working agreement) — not new policy. Provenance:
superbot router Q-0254 (owner-directed 2026-07-07, graduated to the kit's
CONSTITUTION/collaboration-model templates the same day) plus the Q-0263.2
paste-ready-questions directive. Invoke on any non-trivial, non-mechanical
owner ask — especially a fragmented or associative one.

## What this does

The owner builds ideas iteratively and in fragments by design — a rough
draft now, more shape later — and relies on the agent to reason a partial
idea forward to its fuller form (`docs/owner-profile.md`). This skill runs
that step as a procedure: one inline restate that pays off twice —
verification (a wrong assumption stated now costs one correction; found
after an hour of building it costs the hour) and idea-expansion (the
filled-in picture is itself new material the owner reasons against and
redirects).

## Invocation

/intake <the ask, or a pointer to it>

## Instructions

1. CONSOLIDATE — reduce the fragmented ask to its few MAIN IDEAS (usually
   1–3). Name each in one line. The owner thinks associatively on purpose;
   consolidation is your half of the contract. Idea order is not
   implementation order — capture side ideas, never derail on them.
2. RESTATE — state back, inline in your first substantive response (never
   as a separate blocking question), the fuller picture you built from the
   ask: the implied specs, the surrounding constraints, the likely intended
   scope, and the follow-on the owner probably wants but didn't spell out.
3. MAP — map each main idea to known step patterns via the skill index
   (`docs/SKILLS.md`): which existing skill/playbook/checklist covers it,
   which parts are genuinely new. Cite the exact skill or doc per idea, and
   check `docs/CAPABILITIES.md` before assuming any wall.
4. POSSIBILITY SPACE — when the ask starts from uncertain feasibility ("I
   don't know if this is even possible" is a normal starting point, not an
   edge case), surface what is achievable and by what approaches FIRST,
   before committing to a direction. Target: the most advanced capability
   reachable by the simplest, most efficient implementation.
5. DECIDE-AND-FLAG — decide every reversible-until-a-gate call yourself
   (recommendation + one-line rationale + a flag on the run report). Route
   to the owner only genuine product/intent ambiguity, as a structured
   choice — options A/B(/C), a **bolded recommendation**, one-line
   rationale, answerable with one letter. Never an ask that requires the
   owner to parse, derive, or transform anything (that is a drafting
   defect, not an owner task). With no live owner, append the question to
   `docs/question-router.md` instead of skipping it or guessing.

A trivial or fully-unambiguous ask stays exempt: a one-line "doing X
because Y" suffices — the same calibration as the doctrine itself. A big or
vague idea earns a dedicated research pass (a delegated subagent, reviewed
the same session) or its own session, never an answer from memory alone.

## Report format

Print: MAIN IDEAS (numbered) · FULLER PICTURE (short prose) · MAP (idea →
skill/pattern/new) · [POSSIBILITY SPACE if triggered] · DECISIONS FLAGGED ·
QUESTIONS FOR OWNER (structured choices, or `none`).

Declared capabilities: read (the index, the ledger, the profile)."""

_QUALITY_GATE_BODY = """\
Prove a change is good before pushing ${project_name}.

1. Run `${verify_command}` — the project's full verification (tests + lint/types).
2. Run `python3 bootstrap.py check --strict` — doc + session-log hygiene.
3. Report every failure with the exact command to reproduce it.
4. Do NOT push on red — green here should mean green in CI.

Declared capabilities: run."""

_REVIEW_BODY = """\
Review the current branch's diff against ${project_name}'s binding contracts.

1. Read the contracts first (architecture / ownership / runtime), then the diff.
2. For each change check layer boundaries, mutation ownership, and the project's
   invariants. Flag violations with file:line and the rule they break.
3. Produce a verdict (approve / request-changes) + concrete fixes.
4. Do not edit — comment only. (The `review` stance pairs with this skill.)

Declared capabilities: comment."""

_REPO_HEALTH_BODY = """\
Audit ${project_name}'s documentation + session-log hygiene.

1. Run `python3 bootstrap.py check` — badges, link resolution, doc
   reachability, and the required session-log markers.
2. Summarize the drift: orphaned docs, missing badges, incomplete logs.
3. Fix the small ones (link the orphan, badge the doc); capture the rest as ideas.

Declared capabilities: run."""

_DEEP_RESEARCH_BODY = """\
Answer a multi-source factual question with a cited report.

1. Decompose the question into sub-questions; search broadly (fan out).
2. Fetch the strongest sources; cross-check claims adversarially; prefer
   primary/official docs over memory.
3. Flag uncertainty explicitly; never state a guess as fact.
4. Synthesize a concise report with inline citations.

Declared capabilities: run."""

_QUESTION_BODY = """\
Answer a direct question about ${project_name} concisely.

1. Read current-state + the one relevant doc or source file.
2. Answer in a few sentences, grounded in what you read; cite the source.
3. Make no changes. (The `question` stance pairs with this skill.)

Declared capabilities: read-only."""

_ANALYSIS_BODY = """\
Investigate a ${project_name} system and report findings, changing nothing.

1. Read the binding contracts and trace the behavior across files.
2. Produce evidence (file:line) + a conclusion; name the uncertainty.
3. Do not edit. (The `analysis` stance pairs with this skill.)

Declared capabilities: read-only."""

# Each skill declares the capabilities it needs *beyond* read (read is implicit).
# The declared set is what overrides the ambient stance (the precedence rule).
#
# ``grounds`` (grounded-skills plan §7.2, slice 2) is the skill's exact-command
# grounding: the verbatim command strings the body's procedure runs, as
# STRUCTURED DATA — never scraped from prose. Invariants (test-pinned): the
# key exists on every skill; each entry appears verbatim as a backticked span
# in the body (grounds can never drift from what the body actually says); a
# playbook skill's list is non-empty. Read-only skills ground nothing ([]).
# The index table surfaces the column; check_skill_grounds verifies each
# entry's command resolves (advisory, §8 Q2=B).
SKILLS: list[dict] = [
    {
        "name": "session-close",
        "description": "Land the session — claim, born-red card first, READY PR, "
        "batched work, close-out docs, flip complete last; never self-merge.",
        "capabilities": [EDIT, RUN],
        "body": _SESSION_CLOSE_BODY,
        "grounds": [
            "${verify_command}",
            "python3 bootstrap.py check --strict",
        ],
    },
    {
        "name": "upgrade-distribution",
        "description": "Roll a kit release out to one adopter repo — download, "
        "sha256 three-way, banked rollback, carve-out scan, born-red PR, "
        "tree-verified merge.",
        "capabilities": [EDIT, RUN],
        "body": _UPGRADE_DISTRIBUTION_BODY,
        "grounds": [
            "git fetch origin main && git reset --hard origin/main",
            "gh release download vX.Y.Z --repo menno420/substrate-kit "
            "--pattern 'bootstrap.py*' --pattern 'release.json'",
            "sha256sum bootstrap.py.new",
            "python3 bootstrap.py.new upgrade",
            "${verify_command}",
            "python3 bootstrap.py check --strict",
            "git fetch origin main && git log -1 --oneline origin/main",
            "git commit --allow-empty",
        ],
    },
    {
        "name": "release",
        "description": "Cut + publish a substrate-kit release — version bump PR, "
        "workflow_dispatch publish, three-way asset verification, adopter "
        "distribution wave.",
        "capabilities": [EDIT, RUN],
        "body": _RELEASE_BODY,
        "grounds": [
            "python3 src/build_bootstrap.py",
            "git diff --exit-code dist/bootstrap.py",
            "python3 -m pytest tests/ -q",
            "python3 -m ruff check src/engine/",
            "python3 src/build_release_json.py --version X.Y.Z --verify-only",
            "python3 dist/bootstrap.py check --strict",
            "gh workflow run release.yml -f version=X.Y.Z",
            "git fetch --tags && git tag -l vX.Y.Z",
            "gh release view vX.Y.Z",
            "python3 dist/bootstrap.py currency",
        ],
    },
    {
        "name": "intake",
        "description": "Turn a fragmented owner ask into main ideas, a restated "
        "fuller picture, a skill-index map, and structured-choice owner "
        "questions — before building (understand-and-reflect, executable).",
        "capabilities": [],
        "body": _INTAKE_BODY,
        "grounds": [],
    },
    {
        "name": "quality-gate",
        "description": "Run the project's full verification before pushing and "
        "report what must be fixed.",
        "capabilities": [RUN],
        "body": _QUALITY_GATE_BODY,
        "grounds": [
            "${verify_command}",
            "python3 bootstrap.py check --strict",
        ],
    },
    {
        "name": "review",
        "description": "Review the branch diff against the binding contracts; "
        "comment with a verdict and fixes, no edits.",
        "capabilities": [COMMENT],
        "body": _REVIEW_BODY,
        "grounds": [],
    },
    {
        "name": "repo-health",
        "description": "Audit doc + session-log hygiene (bootstrap check) and "
        "summarize drift.",
        "capabilities": [RUN],
        "body": _REPO_HEALTH_BODY,
        "grounds": [
            "python3 bootstrap.py check",
        ],
    },
    {
        "name": "deep-research",
        "description": "Fan out web research, adversarially verify sources, and "
        "synthesize a cited report.",
        "capabilities": [RUN],
        "body": _DEEP_RESEARCH_BODY,
        "grounds": [],
    },
    {
        "name": "question",
        "description": "Answer a direct question concisely from memory and source; "
        "make no changes.",
        "capabilities": [],
        "body": _QUESTION_BODY,
        "grounds": [],
    },
    {
        "name": "analysis",
        "description": "Read-only deep-dive: investigate and report findings "
        "without changing anything.",
        "capabilities": [],
        "body": _ANALYSIS_BODY,
        "grounds": [],
    },
]

_SKILL_BY_NAME = {s["name"]: s for s in SKILLS}


def skill_names() -> list[str]:
    """Return the available skill names, in declared order."""
    return [s["name"] for s in SKILLS]


def get_skill(name: str) -> dict | None:
    """Return the skill definition for ``name`` (or None if unknown)."""
    return _SKILL_BY_NAME.get(name)


def skill_capabilities(name: str) -> list[str]:
    """Return a skill's full capability set (declared + the implicit ``read``)."""
    skill = _SKILL_BY_NAME.get(name)
    if skill is None:
        return []
    return [READ, *skill["capabilities"]]


def skill_permits(name: str, action: str) -> bool:
    """True if skill ``name`` declares (or implies) ``action``."""
    return action in skill_capabilities(name)


def action_permitted(
    stance_name: str,
    action: str,
    skill_name: str | None = None,
) -> bool:
    """Resolve whether ``action`` is permitted under a stance, optionally in a skill.

    Precedence (plan section 3c): a skill's explicitly-declared capability **wins**
    over the ambient stance — so an invoked skill can do what it declares even when
    the stance forbids it. For anything the skill has not declared, the stance's
    advisory tool-scope applies.
    """
    if skill_name is not None and skill_permits(skill_name, action):
        return True
    return action_allowed(stance_name, action)


# A ``${slot}`` inside a grounds string, for the index's display rewrite —
# same braced-only form as engine.render._PLACEHOLDER_RE (skills.py cannot
# import render.py: render.py imports THIS module, and MODULE_ORDER puts
# skills before render).
_GROUND_SLOT_RE = re.compile(r"\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _ground_cell(grounds: list[str], context: dict[str, str] | None) -> str:
    """Render one index-table grounds cell (``—`` when the skill grounds nothing).

    Slot references inside a ground substitute from ``context`` when the
    project has filled them; an unfilled (or context-less) slot displays as
    ``<slot_name>`` — NEVER as a raw ``${slot_name}``, which would make the
    planted ``docs/SKILLS.md`` read as an unrendered doc forever
    (``with_unrendered_banner`` re-banners any text carrying ``${...}``, and
    the index is injected AFTER template substitution, so nothing would ever
    fill it). Multiple grounds join with ``<br>`` so the table stays one row
    per skill.
    """
    if not grounds:
        return "—"
    cells = []
    for ground in grounds:
        shown = _GROUND_SLOT_RE.sub(
            lambda m: (context or {}).get(m.group(1)) or f"<{m.group(1)}>",
            ground,
        )
        cells.append(f"`{shown}`")
    return "<br>".join(cells)


def skills_index_table(context: dict[str, str] | None = None) -> str:
    """Render the skill-index table (planted ``docs/SKILLS.md``) from :data:`SKILLS`.

    Engine-computed on purpose (grounded-skills plan §2, PR #263): the index's
    rows come FROM the same list that emits the skills, so the planted index
    can never hand-drift from what the kit actually installs — the "render
    from ONE source" rule. Consumed as the ``skills_index`` engine context key
    (:func:`engine.render.build_context` injects it on every render path);
    the surrounding prose lives in ``SKILLS-index.md.tmpl``.

    ``context`` (slice 2) fills slot references inside the Grounds column —
    ``build_context`` passes the project's slot values so a filled project's
    index shows its REAL verify command; without context (or unfilled) the
    slot displays as ``<slot_name>`` (see :func:`_ground_cell` for why raw
    ``${...}`` must never survive into the injected table).
    """
    lines = [
        "| Skill | When to reach for it | Capabilities | Grounds (exact commands) |",
        "|---|---|---|---|",
    ]
    for skill in SKILLS:
        caps = ", ".join(f"`{c}`" for c in skill_capabilities(skill["name"]))
        grounds = _ground_cell(skill.get("grounds", []), context)
        lines.append(
            f"| `{skill['name']}` | {skill['description']} | {caps} | {grounds} |"
        )
    return "\n".join(lines)


def skill_frontmatter(skill: dict) -> str:
    """Return the native ``SKILL.md`` YAML frontmatter (metadata-first loading)."""
    return f'---\nname: {skill["name"]}\ndescription: "{skill["description"]}"\n---'


def skill_relpath(skill: dict) -> str:
    """Return the emit path for a skill, relative to the skills root."""
    return f"skills/{skill['name']}/SKILL.md"


def skill_document(skill: dict, body: str) -> str:
    """Compose the full ``SKILL.md`` text from a skill + its (rendered) body."""
    return f"{skill_frontmatter(skill)}\n\n# {skill['name']}\n\n{body.rstrip()}\n"
