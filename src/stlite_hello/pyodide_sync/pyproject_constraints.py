from collections.abc import Sequence

import tomlkit
from packaging.requirements import InvalidRequirement, Requirement


def is_valid_uv_constraint_specification(specification: str) -> bool:
    try:
        Requirement(specification)
    except InvalidRequirement:
        return False
    return True


def filter_valid_uv_constraint_specifications(
    specifications: Sequence[str],
) -> list[str]:
    return sorted(
        specification for specification in specifications if is_valid_uv_constraint_specification(specification)
    )


def read_pyproject_constraint_specifications(pyproject_text: str) -> list[str]:
    document = tomlkit.parse(pyproject_text)
    tool = document.get("tool")
    if tool is None:
        msg = "pyproject.toml is missing [tool]"
        raise ValueError(msg)
    uv = tool.get("uv")
    if uv is None:
        msg = "pyproject.toml is missing [tool.uv]"
        raise ValueError(msg)
    constraints = uv.get("constraint-dependencies")
    if constraints is None:
        msg = "pyproject.toml is missing [tool.uv].constraint-dependencies"
        raise ValueError(msg)
    return [str(specification) for specification in constraints]


def replace_pyproject_constraint_dependencies(
    pyproject_text: str,
    specifications: Sequence[str],
) -> str:
    document = tomlkit.parse(pyproject_text)
    tool = document.get("tool")
    if tool is None:
        msg = "pyproject.toml is missing [tool]"
        raise ValueError(msg)
    uv = tool.get("uv")
    if uv is None:
        msg = "pyproject.toml is missing [tool.uv]"
        raise ValueError(msg)
    uv["constraint-dependencies"] = list(specifications)
    return document.as_string()
