import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.kinetic_exchange import (
    KINETIC_DEFAULT_LAMBDA_MEAN,
    KINETIC_DEFAULT_SEED,
    AdvancedParams,
    KineticExchangeConfig,
    SimpleParams,
    savings_per_agent,
    simulate_once,
)

_CONSERVATION_RTOL = 1e-9
_SAVINGS_MIN = 0.3
_SAVINGS_MAX = 0.7
_SAVINGS_TOL = 1e-3


def test_simple_params_defaults_match_module_constants() -> None:
    assert SimpleParams().lambda_mean == pytest.approx(KINETIC_DEFAULT_LAMBDA_MEAN)


def test_advanced_params_rejects_negative_spread() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(lambda_spread=-0.1)


def test_kinetic_config_default_seed_is_distinct_and_documented() -> None:
    assert KineticExchangeConfig().seed == KINETIC_DEFAULT_SEED


def test_simulate_once_conserves_total_wealth() -> None:
    params = AdvancedParams(n_agents=20, n_steps=50)
    rng = np.random.default_rng(seed=KINETIC_DEFAULT_SEED)

    result = simulate_once(params, rng)

    assert result.focal_panel[-1].sum() == pytest.approx(result.focal_panel[0].sum(), rel=_CONSERVATION_RTOL)


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_agents=20, n_steps=30)

    first = simulate_once(params, np.random.default_rng(seed=KINETIC_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=KINETIC_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_savings_per_agent_uses_homogeneous_value_when_spread_is_zero() -> None:
    params = AdvancedParams(n_agents=12, lambda_spread=0.0, lambda_mean=0.7)
    rng = np.random.default_rng(seed=KINETIC_DEFAULT_SEED)

    savings = savings_per_agent(params, rng)

    assert savings.shape == (params.n_agents,)
    assert np.allclose(savings, 0.7)


def test_savings_per_agent_respects_spread_when_positive() -> None:
    params = AdvancedParams(n_agents=400, lambda_spread=0.2, lambda_mean=0.5)
    rng = np.random.default_rng(seed=KINETIC_DEFAULT_SEED)

    savings = savings_per_agent(params, rng)

    assert float(savings.min()) >= _SAVINGS_MIN - _SAVINGS_TOL
    assert float(savings.max()) <= _SAVINGS_MAX + _SAVINGS_TOL
