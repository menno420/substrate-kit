#!/usr/bin/env python3
"""make_seed — the parameterized seed-corpus generator (founding plan §5.0).

Generates the toy CLI project a cold-start A/B arm starts from: a ~130–200
line Python "record log" CLI (N modules + a test suite of M passing tests +
**one seeded, untested bug**), written to ``--dest``.

Design contract (plan §5.0 — anti-memorization vs comparability):

- **Fresh surface names per run**: the project name, domain noun, and
  function names are drawn from word lists by the ``--seed`` RNG, so no two
  runs share a memorizable surface and a session cannot lean on having seen
  the corpus before.
- **Same shape every run**: always N core modules (`store` / `ops` / `cli`
  roles), always M passing tests, always the SAME seeded bug class — a
  case-sensitive category filter whose docstring + README promise
  case-insensitivity (the Phase-2.5 spendlog bug class, kept so M-measures
  stay comparable across runs). The bug is deliberately untested.

Determinism: identical ``--seed`` ⇒ byte-identical output *within one kit
version*. A paired run generates ONCE and copies the tree to both arms
(companion D §2: the seed is "committed identically for both arms, never
edited between arms") — the runner (`run_ab.py prepare`) does exactly that.

Identifier safety (the run-2 lesson, seed 424242): several drawn tokens
become Python identifiers (the package name, the measure field / function /
argument names), so every pool token — and every drawn name, as a hard
screen in ``_names`` — must be keyword- and builtin-safe. The original
harvest domain's measure token was ``yield``, a Python keyword, and the
generated project was a SyntaxError; run-2 had to deviate to seed 424243
(idea file: ``docs/ideas/make-seed-yield-keyword-bug-2026-07-09.md``).

Bench-side tooling: NOT engine code — print/argparse are fine here; the
generated project is plain stdlib Python 3.10.
"""

from __future__ import annotations

import argparse
import builtins
import keyword
import random
import sys
from pathlib import Path

# Surface-name pools (drawn per seed — anti-memorization). Every token must
# pass _identifier_safe (keyword/builtin screen) — pinned by the test suite
# AND re-screened at draw time in _names (defense in depth: a future pool
# edit that sneaks a keyword in fails loudly, never generates broken code).
_ADJECTIVES = (
    "brook", "cedar", "delta", "ember", "fjord", "gale", "harbor", "iris",
    "juniper", "krill", "lumen", "moss", "north", "opal", "pine", "quartz",
    "reef", "slate", "tarn", "umber", "vale", "wren",
)
_DOMAINS = (
    ("expense", "expenses", "amount"),
    ("catch", "catches", "weight"),
    ("ride", "rides", "distance"),
    # NB: the measure token becomes an identifier — "yield" (a keyword) here
    # generated SyntaxError projects until 2026-07-09 (seed 424242, B1 run-2).
    ("harvest", "harvests", "bushels"),
    ("visit", "visits", "duration"),
    ("donation", "donations", "amount"),
    ("reading", "readings", "value"),
    ("shipment", "shipments", "mass"),
)
_VERBS = ("log", "track", "note", "file", "post", "mark")


def _identifier_safe(token: str) -> bool:
    """True when ``token`` can safely become a generated identifier.

    Rejects Python keywords (the seed-424242 ``yield`` SyntaxError class),
    soft keywords, and builtins (silent shadowing) — not just for the tokens
    used as identifiers today, but for every drawn token, so a template edit
    can never quietly promote an unscreened token into an identifier slot.
    """
    return (
        token.isidentifier()
        and not keyword.iskeyword(token)
        and not keyword.issoftkeyword(token)
        and not hasattr(builtins, token)
    )


def _names(seed: int) -> dict[str, str]:
    """Draw the run's surface names deterministically from ``seed``.

    Raises ``ValueError`` when any drawn token fails the keyword/builtin
    screen — a generation-time hard stop, so a bad vocabulary entry dies
    HERE with a named token instead of emitting a SyntaxError project.
    """
    rng = random.Random(seed)
    adjective = rng.choice(_ADJECTIVES)
    singular, plural, measure = rng.choice(_DOMAINS)
    verb = rng.choice(_VERBS)
    names = {
        "project": f"{adjective}{singular}",
        "singular": singular,
        "plural": plural,
        "measure": measure,
        "verb": verb,
    }
    unsafe = sorted({t for t in names.values() if not _identifier_safe(t)})
    if unsafe:
        raise ValueError(
            f"seed {seed} drew identifier-unsafe token(s) {unsafe} — fix the "
            "surface-name pools (every token must pass _identifier_safe; "
            "the seed-424242 'yield' lesson, 2026-07-09)"
        )
    return names


def _store_py(n: dict[str, str]) -> str:
    return f'''"""JSON-file persistence for {n["project"]} — one list of {n["singular"]} records."""

import json
from pathlib import Path

DEFAULT_PATH = Path("{n["plural"]}.json")


def load_records(path=DEFAULT_PATH):
    """Return the stored {n["singular"]} records (empty list when no file)."""
    path = Path(path)
    if not path.exists():
        return []
    return json.loads(path.read_text(encoding="utf-8"))


def save_records(records, path=DEFAULT_PATH):
    """Write the {n["singular"]} records back to disk."""
    Path(path).write_text(json.dumps(records, indent=2), encoding="utf-8")
'''


