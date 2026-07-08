"""Put the kit's ``src/`` on sys.path so the engine imports as ``engine.*``.

Extracted from superbot's ``tests/unit/substrate_kit/conftest.py`` (which
inserted ``../substrate-kit/src`` from the host repo). Now that the kit lives
in its own repository the tests sit at ``tests/`` and the source at ``src/``,
so the insert is repo-local. Installing the package (``pip install -e .``)
makes this insert a no-op.
"""

import sys
from pathlib import Path

_SRC = Path(__file__).resolve().parents[1] / "src"
if str(_SRC) not in sys.path:
    sys.path.insert(0, str(_SRC))
