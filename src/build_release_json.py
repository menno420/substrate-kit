"""Build (and verify) the release assets for one `vX.Y.Z` tag.

The machine end of the outbound release protocol (founding plan §4.1/§9.2):
`release.yml` calls this on a tag push. It refuses to release when the repo
is not self-consistent, then emits the three Release assets:

- ``bootstrap.py``           — a copy of the committed dist (the pinned asset)
- ``bootstrap.py.sha256``    — ``<hex>  bootstrap.py`` (shasum -a 256 format)
- ``release.json``           — the machine-readable upgrade contract
- ``notes.md``               — the CHANGELOG section (release notes body;
  not attached as an asset, used for the Release description) + the standing
  adopter upgrade checklist (:data:`ADOPTER_CHECKLIST`, ORDER 003 — appended
  to every release so it can't be forgotten)

Refusal conditions (exit 1, one line each):

1. ``KIT_VERSION`` in ``src/engine/lib/config.py`` != the tag version.
2. ``CHANGELOG.md`` has no ``## [<version>]`` section (enforce, don't exhort).
3. The committed ``dist/bootstrap.py`` header is not stamped with the version.

The byte-equality of dist vs a fresh build is verified by the workflow itself
(``python3 src/build_bootstrap.py && git diff --exit-code dist/bootstrap.py``)
— this script only checks the stamp, so it stays read-only.

Optional per-release metadata can ride in the CHANGELOG section as an HTML
comment (defaults shown)::

    <!-- release: breaking=false state_migration=false min_upgrade_from=1.0.0 -->

Usage::

    python3 src/build_release_json.py --version 1.0.0 --out release-assets
    python3 src/build_release_json.py --version 1.0.0 --verify-only
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path

KIT_ROOT = Path(__file__).resolve().parents[1]
DIST_PATH = KIT_ROOT / "dist" / "bootstrap.py"
CHANGELOG_PATH = KIT_ROOT / "CHANGELOG.md"
CONFIG_PATH = KIT_ROOT / "src" / "engine" / "lib" / "config.py"
REPO_SLUG = "menno420/substrate-kit"

_META_RE = re.compile(
    r"<!--\s*release:\s*breaking=(?P<breaking>true|false)\s+"
    r"state_migration=(?P<migration>true|false)\s+"
    r"min_upgrade_from=(?P<min_from>\S+?)\s*-->",
)

# Appended to EVERY release's notes body (inbox ORDER 003, adopter-visibility
# band): the upgrade ritual an adopter walks, ending with the `kit:`
# status-line self-report that feeds the kit's docs/adopters.md registry.
# Lives here — not in each CHANGELOG section — so publishing it is automatic
# (enforce, don't exhort): a release author cannot forget it.
ADOPTER_CHECKLIST = """\
## Adopter upgrade checklist

1. **Run the upgrade**: download `bootstrap.py` from this release next to
   your vendored copy as `bootstrap.py.new`, then
   `python3 bootstrap.py.new upgrade` (archive-first; `--rollback` undoes).
2. **Verify the gate**: `python3 bootstrap.py check --strict` → green on
   your tree (fix findings before shipping the upgrade PR).
3. **Verify engagement**: the post-adopt engagement gate stays green — no
   UNRENDERED banner/slot, live CI runs the gate, session loop engaged.
4. **Update your `kit:` status line**: in your `control/status.md`, set
   `kit: v{version} · check: <verdict> · engaged: <yes|no>` in the same
   session — this heartbeat is how the substrate coordinator sees your kit
   state (registry: `docs/adopters.md` in menno420/substrate-kit).
