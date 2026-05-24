"""Pyodide compatibility shim for pandera 0.31.

Stlite intentionally replaces Pyodide's bundled pyarrow with a tiny mock
package (``Table``/``Array``/``ChunkedArray`` stubs only) via micropip's
``add_mock_package`` to keep page weight down. Pandera 0.31 doesn't know that:
its ``engines/pandas_engine.py`` does ``try: import pyarrow; PYARROW_INSTALLED
= True`` at line 46 and then runs an arrow-typed registration block at line
1613 that calls ``pyarrow.bool_()``, ``pyarrow.int8()``, and friends. None of
those exist on Stlite's mock, so pandera's import explodes before stlite_hello
can even start.

We can't enrich the mock pyarrow because Stlite owns it, and we can't replace
it because Streamlit's runtime DataFrame-to-arrow path expects the same mock to
be importable. Instead we trick pandera into thinking pyarrow isn't installed:
we temporarily set ``sys.modules["pyarrow"] = None`` so ``import pyarrow``
raises ``ImportError``, eagerly import pandera (which sets ``PYARROW_INSTALLED
= False`` and skips the arrow block), then restore the mock so Streamlit's
later imports get the mock back as Stlite intends.

Outside Pyodide (local dev, CI) we never touch ``sys.modules`` and pandera
imports against the real pyarrow normally.
"""

import sys
from collections.abc import Callable, MutableMapping
from typing import Any


def block_pyarrow_and_import(
    platform: str,
    modules: MutableMapping[str, Any],
    importer: Callable[[], None],
) -> bool:
    if platform != "emscripten":
        return False

    sentinel = object()
    saved = modules.get("pyarrow", sentinel)
    modules["pyarrow"] = None
    try:
        importer()
    finally:
        if saved is sentinel:
            modules.pop("pyarrow", None)
        else:
            modules["pyarrow"] = saved
    return True


def import_pandera_module() -> None:
    import pandera  # noqa: F401, PLC0415
    import pandera.pandas  # noqa: F401, PLC0415


block_pyarrow_and_import(sys.platform, sys.modules, import_pandera_module)
