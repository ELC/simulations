import pytest

from stlite_hello.features.double_auction import AdvancedParams, DoubleAuctionConfig

_FAST_TRADERS = 24
_FAST_STEPS = 30
_FAST_RUNS = 4


@pytest.fixture
def double_auction_fast_params() -> AdvancedParams:
    return AdvancedParams(n_traders=_FAST_TRADERS, n_steps=_FAST_STEPS)


@pytest.fixture
def double_auction_fast_config(double_auction_fast_params: AdvancedParams) -> DoubleAuctionConfig:
    return DoubleAuctionConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=8,
        bootstrap_resamples=200,
        params=double_auction_fast_params,
    )
