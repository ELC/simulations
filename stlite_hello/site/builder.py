from __future__ import annotations

from importlib import import_module
from pathlib import Path
from types import ModuleType  # noqa: TC003

from pydantic_extra_types.semantic_version import SemanticVersion  # noqa: TC002

from .extensions import OutputNotDirectoryError
from .models import FrozenSiteModel
from .requirements import Requirements  # noqa: TC001


class SiteBuilder:
    @staticmethod
    def prepare(output_dir: Path) -> SiteBuilderDestination:
        if output_dir.exists() and not output_dir.is_dir():
            raise OutputNotDirectoryError(output_dir)
        return SiteBuilderDestination(destination=output_dir)


class SiteBuilderDestination(FrozenSiteModel):
    destination: Path

    def with_browser_app(self, app_module: ModuleType) -> SiteBuilderBrowser:
        package_name = app_module.__name__.split(".", maxsplit=1)[0]
        package_root = import_module(package_name)
        module_file = package_root.__file__
        if module_file is None:
            msg = f"Package {package_name!r} has no __file__"
            raise TypeError(msg)
        package_dir = Path(module_file).resolve().parent
        return SiteBuilderBrowser(
            destination=self.destination,
            package_name=package_name,
            package_dir=package_dir,
            app_module_name=app_module.__name__,
        )


class SiteBuilderBrowser(FrozenSiteModel):
    destination: Path
    package_name: str
    package_dir: Path
    app_module_name: str

    def with_index(
        self,
        version: SemanticVersion,
        browser_requirements: Requirements,
    ) -> SiteBuilderReady:
        return SiteBuilderReady(
            destination=self.destination,
            package_name=self.package_name,
            package_dir=self.package_dir,
            app_module_name=self.app_module_name,
            version=version,
            browser_requirements=browser_requirements,
        )


class SiteBuilderReady(FrozenSiteModel):
    destination: Path
    package_name: str
    package_dir: Path
    app_module_name: str
    version: SemanticVersion
    browser_requirements: Requirements

    @property
    def entrypoint(self) -> str:
        return f"{self.app_module_name.replace('.', '/')}.py"
