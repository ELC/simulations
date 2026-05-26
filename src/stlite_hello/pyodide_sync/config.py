from functools import cached_property
from pathlib import Path

from pydantic import AliasChoices, Field
from pydantic_extra_types.semantic_version import SemanticVersion
from pydantic_settings import BaseSettings, SettingsConfigDict


class PyodideSyncSettings(BaseSettings):
    model_config = SettingsConfigDict(
        frozen=True,
        arbitrary_types_allowed=True,
        extra="ignore",
    )

    pyodide_version: SemanticVersion = Field(
        default=SemanticVersion.parse("0.29.3"),
        validation_alias=AliasChoices(
            "pyodide_version",
            "PYODIDE_VERSION",
        ),
    )

    @cached_property
    def package_dir(self) -> Path:
        return Path(__file__).resolve().parent

    @cached_property
    def pyproject_path(self) -> Path:
        return self.package_dir.parent.parent.parent / "pyproject.toml"

    @cached_property
    def pyodide_lock_path(self) -> Path:
        return self.pyproject_path.parent / "constraints" / "pyodide-lock.json"

    @cached_property
    def pyodide_lock_url(self) -> str:
        return f"https://cdn.jsdelivr.net/pyodide/v{self.pyodide_version}/full/pyodide-lock.json"


PYODIDE_SYNC_SETTINGS = PyodideSyncSettings()
