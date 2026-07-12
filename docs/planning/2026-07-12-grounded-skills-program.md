# Grounded skills program — kit-owned skills, capability self-knowledge, owner-assist standard (2026-07-12)

> **Status:** `plan`
>
> **Provenance: owner directive via coordinator, 2026-07-12**, given live in the
> coordinator chat (~09:20Z). Owner-directed live = the owner is the reviewer.
> **It supersedes the 2026-07-11 feature-growth freeze FOR THIS PROGRAM ONLY**
> (the freeze itself stays in force for everything else — `control/status.md`
> phase record, `docs/current-state.md` § Next action "Post-freeze state").
> This session ships the PLAN ONLY — no slice is implemented here; every slice
> in §7 is a follow-up session with its own PR.
>
> Evidence base: four survey passes over substrate-kit @ `c83b23e`, superbot @
> `0f42bea`, websites @ `b925072`, fleet-manager @ `9a8518f` (2026-07-12), plus
> the superbot night review `docs/eap/night-review-2026-07-12.md` (verified at
> superbot origin/main) relayed mid-session by the owner via the coordinator.
>
> Grep route: §1 directive · §2 architecture · §3 owner-assist standard ·
> §4 capability self-knowledge · §5 intake playbook · §6 gap map · §7 slices ·
> §8 owner questions.

---

## 1. Consolidated directive + provenance

**Provenance:** owner directive via coordinator, 2026-07-12, given live in the
coordinator chat (~09:20Z). Owner-directed live = owner is the reviewer.
Supersedes the 2026-07-11 feature-growth freeze **for this program only**.

**The directive, consolidated:** fleet agents fail in recurring ways traceable
to two root causes — **(1) they do not reliably know their own capabilities**,
and **(2) there is no centralized, defined skill/playbook set for recurring
actions**. The owner wants the Discord-bot pattern — *everything through tool
use and exact groundings* (superbot's AI answers only from registered,
allowlisted tools and an explicit grounding ledger, never from improvised
memory — `superbot docs/btd6/btd6-ai-tool-calling-plan.md`, `docs/subsystems/ai.md`)
— made **standard practice for all agent work, kit-owned and kit-distributed**:

1. **Capability self-knowledge** — generated + verified, not hand-drifted.
2. **A kit-owned skill/playbook layer with exact groundings** — exact
   commands, exact tool calls, exact links, exact file targets; not
   checklist prose.
3. **An owner-assist output standard** — paste-ready blocks, exact-destination
   links, or control-plane-rendered links; the owner never derives anything.
4. **An owner-request intake playbook** — Q-0254 (understand-and-reflect)
   codified executable: consolidate fragmented asks into their few main ideas,
   mapped to known step patterns.
5. **Cross-repo discoverability** — the kit is the single home, indexed into
   every adopter, **self-propagating**: the kit teaches agents to implement
   these practices themselves when something applicable comes along.

**The pattern being generalized** (from superbot's shipped bot AI, the survey's
distillation): capability = a registered, allowlisted, schema'd tool; truth =
an explicit grounding ledger fed only by approved tools; behavior = verified
against the ledger with reject → regenerate-once → refuse-with-provenance;
every decision leaves an audit row; **extension = a registration in a guarded
registry, not ad-hoc prompt text**. Applied to agent work: a recurring action
= a registered skill with exact groundings; a capability claim = a verified
ledger entry with evidence and freshness; an owner-facing output = a
format-checked block; growth = agents registering new skills/entries through
the kit's own machinery.

---

## 2. Architecture — where skills/playbooks live in the kit

**Build on the existing layer; extend, don't duplicate.** The kit already has
exactly the right substrate (`src/engine/skills/skills.py`): a skill is a
Python-module-defined procedure in the `SKILLS` list (skills.py:103), emitted
as a native `.claude/skills/<name>/SKILL.md` (YAML frontmatter + body); bodies
carry `${slot}` placeholders so every skill is project-aware; a skill declares
the capabilities it needs, and its declared capability takes precedence over
the ambient stance (skills.py module docstring). Seven ship today:
`session-close`, `quality-gate`, `review`, `repo-health`, `deep-research`,
`question`, `analysis`. `cmd_skills(target, build)` stages them under
`.substrate/skills/`; `--build` installs to `.claude/skills/`. **Adding a
playbook-grade skill is one `SKILLS` list entry + dist rebuild** — no new
mechanism needed for the skill bodies themselves.

