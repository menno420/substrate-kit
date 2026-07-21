# Project closeout — substrate-kit

> **Status:** `reference`
>
> A standalone handover for two readers who start from zero: the repository
> owner, and a fresh future agent session. It explains what this repo is, what an
> intensive run of autonomous agent sessions accomplished, exactly where things
> stand as of 2026-07-21, and what to do next. Every claim links to a merged pull
> request, a release tag, or a file, so you can verify rather than trust.

## 1 · What this project is, and what was accomplished

**The project.** substrate-kit is a *portable workflow kit*. A repository installs
it as a single vendored `bootstrap.py` plus a small `.substrate/` state directory,
and in return gets a uniform agent operating doctrine: a self-checking quality gate
(`python3 bootstrap.py check --strict`), session-card discipline, capability and
routine ledgers, and a rendered working agreement (`.claude/CLAUDE.md`). This repo
is the source of truth; doctrine graduates into `src/engine/templates/` and ships to
adopter repositories as versioned releases. The point of the kit is that the claims
it makes about how to work are *enforced by checks*, not merely written down.

**What this run shipped.** (Each item links to the pull request or tag that landed it.)

### Releases
Four releases cut this run, newest last:
[v1.19.0](https://github.com/menno420/substrate-kit/releases/tag/v1.19.0) (`598f820`) →
[v1.20.0](https://github.com/menno420/substrate-kit/releases/tag/v1.20.0) (`4a077ec`) →
[v1.20.1](https://github.com/menno420/substrate-kit/releases/tag/v1.20.1) (`40eb0fe`) →
[v1.20.2](https://github.com/menno420/substrate-kit/releases/tag/v1.20.2) (`4712ebf`).
v1.20.2 is the current kit version; its tag commit `4712ebf` is the merge of
[#561](https://github.com/menno420/substrate-kit/pull/561).

### The claims-only fast-lane guard stack
The gate lets a control-only change (a diff touching only `control/**`) skip the
born-red session-card requirement — the "control fast lane". A guard stack keeps that
lane honest and keeps the kit-side and adopter-side guards in parity:
[#455](https://github.com/menno420/substrate-kit/pull/455),
[#457](https://github.com/menno420/substrate-kit/pull/457); guard-parity
[#459](https://github.com/menno420/substrate-kit/pull/459),
[#463](https://github.com/menno420/substrate-kit/pull/463),
[#465](https://github.com/menno420/substrate-kit/pull/465),
[#466](https://github.com/menno420/substrate-kit/pull/466); surface censuses
[#470](https://github.com/menno420/substrate-kit/pull/470),
[#493](https://github.com/menno420/substrate-kit/pull/493).

### The Model-line exit-gate trilogy
The `📊 Model:` line on a session card is now machine-checked. Three gates fire on a
born-red added card: task-class must match one of nine sanctioned classes
([#512](https://github.com/menno420/substrate-kit/pull/512)); the model name must be
family-level, not an exact dated model ID
([#513](https://github.com/menno420/substrate-kit/pull/513)); and effort must be one of
low/medium/high ([#514](https://github.com/menno420/substrate-kit/pull/514)). A passing
line looks like `- **📊 Model:** opus-4.8 · high · docs-only`.

### Doctrine recipes
Reusable "how to do this class of change" recipes graduated into the kit: the
pinned-feed-contract recipe
([#482](https://github.com/menno420/substrate-kit/pull/482)), the
advisory-to-born-red-gate graduation recipe
([#516](https://github.com/menno420/substrate-kit/pull/516)), and folded-gate
remediation ([#484](https://github.com/menno420/substrate-kit/pull/484),
[#510](https://github.com/menno420/substrate-kit/pull/510)).

### The grounded-skills measurement program
A before/after measurement of the grounded-skills work, with frozen result data:
[#476](https://github.com/menno420/substrate-kit/pull/476),
[#477](https://github.com/menno420/substrate-kit/pull/477),
[#479](https://github.com/menno420/substrate-kit/pull/479). The written report is
[docs/reports/2026-07-19-grounded-skills-measurement.md](reports/2026-07-19-grounded-skills-measurement.md).

### Hardening and tooling
Roughly two dozen hardening and tooling slices landed across
[#488](https://github.com/menno420/substrate-kit/pull/488)–[#546](https://github.com/menno420/substrate-kit/pull/546).
Standouts: the `/scope-backlog-item` skill
([#490](https://github.com/menno420/substrate-kit/pull/490)), `check --remediate`
([#524](https://github.com/menno420/substrate-kit/pull/524)), the freeze/verify pair
([#529](https://github.com/menno420/substrate-kit/pull/529)), and clone-depth
provenance ([#537](https://github.com/menno420/substrate-kit/pull/537)).

### The false-wall gate hardening arc
The `check_no_false_walls` gate — which stops the kit from writing down an
agent-capability wall as if it were permanent — was hardened through four rounds of
independent adversarial review:
[#549](https://github.com/menno420/substrate-kit/pull/549), then
[#558](https://github.com/menno420/substrate-kit/pull/558),
[#559](https://github.com/menno420/substrate-kit/pull/559),
[#560](https://github.com/menno420/substrate-kit/pull/560),
[#561](https://github.com/menno420/substrate-kit/pull/561). This arc is what v1.20.2
released. One known limitation is carried forward (see Continuation item e).

### The v1.20.x adopter wave
Seven of ten tracked repositories were brought current on the kit this run, each via a
merged upgrade PR in its own repo:
[gba-homebrew #211](https://github.com/menno420/gba-homebrew/pull/211),
[fleet-manager #390](https://github.com/menno420/fleet-manager/pull/390),
[idea-engine #740](https://github.com/menno420/idea-engine/pull/740),
[superbot-games #183](https://github.com/menno420/superbot-games/pull/183),
[superbot-mineverse #138](https://github.com/menno420/superbot-mineverse/pull/138),
[websites #452](https://github.com/menno420/websites/pull/452),
[venture-lab #282](https://github.com/menno420/venture-lab/pull/282). The remaining
re-vendor to v1.20.2 for two repos is tracked in Continuation (items a, b).

## 2 · Current true state (verified live 2026-07-21)

- **Kit version:** v1.20.2, tag commit `4712ebf`. Sources agree:
  `dist/bootstrap.py` `KIT_VERSION = "1.20.2"` and `substrate.config.json`
  `"kit_version": "1.20.2"`.
- **Adopter registry:** [docs/adopters.md](adopters.md), regenerated for this closeout.
- **Tests:** ~2,040 test functions under `tests/` (recent cards report ~2,070 collected).
- **Open PRs:** exactly one —
  [#552](https://github.com/menno420/substrate-kit/pull/552), labelled
  `do-not-automerge`, parked for owner ratification (Continuation item c). Every other
  PR from this run reached a terminal state.

## 3 · Continuation — what a future session or the owner picks up, in priority order

**a. trading-strategy #160 — owner governance decision.** The adopter's tree diverges
from fleet doctrine at `current-state.md:389` and `CONSTITUTION.md:166`. The owner
decides between *align-to-fleet* (change the adopter to match) and *keep + allowlist*
(record the divergence as intentional). Once decided, the resident session rewords
`review-queue.md:8` to match. This is a genuine product/governance call — it waits for
the owner.

**b. superbot-next #602 — resident fix, then it goes green.** The product test suite
already passes; the only reds trace to two documentation lines that trip the false-wall
gate. A resident session fixes exactly `current-state.md:101` and `current-state.md:118`
and all four checks go green. No governance question here — it is a mechanical doc fix.

**c. substrate-kit #552 — owner ratifies or rejects.** A shape-2 headless
guard-observability step for the T5 bench task, deliberately held (`do-not-automerge`,
pin path). It waits for the owner: a deliberate merge ratifies it, closing rejects it.
Resume context lives in the PR body.

**d. superbot pin-only bump — owner question.** A pin-only version bump for superbot
awaits an owner A/B decision. No agent work is blocked.

**e. Hardening idea: two-line-spanning-quote repudiation false positive.** A documented
known limitation from the #549–#561 arc: a legitimate wall-repudiation whose quoted
phrase spans a line break currently reds the false-wall gate (the safe direction — a
false red is cheaper than a real wall going green). Fix per-doc by collapsing the quote
to one line, or allowlist it. Future hardening: detect a quote that opens on the wall
line and closes on the next.

**f. Operational decisions — owner.** The kit-lab daily cron (recreate vs retire) and
the repository-visibility decision (public-flip vs PAT) both await the owner.

## 4 · Owner walkthrough (plain language, clickable)

- **See the releases:**
  [github.com/menno420/substrate-kit/releases](https://github.com/menno420/substrate-kit/releases).
  The newest is v1.20.2 — that is what every current adopter now runs.
- **Read the measurement report:**
  [docs/reports/2026-07-19-grounded-skills-measurement.md](reports/2026-07-19-grounded-skills-measurement.md)
  — the before/after on the grounded-skills work, with the raw numbers frozen alongside it.
- **The doctrine recipes** live under [docs/recipes/](recipes/) — reusable playbooks for
  common change shapes.
- **The adopter registry** is [docs/adopters.md](adopters.md) — which repo runs which kit
  version, generated from live discovery.
- **Commands you can paste** (from the repo root):
  - `python3 bootstrap.py check --strict` — run the full quality gate.
  - `python3 bootstrap.py check --why "<phrase>"` — explain why a specific line is flagged.
  - `python3 bootstrap.py check --remediate <kind>` — apply a guided fix for a finding class.
  - `python3 tools/measure_grounded_skills.py --json --freeze` — reproduce and freeze the
    grounded-skills measurement.
- **Your checklist (quickest first):**
  1. trading-strategy #160 — pick align-to-fleet **or** keep+allowlist (A/B).
  2. substrate-kit #552 — merge to ratify **or** close to reject.
  3. kit-lab daily cron — recreate **or** retire (A/B).
  4. Repository visibility — public-flip **or** PAT (A/B).

## 5 · Working this repo with a fresh session

- **Boot route:** read `CONSTITUTION.md` → `control/status.md` → this closeout. That is
  enough to orient; everything else is routed on demand.
- **Verify a change:** `python3 bootstrap.py check --strict` must be green before you push.
- **How PRs land:** branch `claude/<slug>`; the first commit is a born-red session card
  (`> **Status:** \`in-progress\``) which holds the merge; open the PR ready; do the work;
  flip the card to `complete` as the deliberate last step, which releases the
  auto-merge-enabler to land it on green. A control-only diff (touching only `control/**`)
  rides the `claim/*` fast lane with no card. A PR labelled `do-not-automerge` is the
  owner's lane — never auto-merge it.
- **Gotchas:** born-red PRs show red checks by design (two are legacy aliases mirroring
  kit-quality; only the Session-gate hold is real). The distributed `dist/bootstrap.py` is
  built only via `build_bootstrap.py` — never hand-edit it; edit the source under `src/`
  and rebuild. Exclude `bootstrap.py` and `.substrate/` from repo-wide searches (they are
  generated machinery). GitHub MCP reads of PR state lag by ~25 minutes — cross-check live
  before relying on a PR's status.

---

*This project ran as a series of autonomous agent sessions. As of 2026-07-21 the seat is
closed; only committed work survives. This document is the durable record.*
