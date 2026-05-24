from pathlib import Path

import stlite_hello.app as app_module

from .builder import SiteBuilder
from .config import SITE_SETTINGS
from .publisher import SiteFilePublisher
from .requirements import Requirements, RequirementsAdapter
from .template_renderer import SiteTemplateRenderer


def main(
    output_dir: Path,
    *,
    publisher: SiteFilePublisher,
    browser_requirements: Requirements,
) -> Path:
    ready = (
        SiteBuilder.prepare(output_dir)
        .with_browser_app(app_module)
        .with_index(SITE_SETTINGS.stlite_browser_version, browser_requirements)
    )
    destination = publisher.publish_site(ready)
    print(f"Static site written to {destination.resolve()}")
    return destination


def build_default_site() -> Path:
    browser_requirements = RequirementsAdapter.validate_python(
        {"requirements": SITE_SETTINGS.project_dependency_specifications},
    )
    templates = SiteTemplateRenderer(jinja_environment=SITE_SETTINGS.jinja_environment)
    publisher = SiteFilePublisher(
        templates=templates,
        destination=SITE_SETTINGS.default_output_dir,
    )
    return main(
        SITE_SETTINGS.default_output_dir,
        publisher=publisher,
        browser_requirements=browser_requirements,
    )
