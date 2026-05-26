import pytest

from stlite_hello.features.labor_matching import AdvancedParams, LaborMatchingConfig

_FAST_WORKERS = 40
_FAST_STEPS = 20
_FAST_RUNS = 4
_FAST_TRAJECTORY = 8
_FAST_RESAMPLES = 200


@pytest.fixture
def labor_matching_fast_params() -> AdvancedParams:
    return AdvancedParams(n_workers=_FAST_WORKERS, n_steps=_FAST_STEPS)


@pytest.fixture
def labor_matching_fast_config(
    labor_matching_fast_params: AdvancedParams,
) -> LaborMatchingConfig:
    return LaborMatchingConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=_FAST_TRAJECTORY,
        bootstrap_resamples=_FAST_RESAMPLES,
        params=labor_matching_fast_params,
    )
