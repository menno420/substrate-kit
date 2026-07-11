# Gate and generation review — 2026-07-11

> **Status:** `audit` (owner-directed review snapshot; source code, tests, and
> later merged fixes win over this file)
>
> Scope: `menno420/substrate-kit` as a portable agent-memory substrate: the
> generated stdlib-only `dist/bootstrap.py`, the source engine under
> `src/engine/`, generated/adopter session gates, adopt/upgrade safety,
> strict-check truthfulness, and bench validity. The review prioritized gate
> logic first because a false-green session-card gate propagates to every repo
> that vendors the kit.
>
> Evidence discipline: this report cites only current repo files and local
> command results. Historical PRs/commits mentioned in existing source comments
> were not used as independent evidence here.

## Executive summary

Three actionable gaps were found:

1. **HIGH — added-card lane can still shadow a broken modified sibling card.**
   The generated adopter gate handles all added cards, but as soon as the diff
   contains any added card it makes all modified sibling cards advisory-only.
   A PR can therefore add one well-formed complete card and simultaneously
   break another modified session card, and the generated gate can still exit 0.
2. **MEDIUM — deleted session cards are excluded from the gate.** The gate's
   `--diff-filter=d` selection omits deleted `.sessions/*.md` paths, so a
   card-deletion-only PR can fall through to the no-card path.
3. **HIGH — dist generation is pinned to a manual module manifest, not to all
   of `src/engine/`.** CI and release correctly prove that `dist/bootstrap.py`
   equals the builder output, but the builder output itself is only a function
   of the files listed in `MODULE_ORDER` plus top-level templates. A new engine
   module omitted from that manifest can be tested in source yet absent from the
   shipped single-file artifact.

No blocking findings were found in the sampled adopt/upgrade, checker
truthfulness, or bench-validity paths; the verified-clean areas are listed
below so future reviewers can distinguish inspected surfaces from uninspected
ones.

## Findings

### G-1 — HIGH — Added-card lane can still shadow a broken modified sibling card

**Primary surface:** generated live adopter gate from `live_ci_workflow()`.

**Evidence:**

- The gate gathers all non-deleted session cards in `cards` and all added
  session cards in `added`:
  `git diff --name-only --diff-filter=d ... '<sessions_dir>/*.md'` and
  `git diff --name-only --diff-filter=A ... '<sessions_dir>/*.md'`.
- If `added` is non-empty, the gate loops over `cards`, but for any card that
  is not itself added it only prints
  `modified sibling card (advisory — logged, never grade-affecting)`.
- The exit-code-affecting loop then grades only the added cards, using either
  the full locked-door lane when the gate workflow itself changed, or the
  absent-sentinel + `--added-card` lane otherwise.

Current lines: `src/engine/adopt.py:857-888`.

**Concrete failure scenario:**

1. `main` has `.sessions/2026-07-10-closeout.md` complete.
2. A PR adds `.sessions/2026-07-11-new.md` as a well-formed `complete` card.
3. The same PR also modifies `.sessions/2026-07-10-closeout.md` so its status
   becomes `in-progress`, or removes its required `💡` / `📊 Model` marker.
4. Because `added` is non-empty, the generated workflow logs the modified
   sibling as advisory and checks only `.sessions/2026-07-11-new.md`.
5. The gate exits 0 if the added card passes, even though the PR broke another
   session card.

**Why this matters:** this is a remaining multi-card shadowing variant. The
recent fix changed the old single-card picker into an all-added-card loop, but
it still lets an added card control the verdict for broken modified siblings.
For a fleet-wide merge/session gate, this is a false-green class.

**Suggested fix direction:** make modified siblings grade-affecting too, or at
least grade-affecting when they are themselves broken. One safe rule is:

- every added card runs the added-card lane;
- every modified card runs the locked-door `--require-session-log --session-log`
  lane;
- any red result sets `fail=1`.

If the intended product behavior is to keep benign sibling backfills advisory,
then add a separate mechanical proof that advisory siblings cannot introduce an
incomplete/broken card; absent that proof, advisory-only is too broad.

### G-2 — MEDIUM — Session-card deletions are excluded from the gate

**Primary surfaces:** generated adopter gate and kit dogfood gate.

**Evidence:**

- The generated gate builds `cards` with `--diff-filter=d`, which excludes
  deleted paths before matching `'<sessions_dir>/*.md'`.
- This repo's own CI session-gate step uses the same deletion-excluding filter
  for `.sessions/*.md`.

Current lines: `src/engine/adopt.py:857-888` and
`.github/workflows/ci.yml:246-255`.

**Concrete failure scenario:**

1. A repo has multiple complete historical cards.
2. A PR deletes `.sessions/2026-07-01-important.md` and touches no other
   session card.
3. The deleted path is excluded from `cards`.
4. The generated gate falls to the no-card sentinel path; the dogfood gate falls
   back to the mtime/newest-card path.
5. If the remaining repo is otherwise healthy, the PR can merge while removing
   session memory.

**Why this matters:** this is not the same immediate premature-merge risk as an
in-progress current-session card, but it violates the durability expectation of
an agent-memory substrate and leaves a false-green for destructive session-log
changes.