def _ops_py(n: dict[str, str]) -> str:
    # THE seeded bug lives in filter_by_category: the docstring (and the
    # README) promise case-insensitive matching; the implementation compares
    # raw strings. No test covers mixed case. Same bug class every seed.
    return f'''"""Core operations over {n["singular"]} records."""


def add_record(records, category, {n["measure"]}, note=""):
    """Append a {n["singular"]} record and return it."""
    record = {{
        "category": category,
        "{n["measure"]}": float({n["measure"]}),
        "note": note,
    }}
    records.append(record)
    return record


def total_{n["measure"]}(records):
    """Sum the {n["measure"]} field across records."""
    return sum(r["{n["measure"]}"] for r in records)


def filter_by_category(records, category):
    """Return records whose category matches (case-insensitive)."""
    return [r for r in records if r["category"] == category]


def top_categories(records, limit=3):
    """Return the ``limit`` categories with the highest summed {n["measure"]}."""
    totals = {{}}
    for r in records:
        totals[r["category"]] = totals.get(r["category"], 0.0) + r["{n["measure"]}"]
    ranked = sorted(totals.items(), key=lambda kv: (-kv[1], kv[0]))
    return ranked[:limit]
'''


def _cli_py(n: dict[str, str]) -> str:
    return f'''"""{n["project"]} — a tiny {n["singular"]}-log CLI.

Commands: {n["verb"]} (add a record) · list · total · filter <category> · top.
"""

import argparse
import sys

from {n["project"]} import ops, store


def main(argv=None):
    parser = argparse.ArgumentParser(prog="{n["project"]}")
    sub = parser.add_subparsers(dest="command", required=True)
    add_p = sub.add_parser("{n["verb"]}", help="add a {n["singular"]} record")
    add_p.add_argument("category")
    add_p.add_argument("{n["measure"]}", type=float)
    add_p.add_argument("--note", default="")
    sub.add_parser("list", help="list all records")
    sub.add_parser("total", help="sum the {n["measure"]} field")
    filter_p = sub.add_parser("filter", help="records in one category")
    filter_p.add_argument("category")
    top_p = sub.add_parser("top", help="highest-{n["measure"]} categories")
    top_p.add_argument("--limit", type=int, default=3)
    args = parser.parse_args(argv)

    records = store.load_records()
    if args.command == "{n["verb"]}":
        ops.add_record(records, args.category, args.{n["measure"]}, args.note)
        store.save_records(records)
        print("recorded.")
    elif args.command == "list":
        for r in records:
            print(f"{{r['category']}}: {{r['{n["measure"]}']}} {{r['note']}}".rstrip())
    elif args.command == "total":
        print(ops.total_{n["measure"]}(records))
    elif args.command == "filter":
        for r in ops.filter_by_category(records, args.category):
            print(f"{{r['category']}}: {{r['{n["measure"]}']}}")
    elif args.command == "top":
        for category, subtotal in ops.top_categories(records, args.limit):
            print(f"{{category}}: {{subtotal}}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
'''


def _tests_py(n: dict[str, str]) -> str:
    # M passing tests; NONE covers mixed-case filtering (the seeded gap).
    return f'''"""Tests for {n["project"]} core operations."""

from {n["project"]} import ops


def _sample():
    records = []
    ops.add_record(records, "food", 12.5, "lunch")
    ops.add_record(records, "travel", 30.0)
    ops.add_record(records, "food", 7.5)
    return records


def test_add_record_appends():
    records = _sample()
    assert len(records) == 3


def test_add_record_returns_record():
    records = []
    record = ops.add_record(records, "misc", 1.0, "x")
    assert record["category"] == "misc"


def test_total_{n["measure"]}():
    assert ops.total_{n["measure"]}(_sample()) == 50.0


def test_filter_by_category_exact():
    assert len(ops.filter_by_category(_sample(), "food")) == 2


def test_top_categories_ranked():
    ranked = ops.top_categories(_sample())
    assert ranked[0] == ("travel", 30.0)


def test_top_categories_limit():
    assert len(ops.top_categories(_sample(), limit=1)) == 1
'''


def _readme_md(n: dict[str, str]) -> str:
    return f"""# {n["project"]}

A tiny {n["singular"]}-log CLI: `{n["verb"]}` records with a category and
{n["measure"]}, then `list`, `total`, `filter <category>` (case-insensitive),
and `top` them.

Run the tests with `python3 -m pytest tests/`.
"""


def generate(dest: Path, seed: int) -> list[Path]:
    """Write the seed project under ``dest``; return the files written."""
    n = _names(seed)
    package = dest / n["project"]
    files = {
        package / "__init__.py": "",
        package / "store.py": _store_py(n),
        package / "ops.py": _ops_py(n),
        package / "cli.py": _cli_py(n),
        dest / "tests" / "__init__.py": "",
        dest / "tests" / f"test_{n['project']}.py": _tests_py(n),
        dest / "README.md": _readme_md(n),
    }
    written = []
    for path, text in files.items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        written.append(path)
    return written


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--dest", type=Path, required=True, help="output directory")
    parser.add_argument("--seed", type=int, required=True, help="RNG seed (fresh per run)")
    args = parser.parse_args(argv)
    written = generate(args.dest, args.seed)
    for path in written:
        print(f"wrote {path}")
    print(f"seed project ready under {args.dest} (seed={args.seed}).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
