import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.yard_sale import (
    YARD_SALE_DEFAULT_AGENTS,
    YARD_SALE_DEFAULT_INITIAL_WEALTH,
    YARD_SALE_DEFAULT_SEED,
    YARD_SALE_DEFAULT_STEPS,
    AdvancedParams,
    SimpleParams,
    YardSaleConfig,
    simulate_once,
)


def test_simple_params_defaults_match_module_constants() -> None:
    params = SimpleParams()

    assert params.n_agents == YARD_SALE_DEFAULT_AGENTS
    assert params.n_steps == YARD_SALE_DEFAULT_STEPS


def test_advanced_params_extends_simple_with_initial_wealth() -> None:
    params = AdvancedParams()

    assert params.initial_wealth == pytest.approx(YARD_SALE_DEFAULT_INITIAL_WEALTH)
    assert 0.0 < params.win_probability < 1.0


def test_advanced_params_rejects_invalid_win_probability() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(win_probability=1.5)


def test_yard_sale_config_default_seed_is_distinct_and_documented() -> None:
    config = YardSaleConfig()

    assert config.seed == YARD_SALE_DEFAULT_SEED


def test_simulate_once_conserves_total_wealth() -> None:
    params = AdvancedParams(n_agents=20, n_steps=50)
    rng = np.random.default_rng(seed=YARD_SALE_DEFAULT_SEED)

    result = simulate_once(params, rng)

    initial_total = result.focal_panel[0].sum()
    final_total = result.focal_panel[-1].sum()
    assert final_total == pytest.approx(initial_total, rel=1e-9)


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_agents=20, n_steps=50)

    first = simulate_once(params, np.random.default_rng(seed=YARD_SALE_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=YARD_SALE_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_simulate_once_emits_expected_panel_shape() -> None:
    params = AdvancedParams(n_agents=15, n_steps=12)

    result = simulate_once(params, np.random.default_rng(seed=YARD_SALE_DEFAULT_SEED))

    assert result.focal_panel.shape == (params.n_steps + 1, params.n_agents)
    assert result.step_index.shape == (params.n_steps + 1,)
