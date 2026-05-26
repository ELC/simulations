import json
import tomllib
from pathlib import Path

from stlite_hello.pyodide_sync import (
    PYODIDE_SYNC_SETTINGS,
    PyodideLockIndex,
    SemanticVersion,
    filter_valid_uv_constraint_specifications,
    load_pyodide_constraint_specifications,
    read_pyproject_constraint_specifications,
    sync_pyodide_constraints,
    sync_pyodide_lock_file,
    update_pyproject_constraint_dependencies,
)


def test_pyodide_version_matches_stlite_browser_bundle() -> None:
    assert PYODIDE_SYNC_SETTINGS.pyodide_version == SemanticVersion.parse("0.29.3")


def test_pyodide_lock_url_targets_pinned_release() -> None:
    assert PYODIDE_SYNC_SETTINGS.pyodide_lock_url == (
        f"https://cdn.jsdelivr.net/pyodide/v{PYODIDE_SYNC_SETTINGS.pyodide_version}/full/pyodide-lock.json"
    )


def test_committed_constraint_dependencies_match_vendored_lock() -> None:
    lock_data = json.loads(
        PYODIDE_SYNC_SETTINGS.pyodide_lock_path.read_text(encoding="utf-8"),
    )
    index = PyodideLockIndex.from_lock_data(lock_data)
    expected = filter_valid_uv_constraint_specifications(
        index.all_pinned_specifications(),
    )
    pyproject_constraints = read_pyproject_constraint_specifications(
        PYODIDE_SYNC_SETTINGS.pyproject_path.read_text(encoding="utf-8"),
    )

    assert pyproject_constraints == expected


def test_project_dependencies_match_vendored_lock_versions() -> None:
    lock_data = json.loads(
        PYODIDE_SYNC_SETTINGS.pyodide_lock_path.read_text(encoding="utf-8"),
    )
    index = PyodideLockIndex.from_lock_data(lock_data)
    pyproject = tomllib.loads(
        PYODIDE_SYNC_SETTINGS.pyproject_path.read_text(encoding="utf-8"),
    )
    project_dependencies = pyproject["project"]["dependencies"]

    pinned_versions = {
        name: pinned_version
        for pinned_specification in index.all_pinned_specifications()
        for name, _, pinned_version in [pinned_specification.partition("==")]
    }

    for specification in project_dependencies:
        name, _, version = specification.partition("==")
        if name not in pinned_versions:
            continue
        assert version == pinned_versions[name]


def test_sync_pyodide_lock_file_writes_indented_json(
    tmp_path: Path,
    pyodide_lock_snippet: dict[str, object],
) -> None:
    lock_path = tmp_path / "constraints" / "pyodide-lock.json"

    sync_pyodide_lock_file(lock_path, lock_data=pyodide_lock_snippet)

    written_text = lock_path.read_text(encoding="utf-8")
    assert written_text.endswith("\n")
    assert '    "numpy"' in written_text
    assert json.loads(written_text)["packages"]["numpy"]["version"] == "2.2.5"


def test_load_pyodide_constraint_specifications_returns_current_and_expected(
    snippet_lock_url: str,
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        "[tool.uv]\nconstraint-dependencies = []\n",
        encoding="utf-8",
    )
    lock_path = tmp_path / "pyodide-lock.json"

    current, expected = load_pyodide_constraint_specifications(
        url=snippet_lock_url,
        lock_path=lock_path,
        pyproject_path=pyproject_path,
    )

    assert current == []
    assert expected == ["altair==6.0.0", "numpy==2.2.5", "pandas==2.3.3"]


def test_update_pyproject_constraint_dependencies_writes_specifications(
    tmp_path: Path,
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        "[tool.uv]\nconstraint-dependencies = []\n",
        encoding="utf-8",
    )
    specifications = ["altair==6.0.0", "numpy==2.2.5", "pandas==2.3.3"]

    update_pyproject_constraint_dependencies(pyproject_path, specifications)

    updated = read_pyproject_constraint_specifications(
        pyproject_path.read_text(encoding="utf-8"),
    )

    assert updated == specifications


def test_sync_pyodide_constraints_returns_expected_specifications(
    snippet_lock_url: str,
    tmp_path: Path,
) -> None:
    lock_path = tmp_path / "pyodide-lock.json"

    expected = sync_pyodide_constraints(
        url=snippet_lock_url,
        lock_path=lock_path,
    )

    assert expected == ["altair==6.0.0", "numpy==2.2.5", "pandas==2.3.3"]
    assert lock_path.is_file()
