# 2026-07-11 — host workflow action-pin bump (checkout@v5 / setup-python@v6)

> **Status:** `complete`

- **📊 Model:** fable-5 · low · mechanical refactor

## Scope (what is about to happen)

One bounded slice, claim `control/claims/host-workflow-pin-bump.md`
(#198 @ 6d34913, on main before build). Bump the kit's OWN host workflows
off the Node-20-deprecated action majors — the "Kit's OWN workflow
action-pin bump" next-queue item from the ORDER 013 self-review (W-10b):
`.github/workflows/ci.yml` (checkout@v4 L21, setup-python@v5 L96) and
`.github/workflows/release.yml` (L39/L40) go to `actions/checkout@v5` /
`actions/setup-python@v6`, matching what the generated gate emits since
PR #195 (`src/engine/adopt.py` pins, verified). Inventory says these are
the ONLY action pins in `.github/workflows/` — `auto-merge-enabler.yml` and
`auto-merge-disarm.yml` carry no `uses:` at all — so no other majors to
sweep. `release.yml` cannot be exercised without cutting a release (never
dispatched for a pin bump): validated by careful YAML review and marked
**verified-at-next-release**. `ci.yml` exercises itself on this PR.
Rider on the final flip commit ONLY (sibling-card rule): rewrite the 4
off-PL-004 `📊 Model:` lines flagged by self-review W-10a (the 4 of the 5
newest complete cards) to the family-level `<model> · <effort> ·
<task-class>` taxonomy form. No CHANGELOG entry (host-workflow pins are
kit-internal, not adopter-visible; no engine/dist change). Close-out:
status.md overwrite (preserving ALL standing content — orders through 013,
⚑ OWNER-ACTION 2–13, ROUTINE STATE/Q-0265, Self-review 2026-07-11,
release/wave/P4 records) + claim delete as the deliberate last step before
this card's flip. Files: `.github/workflows/ci.yml` +
`.github/workflows/release.yml` + the 4 model-line card fixes (flip commit
only) + `control/status.md` + claim delete + this card. NEVER
control/inbox.md, bench/, src/, dist/, or PR #181.

## Close-out

Shipped the declared scope exactly. Pins bumped (commit 9c9db12, 4 lines,
2 files): `ci.yml` checkout v4→v5 + setup-python v5→v6, `release.yml`
checkout v4→v5 + setup-python v5→v6 — grep-confirmed the only `uses:`
pins in `.github/workflows/`; targets match `src/engine/adopt.py`'s
generated-gate emissions (#195). **ci.yml self-exercised green on the new
pins:** run 29150139885 at 9c9db12 executed every heavy step (pytest, dist
pin, ruff, idea index, program law, bench integrity, cold-adoption smoke)
on checkout@v5/setup-python@v6 — Python 3.10.20 resolved, the Node-20
deprecation warning GONE from the log tail — with the sole red being this
card's own designed born-red hold (job 86538212482, "HOLD (by design)…
nothing to investigate"). `release.yml` deliberately NOT dispatched:
YAML-reviewed, **verified-at-next-release** (its pins first fire live at
the next release cut). Rider landed on this flip commit: the 4 W-10a
model-line fixes (gate-tail1-v1101-fix → `fable-5 · medium · feature
build`; bump-v1.10.1 → `mechanical refactor`; close-v1.10.1 +
wave-v1101-adopters-regen → `docs-only`). Mid-slice: TWO coordinator
red-pings (heads aa6d77c and 9c9db12) were job-log-verified per PL-006 as
the designed hold mirrored by the two legacy alias jobs — the W-9
false-alarm class firing twice more; the second ping's "the action bump
broke CI" hypothesis was disproven by the first red predating the bump
entirely. Verify: `python3 -m pytest tests/ -q` → **995 passed**;
`python3 src/build_bootstrap.py` → 666924 B, `git diff dist/bootstrap.py`
empty (byte-pin clean); `check --strict` red only by this card's pre-flip
hold. CHANGELOG decision: **no entry** — kit-internal CI plumbing,
adopters consume the generated gate (bumped in #195), no engine/dist
change, no release cut. Diff = 2 workflows + 4 sibling model lines +
status.md + claim delete + this card.

## 💡 Session idea

**Host-vs-generated pin-parity check:** the W-10b drift class — the
generator's emitted workflow pins moving ahead of the kit's own
`.github/workflows/` (live for ~9 hours between #195 and #199) — is
mechanically detectable: a small `check` advisory (or a pytest case) that
greps the action majors the templates in `src/engine/adopt.py` emit and
compares them against the majors pinned in the kit's own host workflows,
warning on any mismatch. The release runbook already gained a checklist
line for this (the #197 card's suggestion); a checker makes it
enforce-don't-exhort (PL-007) and would have caught this drift the same
hour #195 merged.

## ⟲ Previous-session review

The ORDER 013 self-review session (#196/#197) did the hard thing well:
honest-negative first (1 PASS / 4 FAIL headline preserved), every claim
cited, and its W-10 "drift found, NOT yet fixed" list converted directly
into this slice's work order — a self-review that generates the next
session's queue is the loop working as designed. One improvement it
surfaces: its W-9 documentation of the false-alarm class did not prevent
the same class from consuming two more coordinator round-trips in THIS
slice (red-pings on both heads, one proposing a wrong root cause). The
enforcing fix is already identified on the #197 card (teach the HOLD
banner/check advisory to name the alias topology) — it should be promoted
from idea to a queued slice, since the class now demonstrably costs a
diagnosis round in nearly every born-red session while OWNER-ACTION 2
stays unclicked.
