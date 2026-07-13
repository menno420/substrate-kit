# 2026-07-14 — ORDER 019 item 4: auto-merge-enabler INSTALL-time preflight

> **Status:** `complete`

About to (opening declaration): ship the install-time half of the enabler
preflight (`docs/ideas/enabler-install-preflight-2026-07-13.md`) — at
adopt/upgrade time, when the live enabler is planted/regenerated, best-effort
verify the owner-UI preconditions that leave it silently INERT ("Allow
auto-merge" OFF, zero required status-check contexts, required-context name
mismatch) and surface them as advisory report lines, degrading gracefully
offline/tokenless. The check-time branch-drift half shipped in PR #321 and is
not duplicated.

## What shipped (PR #344)

- `src/engine/enabler_preflight.py` (new): `enabler_install_preflight(root,
  required_context)` — origin slug read from `.git/config` directly (normal
  dir, worktree `.git` file, `commondir` indirection; no subprocess, §3.2),
  github.com slug parsing (https/ssh/scp shapes), then two stdlib-urllib
  API reads with a 5 s timeout: `GET /repos/{o}/{r}` (`allow_auto_merge`,
  `default_branch`) and `GET /repos/{o}/{r}/rules/branches/{branch}` — the
  SAME rules endpoint the enabler's own refuse-to-arm guard counts, so
  preflight and workflow can never disagree on semantics. Verdicts, all
  prefixed `enabler preflight:`: Allow-auto-merge ON/OFF/hidden-without-
  push-scope; zero contexts → loud INERT line; name mismatch → line naming
  the actual required contexts to pin via `automerge."required_context"`;
  both-verified → confirmation lines.
- `src/engine/adopt.py`: one call site right after the repo-settings
  checklist (same live-enabler existence gate) — runs on every
  adopt/upgrade pass, which is exactly enabler plant/regen time.
- **Fail-open contract** (flagged design point): no git / no origin /
  non-github origin (incl. agent-seat local git proxies) / offline / HTTP
  errors / tokenless visibility / malformed JSON each collapse to ONE
  honest `UNVERIFIED` line pointing at the manual checklist. The preflight
  never raises, never affects exit codes, never slows an offline install
  beyond the transport timeout. `GITHUB_TOKEN`/`GH_TOKEN` honoured.
- Decide-and-flag — **ADVISORY posture**: the idea file prescribes
  "report what the owner must configure" and routes output to the owner
  rather than asserting; matched the #321 advisory contract (never a
  locked door).
- Decide-and-flag — **branch-allowlist NOT re-checked here**: install-time
  regen forces workflow == config by construction; later drift is #321's
  check-time advisory. Duplicating would double-report every finding.
- Decide-and-flag — **no engine.adopt imports** in the new module (adopt
  imports it; the reverse edge would cycle); `_preflight_urllib_get` named
  to avoid dist-concatenation shadowing with `currency._urllib_get` (the
  Q-0200 exact-name class — caught by pre-commit grep, not by CI).
- `src/build_bootstrap.py`: module registered before `adopt.py`; dist
  regenerated.
- `tests/test_enabler_preflight.py`: 28 tests — happy path, each failure
  condition, every degradation path, origin parsing (5 accepted / 4
  rejected shapes), worktree indirection, token header on/off, adopt-report
  integration (scratch adopts never touch the network).
- `docs/ideas/enabler-install-preflight-2026-07-13.md` Progress updated
  (install-time half shipped, owner-UI residue named);
  `docs/current-state.md` lab-loop paragraph updated.

## Verify

- `python3 -m pytest -q` → 1284 passed at session-start HEAD (08de140) →
  **1322 passed** after the change + the origin/main merge (#342 brought
  +10; this PR brings +28).
- `python3 src/build_bootstrap.py` run twice → byte-identical
  (sha256 9a66fe98… both runs, 894989 bytes).
- `python3 dist/bootstrap.py check --strict` → exit 0; red only this card's
  own designed born-red hold pre-flip (plus the standing preflight-script
  NOTE).
- `python3 -m ruff check src/engine/` → All checks passed.
- Merged origin/main (#342 session-gate diff-derived selection) into the
  branch mid-session; sole conflict `.substrate/guard-fires.jsonl` resolved
  as append-only union; dist regenerated post-merge, byte-stable.

## Enders

💡 **Session idea:** the enabler workflow's refuse-to-arm step already
computes the required-context count at PR time — extend it to also emit the
*names* it counted and compare against the `required_context` the workflow
was generated with, posting a `::notice::` on mismatch. That would catch a
required-check rename made AFTER install (the preflight sees install-time
truth only; the workflow sees every PR) — the one drift window neither #321
nor #344 covers. Dedup-grepped `docs/ideas/`:
`engagement-wiring-strength-verification-2026-07-12.md` is adjacent (wiring
strength at check time) but does not cover PR-time name drift inside the
enabler itself.

- **📊 Model:** Claude Fable 5 · high · feature-build (engine module + wiring
  + tests + dist)

⟲ **Previous-session review** (2026-07-14-enabler-allowlist-claude.md, ORDER
019 item 2): exemplary verification no-op — it dated the evidence both ways
(#300 landed ~3h BEFORE ASK 001 was filed) and closed the loop on the
evidencing jam (idea-engine #271's own timeline), which is exactly what kept
this session from re-doing item 2. One improvement it surfaces: its finding
("allowlist satisfied since #300") lived in the card + heartbeat but not in
the idea file's Progress section — this session had to re-derive the
#321-vs-remaining split from the idea file alone. Rule of thumb worth
keeping: a verification session touching an idea's territory appends one
line to that idea's Progress section, so the idea file stays the single
design authority its header claims.

Run type: ORDER-dispatched worker session (ORDER 019 item 4).