### Artifact classification (template vs generated vs engine-computed)

| Artifact | Class | Mechanism |
|---|---|---|
| Skill bodies (playbooks) | **Generated** (staged, always regenerated) | `SKILLS` entry → `.substrate/skills/` → `--build` installs; regenerates on every adopt/upgrade, so playbooks can never be consumer-drifted |
| Skill index (`docs/SKILLS.md`) | **Template** (planted doc) | new `SKILLS-index.md.tmpl` + one `ADOPT_PLAN` tuple (adopt.py:52); hash-classified at upgrade like every planted doc — but see the single-source rule below |
| Index freshness (names/one-liners of the installed skills) | **Engine-computed** | render the index's skill table FROM the `SKILLS` list at plant time (the same code path that emits the skills), not hand-written prose — one source, the "render from ONE source" rule (`docs/reports/2026-07-12-prompt-template-hardening-input.md` §(b) closing line) |
| Boot-set pointer to the index | **Template edit** | one line each in `AGENT_ORIENTATION.md.tmpl`, `CONSTITUTION.md.tmpl`, `CLAUDE.md.tmpl` — the same four-place wiring `CAPABILITIES.md` already has |
| New engine-computed values (if any) | **Engine-computed** | `ENGINE_CONTEXT_KEYS` (render.py:35) + unconditional injection in `build_context`/callers — the `agreement_home` precedent, PR #261 |
| Owner-assist output standard | **Template** (extends existing) | extend `control-README.md.tmpl` (OWNER-ACTION's canonical home) + `collaboration-model.md.tmpl`; advisory checker extends `check_owner_actions.py` |
| Capability ledger | **Template today** (`CAPABILITIES.md.tmpl`) → gains an engine-refresh path (§4) | |

### Distribution — adopt/upgrade hash-classified re-render

A new doc = one `.tmpl` in `src/engine/templates/` + one `ADOPT_PLAN` tuple +
`python3 src/build_bootstrap.py`. It then flows automatically through: **adopt**
(new installs plant it, sha256 recorded via `record_doc_hash`), **upgrade**
(`engine/upgrade.py` classifies every planted doc by hash — `unchanged` /
`template-improved` / `consumer-edited` / `diverged` / `missing`; improvements
apply under `--apply-docs` to consumer-untouched docs; missing docs replant),
and **`render --live`**. Staged artifacts (skills, agents, hooks, CI) **always
regenerate at upgrade** — which is why playbook bodies belong in the staged
skill layer, not in planted docs: distribution is automatic and drift-proof.

### Discovery without repo-searching

Two layers, matching the two audiences:

1. **In-repo (every adopter):** a kit-generated **skill index** in the boot
   set. `docs/SKILLS.md` — one table: skill → when to reach for it → what it
   grounds (exact commands/tools) — rendered from the `SKILLS` list, planted
   by adopt, pointed to from `AGENT_ORIENTATION.md` (which already enumerates
   the full planted doc set: "this router reaches every live doc — keep it
   that way"). An agent booting any adopter sees the index in orientation and
   never greps for "how do we do X here".

2. **Fleet-level (the manager's prompt system):** the fleet-manager plug
   points from the survey (`survey-fleet-manager.md` §5, all verified at
   fleet-manager `9a8518f`):
   - `docs/prompts/v3/universal-startup.md` BOOT step 1's **`{{ORIENTATION_PATH}}`**
     slot — add the skill index to each seat's orient chain via the seat
     config in `docs/prompts/v3/tools/regen_b_files.py` (precedent: websites
     already carries `docs/CAPABILITIES.md` in exactly this slot).
   - `docs/prompts/v3/custom-instructions-core.md` seat-block **`{{WALLS}}`**
     slot — already *defined* as sourced from `docs/CAPABILITIES.md`; the
     kit-owned venue-scoped ledger (§4) upgrades the slot's source without
     changing the template.
   - `projects/UNIVERSAL.md` **wake-prompt fetch list** — "skill index = your
     playbook" as a fourth fetched part (needs a vN bump + owner re-paste per
     the edit-registry-first flow).
   - `projects/README.md` **Doctrine 4** — the declared render-target
     mechanism: "Future distribution belongs to the kit seat … when those
     templates ship, this registry becomes their render target." The kit
     shipping seat-prompt-feeding artifacts is the *named* plan of record on
     the fleet-manager side, not an invention of this program.
   - **The 8,000-char paste cap constraint** (all 8 assembled seat pastes sit
     at 7,943–7,998 chars — effectively zero headroom, `docs/prompts/v3/
     per-project/README.md` budget table): the skill index can NEVER be
     inlined into instructions/startup pastes. It rides the established
     **digest-plus-canonical-pointer pattern** (as the GEN-3 RIDER and
     PERMISSIONS blocks already do) or the orientation path as an in-repo doc
     read at boot. **Digest + pointer, never inline** is a design invariant
     for every fleet-facing artifact in this program.

---

## 3. Owner-assist output standard

The kit has half of this: the **OWNER-ACTION six fields** (WHAT / WHERE / HOW /
WHY-IT-MATTERS / UNBLOCKS / VERIFIED-NEEDED) are canonical in
`control-README.md.tmpl`, enforced advisory by `check_owner_actions.py`,
cross-referenced by `check_capability_xref.py`. But that covers only the
*needs-owner ask*. The missing general standard for **all owner-facing
output** extends **Q-0263.2** (superbot router: "Agents never route derivable
values or safety string-work to the owner … an ask that requires the owner to
parse, derive, or transform anything is a drafting defect") plus the
maintainer-profile riders (risk-class labels `✅ / ↩️ / ⚠️` on every manual
step; do-the-arithmetic; phone-actionable).

### 3.1 The paste-ready block rules

1. **Finished one-paste values.** Every value the owner must enter is computed
   and printed final — `NAME=value`, full command, full file body — never a
   recipe for deriving it. Full files go in one copyable fenced block.
2. **Exact destination named.** Every action names its exact destination:
   deep URL, console path to the exact field ("Railway → project `websites` →
   service `control-plane` → Variables"), or repo path + line. Never "go to
   settings".
3. **Risk class on every manual step:** `✅ safe / read-only`, `↩️ reversible`,
   `⚠️ irreversible / destructive` (maintainer-working-profile standing rule).
4. **Structured choices, recommendation first.** A decision put to the owner
   is options A/B(/C) with a **bolded recommendation** and one-line rationale,
   answerable with one letter (idea-engine CLAUDE.md carries this as adopter
   prose today — Q-0263.2; this program makes it kit template text). §8 of
   this plan practices the format.
5. **Large outputs: digest in chat + rendered link, never a wall of text.**

### 3.2 Exact-destination link rules

- Deep-link the exact file, never the repo root; prefer the control-plane
  render (below) for markdown the owner should *read*, the GitHub blob URL
  for things he should *edit*.
- Post-merge, link `ref=main` (stable); pre-merge, the branch ref works too.
- The control-plane cache is 180 s TTL — append `&refresh=1` when the owner
  must see a just-pushed change.

### 3.3 The control-plane link pattern (verified live)

From `survey-websites.md` (verified against websites @ `b925072`):
**`GET /journal/{repo}/file?path=<path>&ref=<ref>` already renders any
committed markdown file as sanitized HTML** (headings, tables, fenced code;
non-markdown as escaped `<pre>`) at
**https://control-plane-production-abb0.up.railway.app** — for exactly **4
repos**: `superbot`, `superbot-next`, `substrate-kit`, `websites`
(app/main.py `journal_file`, app/config.py REPOS, app/journal.py
`render_markdown`, docs/site.md Routes table, [D-0020]). **Fleet-wide coverage
is a ~20-line repo-guard widening** in the websites repo (`github.fetch_file`
already reads any public menno420 repo; only the `repo not in config.REPOS`
route guard blocks the rest) — §7 slice 7. **Private repos (fleet-manager)
wait on the queued GITHUB_TOKEN owner action** (token currently UNSET on the
live service — websites `docs/owner/OWNER-ACTIONS.md`, existing queued ask,
not new work).

### 3.4 Fully worked example (the standard applied)

An agent finishing a large report for the owner emits, in chat:

```
📄 Adopter-outcomes report — shipped (PR #247, merged b862e9a)

Digest: before/after adoption is unmeasurable (9/10 adopters born <20h before
their kit-install PR); false-claim audit near-clean (1 confirmed, self-corrected
in 6 min); post-adoption time-to-ship baselines recorded.

Full report (rendered, phone-readable):
https://control-plane-production-abb0.up.railway.app/journal/substrate-kit/file?path=docs/reports/2026-07-11-adopter-outcomes-measurement.md

⚑ OWNER-ACTION — set GITHUB_TOKEN on the control-plane service
WHAT: paste one variable into Railway so private-repo pages stop degrading.
WHERE: railway.app → project `websites` → service `control-plane` → Variables
       → New Variable.
HOW (paste-ready): name `GITHUB_TOKEN`, value = the fine-grained PAT you
       created for menno420 repos (contents: read). One paste, Save.
RISK: ↩️ reversible — delete the variable to undo.
WHY-IT-MATTERS: fleet-manager (private) renders show "not-configured" banners
       until this is set; API reads ride the anonymous rate limit.
UNBLOCKS: /journal file renders + /queue items for private repos.
VERIFIED-NEEDED: attempted 2026-07-11 — raw fetch of a private path returns
       404 without a token (exact error in websites docs; token-on-raw also
       verified NOT to work, so the API fallback is the only private path).
```

Every element above is the standard: digest + rendered deep link, six-field
ask, finished values, exact console path, risk class, verified evidence.

---

## 4. Capability self-knowledge — generation + verification, not prose exhortation

### 4.1 What ships today (mostly built — the owner's "partly done" is accurate here)

- **`CAPABILITIES.md.tmpl` → `docs/CAPABILITIES.md` is in `ADOPT_PLAN`**
  (adopt.py:52 block; ORDER 006, PR #63): pre-seeded verified
  capabilities/walls + **THE DISCOVERY RULE** (4 steps: check the file →
  check the env (`printenv` before assuming no credentials) → attempt once +
  capture the exact error → append the finding same session) + an append log
  with a line grammar (`- YYYY-MM-DD · capability|wall · finding · evidence ·
  workaround`).
- **Wired in four places:** `CLAUDE.md.tmpl` orientation ("before declaring
  any wall or missing credential"), `CONSTITUTION.md.tmpl` bullet,
  `AGENT_ORIENTATION.md.tmpl` planted-doc list, and the `session-close` skill
  step 2 (capability delta → append).
- **Advisory verification exists:** `src/engine/checks/check_capability_xref.py`
  cross-references OWNER-ACTION `VERIFIED-NEEDED` walls against the ledger
  both ways (`owner-ask-wall-unrecorded`, `owner-ask-capability-resolved`).
- **Proven load-bearing:** the kit's trigger forensics
  (`docs/reports/2026-07-12-trigger-forensics.md`) root-caused H1 off a
  *recorded unknown* in the ledger ("fresh-session-per-fire scheduling
  unverified" @ 9f5d8e2).

### 4.2 The gaps, and the mechanism to close them

**(a) Capabilities are venue-scoped, not global** *(owner/night-review input
relayed mid-session, 2026-07-12; evidence verified at superbot origin/main
`docs/eap/night-review-2026-07-12.md`)*. The same operation behaved three
ways in one night depending on venue: `fire_trigger` **worked** from the
review session on a fresh-session trigger (kit-lab re-fired 08:46Z), was
**org-refused** on a trigger bound to another session ("not enabled for this
organization" — night-review §1 timeline 08:5x, lesson 2), and **prompted**
in the plain-started hub session despite exact `.claude/settings.json` allow
entries while **never prompting** in Routine-spawned coordinator seats whose
grants ride the spawn-time `session_context` per-tool `always_allow`
(night-review lesson 3; "in an unattended session, a prompt is a silent
stall"). **A flat CAN/CANNOT ledger is therefore wrong somewhere by
construction.** The kit-generated record must be **(venue × operation)**, plus
a **posture decision rule** consuming it: owner-live session = assume no
special limitations, act directly (superbot Q-0269); autonomous/routine-fired
seat = pre-route around every known stall class, park only on a real denial
(superbot Q-0270 boot triad: model · venue · ability envelope, established at
session start). Q-0270 is superbot **prose written deliberately as a
local-copy-until-the-kit-ships-it** — the kit artifact here is designed to
**REPLACE it at the next upgrade**, the same collapse pattern Q-0254 followed
(local rule → kit template → local copy retired).

Concrete shape: the ledger's capability/wall entries gain a **venue column**
(values seeded from the boot triad: `owner-live` · `autonomous-project` ·
`routine-fired` · `subagent` · `any`), and the template's header gains the
two-line posture rule. The append-line grammar extends compatibly:
`- YYYY-MM-DD · capability|wall · <venue> · finding · evidence · workaround`.

**(b) Verified entries age.** A capability refutation partially self-resolved
overnight (platform-side fix of a Routines model-display bug — relayed with
the same night-review batch): a ledger without freshness data becomes
**confidently stale**, which is worse than ignorant. Two additions: **a
per-entry last-verified date** (the append grammar already dates entries; the
seeded template rows need dates added, and re-verifications append rather
than edit — the log stays append-only) and **a staleness clause as discovery
rule step 5**: *"an entry older than the staleness window (default: the
config's `staleness_days`, 14) that your work depends on is a claim, not a
fact — re-verify with one cheap attempt before building on it, and append the
re-verification."* Cheap, uses the existing config knob, and turns the
existing 4-step rule into a closed loop.

**(c) Upgrade-time refresh for consumer-edited ledgers.** Today the seeds are
a frozen 2026-07 snapshot baked into the template; a consumer-edited
`docs/CAPABILITIES.md` (which every *good* adopter has, by design — appending
is the point) classifies `consumer-edited` at upgrade and **never receives
new fleet-wide findings**. Mechanism: split the file into a **kit-owned seed
section** (fenced by markers, refreshed at upgrade the way staged artifacts
regenerate) and the **consumer append log** (never touched by upgrade). The
upgrade step re-renders only the marker-fenced block; a modified block
downgrades to a report line in `upgrade-report.md` rather than clobbering.

**(d) Verification: advisory → enforcing where safe.** Extend
`check_capability_xref.py`: (i) grammar-check append-log lines (the writer
and enforcer share `grammar.py` constants — the established pattern);
(ii) flag ledger entries older than `staleness_days` that a session card's
close-out cites (advisory); (iii) keep the existing two-way OWNER-ACTION
xref. Graduation to enforcing follows the kit's provenance-header /
kill-switch rule: prove reliability across sessions first.

**(e) Fleet-level sync/visibility.** Today: one prose pointer ("Fleet master
copy: menno420/fleet-manager → docs/capabilities.md"), plus a named drift
case (venture-lab carries BOTH `docs/CAPABILITIES.md` and
`docs/capabilities.md` — fleet-manager `projects/_inventory/inventory-lanes.md:84`).
Mechanism: the manager consumes each adopter's ledger through the existing
tree-scan machinery (`engine/currency.py` precedent — scan trees, not
heartbeats), and fleet-wide findings travel back as kit seed-section updates
at the next release. The kit is the distribution channel; fleet-manager is
the aggregation point; no third copy.

---

## 5. The intake playbook — Q-0254 codified executable

A new kit-shipped skill (working name **`intake`**), one `SKILLS` list entry,
using the superbot skill anatomy (survey-superbot.md §1: `# /<name>` →
one-line purpose → **What this does** → **Invocation** → numbered
**Instructions** with exact steps → mandated **report format**; "wrapper
around the existing procedure, not new policy" — the procedure is Q-0254,
already kit doctrine prose in three templates).

Draft body (the skill as it would ship, slots included):

```markdown
# /intake — owner-request intake (understand-and-reflect, executable)

Turn a fragmented owner ask into a verified fuller picture before building.
Wrapper around the understand-and-reflect doctrine (CONSTITUTION.md), not new
policy. Invoke on any non-trivial, non-mechanical owner ask.

## Invocation
/intake <the ask, or a pointer to it>

## Instructions
1. CONSOLIDATE — reduce the fragmented ask to its few MAIN IDEAS (usually
   1–3). Name each in one line. The owner builds ideas iteratively and in
   fragments by design; consolidation is your half of the contract.
2. RESTATE — state back, inline in your first substantive response (never a
   blocking question), the fuller picture: the implied specs, surrounding
   constraints, likely intended scope, and the follow-on the owner probably
   wants but didn't spell out. One wrong assumption stated now costs one
   correction; found after an hour of building it costs the hour.
3. MAP — map each main idea to known step patterns via the skill index
   (`docs/SKILLS.md`): which existing skill/playbook/checklist covers it,
   which parts are genuinely new. Cite the exact skill or doc per idea.
4. POSSIBILITY SPACE — when the ask starts from uncertain feasibility ("I
   don't know if this is even possible" is a normal starting point, not an
   edge case), surface what is achievable and by what approaches FIRST,
   before committing to a direction. Target: the most advanced capability
   reachable by the simplest, most efficient implementation.
5. DECIDE-AND-FLAG — decide every reversible-until-a-gate call yourself
   (recommendation + one-line rationale + a flag on the run report). Route
   to the owner only genuine product/intent ambiguity, as a structured
   choice with a bolded recommendation (the owner-assist output standard).

## Report format
Print: MAIN IDEAS (numbered) · FULLER PICTURE (short prose) · MAP (idea →
skill/pattern/new) · [POSSIBILITY SPACE if triggered] · DECISIONS FLAGGED ·
QUESTIONS FOR OWNER (structured choices, or `none`).

Declared capabilities: read.
```

A trivial or fully-unambiguous ask stays exempt (one-line "doing X because
Y") — same calibration as Q-0254 itself. The skill's existence closes the
survey's finding: the doctrine's *what* ships in three templates; the *how*
ships nowhere.

---

## 6. Honest gap map

The owner called this program "partly done" — correct for capability
self-knowledge and the skill *skeleton*; wrong for playbook depth, intake,
output standard, index, refresh, and fleet render. Row by row:

| Capability | Exists today (cite) | Gap |
|---|---|---|
| Capability ledger, generated per repo | ✅ `CAPABILITIES.md.tmpl` in ADOPT_PLAN (adopt.py:52); 4-step DISCOVERY RULE; wired in 4 places; `check_capability_xref.py` advisory | Seeds frozen (2026-07 snapshot); no upgrade refresh for consumer-edited ledgers; **flat, not venue-scoped** (§4.2a); **no freshness/staleness data** (§4.2b); fleet sync is one prose pointer + a live duplicate-file drift case |
| Skill layer (emit pipeline) | ✅ `src/engine/skills/skills.py` SKILLS list → slot-rendered SKILL.md → staged → `--build`; 7 skills ship | **Bodies are short checklists, not exact-command playbooks** — no trigger-arming recipe, no PR-landing recipe, no verbatim tool-call shapes (superbot's 12 skills show the target grade: numbered steps with exact commands + mandated report format) |
| Landing-path doctrine (born-red/flip-last, never-self-merge, designed-red reading) | ❌ the gate WORKFLOW ships; its doctrine text does not (graduation map row, `docs/reports/2026-07-12-prompt-template-hardening-input.md` §(b): `landing-path.md.tmpl` missing) | New template or playbook skill; designed-red reading matters — this very session's 3 CI reds were all the designed hold (W-9 class) |
| Routine/wake-chain doctrine (binding choice, verbatim create-call records, re-verify at wake, pacing) | ❌ graduation map row: `routines.md.tmpl` missing; fleet-manager meta names it "the known kit gap" | New template/skill; night-review lessons (wedge signature `enabled ∧ next_run_at < now−15min`, probe-not-record) are the seed content |
| Verify-don't-trust Evidence block | ❌ graduation map row: CONSTITUTION.md.tmpl has only fragments (`drift_resolution` slot) | New CONSTITUTION bullet block; trigger-forensics report supplies the exact doctrine sentences |
| Preflight fetch + hard-reset first step | ❌ graduation map row: missing as an explicit first step in CLAUDE/AGENT_ORIENTATION tmpl | One orientation-step edit |
| Owner-request intake procedure | ❌ Q-0254 doctrine prose ships in 3 templates; **no skill/checklist gives the how** | §5 skill — one SKILLS entry |
| Owner-assist output standard | ◐ OWNER-ACTION six fields (control-README.md.tmpl) + `check_owner_actions.py`, advisory; **nothing beyond the ask format** | No paste-ready/structured-choice/link-rules standard for general outputs; idea-engine's Q-0263.2 adopter prose is ahead of the kit |
| Skill index / router | ❌ none — no `docs/SKILLS.md`, no boot-set pointer; agents discover skills by directory listing or not at all; fleet-manager has **no `.claude/skills/` and no skill reference anywhere** (greenfield) | §2 index + wiring |
| Single-source render shared with fleet prompts | ❌ fleet-manager hand-generates its 8 seat prompts from its own `docs/prompts/v3/`; kit templates and fleet prompts can drift apart; Doctrine 4 declares the kit-render intent but nothing implements it | §7 slice 6; the hardening report calls this "the highest-leverage single change" |
| Control-plane render for owner links | ◐ live for 4 repos (`/journal/{repo}/file`) with sanitized markdown render + copy machinery | Guard limited to 4 repos (~20-line widening, websites repo); private repos blocked on the queued GITHUB_TOKEN owner action |
| Self-propagation (agents extend the practice) | ◐ precedents exist (superbot fleet-vocab growth loop "prose → vocab row → skill"; friction→guard; Q-0105 adopt-freely) | No CONSTITUTION clause makes skill-registration the *expected reflex* when a recurring action appears; propose-don't-apply boundary for binding text needs stating |

---

## 7. Phased implementation slices

Each slice = **one merged-on-green PR**, ordered by leverage. **None is
implemented in this session** — this plan is the whole deliverable; slices are
follow-up sessions. Order is evidence-based but adjustable on new evidence.

1. **Skill-index skeleton + boot-set wiring** *(kit)* — `docs/SKILLS.md`
   rendered from the `SKILLS` list (engine-computed table), planted via
   ADOPT_PLAN; pointer lines in AGENT_ORIENTATION/CONSTITUTION/CLAUDE
   templates; dist rebuild. *Accept:* fresh adopt plants the index; the index
   names all 7+ skills with when-to-use lines; `check --strict` green;
   existing adopters receive it at next upgrade as `missing → replanted`.
2. **Playbook-grade skill bodies for the top recurring actions** *(kit)* —
   upgrade `session-close` to the full landing-path playbook (born-red card →
   flip-last → designed-red reading → never-self-merge), add
   `upgrade-distribution` (the wave runbook: download → sha256 three-way →
   bank old dist → carve-out scan → born-red PR → verify merged main) and
   `release` (the cut runbook) — exact commands, verbatim check invocations,
   mandated report formats (superbot anatomy). *Accept:* each body names only
   commands that exist; suite green; bodies regenerate at upgrade.
3. **Intake-playbook skill** *(kit)* — §5's `/intake` as a SKILLS entry +
   index row. *Accept:* skill stages + installs; report format matches §5.
4. **Owner-assist output standard** *(kit)* — §3 rules into
   `control-README.md.tmpl` (extend OWNER-ACTION section) +
   `collaboration-model.md.tmpl`; worked examples included;
   `check_owner_actions.py` extended advisory (risk-class token present on
   manual steps; bare "go to settings"-class asks flagged). *Accept:* checker
   green on well-formed asks, flags the anti-patterns from Q-0263's incident.
5. **Capability refresh + venue-scoping + staleness + enforcement** *(kit)* —
   §4.2 in full: venue column + posture rule (replaces superbot Q-0270 local
   prose at its next upgrade), per-entry dates + discovery-rule step 5
   (staleness clause, `staleness_days` knob), marker-fenced seed section with
   upgrade-time refresh, `check_capability_xref` extensions (grammar +
   staleness, advisory). *Accept:* upgrade on a consumer-edited ledger
   refreshes only the fenced seed block; xref checker validates the new
   grammar; superbot's Q-0270 collapse documented in the upgrade report.
6. **Fleet-manager single-source render integration** *(kit + fleet-manager,
   coordinated)* — kit ships the seat-prompt-feeding artifacts (skill-index
   digest block, WALLS-source render) so `projects/` becomes the render
   target per Doctrine 4; fleet-manager side: `regen_b_files.py` seat configs
   point `{{ORIENTATION_PATH}}`/`{{WALLS}}` at the kit-generated files;
   UNIVERSAL wake fetch list gains the index (vN bump, owner re-paste).
   *Accept:* `--check-registry`-style drift guard proves prompt blocks equal
   kit truth; 8,000-char budgets still fit (digest + pointer, never inline).
7. **Control-plane guard widening** *(websites repo — distribution scope)* —
   the ~20-line `/journal/{repo}/file` repo-guard widening to fleet lane
   repos (survey-websites.md §5 options a/b), tests included. Private-repo
   rendering stays gated on the owner's GITHUB_TOKEN action (already queued —
   not this slice's work). *Accept:* a lane-repo markdown path renders; 404
   behavior for unknown repos unchanged; websites suite green.
8. **Self-propagation doctrine** *(kit)* — CONSTITUTION.md.tmpl clause: when
   an applicable recurring action appears, agents add/extend the skill (the
   registration reflex — extension = a registry entry, not ad-hoc prose),
   with **propose-don't-apply preserved for binding text** (skills/index =
   free to ship; CONSTITUTION/binding-rule changes = router proposal). Plus
   the superbot fleet-vocab growth loop generalized: prose workflow → index
   row → promoted skill. *Accept:* clause renders in fresh adopts; wording
   keeps the existing propose-don't-apply boundary intact.

Graduation-map ❌ rows not named above (`routines.md.tmpl` doctrine,
verify-don't-trust Evidence block, preflight step) ride slices 2 and 8's
template edits or a small follow-on — they are content, not new mechanism.

---

## 8. Open questions for the owner

*Structured choices — answerable with one letter each; recommendation bolded.
Everything else in this plan is decide-and-flag and proceeds unless vetoed.*

```
Q1 — Default channel for large owner-facing outputs?
  A) Control-plane link + 3-line digest in chat (phone-friendly, one tap;
     needs slice 7 for full fleet coverage).
  B) Full text in chat every time (no dependency, but walls of text on a
     phone).
  RECOMMENDATION: A — you already read fleet state on the control plane, and
  the digest keeps chat scannable; B stays the fallback for repos the plane
  can't render yet.

Q2 — Should the skill/playbook layer become a required gate, or stay advisory?
  A) Advisory: skills + index ship, sessions are expected to use them, no CI
     enforcement of "you followed the playbook".
  B) Enforcing where cheap: advisory now, plus grammar-level checks (e.g.
     owner-ask format, capability-ledger line grammar) graduate to CI-red
     once proven reliable over multiple sessions (the kit's existing
     kill-switch rule).
  RECOMMENDATION: B — matches "enforce, don't exhort" (PL-007) without
  betting CI on unproven checkers; pure process-compliance stays advisory
  forever.

Q3 — Does fleet-manager's seat-prompt render move onto kit-shipped sources
     (slice 6)?
  A) Yes — kit ships the canonical blocks; fleet-manager's regen tool renders
     seat prompts from them (Doctrine 4's declared plan; one source, zero
     drift).
  B) No — fleet-manager keeps hand-owning docs/prompts/v3; the kit only
     ships in-repo docs.
  RECOMMENDATION: A — the hardening report calls single-source render "the
  highest-leverage single change"; the drift class it kills (seat prompt
  contradicting kit truth) is already evidenced.

Q4 — Freeze interaction for the implementation slices (1–6, 8 are new kit
     surface → MINOR releases under the freeze you set 2026-07-11)?
  A) The program supersession covers its slices: build, merge, and cut MINOR
     releases as slices land (your directive already scoped the supersession
     to this program).
  B) Build + merge to main, but hold release/distribution until you lift the
     freeze explicitly.
  RECOMMENDATION: A — an unreleased slice helps no adopter, and the
  supersession was given for exactly this program; each release still rides
  the normal runbook + your standing veto window.
```

---

*Plan lane: PR #263, session card `.sessions/2026-07-12-grounded-skills-program.md`,
claim `control/claims/claude-grounded-skills-program.md` (deleted at close).*
