import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.labor_matching import (
    LABOR_MATCHING_DEFAULT_SEED,
    LABOR_MATCHING_DEFAULT_WORKERS,
    AdvancedParams,
    LaborMatchingConfig,
    SimpleParams,
    labor_market_history,
    simulate_once,
)

_DEFAULT_SEPARATION = 0.05


def test_simple_params_defaults_are_valid() -> None:
    params = SimpleParams()

    assert params.n_workers == LABOR_MATCHING_DEFAULT_WORKERS
    assert params.separation_rate == pytest.approx(_DEFAULT_SEPARATION)


def test_advanced_params_rejects_alpha_at_one() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(alpha=1.0)


def test_labor_matching_config_default_seed_is_distinct() -> None:
    assert LaborMatchingConfig().seed == LABOR_MATCHING_DEFAULT_SEED


def test_simulate_once_panel_shape_and_zero_starting_earnings() -> None:
    params = AdvancedParams(n_workers=50, n_steps=20)
    rng = np.random.default_rng(seed=LABOR_MATCHING_DEFAULT_SEED)

    result = simulate_once(params, rng)

    assert result.focal_panel.shape == (params.n_steps + 1, params.n_workers)
    assert np.allclose(result.focal_panel[0], 0.0)


def test_simulate_once_earnings_are_monotone_per_worker() -> None:
    params = AdvancedParams(n_workers=50, n_steps=30)
    rng = np.random.default_rng(seed=LABOR_MATCHING_DEFAULT_SEED)

    result = simulate_once(params, rng)

    diffs = np.diff(result.focal_panel, axis=0)
    assert bool(np.all(diffs >= 0.0))


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_workers=50, n_steps=20)

    first = simulate_once(params, np.random.default_rng(seed=LABOR_MATCHING_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=LABOR_MATCHING_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_labor_market_history_records_rates_in_unit_interval() -> None:
    params = AdvancedParams(n_workers=50, n_steps=15)
    rng = np.random.default_rng(seed=LABOR_MATCHING_DEFAULT_SEED)

    history = labor_market_history(params, rng)

    assert history.unemployment_rate.size == params.n_steps + 1
    assert bool(np.all(history.unemployment_rate >= 0.0))
    assert bool(np.all(history.unemployment_rate <= 1.0))
