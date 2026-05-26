import json
import sys
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from .pyodide_lock import PyodideLockIndex
from .pyproject_constraints import (
    filter_valid_uv_constraint_specifications,
    read_pyproject_constraint_specifications,
    replace_pyproject_constraint_dependencies,
)


def sync_pyodide_lock_file(lock_path: Path, *, lock_data: Mapping[str, Any]) -> None:
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    lock_path.write_text(
        json.dumps(dict(lock_data), indent=4, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def sync_pyodide_constraints(*, url: str, lock_path: Path) -> list[str]:
    lock_data = PyodideLockIndex.fetch_lock_data(url)
    sync_pyodide_lock_file(lock_path, lock_data=lock_data)
    index = PyodideLockIndex.from_lock_data(lock_data)
    return filter_valid_uv_constraint_specifications(index.all_pinned_specifications())


def load_pyodide_constraint_specifications(
    *,
    url: str,
    lock_path: Path,
    pyproject_path: Path,
) -> tuple[list[str], list[str]]:
    expected = sync_pyodide_constraints(url=url, lock_path=lock_path)
    current = read_pyproject_constraint_specifications(
        pyproject_path.read_text(encoding="utf-8"),
    )
    return current, expected


def update_pyproject_constraint_dependencies(
    pyproject_path: Path,
    specifications: Sequence[str],
) -> None:
    pyproject_text = pyproject_path.read_text(encoding="utf-8")
    pyproject_path.write_text(
        replace_pyproject_constraint_dependencies(pyproject_text, specifications),
        encoding="utf-8",
    )


def run_pyodide_constraints_sync(
    *,
    ci: bool,
    url: str,
    lock_path: Path,
    pyproject_path: Path,
) -> int:
    current, expected = load_pyodide_constraint_specifications(
        url=url,
        lock_path=lock_path,
        pyproject_path=pyproject_path,
    )

    if current == expected:
        print("Pyodide constraint-dependencies already up to date")  # noqa: T201
        return 0

    if ci:
        print(  # noqa: T201
            "pyproject.toml constraint-dependencies are out of date; run: uv run poe sync-pyodide-constraints",
            file=sys.stderr,
        )
        return 1

    update_pyproject_constraint_dependencies(pyproject_path, expected)
    print(f"Updated Pyodide constraint-dependencies in {pyproject_path}")  # noqa: T201
    return 0
