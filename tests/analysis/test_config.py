import pytest
from pydantic import ValidationError

from stlite_hello.analysis import AggregationConfig


def test_aggregation_config_defaults_when_seed_set() -> None:
    config = AggregationConfig(seed=42)

    assert config.runs == 30
    assert config.trajectory_step_samples == 50
    assert config.bootstrap_resamples == 2_000
    assert config.confidence_level == 0.95
    assert config.bootstrap_method == "BCa"


def test_aggregation_config_is_frozen() -> None:
    config = AggregationConfig(seed=1)

    with pytest.raises(ValidationError):
        config.runs = 50  # type: ignore[misc]


def test_aggregation_config_rejects_too_many_runs() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig(seed=1, runs=10_000)


def test_aggregation_config_rejects_invalid_confidence_level() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig(seed=1, confidence_level=1.5)


def test_aggregation_config_requires_seed() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig()  # type: ignore[call-arg]
