import sys
from typing import Any

import pytest

from stlite_hello import block_pyarrow_and_import, import_pandera_module


def test_block_pyarrow_and_import_skips_non_emscripten() -> None:
    modules: dict[str, Any] = {"pyarrow": "mock"}
    seen_during_action: list[Any] = []

    applied = block_pyarrow_and_import(
        "win32",
        modules,
        lambda: seen_during_action.append(modules.get("pyarrow")),
    )

    assert applied is False
    assert seen_during_action == []
    assert modules == {"pyarrow": "mock"}


def test_block_pyarrow_and_import_blocks_pyarrow_during_action_and_restores_it() -> None:
    modules: dict[str, Any] = {"pyarrow": "mock", "other": "preserved"}
    seen_during_action: list[Any] = []

    applied = block_pyarrow_and_import(
        "emscripten",
        modules,
        lambda: seen_during_action.append(modules["pyarrow"]),
    )

    assert applied is True
    assert seen_during_action == [None]
    assert modules == {"pyarrow": "mock", "other": "preserved"}


def test_block_pyarrow_and_import_pops_pyarrow_when_not_originally_present() -> None:
    modules: dict[str, Any] = {}
    seen_during_action: list[Any] = []

    applied = block_pyarrow_and_import(
        "emscripten",
        modules,
        lambda: seen_during_action.append(modules.get("pyarrow", "absent")),
    )

    assert applied is True
    assert seen_during_action == [None]
    assert modules == {}


def test_block_pyarrow_and_import_restores_pyarrow_after_action_failure() -> None:
    modules: dict[str, Any] = {"pyarrow": "mock"}

    def failing() -> None:
        msg = "boom"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="boom"):
        block_pyarrow_and_import("emscripten", modules, failing)

    assert modules == {"pyarrow": "mock"}


def test_block_pyarrow_and_import_pops_pyarrow_after_action_failure_when_originally_absent() -> None:
    modules: dict[str, Any] = {}

    def failing() -> None:
        msg = "boom"
        raise RuntimeError(msg)

    with pytest.raises(RuntimeError, match="boom"):
        block_pyarrow_and_import("emscripten", modules, failing)

    assert modules == {}


def test_import_pandera_module_imports_pandera_and_pandera_pandas() -> None:
    import_pandera_module()

    assert "pandera" in sys.modules
    assert "pandera.pandas" in sys.modules
