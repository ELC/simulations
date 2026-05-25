import tomllib
from collections.abc import Sequence
from functools import cached_property
from pathlib import Path
from typing import TypedDict, cast

from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import AliasChoices, Field
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_settings import BaseSettings, SettingsConfigDict


class PyprojectProject(TypedDict):
    dependencies: Sequence[str]


class Pyproject(TypedDict):
    project: PyprojectProject


class SiteSettings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        extra="ignore",
    )

    stlite_browser_version: SemanticVersion = Field(
        default=SemanticVersion.parse("1.7.3"),
        validation_alias=AliasChoices(
            "stlite_browser_version",
            "STLITE_BROWSER_VERSION",
        ),
    )
    default_output_dir: Path = Field(default=Path("_site"))
    pyodide_bundle_versions: dict[str, SemanticVersion] = Field(
        default_factory=lambda: {
            "numpy": SemanticVersion.parse("2.2.5"),
            "pandas": SemanticVersion.parse("2.3.3"),
        },
    )

    @cached_property
    def package_dir(self) -> Path:
        return Path(__file__).resolve().parent

    @cached_property
    def templates_dir(self) -> Path:
        return self.package_dir / "templates"

    @cached_property
    def pyproject_path(self) -> Path:
        return self.package_dir.parent.parent.parent / "pyproject.toml"

    @cached_property
    def jinja_environment(self) -> Environment:
        return Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(["html"]),
        )

    @cached_property
    def pyproject(self) -> Pyproject:
        return cast(
            "Pyproject",
            tomllib.loads(self.pyproject_path.read_text(encoding="utf-8")),
        )

    @cached_property
    def project_dependency_specifications(self) -> Sequence[str]:
        return self.pyproject["project"]["dependencies"]


SITE_SETTINGS = SiteSettings()
