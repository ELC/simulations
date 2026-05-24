from collections.abc import Sequence
from pathlib import Path

from pydantic_extra_types.semantic_version import SemanticVersion

from stlite_hello.presentation import app as app_module

from .builder import SiteBuilder, SiteBuilderReady
from .config import SITE_SETTINGS
from .publisher import SiteFilePublisher
from .requirements import Requirements, RequirementsAdapter
from .template_renderer import SiteTemplateRenderer


def load_browser_requirements(
    *,
    project_dependency_specifications: Sequence[str],
    pyodide_bundle_versions: dict[str, SemanticVersion],
) -> Requirements:
    project_requirements = RequirementsAdapter.validate_python(
        {"requirements": project_dependency_specifications},
    )
    return project_requirements.aligned_to(pyodide_bundle_versions)


def prepare_site(
    *,
    output_dir: Path,
    stlite_browser_version: SemanticVersion,
    browser_requirements: Requirements,
) -> SiteBuilderReady:
    return (
        SiteBuilder
        .prepare(output_dir)
        .with_browser_app(app_module)
        .with_index(stlite_browser_version, browser_requirements)
    )


def main() -> Path:
    browser_requirements = load_browser_requirements(
        project_dependency_specifications=SITE_SETTINGS.project_dependency_specifications,
        pyodide_bundle_versions=SITE_SETTINGS.pyodide_bundle_versions,
    )
    templates = SiteTemplateRenderer(jinja_environment=SITE_SETTINGS.jinja_environment)
    publisher = SiteFilePublisher(
        templates=templates,
        destination=SITE_SETTINGS.default_output_dir,
    )
    ready = prepare_site(
        output_dir=SITE_SETTINGS.default_output_dir,
        stlite_browser_version=SITE_SETTINGS.stlite_browser_version,
        browser_requirements=browser_requirements,
    )
    destination = publisher.publish_site(ready)
    print(f"Static site written to {destination.resolve()}")  # noqa: T201
    return destination
