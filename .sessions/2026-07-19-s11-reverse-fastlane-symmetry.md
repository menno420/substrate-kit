# S11 — reverse fast-lane symmetry (ci.yml self-declares card-less prefixes)

> **Status:** `in-progress`

**Session:** 2026-07-19 · Self Improvement work-loop · substrate-kit
**Baton:** wave-2 groom rank S11 (docs/planning/2026-07-19-night-run-idea-groom-wave2.md line 33) — "reverse fastlane symmetry — ci.yml self-declares cardless prefixes (`# fastlane-cardless:`)." Provenance: fm ORDER 048 standing grant + coordinator dispatch (S10 shipped #531; baton advanced to S11).

## What I'm about to do

Close the reverse direction of the fast-lane prefix symmetry advisory. The R8 runtime advisory `check_fastlane_symmetry` covers only ONE direction (`carded − armed`: the guard cards a prefix the enabler never arms — a benign "cards a branch that never rides"). The **dangerous** reverse direction — `armed − carded` (a prefix the enabler ARMS so it rides the fast lane, but the guard never CARDS, so it merges card-less: the #451 race class) — is uncheckable at runtime today because the check cannot tell an *intentionally* card-less prefix (`claim/`, by design) from an *accidental* one. S11 gives ci.yml a `# fastlane-cardless:` self-declaration so the reverse leg becomes checkable host-locally, on the host's own two surfaces, with no dependency on the kit's `guards.FASTLANE_PREFIX_REGISTRY` (which an adopter never runs).

- `.github/workflows/ci.yml` — add a `# fastlane-cardless: claim/` self-declaration near the claims-only guard.
- `src/engine/checks/check_fastlane_symmetry.py` — parse the declaration; add the reverse leg (`armed − carded − declared_cardless`), self-gated on the declaration's presence so an un-regenerated adopter stays silent.
- `tests/test_check_fastlane_symmetry.py` — reverse-direction + declaration-parse tests; real-kit-surfaces stay green.
- `dist/bootstrap.py` — rebuilt + byte-pinned (engine code changed).

- **📊 Model:** opus-4.8 · medium · feature build
- **⚑ Self-initiated:** [[fill: NOT self-initiated / self-initiated]]
- **💡 Session idea:** [[fill at close]]
- **⟲ Previous-session review:** [[fill at close]]
