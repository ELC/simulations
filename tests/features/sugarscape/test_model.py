import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.sugarscape import (
    SUGARSCAPE_DEFAULT_AGENTS,
    SUGARSCAPE_DEFAULT_SEED,
    AdvancedParams,
    SimpleParams,
    SugarscapeConfig,
    final_snapshot,
    simulate_once,
)

_DEFAULT_VISION = 4


def test_simple_params_defaults_are_valid() -> None:
    params = SimpleParams()

    assert params.n_agents == SUGARSCAPE_DEFAULT_AGENTS
    assert params.vision == _DEFAULT_VISION


def test_advanced_params_rejects_zero_grid() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(grid_size=0)


def test_sugarscape_config_default_seed_is_distinct() -> None:
    assert SugarscapeConfig().seed == SUGARSCAPE_DEFAULT_SEED


def test_simulate_once_emits_panel_with_initial_endowment_row() -> None:
    params = AdvancedParams(n_agents=12, n_steps=10, grid_size=8)
    rng = np.random.default_rng(seed=SUGARSCAPE_DEFAULT_SEED)

    result = simulate_once(params, rng)

    assert result.focal_panel.shape == (params.n_steps + 1, params.n_agents)
    assert np.allclose(result.focal_panel[0], params.initial_endowment)


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_agents=12, n_steps=10, grid_size=8)

    first = simulate_once(params, np.random.default_rng(seed=SUGARSCAPE_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=SUGARSCAPE_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_final_snapshot_returns_grid_and_agent_positions_in_bounds() -> None:
    params = AdvancedParams(n_agents=12, n_steps=10, grid_size=8)
    rng = np.random.default_rng(seed=SUGARSCAPE_DEFAULT_SEED)

    snapshot = final_snapshot(params, rng)

    assert snapshot.sugar_grid.shape == (params.grid_size, params.grid_size)
    assert snapshot.agent_rows.size == params.n_agents
    assert int(snapshot.agent_rows.max()) < params.grid_size
    assert int(snapshot.agent_cols.max()) < params.grid_size


def test_simulate_once_rejects_more_agents_than_cells() -> None:
    params = AdvancedParams(n_agents=400, n_steps=5, grid_size=5)
    rng = np.random.default_rng(seed=SUGARSCAPE_DEFAULT_SEED)

    with pytest.raises(ValueError, match="More agents than cells"):
        simulate_once(params, rng)
