from pathlib import Path

import pytest

from stlite_hello.site import (
    SITE_SETTINGS,
    Requirements,
    SiteBuilderReady,
    SiteFilePublisher,
    SiteTemplateRenderer,
)


def test_clean_removes_existing_output_dir(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
) -> None:
    marker = output_dir / "stale.txt"
    marker.write_text("stale", encoding="utf-8")

    file_publisher.clean()

    assert not output_dir.exists()


def test_clean_is_noop_when_output_dir_missing(
    tmp_path: Path,
    template_renderer: SiteTemplateRenderer,
) -> None:
    missing = tmp_path / "missing"
    publisher = SiteFilePublisher(
        templates=template_renderer,
        destination=missing,
    )

    publisher.clean()

    assert not missing.exists()


@pytest.mark.usefixtures("_publish_site")
def test_build_site_writes_package_layout(
    output_dir: Path,
    app_entrypoint: str,
) -> None:
    package = output_dir / "stlite_hello"

    assert all((output_dir / name).is_file() for name in ("index.html", "404.html", ".nojekyll"))
    assert all(
        (output_dir / path).is_file()
        for path in (
            app_entrypoint,
            "stlite_hello/features/yard_sale/model.py",
            "stlite_hello/features/yard_sale/simulation.py",
            "stlite_hello/features/yard_sale/presentation/page.py",
            "stlite_hello/features/yard_sale/presentation/controller.py",
            "stlite_hello/presentation/sections.py",
        )
    )
    assert not (package / "site").exists()
    assert not (package / "__main__.py").exists()
    assert not any(path.name == "__main__.py" for path in package.rglob("*"))
    assert not any(path.name == "__pycache__" for path in package.rglob("*"))


@pytest.mark.usefixtures("_publish_site")
def test_index_html_references_stlite_and_requirements(
    output_dir: Path,
    browser_requirements: Requirements,
) -> None:
    index_html = (output_dir / "index.html").read_text(encoding="utf-8")

    assert f"@stlite/browser@{SITE_SETTINGS.stlite_browser_version}" in index_html
    for spec in browser_requirements.specs:
        assert spec in index_html


@pytest.mark.usefixtures("_publish_site")
def test_index_html_mounts_every_package_file(
    output_dir: Path,
    app_entrypoint: str,
) -> None:
    index_html = (output_dir / "index.html").read_text(encoding="utf-8")

    expected_files = (
        "stlite_hello/__init__.py",
        app_entrypoint,
        "stlite_hello/features/__init__.py",
        "stlite_hello/features/yard_sale/__init__.py",
        "stlite_hello/features/yard_sale/model.py",
        "stlite_hello/features/yard_sale/simulation.py",
        "stlite_hello/features/yard_sale/presentation/__init__.py",
        "stlite_hello/features/yard_sale/presentation/page.py",
        "stlite_hello/features/yard_sale/presentation/controller.py",
        "stlite_hello/presentation/__init__.py",
        "stlite_hello/presentation/sections.py",
    )
    for relative_path in expected_files:
        assert f'<app-file name="{relative_path}"' in index_html
        assert f'url="./{relative_path}"' in index_html


@pytest.mark.usefixtures("_publish_site")
def test_index_html_uses_app_entrypoint(
    output_dir: Path,
    app_entrypoint: str,
) -> None:
    index_html = (output_dir / "index.html").read_text(encoding="utf-8")

    assert f'<streamlit-app src="./{app_entrypoint}">' in index_html


def test_build_site_replaces_existing_package_copy(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    site_builder_ready: SiteBuilderReady,
    app_entrypoint: str,
) -> None:
    stale_package = output_dir / "stlite_hello"
    stale_package.mkdir()
    stale_marker = stale_package / "stale.py"
    stale_marker.write_text("# stale\n", encoding="utf-8")

    file_publisher.publish_site(site_builder_ready)

    assert not stale_marker.exists()
    assert (output_dir / app_entrypoint).is_file()
