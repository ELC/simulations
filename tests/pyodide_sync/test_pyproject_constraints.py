import pytest

from stlite_hello.pyodide_sync import (
    filter_valid_uv_constraint_specifications,
    is_valid_uv_constraint_specification,
    read_pyproject_constraint_specifications,
    replace_pyproject_constraint_dependencies,
)


def test_is_valid_uv_constraint_specification_accepts_pep508_versions() -> None:
    assert is_valid_uv_constraint_specification("numpy==2.2.5") is True


def test_is_valid_uv_constraint_specification_rejects_pyodide_suffix_versions() -> None:
    assert is_valid_uv_constraint_specification("libopenssl==1.1.1w") is False


def test_filter_valid_uv_constraint_specifications_sorts_results() -> None:
    filtered = filter_valid_uv_constraint_specifications(
        ["pandas==2.3.3", "numpy==2.2.5", "libopenssl==1.1.1w"],
    )

    assert filtered == ["numpy==2.2.5", "pandas==2.3.3"]


def test_read_pyproject_constraint_specifications_requires_tool_table() -> None:
    with pytest.raises(ValueError, match=r"missing \[tool\]"):
        read_pyproject_constraint_specifications("[project]\nname = 'x'\n")


def test_read_pyproject_constraint_specifications_requires_uv_table() -> None:
    with pytest.raises(ValueError, match=r"missing \[tool.uv\]"):
        read_pyproject_constraint_specifications("[tool.poe]\ntest = 'pytest'\n")


def test_read_pyproject_constraint_specifications_requires_constraint_dependencies() -> None:
    with pytest.raises(
        ValueError,
        match=r"missing \[tool.uv\].constraint-dependencies",
    ):
        read_pyproject_constraint_specifications("[tool.uv]\npackage = true\n")


def test_replace_pyproject_constraint_dependencies_requires_tool_table() -> None:
    with pytest.raises(ValueError, match=r"missing \[tool\]"):
        replace_pyproject_constraint_dependencies(
            "[project]\nname = 'x'\n",
            ["numpy==2.2.5"],
        )


def test_replace_pyproject_constraint_dependencies_requires_uv_table() -> None:
    with pytest.raises(ValueError, match=r"missing \[tool.uv\]"):
        replace_pyproject_constraint_dependencies(
            "[tool.poe]\ntest = 'pytest'\n",
            ["numpy==2.2.5"],
        )


def test_replace_pyproject_constraint_dependencies_updates_constraint_dependencies() -> None:
    pyproject_text = "[tool.uv]\nconstraint-dependencies = []\n"

    updated = replace_pyproject_constraint_dependencies(
        pyproject_text,
        ["numpy==2.2.5"],
    )

    assert read_pyproject_constraint_specifications(updated) == ["numpy==2.2.5"]
