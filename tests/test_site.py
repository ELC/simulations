import os
import runpy
from pathlib import Path

import pytest
from pydantic import TypeAdapter

import stlite_hello.app as app_module
from stlite_hello.site import (
    SITE_SETTINGS,
    OutputNotDirectoryError,
    Requirement,
    Requirements,
    RequirementsAdapter,
    SiteBuilder,
    SiteFilePublisher,
    SiteTemplateRenderer,
)
from stlite_hello.site import main as build_site


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    site_output = tmp_path / "_site"
    site_output.mkdir()
    return site_output


@pytest.fixture
def template_renderer() -> SiteTemplateRenderer:
    return SiteTemplateRenderer(jinja_environment=SITE_SETTINGS.jinja_environment)


@pytest.fixture
def browser_requirements() -> Requirements:
    return RequirementsAdapter.validate_python(
        {"requirements": SITE_SETTINGS.project_dependency_specifications},
    )


@pytest.fixture
def file_publisher(
    template_renderer: SiteTemplateRenderer,
    output_dir: Path,
) -> SiteFilePublisher:
    return SiteFilePublisher(
        templates=template_renderer,
        destination=output_dir,
    )


@pytest.fixture
def site_dir(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    browser_requirements: Requirements,
) -> Path:
    return build_site(
        output_dir,
        publisher=file_publisher,
        browser_requirements=browser_requirements,
    )


def test_site_builder_prepare_sets_destination(output_dir: Path) -> None:
    builder = SiteBuilder.prepare(output_dir)

    assert builder.destination == output_dir


def test_site_builder_prepare_rejects_existing_file(tmp_path: Path) -> None:
    file_path = tmp_path / "notadir"
    file_path.write_text("x", encoding="utf-8")

    with pytest.raises(OutputNotDirectoryError, match="Output path must be a directory"):
        SiteBuilder.prepare(file_path)


def test_build_site_writes_static_assets(site_dir: Path) -> None:
    expected_files = ("index.html", "app.py", "404.html", ".nojekyll")
    for filename in expected_files:
        assert (site_dir / filename).is_file()
    assert (site_dir / "stlite_hello").is_dir()
    assert (site_dir / "stlite_hello" / "app.py").is_file()
    assert (site_dir / "stlite_hello" / "charts.py").is_file()


def test_build_site_excludes_build_tooling_from_package_copy(site_dir: Path) -> None:
    assert not (site_dir / "stlite_hello" / "site").exists()
    assert not (site_dir / "stlite_hello" / "__main__.py").exists()
    assert not any(
        path.name == "__pycache__"
        for path in (site_dir / "stlite_hello").rglob("*")
    )


def test_index_html_references_stlite_and_requirements(
    site_dir: Path,
    browser_requirements: Requirements,
) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert f"@stlite/browser@{SITE_SETTINGS.stlite_browser_version}" in index_html
    for spec in browser_requirements.specs:
        assert spec in index_html


def test_index_html_mounts_every_package_file(site_dir: Path) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    expected_files = (
        "stlite_hello/__init__.py",
        "stlite_hello/app.py",
        "stlite_hello/charts.py",
    )
    for relative_path in expected_files:
        assert f'<app-file name="{relative_path}"' in index_html
        assert f'url="./{relative_path}"' in index_html


def test_browser_app_imports_main_from_package(
    site_dir: Path,
    template_renderer: SiteTemplateRenderer,
) -> None:
    app_source = (site_dir / "app.py").read_text(encoding="utf-8")

    expected = template_renderer.render_app_source(
        app_module_name=app_module.__name__,
    )
    assert app_source == expected
    assert "from stlite_hello.app import main" in app_source
    assert "main()" in app_source


def test_browser_requirement_rejects_unpinned_specification() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("numpy")


def test_browser_requirement_rejects_non_equality_version() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("numpy>=2.4.6")


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


def test_browser_requirement_parses_name_and_version() -> None:
    requirement = Requirement.model_validate("numpy==2.4.6")

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_accepts_explicit_fields() -> None:
    requirement = Requirement.model_validate(
        {"name": "numpy", "version": "2.4.6"},
    )

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_parses_specification_from_dict() -> None:
    requirement = Requirement.model_validate({"name": "numpy==2.4.6"})

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_rejects_unparseable_specification() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("@@@")


def test_browser_requirements_loads_project_dependencies(
    browser_requirements: Requirements,
) -> None:
    assert browser_requirements.names == [
        "altair",
        "numpy",
        "pandas",
        "pydantic",
        "pydantic-extra-types",
        "semver",
        "pydantic-settings",
        "pandera",
    ]


def test_browser_requirements_specs_pin_each_version(
    browser_requirements: Requirements,
) -> None:
    for spec in browser_requirements.specs:
        assert "==" in spec
        name, _, version = spec.partition("==")
        assert name in browser_requirements.names
        assert version


def test_browser_requirements_exclude_streamlit() -> None:
    loaded = TypeAdapter(Requirements).validate_python(
        {"requirements": ("altair==6.1.0", "streamlit==1.57.0")},
    )

    assert loaded.names == ["altair"]


def test_browser_requirements_keeps_non_streamlit_requirements() -> None:
    loaded = TypeAdapter(Requirements).validate_python(
        {"requirements": ("altair==6.1.0",)},
    )

    assert loaded.names == ["altair"]


def test_browser_requirements_accepts_requirements_mapping() -> None:
    loaded = Requirements.model_validate(
        {"requirements": [Requirement(name="altair", version="6.1.0")]},
    )

    assert loaded.names == ["altair"]


def test_template_renderer_substitutes_version_and_requirements(
    template_renderer: SiteTemplateRenderer,
) -> None:
    rendered = template_renderer.render_index_html(
        version="9.9.9",
        requirements=("altair",),
        package_files=("stlite_hello/__init__.py",),
    )

    assert "@stlite/browser@9.9.9" in rendered
    assert "altair" in rendered
    assert '<app-file name="stlite_hello/__init__.py"' in rendered


def test_template_renderer_not_found_html_returns_redirect_page(
    template_renderer: SiteTemplateRenderer,
) -> None:
    html = template_renderer.render_not_found_html()

    assert "sessionStorage.setItem" in html
    assert "location.replace" in html


def test_jinja_environment_does_not_autoescape_python_templates(
    template_renderer: SiteTemplateRenderer,
) -> None:
    rendered = template_renderer.render_app_source(
        app_module_name="stlite_hello.app",
    )

    assert "->" not in rendered or "-&gt;" not in rendered
    assert "&gt;" not in rendered
    assert "&lt;" not in rendered


def test_build_site_replaces_existing_package_copy(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    browser_requirements: Requirements,
) -> None:
    stale_package = output_dir / "stlite_hello"
    stale_package.mkdir()
    stale_marker = stale_package / "stale.py"
    stale_marker.write_text("# stale\n", encoding="utf-8")

    build_site(
        output_dir,
        publisher=file_publisher,
        browser_requirements=browser_requirements,
    )

    assert not stale_marker.exists()
    assert (output_dir / "stlite_hello" / "app.py").is_file()


def test_build_site_main_prints_destination(
    output_dir: Path,
    file_publisher: SiteFilePublisher,
    browser_requirements: Requirements,
    capsys: pytest.CaptureFixture[str],
) -> None:
    destination = build_site(
        output_dir,
        publisher=file_publisher,
        browser_requirements=browser_requirements,
    )

    captured = capsys.readouterr().out
    assert str(destination.resolve()) in captured
