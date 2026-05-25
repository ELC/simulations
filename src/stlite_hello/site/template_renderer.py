from collections.abc import Sequence

from jinja2 import Environment
from pydantic_extra_types.semantic_version import SemanticVersion

from .models import FrozenSiteModel


class SiteTemplateRenderer(FrozenSiteModel):
    jinja_environment: Environment

    def render_index_html(
        self,
        *,
        version: SemanticVersion,
        requirements: Sequence[str],
        package_files: Sequence[str],
        entrypoint: str,
    ) -> str:
        template = self.jinja_environment.get_template("index.html.jinja")
        return template.render(
            version=version,
            requirements=requirements,
            package_files=package_files,
            entrypoint=entrypoint,
        )

    def render_not_found_html(self) -> str:
        template = self.jinja_environment.get_template("404.html.jinja")
        return template.render()
