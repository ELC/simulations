import json
from pathlib import Path

import pytest


@pytest.fixture
def pyodide_lock_snippet() -> dict[str, object]:
    return {
        "info": {"version": "0.29.3"},
        "packages": {
            "numpy": {"name": "numpy", "version": "2.2.5"},
            "pandas": {"name": "pandas", "version": "2.3.3"},
            "altair": {"name": "altair", "version": "6.0.0"},
        },
    }


@pytest.fixture
def snippet_lock_url(
    tmp_path: Path,
    pyodide_lock_snippet: dict[str, object],
) -> str:
    snippet_path = tmp_path / "snippet-lock.json"
    snippet_path.write_text(json.dumps(pyodide_lock_snippet), encoding="utf-8")
    return snippet_path.as_uri()
