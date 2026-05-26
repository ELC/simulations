import pytest
from pydantic import ValidationError

from stlite_hello.analysis import AggregationConfig

_DEFAULT_RUNS = 30
_DEFAULT_TRAJECTORY_SAMPLES = 15
_DEFAULT_BOOTSTRAP_RESAMPLES = 500
_DEFAULT_CONFIDENCE_LEVEL = 0.95


def test_aggregation_config_defaults_when_seed_set() -> None:
    config = AggregationConfig(seed=42)

    assert config.runs == _DEFAULT_RUNS
    assert config.trajectory_step_samples == _DEFAULT_TRAJECTORY_SAMPLES
    assert config.bootstrap_resamples == _DEFAULT_BOOTSTRAP_RESAMPLES
    assert config.confidence_level == pytest.approx(_DEFAULT_CONFIDENCE_LEVEL)
    assert config.bootstrap_method == "BCa"


def test_aggregation_config_is_frozen() -> None:
    config = AggregationConfig(seed=1)

    frozen_field = "runs"
    with pytest.raises(ValidationError):
        setattr(config, frozen_field, 50)


def test_aggregation_config_rejects_too_many_runs() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig(seed=1, runs=10_000)


def test_aggregation_config_rejects_invalid_confidence_level() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig(seed=1, confidence_level=1.5)


def test_aggregation_config_requires_seed() -> None:
    with pytest.raises(ValidationError):
        AggregationConfig.model_validate({})
