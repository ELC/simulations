from pathlib import Path

import pytest

from stlite_hello.pyodide_sync import (
    PYODIDE_SYNC_SETTINGS,
    read_pyproject_constraint_specifications,
    replace_pyproject_constraint_dependencies,
    run_pyodide_constraints_sync,
)


def test_run_pyodide_constraints_sync_ci_passes_for_repository_pyproject() -> None:
    exit_code = run_pyodide_constraints_sync(
        ci=True,
        url=PYODIDE_SYNC_SETTINGS.pyodide_lock_url,
        lock_path=PYODIDE_SYNC_SETTINGS.pyodide_lock_path,
        pyproject_path=PYODIDE_SYNC_SETTINGS.pyproject_path,
    )

    assert exit_code == 0


def test_run_pyodide_constraints_sync_ci_returns_error_when_constraints_stale(
    tmp_path: Path,
    snippet_lock_url: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        "[tool.uv]\nconstraint-dependencies = []\n",
        encoding="utf-8",
    )
    lock_path = tmp_path / "pyodide-lock.json"

    exit_code = run_pyodide_constraints_sync(
        ci=True,
        url=snippet_lock_url,
        lock_path=lock_path,
        pyproject_path=pyproject_path,
    )

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "out of date" in captured.err


def test_run_pyodide_constraints_sync_updates_stale_constraints(
    tmp_path: Path,
    snippet_lock_url: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    pyproject_path = tmp_path / "pyproject.toml"
    pyproject_path.write_text(
        "[tool.uv]\nconstraint-dependencies = []\n",
        encoding="utf-8",
    )
    lock_path = tmp_path / "pyodide-lock.json"

    exit_code = run_pyodide_constraints_sync(
        ci=False,
        url=snippet_lock_url,
        lock_path=lock_path,
        pyproject_path=pyproject_path,
    )

    updated = read_pyproject_constraint_specifications(
        pyproject_path.read_text(encoding="utf-8"),
    )
    captured = capsys.readouterr().out

    assert exit_code == 0
    assert updated == ["altair==6.0.0", "numpy==2.2.5", "pandas==2.3.3"]
    assert "Updated Pyodide constraint-dependencies" in captured


def test_run_pyodide_constraints_sync_reports_already_up_to_date(
    tmp_path: Path,
    snippet_lock_url: str,
    capsys: pytest.CaptureFixture[str],
) -> None:
    expected = ["altair==6.0.0", "numpy==2.2.5", "pandas==2.3.3"]
    pyproject_path = tmp_path / "pyproject.toml"
    lock_path = tmp_path / "pyodide-lock.json"
    pyproject_path.write_text(
        replace_pyproject_constraint_dependencies(
            "[tool.uv]\nconstraint-dependencies = []\n",
            expected,
        ),
        encoding="utf-8",
    )

    exit_code = run_pyodide_constraints_sync(
        ci=False,
        url=snippet_lock_url,
        lock_path=lock_path,
        pyproject_path=pyproject_path,
    )

    assert exit_code == 0
    assert "already up to date" in capsys.readouterr().out
