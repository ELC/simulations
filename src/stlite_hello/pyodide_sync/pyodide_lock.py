import urllib.error
import urllib.request
from collections.abc import Mapping
from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, ValidationError, field_validator

PYODIDE_LOCK_JSON_ADAPTER = TypeAdapter[dict[str, Any]](dict[str, Any])


class Requirement(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    version: str

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.lower().replace("-", "_")

    @property
    def pinned_specification(self) -> str:
        return f"{self.name}=={self.version}"


class PyodideLockIndex(BaseModel):
    model_config = ConfigDict(frozen=True)

    packages: Mapping[str, str] = Field(default_factory=dict[str, str])

    @staticmethod
    def fetch_lock_data(url: str) -> dict[str, Any]:
        try:
            with urllib.request.urlopen(url, timeout=30) as response:  # noqa: S310
                payload = response.read()
        except urllib.error.URLError as error:
            msg = f"Failed to download Pyodide lock file from {url}"
            raise ValueError(msg) from error

        return PYODIDE_LOCK_JSON_ADAPTER.validate_json(payload)

    @classmethod
    def from_lock_data(cls, lock_data: Mapping[str, Any]) -> Self:
        packages: dict[str, str] = {}
        raw_packages = lock_data.get("packages")
        if not isinstance(raw_packages, Mapping):
            return cls(packages=packages)

        for entry in raw_packages.values():
            if not isinstance(entry, Mapping):
                continue
            try:
                requirement = Requirement.model_validate(entry)
            except ValidationError:
                continue
            packages[requirement.name] = requirement.version

        return cls(packages=packages)

    def all_pinned_specifications(self) -> list[str]:
        return sorted(f"{name}=={version}" for name, version in self.packages.items())
