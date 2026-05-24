import shutil
from collections.abc import Sequence
from pathlib import Path
from typing import TYPE_CHECKING

from .models import FrozenSiteModel
from .template_renderer import SiteTemplateRenderer

if TYPE_CHECKING:
    from .builder import SiteBuilderReady


class SiteFilePublisher(FrozenSiteModel):
    templates: SiteTemplateRenderer
    destination: Path

    def package_path(self, package_name: str) -> Path:
        return self.destination / package_name

    @property
    def index_path(self) -> Path:
        return self.destination / "index.html"

    @property
    def not_found_path(self) -> Path:
        return self.destination / "404.html"

    @property
    def nojekyll_path(self) -> Path:
        return self.destination / ".nojekyll"

    def clean(self) -> None:
        if self.destination.exists():
            shutil.rmtree(self.destination)

    def copy_package(self, source: Path, package_name: str) -> Sequence[str]:
        destination = self.package_path(package_name)
        shutil.copytree(
            source,
            destination,
            ignore=shutil.ignore_patterns(
                "site",
                "browser",
                "__main__.py",
                "__pycache__",
                "*.pyc",
            ),
        )
        return sorted(
            path.relative_to(self.destination).as_posix() for path in destination.rglob("*") if path.is_file()
        )

    def publish_site(self, ready: "SiteBuilderReady") -> Path:
        publisher = self.model_copy(update={"destination": ready.destination})
        publisher.clean()
        ready.destination.mkdir(parents=True, exist_ok=True)

        package_files = publisher.copy_package(ready.package_dir, ready.package_name)

        index_html = publisher.templates.render_index_html(
            version=ready.version,
            requirements=ready.browser_requirements.specs,
            package_files=package_files,
            entrypoint=ready.entrypoint,
        )
        not_found_html = publisher.templates.render_not_found_html()

        publisher.index_path.write_text(index_html, encoding="utf-8")
        publisher.not_found_path.write_text(not_found_html, encoding="utf-8")
        publisher.nojekyll_path.touch()

        return ready.destination
