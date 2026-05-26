import pytest
from pydantic import TypeAdapter

from stlite_hello.site import Requirement, Requirements


def test_browser_requirement_rejects_unpinned_specification() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("numpy")


def test_browser_requirement_rejects_non_equality_version() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("numpy>=2.4.6")


def test_browser_requirement_parses_name_and_version() -> None:
    requirement = Requirement.model_validate("numpy==2.4.6")

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_accepts_explicit_fields() -> None:
    requirement = Requirement.model_validate(
        {"name": "numpy", "version": "2.4.6"},
    )

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_parses_specification_from_dict() -> None:
    requirement = Requirement.model_validate({"name": "numpy==2.4.6"})

    assert requirement.name == "numpy"
    assert requirement.version == "2.4.6"


def test_browser_requirement_rejects_unparseable_specification() -> None:
    with pytest.raises(ValueError, match="Unparseable dependency requirement"):
        Requirement.model_validate("@@@")


def test_browser_requirements_loads_project_dependencies(
    browser_requirements: Requirements,
) -> None:
    assert browser_requirements.names == [
        "altair",
        "numpy",
        "pandas",
        "pydantic",
        "pydantic-extra-types",
        "semver",
        "pydantic-settings",
        "pandera",
    ]


def test_browser_requirements_specs_pin_each_version(
    browser_requirements: Requirements,
) -> None:
    for spec in browser_requirements.specs:
        assert "==" in spec
        name, _, version = spec.partition("==")
        assert name in browser_requirements.names
        assert version


def test_browser_requirements_exclude_streamlit() -> None:
    loaded = TypeAdapter(Requirements).validate_python(
        {"requirements": ("altair==6.1.0", "streamlit==1.57.0")},
    )

    assert loaded.names == ["altair"]


def test_browser_requirements_keeps_non_streamlit_requirements() -> None:
    loaded = TypeAdapter(Requirements).validate_python(
        {"requirements": ("altair==6.1.0",)},
    )

    assert loaded.names == ["altair"]


def test_browser_requirements_accepts_requirements_mapping() -> None:
    loaded = Requirements.model_validate(
        {"requirements": [Requirement(name="altair", version="6.1.0")]},
    )

    assert loaded.names == ["altair"]
