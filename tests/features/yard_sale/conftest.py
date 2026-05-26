import pytest

from stlite_hello.analysis import RunBundle, run_replicates
from stlite_hello.features.yard_sale import (
    AdvancedParams,
    YardSaleConfig,
    simulate_once,
)

_FAST_AGENTS = 24
_FAST_STEPS = 30
_FAST_RUNS = 4


@pytest.fixture
def yard_sale_fast_params() -> AdvancedParams:
    return AdvancedParams(n_agents=_FAST_AGENTS, n_steps=_FAST_STEPS)


@pytest.fixture
def yard_sale_fast_config(yard_sale_fast_params: AdvancedParams) -> YardSaleConfig:
    return YardSaleConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=8,
        bootstrap_resamples=200,
        params=yard_sale_fast_params,
    )


@pytest.fixture
def yard_sale_fast_bundle(yard_sale_fast_config: YardSaleConfig) -> RunBundle:
    return run_replicates(
        simulate_once=simulate_once,
        params=yard_sale_fast_config.params,
        config=yard_sale_fast_config,
    )
