import os
import runpy
import sys
import types
from pathlib import Path

import pytest
from pydantic import TypeAdapter

from stlite_hello.site import (
    SITE_SETTINGS,
    OutputNotDirectoryError,
    Requirement,
    Requirements,
    SemanticVersion,
    SiteBuilder,
    SiteFilePublisher,
    SiteTemplateRenderer,
    load_browser_requirements,
    main,
    prepare_site,
)

PRESENTATION_ENTRYPOINT = "stlite_hello/presentation/app.py"


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


def test_load_browser_requirements_aligns_to_pyodide_bundle() -> None:
    requirements = load_browser_requirements(
        project_dependency_specifications=SITE_SETTINGS.project_dependency_specifications,
        pyodide_bundle_versions=SITE_SETTINGS.pyodide_bundle_versions,
    )

    bundle_versions: dict[str, SemanticVersion] = SITE_SETTINGS.pyodide_bundle_versions

    for name, version in bundle_versions.items():  # pylint: disable=no-member
        assert f"{name}=={version}" in requirements.specs


def test_build_site_writes_static_assets(site_dir: Path) -> None:
    expected_files = ("index.html", "404.html", ".nojekyll")
    for filename in expected_files:
        assert (site_dir / filename).is_file()
    assert (site_dir / "stlite_hello").is_dir()
    assert (site_dir / PRESENTATION_ENTRYPOINT).is_file()
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


def test_index_html_mounts_every_package_file(site_dir: Path) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    expected_files = (
        "stlite_hello/__init__.py",
        "stlite_hello/charts.py",
        PRESENTATION_ENTRYPOINT,
        "stlite_hello/presentation/pages/__init__.py",
        "stlite_hello/presentation/pages/home.py",
        "stlite_hello/presentation/pages/charts.py",
        "stlite_hello/presentation/pages/about.py",
    )
    for relative_path in expected_files:
        assert f'<app-file name="{relative_path}"' in index_html
        assert f'url="./{relative_path}"' in index_html


def test_index_html_uses_presentation_entrypoint(site_dir: Path) -> None:
    index_html = (site_dir / "index.html").read_text(encoding="utf-8")

    assert f'<streamlit-app src="./{PRESENTATION_ENTRYPOINT}">' in index_html


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


def test_requirements_aligned_to_overrides_known_names() -> None:
    requirements = Requirements.model_validate(
        {"requirements": ["altair==6.5.0", "numpy==2.4.0", "pydantic==2.12.5"]},
    )

    aligned = requirements.aligned_to(
        {
            "altair": SemanticVersion.parse("6.0.0"),
            "numpy": SemanticVersion.parse("2.2.5"),
        },
    )

    assert aligned.specs == ["altair==6.0.0", "numpy==2.2.5", "pydantic==2.12.5"]


def test_requirements_aligned_to_keeps_versions_without_overrides() -> None:
    requirements = Requirements.model_validate(
        {"requirements": ["pydantic==2.12.5"]},
    )

    aligned = requirements.aligned_to({})

    assert aligned.specs == ["pydantic==2.12.5"]


def test_pyodide_bundle_versions_pins_binary_packages() -> None:
    bundle = SITE_SETTINGS.pyodide_bundle_versions

    assert bundle["numpy"] == SemanticVersion.parse("2.2.5")
    assert bundle["pandas"] == SemanticVersion.parse("2.3.3")


def test_main_aligns_browser_requirements_to_pyodide_bundle(
    tmp_path: Path,
) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        destination = main()
    finally:
        os.chdir(original_cwd)

    index_html = (destination.resolve() / "index.html").read_text(encoding="utf-8")

    bundle_versions: dict[str, SemanticVersion] = SITE_SETTINGS.pyodide_bundle_versions

    for name, version in bundle_versions.items():  # pylint: disable=no-member
        assert f"{name}=={version}" in index_html


def test_template_renderer_substitutes_version_and_requirements(
    template_renderer: SiteTemplateRenderer,
) -> None:
    rendered = template_renderer.render_index_html(
        version=SemanticVersion.parse("9.9.9"),
        requirements=("altair",),
        package_files=("stlite_hello/__init__.py",),
        entrypoint=PRESENTATION_ENTRYPOINT,
    )

    assert "@stlite/browser@9.9.9" in rendered
    assert "altair" in rendered
    assert '<app-file name="stlite_hello/__init__.py"' in rendered
    assert f'<streamlit-app src="./{PRESENTATION_ENTRYPOINT}">' in rendered


def test_template_renderer_not_found_html_returns_redirect_page(
    template_renderer: SiteTemplateRenderer,
) -> None:
    html = template_renderer.render_not_found_html()

    assert "sessionStorage.setItem" in html
    assert "location.replace" in html


def test_jinja_environment_does_not_autoescape_python_templates(
    template_renderer: SiteTemplateRenderer,
) -> None:
    rendered = template_renderer.render_index_html(
        version=SemanticVersion.parse("1.0.0"),
        requirements=(),
        package_files=("stlite_hello/presentation/app.py",),
        entrypoint=PRESENTATION_ENTRYPOINT,
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

    file_publisher.publish_site(
        prepare_site(
            output_dir=output_dir,
            stlite_browser_version=SITE_SETTINGS.stlite_browser_version,
            browser_requirements=browser_requirements,
        ),
    )

    assert not stale_marker.exists()
    assert (output_dir / PRESENTATION_ENTRYPOINT).is_file()


def test_main_prints_destination(
    tmp_path: Path,
    capsys: pytest.CaptureFixture[str],
) -> None:
    original_cwd = Path.cwd()
    try:
        os.chdir(tmp_path)
        destination = main()
        expected_destination = str(destination.resolve())
    finally:
        os.chdir(original_cwd)

    captured = capsys.readouterr().out
    assert expected_destination in captured
