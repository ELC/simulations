import os
import runpy
from pathlib import Path

import pytest

from stlite_hello.site import SITE_SETTINGS, load_browser_requirements, main


def test_load_browser_requirements_pins_each_project_dependency() -> None:
    requirements = load_browser_requirements(
        SITE_SETTINGS.project_dependency_specifications,
    )

    for specification in SITE_SETTINGS.project_dependency_specifications:
        name = specification.partition("==")[0]
        if name == "streamlit":
            continue
        assert specification in requirements.specs


def test_site_module_main_builds_default_output(tmp_path: Path) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        runpy.run_module("stlite_hello.site", run_name="__main__")
    finally:
        os.chdir(original_cwd)

    site_dir = tmp_path / SITE_SETTINGS.default_output_dir
    assert site_dir.is_dir()
    assert (site_dir / "index.html").is_file()


def test_main_writes_project_dependency_specifications_into_index(
    tmp_path: Path,
) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        destination = main()
        index_html = (destination.resolve() / "index.html").read_text(encoding="utf-8")
    finally:
        os.chdir(original_cwd)

    for specification in SITE_SETTINGS.project_dependency_specifications:
        if specification.startswith("streamlit=="):
            continue
        assert specification in index_html


@pytest.mark.usefixtures("_patch_site_settings")
def test_main_prints_destination(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    main()

    captured = capsys.readouterr().out
    assert f"Static site written to {tmp_path.resolve()}" in captured