"""


def kit_version() -> str:
    """Return ``KIT_VERSION`` parsed from ``lib/config.py``."""
    source = CONFIG_PATH.read_text(encoding="utf-8")
    match = re.search(r'^KIT_VERSION = "([^"]+)"$', source, re.MULTILINE)
    if match is None:
        raise ValueError("KIT_VERSION not found in src/engine/lib/config.py")
    return match.group(1)


def changelog_section(version: str, changelog: str) -> tuple[str, str] | None:
    """Return ``(heading, body)`` of the ``## [version]`` section, or None."""
    pattern = re.compile(
        rf"^(## \[{re.escape(version)}\][^\n]*)\n(.*?)(?=^## \[|\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(changelog)
    if match is None:
        return None
    return match.group(1), match.group(2).strip()


def heading_anchor(heading: str) -> str:
    """Return the GitHub rendered-markdown anchor for a ``##`` heading."""
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[^\w\s-]", "", text)
    return text.replace(" ", "-")


def section_metadata(body: str, version: str) -> dict:
    """Parse the optional release-metadata comment (defaults when absent)."""
    match = _META_RE.search(body)
    if match is None:
        return {
            "breaking": False,
            "requires_state_migration": False,
            "min_upgrade_from": "1.0.0" if version >= "1.0.0" else version,
        }
    return {
        "breaking": match.group("breaking") == "true",
        "requires_state_migration": match.group("migration") == "true",
        "min_upgrade_from": match.group("min_from"),
    }


def verify(version: str) -> list[str]:
    """Return the refusal reasons for releasing ``version`` (empty = clear)."""
    problems: list[str] = []
    declared = kit_version()
    if declared != version:
        problems.append(
            f"KIT_VERSION is {declared!r} but the tag names {version!r} — "
            "bump src/engine/lib/config.py (and pyproject.toml) first.",
        )
    if not DIST_PATH.exists():
        problems.append("dist/bootstrap.py is missing.")
    else:
        header = DIST_PATH.read_text(encoding="utf-8").splitlines()[0]
        if f"bootstrap v{version} " not in header:
            problems.append(
                f"dist/bootstrap.py header is not stamped v{version} "
                "(regenerate: python3 src/build_bootstrap.py).",
            )
    changelog = (
        CHANGELOG_PATH.read_text(encoding="utf-8") if CHANGELOG_PATH.exists() else ""
    )
    if changelog_section(version, changelog) is None:
        problems.append(
            f"CHANGELOG.md has no '## [{version}]' section — the release "
            "workflow refuses to publish an undocumented version.",
        )
    return problems


def build_release_json(version: str, sha256: str) -> str:
    """Return the ``release.json`` text for ``version`` (plan §4.1 schema)."""
    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    section = changelog_section(version, changelog)
    heading, body = section if section else (f"## [{version}]", "")
    payload = {
        "version": version,
        "sha256": sha256,
        **section_metadata(body, version),
        "changelog_anchor": (
            f"https://github.com/{REPO_SLUG}/blob/main/CHANGELOG.md"
            f"#{heading_anchor(heading)}"
        ),
        "upgrade_steps": [
            "download bootstrap.py next to your vendored copy as bootstrap.py.new",
            "run: python3 bootstrap.py.new upgrade",
        ],
    }
    return json.dumps(payload, indent=2, sort_keys=True) + "\n"


def main(argv: list[str] | None = None) -> int:
    """Verify the release preconditions and emit the assets."""
    parser = argparse.ArgumentParser(description="build substrate-kit release assets")
    parser.add_argument("--version", required=True, help="the tag version, no 'v'")
    parser.add_argument("--out", type=Path, default=None, help="assets output dir")
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args(argv)

    problems = verify(args.version)
    if problems:
        for problem in problems:
            sys.stderr.write(f"release: REFUSED — {problem}\n")
        return 1
    if args.verify_only:
        sys.stdout.write(f"release: v{args.version} preconditions all green.\n")
        return 0

    out = args.out if args.out is not None else KIT_ROOT / "release-assets"
    out.mkdir(parents=True, exist_ok=True)
    dist_bytes = DIST_PATH.read_bytes()
    sha256 = hashlib.sha256(dist_bytes).hexdigest()
    (out / "bootstrap.py").write_bytes(dist_bytes)
    (out / "bootstrap.py.sha256").write_text(
        f"{sha256}  bootstrap.py\n",
        encoding="utf-8",
    )
    (out / "release.json").write_text(
        build_release_json(args.version, sha256),
        encoding="utf-8",
    )
    changelog = CHANGELOG_PATH.read_text(encoding="utf-8")
    section = changelog_section(args.version, changelog)
    heading, body = section if section else ("", "")
    checklist = ADOPTER_CHECKLIST.format(version=args.version)
    (out / "notes.md").write_text(body + "\n\n" + checklist, encoding="utf-8")
    sys.stdout.write(f"release: wrote 4 asset file(s) to {out} (sha256 {sha256}).\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
