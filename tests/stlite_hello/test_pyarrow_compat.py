import sys
from typing import Any

from stlite_hello import block_pyarrow_and_import


def test_block_pyarrow_and_import_skips_non_emscripten() -> None:
    modules: dict[str, Any] = {"pyarrow": "mock"}

    applied = block_pyarrow_and_import("win32", modules)

    assert applied is False
    assert modules == {"pyarrow": "mock"}


def test_block_pyarrow_and_import_restores_pyarrow_after_import() -> None:
    modules: dict[str, Any] = {"pyarrow": "mock", "other": "preserved"}

    applied = block_pyarrow_and_import("emscripten", modules)

    assert applied is True
    assert modules == {"pyarrow": "mock", "other": "preserved"}
    assert "pandera" in sys.modules
    assert "pandera.pandas" in sys.modules


def test_block_pyarrow_and_import_pops_pyarrow_when_not_originally_present() -> None:
    modules: dict[str, Any] = {}

    applied = block_pyarrow_and_import("emscripten", modules)

    assert applied is True
    assert not modules
    assert "pandera" in sys.modules
    assert "pandera.pandas" in sys.modules
