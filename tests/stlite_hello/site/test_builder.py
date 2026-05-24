import sys
import types
from pathlib import Path

import pytest

from stlite_hello.site import OutputNotDirectoryError, SiteBuilder


def test_site_builder_prepare_sets_destination(output_dir: Path) -> None:
    builder = SiteBuilder.prepare(output_dir)

    assert builder.destination == output_dir


def test_site_builder_prepare_rejects_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "notadir"
    file_path.write_text("x", encoding="utf-8")

    with pytest.raises(OutputNotDirectoryError, match="Output path must be a directory"):
        SiteBuilder.prepare(file_path)


def test_with_browser_app_rejects_package_without_file(tmp_path: Path) -> None:
    package_name = "coverage_fake_pkg"
    fake_package = types.ModuleType(package_name)
    fake_package.__file__ = None
    sys.modules[package_name] = fake_package
    app_module = types.ModuleType(f"{package_name}.app")
    app_module.__name__ = f"{package_name}.app"
    builder = SiteBuilder.prepare(tmp_path)

    try:
        with pytest.raises(TypeError, match="has no __file__"):
            builder.with_browser_app(app_module)
    finally:
        sys.modules.pop(package_name, None)
