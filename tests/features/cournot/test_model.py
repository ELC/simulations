import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.cournot import (
    COURNOT_DEFAULT_FIRMS,
    COURNOT_DEFAULT_SEED,
    AdvancedParams,
    CournotConfig,
    SimpleParams,
    quantity_trajectory,
    simulate_once,
)

_DEFAULT_INERTIA = 0.5
_NEAR_NASH_TOLERANCE = 1e-3


def test_simple_params_defaults_carry_inertia() -> None:
    params = SimpleParams()

    assert params.n_firms == COURNOT_DEFAULT_FIRMS
    assert params.inertia == pytest.approx(_DEFAULT_INERTIA)


def test_advanced_params_rejects_inertia_above_one() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(inertia=1.5)


def test_cournot_config_default_seed_is_distinct() -> None:
    assert CournotConfig().seed == COURNOT_DEFAULT_SEED


def test_simulate_once_focal_panel_has_one_row_per_step_plus_initial() -> None:
    params = AdvancedParams(n_firms=5, n_steps=20, cost_spread=0.0)
    rng = np.random.default_rng(seed=COURNOT_DEFAULT_SEED)

    result = simulate_once(params, rng)

    assert result.focal_panel.shape == (params.n_steps + 1, params.n_firms)
    assert result.step_index.shape == (params.n_steps + 1,)


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_firms=5, n_steps=20)

    first = simulate_once(params, np.random.default_rng(seed=COURNOT_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=COURNOT_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_simulate_once_converges_toward_symmetric_nash_when_costs_are_identical() -> None:
    n_firms = 4
    intercept = 100.0
    slope = 1.0
    cost = 20.0
    params = AdvancedParams(
        n_firms=n_firms,
        n_steps=400,
        inertia=0.7,
        intercept=intercept,
        slope=slope,
        cost_mean=cost,
        cost_spread=0.0,
    )
    rng = np.random.default_rng(seed=COURNOT_DEFAULT_SEED)

    quantities = quantity_trajectory(params, rng)

    nash_quantity = (intercept - cost) / (slope * (n_firms + 1))
    final = quantities[-1]
    assert np.allclose(final, nash_quantity, atol=_NEAR_NASH_TOLERANCE)
