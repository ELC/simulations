import pytest

from stlite_hello.analysis import RunBundle, run_replicates
from stlite_hello.features.kinetic_exchange import (
    AdvancedParams,
    KineticExchangeConfig,
    simulate_once,
)

_FAST_AGENTS = 24
_FAST_STEPS = 30
_FAST_RUNS = 4


@pytest.fixture
def kinetic_fast_params() -> AdvancedParams:
    return AdvancedParams(n_agents=_FAST_AGENTS, n_steps=_FAST_STEPS)


@pytest.fixture
def kinetic_fast_config(kinetic_fast_params: AdvancedParams) -> KineticExchangeConfig:
    return KineticExchangeConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=8,
        bootstrap_resamples=200,
        params=kinetic_fast_params,
    )


@pytest.fixture
def kinetic_fast_bundle(kinetic_fast_config: KineticExchangeConfig) -> RunBundle:
    return run_replicates(
        simulate_once=simulate_once,
        params=kinetic_fast_config.params,
        config=kinetic_fast_config,
    )
