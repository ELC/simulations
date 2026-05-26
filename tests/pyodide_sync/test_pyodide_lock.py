import pytest

from stlite_hello.pyodide_sync import (
    PYODIDE_LOCK_JSON_ADAPTER,
    PYODIDE_SYNC_SETTINGS,
    PyodideLockIndex,
    Requirement,
)


def test_requirement_pinned_specification_uses_normalized_name() -> None:
    requirement = Requirement.model_validate(
        {"name": "scikit-learn", "version": "1.6.1"},
    )

    assert requirement.pinned_specification == "scikit_learn==1.6.1"


def test_pyodide_lock_index_lists_all_pinned_specifications(
    pyodide_lock_snippet: dict[str, object],
) -> None:
    index = PyodideLockIndex.from_lock_data(pyodide_lock_snippet)

    assert index.all_pinned_specifications() == [
        "altair==6.0.0",
        "numpy==2.2.5",
        "pandas==2.3.3",
    ]


def test_pyodide_lock_index_without_packages_is_empty() -> None:
    index = PyodideLockIndex.from_lock_data({})

    assert index.all_pinned_specifications() == []


def test_pyodide_lock_index_skips_invalid_package_entries() -> None:
    index = PyodideLockIndex.from_lock_data(
        {
            "packages": {
                "invalid": "not-a-mapping",
                "incomplete": {"name": "incomplete"},
                "numpy": {"name": "numpy", "version": "2.2.5"},
            },
        },
    )

    assert index.all_pinned_specifications() == ["numpy==2.2.5"]


def test_pyodide_lock_json_adapter_rejects_non_object_root() -> None:
    with pytest.raises(ValueError, match="dict"):
        PYODIDE_LOCK_JSON_ADAPTER.validate_json("[]")


def test_fetch_lock_data_returns_released_lock() -> None:
    data = PyodideLockIndex.fetch_lock_data(PYODIDE_SYNC_SETTINGS.pyodide_lock_url)
    index = PyodideLockIndex.from_lock_data(data)

    assert "numpy==2.2.5" in index.all_pinned_specifications()


def test_fetch_lock_data_rejects_unreachable_url() -> None:
    bad_url = "https://cdn.jsdelivr.net/pyodide/v0.0.0/full/pyodide-lock.json"

    with pytest.raises(ValueError, match="Failed to download Pyodide lock file"):
        PyodideLockIndex.fetch_lock_data(bad_url)
