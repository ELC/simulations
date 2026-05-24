from pathlib import Path

from stlite_hello.site import (
    SITE_SETTINGS,
    Requirements,
    SiteFilePublisher,
    SiteTemplateRenderer,
    prepare_site,
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


def test_build_site_writes_static_assets(
    site_dir: Path,
    presentation_entrypoint: str,
) -> None:
    expected_files = ("index.html", "404.html", ".nojekyll")
    for filename in expected_files:
        assert (site_dir / filename).is_file()
    assert (site_dir / "stlite_hello").is_dir()
    assert (site_dir / presentation_entrypoint).is_file()
    assert (site_dir / "stlite_hello" / "charts.py").is_file()
    assert (site_dir / "stlite_hello" / "presentation" / "pages" / "home.py").is_file()
    assert (site_dir / "stlite_hello" / "presentation" / "pages" / "charts.py").is_file()


def test_build_site_excludes_build_tooling_from_package_copy(site_dir: Path) -> None:
    assert not (site_dir / "stlite_hello" / "site").exists()
    assert not (site_dir / "stlite_hello" / "__main__.py").exists()
    assert not any(path.name == "__pycache__" for path in (site_dir / "stlite_hello").rglob("*"))


def test_index_html_references_stlite_and_requirements(
    site_dir: Path,
    browser_requirements: Requirements,
) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert f"@stlite/browser@{SITE_SETTINGS.stlite_browser_version}" in index_html
    for spec in browser_requirements.specs:
        assert spec in index_html


def test_index_html_mounts_every_package_file(
    site_dir: Path,
    presentation_entrypoint: str,
) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    expected_files = (
        "stlite_hello/__init__.py",
        "stlite_hello/charts.py",
        presentation_entrypoint,
        "stlite_hello/presentation/pages/__init__.py",
        "stlite_hello/presentation/pages/home.py",
        "stlite_hello/presentation/pages/charts.py",
        "stlite_hello/presentation/pages/about.py",
    )
    for relative_path in expected_files:
        assert f'<app-file name="{relative_path}"' in index_html
        assert f'url="./{relative_path}"' in index_html


def test_index_html_uses_presentation_entrypoint(
    site_dir: Path,
    presentation_entrypoint: str,
) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert f'<streamlit-app src="./{presentation_entrypoint}">' in index_html


def test_build_site_replaces_existing_package_copy(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    browser_requirements: Requirements,
    presentation_entrypoint: str,
) -> None:
    stale_package = output_dir / "stlite_hello"
    stale_package.mkdir()
    stale_marker = stale_package / "stale.py"
    stale_marker.write_text("# stale\n", encoding="utf-8")

    file_publisher.publish_site(
        prepare_site(
            output_dir=output_dir,
            stlite_browser_version=SITE_SETTINGS.stlite_browser_version,
            browser_requirements=browser_requirements,
        ),
    )

    assert not stale_marker.exists()
    assert (output_dir / presentation_entrypoint).is_file()
