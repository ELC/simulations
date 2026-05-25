from pathlib import Path

import pytest

from stlite_hello.site import (
    SITE_SETTINGS,
    Requirements,
    RequirementsAdapter,
    SiteBuilderReady,
    SiteFilePublisher,
    SiteSettings,
    SiteTemplateRenderer,
    prepare_site,
)


@pytest.fixture
def presentation_entrypoint() -> str:
    return "stlite_hello/presentation/app.py"


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    return tmp_path


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
def site_builder_ready(
    output_dir: Path,
    browser_requirements: Requirements,
) -> SiteBuilderReady:
    return prepare_site(
        output_dir=output_dir,
        stlite_browser_version=SITE_SETTINGS.stlite_browser_version,
        browser_requirements=browser_requirements,
    )


@pytest.fixture
def patched_site_settings(tmp_path: Path) -> SiteSettings:
    return SITE_SETTINGS.model_copy(update={"default_output_dir": tmp_path})


@pytest.fixture
def _patch_site_settings(
    monkeypatch: pytest.MonkeyPatch,
    patched_site_settings: SiteSettings,
) -> None:
    monkeypatch.setattr("stlite_hello.site.build.SITE_SETTINGS", patched_site_settings)


@pytest.fixture
def _publish_site(
    file_publisher: SiteFilePublisher,
    site_builder_ready: SiteBuilderReady,
) -> None:
    file_publisher.publish_site(site_builder_ready)
