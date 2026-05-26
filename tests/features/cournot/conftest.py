import pytest

from stlite_hello.features.cournot import AdvancedParams, CournotConfig

_FAST_FIRMS = 5
_FAST_STEPS = 30
_FAST_RUNS = 4
_FAST_TRAJECTORY = 8
_FAST_RESAMPLES = 200


@pytest.fixture
def cournot_fast_params() -> AdvancedParams:
    return AdvancedParams(n_firms=_FAST_FIRMS, n_steps=_FAST_STEPS)


@pytest.fixture
def cournot_fast_config(cournot_fast_params: AdvancedParams) -> CournotConfig:
    return CournotConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=_FAST_TRAJECTORY,
        bootstrap_resamples=_FAST_RESAMPLES,
        params=cournot_fast_params,
    )
