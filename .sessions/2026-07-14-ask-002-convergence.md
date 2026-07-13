# 2026-07-14 — ORDER 019 item 3 / ASK 002: check --strict ⇄ CI substrate-gate convergence — verification (no-op)

> **Status:** `complete`

About to: verify ORDER 019 item 3 (ASK 002 relay: converge local
`check --strict` with the CI substrate-gate, evidenced by idea-engine
#274/#299) against kit HEAD, and land the finding — pre-dispatch verification
already indicates the ask is satisfied by merged PR #332, so the expected
deliverable is a verification-report PR only: gap-by-gap verdicts, live
red-fixture reproductions on the HEAD dist, heartbeat fact line, and this
card.

Did (findings — no engine/template/dist change; verification record only):

- **The ask** (ASK 002 verbatim source: idea-engine control/outbox.md
  @ 2808b16, ASK 002 · 2026-07-13T12:45:33Z; relayed as ORDER 019 item 3):
  converge local `check --strict` with the CI substrate-gate so
  locally-green pushes stop going red in CI on legs the local check never
  ran (idea-engine #274 non-append inbox, #299 failing preflight).
  Verified against kit HEAD fdeb4391ccda1fecfd972b5b4be33323e1ba2b6a
  (#339 merge).
- **ALREADY SATISFIED:** ASK 002 = the same ask already routed as ORDER 018
  and shipped as kit PR #332. **Ledger drift correction:** the merge commit
  on main is **3d58a46** — the heartbeat's cited e7737e0 does not exist on
  main (likely the PR branch head).
- **5-gap verdict table** (all at HEAD):

  | # | ASK 002 gap | Verdict | Evidence |
  |---|---|---|---|
  | 1 | check_ideas/preflight leg local | CLOSED | `src/engine/lib/config.py:157` `_default_preflight_scripts()` → `["scripts/preflight.py"]`, config key `preflight_scripts` (config.py:254); `_run_preflight_scripts` in `src/engine/cli.py` (~748): non-zero exit → exit-affecting `preflight-script` finding; absent script → NOTE self-skip; nested-run guard env `SUBSTRATE_KIT_PREFLIGHT`. Full lane only (cli.py:1099). |
  | 2 | inbox append-only leg local | CLOSED | `src/engine/cli.py:690` `_derive_inbox_base` (git merge-base HEAD origin/main → `git show <base>:control/inbox.md`, absent-at-base → empty blob), wired in cmd_check at cli.py:1042, also on `--status-only` lane. |
  | 3 | merge-base derivation + self-skip posture | CLOSED | cli.py:709–746: silent skip on non-git, NOTE on unresolvable origin/main. |
  | 4 | ONE check-list convergence | CLOSED | CI full lane invokes `check --strict` which runs `preflight_scripts`; nested guard prevents recursion. |
  | 5 | verified-needed (red fixture per leg after next kit upgrade) | HALF | Red-fixture tests exist (`tests/test_check_parity.py` — inbox: `test_local_strict_reds_on_non_append_inbox_with_derivable_origin_main`, `test_local_strict_reds_on_malformed_appended_order`; preflight: `test_local_strict_reds_on_failing_preflight_script`, plus green/self-skip/nested-guard companions) AND both classes re-proved live this session against the HEAD dist in a scratch adopter. RESIDUAL = distribution only (below). |

- **Live reproduction evidence** (scratch adopter on HEAD dist):

  Repro A (#274 inbox class — edited an existing ORDER line, plain
  `python3 bootstrap.py check --strict`):

  ```
  check: 1 finding(s):
    [inbox-not-append] control/inbox.md: control/inbox.md changed non-append vs the merge-base — the one-writer/append-only law (control/README.md) allows only additions at the end; an existing ORDER was edited, reordered, or deleted. Restore the prior bytes verbatim and append your new ORDER block instead.
  EXIT=1
  ```

  Repro B (#299 preflight class — planted scripts/preflight.py exiting 2):

  ```
  check: 1 finding(s):
    [preflight-script] scripts/preflight.py: exit 2: preflight: deliberate red fixture (repro B) — the CI substrate-gate runs this same preflight; fix it before pushing.
  EXIT=1
  ```

  Controls: clean tree and passing preflight both →
  `check: all checks passed.` EXIT=0.
- **Residual = distribution only:** idea-engine's committed `bootstrap.py`
  is KIT_VERSION 1.10.0 with 0 hits for `_derive_inbox_base` /
  `preflight_scripts`; the release wave is owner-gated on parked PR #317, so
  the on-asking-repo verification completes only after the next kit release
  + upgrade lands there.
- **CI-vs-local residuals explicitly OUT of ASK 002 scope:** (a) the
  session-card diff-aware leg = ASK 003 / ORDER 019 item 1 lane (separate);
  (b) kit-repo-only kit-quality legs (pytest, dist byte-pin, ruff bans,
  idea-index, program-law label gate, bench integrity, cold-adoption smoke,
  session gate) — the adopter gate was the ask's target; a kit-side
  `scripts/preflight.py` folding pytest/ruff/dist-pin is a natural follow-up
  (this card's session idea).
- **Anomalies (noted neutrally, no action taken):** idea-engine origin/main
  showed a forced update on fetch, and its bootstrap.py at 1.10.0
  contradicts the kit heartbeat's "all reachable adopters tree-current at
  v1.15.0" — flagged for coordinator attention.
- **Walls:** none this session (no denials).

Verify: `python3 -m pytest -q` green; `python3 bootstrap.py check --strict`
exit 0 apart from this card's own designed born-red hold pre-flip.

💡 Session idea: kit-side `scripts/preflight.py` in the kit repo itself,
folding pytest + ruff bans + dist byte-pin + idea-index into
`check --strict` — the kit eats its own convergence dogfood: the exact
CI-red-after-local-green class ASK 002 named for adopters still exists for
the kit's own kit-quality legs, and #332 already built the folding mechanism
(preflight_scripts) that would close it for free. Dedup-grepped
`docs/ideas/` — `adopt-plants-pytest-gate-step-2026-07-10.md` and
`enabler-install-preflight-2026-07-13.md` are adopter/install-side, not the
kit-repo's own gate; no existing entry covers this. Kept card-only to hold
this PR to its control/+.sessions/ scope.

⟲ Previous-session review: `.sessions/2026-07-14-enabler-allowlist-claude.md`
(the #339 ASK 001 no-op) is a model verification card — exact source-line
citations with SHAs on both engine and dist, the evidencing adopter jam
traced to resolution with timestamps, and a session idea (relay-side ASK
staleness pre-check with a kit-HEAD SHA field) that directly attacks the
waste class it lived through. One concrete workflow improvement from this
session's vantage: that same waste class fired AGAIN here — ORDER 019 items
2 AND 3 were both already-shipped asks dispatched as full worker sessions —
so the relay-side pre-check idea deserves promotion from card-note to a
`docs/ideas/` file + groom-pass candidate; two consecutive no-op dispatches
in one ORDER is the measured evidence it was waiting for.

⚑ Self-initiated: none.

- **📊 Model:** Fable 5
