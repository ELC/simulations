import argparse
from collections.abc import Sequence

from .config import PYODIDE_SYNC_SETTINGS
from .constraints_sync import run_pyodide_constraints_sync


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Sync [tool.uv].constraint-dependencies from the Pyodide lock file",
    )
    parser.add_argument(
        "--ci",
        action="store_true",
        help="Exit with status 1 when constraint-dependencies are stale",
    )
    args = parser.parse_args(list(argv) if argv is not None else None)

    return run_pyodide_constraints_sync(
        ci=args.ci,
        url=PYODIDE_SYNC_SETTINGS.pyodide_lock_url,
        lock_path=PYODIDE_SYNC_SETTINGS.pyodide_lock_path,
        pyproject_path=PYODIDE_SYNC_SETTINGS.pyproject_path,
    )


if __name__ == "__main__":
    raise SystemExit(main())
