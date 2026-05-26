import numpy as np
import pandas as pd
import pytest

from stlite_hello.analysis import (
    AggregationConfig,
    ReplicateResult,
    RunBundle,
    SimulateOnce,
    run_replicates,
)
from stlite_hello.analysis.aggregation import ParamsProtocol

_DEFAULT_STEPS = 4
_DEFAULT_AGENTS = 3


class _NoParams:
    """Minimal Pydantic-style stand-in implementing ``ParamsProtocol``."""


def _make_constant_simulator(value: float) -> SimulateOnce:
    def _sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        panel = np.full((_DEFAULT_STEPS, _DEFAULT_AGENTS), value, dtype=np.float64)
        return ReplicateResult(focal_panel=panel, step_index=np.arange(_DEFAULT_STEPS, dtype=np.int_))

    return _sim


def test_run_replicates_runs_for_each_seed(
    aggregation_config: AggregationConfig,
    trivial_params: ParamsProtocol,
) -> None:
    sim = _make_constant_simulator(1.0)

    bundle: RunBundle = run_replicates(simulate_once=sim, params=trivial_params, config=aggregation_config)

    expected_final_rows = aggregation_config.runs * _DEFAULT_AGENTS
    expected_panel_rows = aggregation_config.runs * _DEFAULT_STEPS * _DEFAULT_AGENTS
    assert bundle.final_population.shape[0] == expected_final_rows
    assert bundle.focal_panel.shape[0] == expected_panel_rows


def test_run_replicates_is_reproducible(
    aggregation_config: AggregationConfig,
    trivial_params: ParamsProtocol,
    exponential_simulate_once: SimulateOnce,
) -> None:
    first = run_replicates(
        simulate_once=exponential_simulate_once,
        params=trivial_params,
        config=aggregation_config,
    )
    second = run_replicates(
        simulate_once=exponential_simulate_once,
        params=trivial_params,
        config=aggregation_config,
    )

    pd.testing.assert_frame_equal(first.final_population, second.final_population)
    pd.testing.assert_frame_equal(first.focal_panel, second.focal_panel)


def test_run_replicates_rejects_non_2d_panel(
    aggregation_config: AggregationConfig,
    trivial_params: ParamsProtocol,
) -> None:
    def bad_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        return ReplicateResult(focal_panel=np.zeros(5, dtype=np.float64), step_index=np.zeros(5, dtype=np.int_))

    with pytest.raises(ValueError, match="2-D"):
        run_replicates(simulate_once=bad_sim, params=trivial_params, config=aggregation_config)


def test_run_replicates_rejects_step_index_mismatch(
    aggregation_config: AggregationConfig,
    trivial_params: ParamsProtocol,
) -> None:
    def bad_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        return ReplicateResult(
            focal_panel=np.zeros((3, 2), dtype=np.float64),
            step_index=np.arange(5, dtype=np.int_),
        )

    with pytest.raises(ValueError, match="step_index"):
        run_replicates(simulate_once=bad_sim, params=trivial_params, config=aggregation_config)


def test_run_replicates_rejects_mismatched_agent_counts(
    aggregation_config: AggregationConfig,
    trivial_params: ParamsProtocol,
) -> None:
    call_counter = {"count": 0}

    def changing_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        call_counter["count"] += 1
        size = _DEFAULT_AGENTS if call_counter["count"] % 2 == 0 else _DEFAULT_AGENTS + 1
        panel = np.ones((_DEFAULT_STEPS - 2, size), dtype=np.float64)
        return ReplicateResult(focal_panel=panel, step_index=np.arange(_DEFAULT_STEPS - 2, dtype=np.int_))

    with pytest.raises(ValueError, match="same number of agents"):
        run_replicates(simulate_once=changing_sim, params=trivial_params, config=aggregation_config)
