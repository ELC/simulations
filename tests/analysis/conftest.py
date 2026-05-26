import numpy as np
import pytest
from numpy.typing import NDArray
from pydantic import BaseModel

from stlite_hello.analysis import (
    AggregationConfig,
    ReplicateResult,
    RunBundle,
    SimulateOnce,
    SimulationReport,
    run_replicates,
    summarize,
)


class _NoParams(BaseModel):
    pass


@pytest.fixture
def trivial_params() -> _NoParams:
    return _NoParams()


@pytest.fixture
def aggregation_seed() -> int:
    return 1_000_003


@pytest.fixture
def aggregation_runs() -> int:
    return 6


@pytest.fixture
def aggregation_bootstrap_resamples() -> int:
    return 300


@pytest.fixture
def aggregation_trajectory_samples() -> int:
    return 8


@pytest.fixture
def aggregation_config(
    aggregation_seed: int,
    aggregation_runs: int,
    aggregation_bootstrap_resamples: int,
    aggregation_trajectory_samples: int,
) -> AggregationConfig:
    return AggregationConfig(
        seed=aggregation_seed,
        runs=aggregation_runs,
        bootstrap_resamples=aggregation_bootstrap_resamples,
        trajectory_step_samples=aggregation_trajectory_samples,
    )


@pytest.fixture
def exponential_simulate_once() -> SimulateOnce:
    def _sim(_params: BaseModel, rng: np.random.Generator) -> ReplicateResult:
        panel = rng.exponential(1.0, size=(40, 25)).astype(np.float64)
        return ReplicateResult(focal_panel=panel, step_index=np.arange(panel.shape[0], dtype=np.int_))

    return _sim


@pytest.fixture
def exponential_bundle(
    aggregation_config: AggregationConfig,
    trivial_params: _NoParams,
    exponential_simulate_once: SimulateOnce,
) -> RunBundle:
    return run_replicates(
        simulate_once=exponential_simulate_once,
        params=trivial_params,
        config=aggregation_config,
    )


@pytest.fixture
def exponential_report(
    exponential_bundle: RunBundle,
    aggregation_config: AggregationConfig,
) -> SimulationReport:
    return summarize(bundle=exponential_bundle, config=aggregation_config)


@pytest.fixture
def equal_panel() -> NDArray[np.float64]:
    return np.ones((5, 4), dtype=np.float64)


@pytest.fixture
def linear_panel() -> NDArray[np.float64]:
    base = np.arange(1, 5, dtype=np.float64)
    return np.tile(base, (5, 1))
