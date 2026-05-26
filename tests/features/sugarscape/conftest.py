import pytest

from stlite_hello.features.sugarscape import AdvancedParams, SugarscapeConfig

_FAST_AGENTS = 16
_FAST_GRID = 10
_FAST_STEPS = 20
_FAST_RUNS = 4
_FAST_TRAJECTORY = 8
_FAST_RESAMPLES = 200


@pytest.fixture
def sugarscape_fast_params() -> AdvancedParams:
    return AdvancedParams(
        n_agents=_FAST_AGENTS,
        n_steps=_FAST_STEPS,
        grid_size=_FAST_GRID,
    )


@pytest.fixture
def sugarscape_fast_config(sugarscape_fast_params: AdvancedParams) -> SugarscapeConfig:
    return SugarscapeConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=_FAST_TRAJECTORY,
        bootstrap_resamples=_FAST_RESAMPLES,
        params=sugarscape_fast_params,
    )
