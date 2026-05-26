import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.double_auction import (
    DOUBLE_AUCTION_DEFAULT_SEED,
    AdvancedParams,
    DoubleAuctionConfig,
    SimpleParams,
    final_orderbook,
    simulate_once,
)

_VALUE_CEILING = 100.0


def test_simple_params_defaults_are_valid() -> None:
    params = SimpleParams()

    assert params.value_ceiling == pytest.approx(_VALUE_CEILING)


def test_advanced_params_rejects_shading_above_cap() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(shading=1.5)


def test_double_auction_config_default_seed_is_distinct_and_documented() -> None:
    assert DoubleAuctionConfig().seed == DOUBLE_AUCTION_DEFAULT_SEED


def test_simulate_once_emits_non_decreasing_cumulative_surplus() -> None:
    params = AdvancedParams(n_traders=20, n_steps=30)
    rng = np.random.default_rng(seed=DOUBLE_AUCTION_DEFAULT_SEED)

    result = simulate_once(params, rng)

    diffs = np.diff(result.focal_panel, axis=0)
    assert bool(np.all(diffs >= 0.0))


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_traders=20, n_steps=30)

    first = simulate_once(params, np.random.default_rng(seed=DOUBLE_AUCTION_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=DOUBLE_AUCTION_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_final_orderbook_returns_bids_and_asks_with_clearing_price() -> None:
    params = AdvancedParams(n_traders=20, n_steps=10)
    rng = np.random.default_rng(seed=DOUBLE_AUCTION_DEFAULT_SEED)

    snapshot = final_orderbook(params, rng)

    assert snapshot.bids.size + snapshot.asks.size == params.n_traders
    assert 0.0 <= snapshot.clearing_price <= params.value_ceiling