**Suggested fix direction:** treat deleted session-card paths as a distinct red
finding unless the repo has an explicit, reviewed archive/prune path. If pruning
is allowed, route deletions through that path and test the gate behavior.

### B-1 — HIGH — Dist generation is not proven against all of `src/engine/`

**Primary surfaces:** builder manifest and CI/release verification.

**Evidence:**

- `src/build_bootstrap.py` defines `ENGINE_ROOT`, `TEMPLATES_ROOT`, and
  `DIST_PATH`, then manually lists engine files in `MODULE_ORDER`.
- `build()` iterates only `MODULE_ORDER`, strips intra-package imports, and
  embeds top-level template files from `src/engine/templates/`.
- CI and release re-run `python3 src/build_bootstrap.py` and byte-compare
  `dist/bootstrap.py`, which proves `dist` equals the builder output.
- `src/build_release_json.py` then copies the committed/pinned dist bytes into
  release assets and records their sha256.

Current lines: `src/build_bootstrap.py:25-28`, `src/build_bootstrap.py:30-108`,
`src/build_bootstrap.py:204-224`, `.github/workflows/release.yml:55-76`, and
`src/build_release_json.py:202-214`.

**Concrete failure scenario:**

1. A developer adds `src/engine/checks/check_new_gate.py`.
2. Source tests import and exercise that module directly, or `src/engine/cli.py`
   imports it.
3. The developer forgets to add the file to `MODULE_ORDER`.
4. Regenerating `dist/bootstrap.py` and byte-comparing it succeeds, because the
   builder deterministically omits the new file.
5. The source tree can pass tests while the generated single-file artifact lacks
   the new behavior or raises a runtime `NameError` on an exercised dist-only
   path.

**Why this matters:** the repo's most important distribution promise is that
adopters receive the tested engine as one file. The current checks prove
reproducibility of the generator output, but not completeness of the generator
input.

**Suggested fix direction:** add a manifest-completeness checker that walks
`src/engine/**/*.py` and fails if any importable engine module is omitted from
`MODULE_ORDER`, with an explicit allowlist for intentionally unbundled files if
such files ever exist. Run it in CI before the byte-equality pin.

## Verified-clean areas

### Gate logic inspected clean, except findings above

- **Multiple added cards:** the generated adopter gate loops over every path in
  `added`; the CLI added-card checker returns a hold finding for
  in-progress/drafted added cards and full grammar findings for complete but
  malformed added cards.
- **Cards edited in the same push as their own flip:** modified-card-only diffs
  run the locked-door `--require-session-log --session-log "$card"` lane for
  each card in `cards`.
- **Case sensitivity / path shape:** the gate intentionally matches
  `'<sessions_dir>/*.md'` and excludes `README.md`; no false-green was proven
  for normal convention-compliant `.md` cards. Non-`.md` session-like files are
  outside the current convention and should be made explicit if they are meant
  to gate.

### Generation integrity inspected clean, except B-1

- The builder is deterministic for the files it includes: fixed module order,
  sorted imports, sorted top-level template embedding, and fixed UTF-8 byte
  writing.
- CI and release both re-run the builder and require `git diff --exit-code
  dist/bootstrap.py`, preventing committed `dist` from drifting from builder
  output.
- Release asset generation hashes the exact dist bytes that it publishes, and
  writes the same sha256 into `release.json` and `bootstrap.py.sha256`.

### Adopt / upgrade safety inspected clean

- First-time adopt plants user docs with skip-if-exists behavior rather than
  overwriting existing host files.
- Opt-in `.claude/CLAUDE.md` and `.claude/settings.json` are also
  skip-if-exists.
- Staged artifacts under `.substrate/` are intentionally regenerated.
- Once a live gate exists, it is kit-owned and regenerated, but host additions
  are banked/reported as carve-outs rather than silently disappearing.
- Upgrade archives before replacing the vendored file, regenerates staged
  artifacts after replacement, and writes an upgrade report.

### Checker truthfulness inspected clean

- `check_added_card()` distinguishes missing status badge, born-red hold, and
  complete-card grammar/completeness checking.
- `check_log()` fails incomplete cards on missing markers, unresolved
  `[[fill:]]` slots, and in-progress status.
- The CLI appends `--added-card` findings after the allowlist pass, so the
  added-card hold is not allowlistable.

### Bench validity inspected clean

- `bench/run_ab.py prepare` asserts the ON arm reaches green under
  `check --strict` before paired sessions begin.
- `bench/score_m1.py` documents and implements M1 as tool-output words consumed
  before first mutation, matching the stated orientation-cost measurement.

## Verification commands run during the review

```sh
python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py
python3 -m pytest tests/test_cli_gate.py tests/test_adopt.py -q
git status --short
```

A mistaken targeted test command was also attempted and failed because the named
test did not exist:

```sh
python3 -m pytest tests/test_adopt.py::test_live_gate_grades_every_added_card tests/test_cli_gate.py -q
```

That failure was a test-selection error, not a product failure; the broader
`tests/test_cli_gate.py tests/test_adopt.py` run passed afterward.
