# 2026-09-04 · Adoption profiles — K1–K5 for the `estate` seed

> **Status:** `complete`

- **📊 Model:** opus-5 · xhigh · feature build
- **📍 Venue:** cloud-container
- **🔗 Session:** [session_01Y3DjrdYmx4ahPkvdZnWNNm](https://claude.ai/code/session_01Y3DjrdYmx4ahPkvdZnWNNm) · "Fleet Manager substrate-kit implementation"

💡 Session idea: **five "the hub needs a different shape" requirements were
one missing abstraction, not five flags.** `ADOPT_PLAN` was already a data
table and `Config` already carried `sessions_dir`/`docs_root`/`claims_dir`;
what the kit lacked was a name for *which shape an install was born in*, so
every consumer that iterates the plan (`check_engagement`,
`check_template_sync`, `check_skill_grounds`) assumed the one shape. The
smallest honest fix is a declared profile on the config plus one accessor
every consumer reads — not five conditionals at five call sites.

## previous-session review

`2026-08-28` (kit #587/#588) fixed the false-negative family in
`check_no_false_walls` and reconciled the kit's own `current-state.md`, each
fix reproduced against the published asset before it was written. This
session inherits that discipline in a harder place: the change is to
**adoption itself**, where the regression surface is every existing adopter,
so every K item ships with a paired negative test — a mutant that must go red
— and the generated `dist/bootstrap.py` is exercised through the same public
interface a future `estate` seed will use, not just the source package.

## Why this session exists

fleet-manager `[D-0035]` (owner, live, 2026-09-01, all defaults on question E)
sets the `estate` build order and puts **K1–K5 in substrate-kit, one release**
ahead of the seed, because they shape the tree at birth and would cost renames
later — against his no-renames condition (`[D-0025]`). The requirement text is
`fleet-manager:docs/planning/2026-09-01-estate-structure-proposal/kit-prerequisites-and-migration.md`;
the decided form (which resolves each of the proposal's either/ors) is
`fleet-manager:docs/decisions.md` `[D-0035]`.

## What this ships

**One capability, not five flags.** `engine/lib/profiles.py` names what the kit
had no name for — *which shape an install was born in*. `Config.adoption_profile`
persists it; `adopt.adoption_plan(config)` is the single accessor every consumer
reads. `upgrade` and `render` already re-ran `adopt` with the loaded config, so
honouring the profile cost no second orchestration path.

- **K1** hub plants no `control/` bus; the bus checkers are input-gated, so
  omitting it quiets them by construction rather than by an allowlist entry.
- **K2** no generic `docs/` set, no seat-digest render, and the boot list
  follows the shape in both agreement homes.
- **K3** `sessions_dir` was already the seam; the hub is born on `sessions/`,
  and the advice text four findings carried gets one home in `engine.grammar`.
- **K4** `owner_context` renders one pointer instead of an Nth copy of the same
  two answers. The kit ships the sentence, never its destination.
- **K5** `telemetry.guard_fires` separates enabled / path / tracked /
  max_records. The KF-11 default is untouched; the hub is untracked and capped.

The most consequential fix was not in any K row: `check_skill_grounds` folded
every plan destination into its grounded-by-construction set unconditionally, so
a skill body naming a doc a sparse shape never plants would have passed as
grounded — a false green in the checker whose entire job is dead pointers.

## Verify

```bash
python3 -m pytest tests/ -q          # 2277 passed, 1 skipped
python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py   # 0
# every kit-quality leg, run verbatim from ci.yml: all exit 0
# the full cold-adoption smoke step, run verbatim: exit 0
```

**40 mutants applied across the change, 40 killed** — each fix reverted one
line at a time to confirm the test that guards it actually goes red. Four of my
own tests failed that check before they passed, which is the part worth
recording: a test that cannot fail is a comment.

## What review found, and what it cost

Three rounds (the per-PR cap) returned **21 findings**: 4 P1 + 6 P2, then 5 P2,
then 2 P1 + 4 P2. An independent 43-agent adversarial pass ran alongside — 37
raw findings, each handed to a separate agent instructed to REFUTE it; 14
survived, collapsing to 8 distinct defects.

Two were latent rather than cosmetic, and both were mine:

- **Containment was parsed, not resolved.** The telemetry `path` axis rejected
  absolute paths and literal `..`, which is a claim about a string. An
  intermediate symlink escaped both tests and had `check` writing the ledger
  outside the repository; `path: "."` put the sidecar lock at a sibling of the
  repo root. Reproduced, then fixed by resolving and containment-checking.
- **A refusal in the wrong place is a corruption.** `upgrade` reached its
  strict profile resolution only through `adopt` at step 6, after archiving
  state, applying document changes, refreshing derived files and replacing the
  vendored bootstrap — so an unknown persisted profile aborted over a partially
  upgraded repository.

And one overturned a judgement I had already made and written down: I left
`readpath_docs` at the shipped default because a hub plants no docs, so nothing
engages. That holds only while the hub stays **empty**.

## Honest null — what is deliberately not here

- **The hub has no skill pack.** A fresh hub emits 26 skill-ground advisories
  over 8 paths. Those advisories are this change working — before the filter
  they passed silently as grounded-by-construction. The gap is a
  hub-compatible skill set: the skills channel, deferred by the accepted build
  order. A test pins its exact shape rather than asserting zero.
- **Doctrine prose is reported, not forked.** `CONSTITUTION.md` and the
  working agreement still name omitted docs in prose outside the boot
  sections. Forking the kit's most important document per shape would double
  its maintenance surface; `adopt` instead reports every surviving route, by
  file, every pass.
- **The final head carries no review verdict.** The third round is the cap
  ([D-0039]), and its six findings were fixed *after* it. Everything on this
  head was verified by the suite, every CI leg, the cold-adoption smoke, and
  the 40-mutant pass — but not by a fourth round, because there is not one.
- **A pre-existing defect found and not fixed:** `[boot-section-missing]` on
  `.claude/CLAUDE.md` after any `adopt --include-claude`. The staged
  agreement's heading does not match `check_boot_path`'s regex. Reproduced
  identically on `origin/main`, so it is unrelated to this change and belongs
  in its own PR.
- **Not released.** `[Unreleased]` carries the entry; no version bump, no tag.
  The next cut is owner-paced.
