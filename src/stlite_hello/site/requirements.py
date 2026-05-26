from collections.abc import Sequence
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, TypeAdapter, field_validator, model_validator
from pydantic_extra_types.semantic_version import SemanticVersion


class Requirement(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: str
    version: SemanticVersion

    @model_validator(mode="before")
    @classmethod
    def parse_specification(cls, data: Any) -> Any:
        if isinstance(data, str):
            return cls._split_pinned(data)
        if isinstance(data, dict):
            raw_name = data.get("name")
            if isinstance(raw_name, str) and "version" not in data:
                return cls._split_pinned(raw_name)
        return data

    @staticmethod
    def _split_pinned(specification: str) -> dict[str, str]:
        name, separator, version = specification.partition("==")
        if not separator:
            msg = f"Unparseable dependency requirement: {specification!r}"
            raise ValueError(msg)
        return {"name": name, "version": version}

    @field_validator("name", mode="after")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.lower().replace(" ", "_")


class Requirements(BaseModel):
    model_config = ConfigDict(frozen=True)

    requirements: Sequence[Requirement] = Field(
        default_factory=list[Requirement],
    )

    @field_validator("requirements", mode="after")
    @classmethod
    def exclude_streamlit(
        cls,
        requirements: Sequence[Requirement],
    ) -> list[Requirement]:
        return [requirement for requirement in requirements if requirement.name != "streamlit"]

    @property
    def names(self) -> list[str]:
        return [requirement.name for requirement in self.requirements]

    @property
    def specs(self) -> list[str]:
        return [f"{requirement.name}=={requirement.version}" for requirement in self.requirements]


RequirementsAdapter = TypeAdapter[Requirements](Requirements)  # pylint: disable=invalid-name
