from pathlib import Path

import pytest

from stlite_hello.site import (
    SITE_SETTINGS,
    Requirements,
    RequirementsAdapter,
    SiteFilePublisher,
    SiteTemplateRenderer,
    prepare_site,
)


@pytest.fixture
def presentation_entrypoint() -> str:
    return "stlite_hello/presentation/app.py"


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
    return file_publisher.publish_site(
        prepare_site(
            output_dir=output_dir,
            stlite_browser_version=SITE_SETTINGS.stlite_browser_version,
            browser_requirements=browser_requirements,
        ),
    )
