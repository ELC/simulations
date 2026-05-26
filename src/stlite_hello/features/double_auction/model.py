"""Continuous double-auction price-discovery model (vectorised)."""

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

DOUBLE_AUCTION_DEFAULT_SEED = 1_000_037
DOUBLE_AUCTION_FEATURE = "double_auction"
DOUBLE_AUCTION_DEFAULT_TRADERS = 80
DOUBLE_AUCTION_DEFAULT_STEPS = 200
DOUBLE_AUCTION_DEFAULT_VALUE_CEILING = 100.0
DOUBLE_AUCTION_DEFAULT_SHADING = 0.2


class SimpleParams(BaseModel):
    """Two knobs: number of traders + simulation length."""

    model_config = ConfigDict(frozen=True)

    n_traders: int = Field(default=DOUBLE_AUCTION_DEFAULT_TRADERS, ge=4, le=1_000)
    n_steps: int = Field(default=DOUBLE_AUCTION_DEFAULT_STEPS, ge=10, le=2_000)
    value_ceiling: float = Field(default=DOUBLE_AUCTION_DEFAULT_VALUE_CEILING, gt=0.0)


class AdvancedParams(SimpleParams):
    """Adds bid/ask shading and the buyer share."""

    shading: float = Field(default=DOUBLE_AUCTION_DEFAULT_SHADING, ge=0.0, le=0.9)
    buyer_share: float = Field(default=0.5, gt=0.0, lt=1.0)


class DoubleAuctionConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=DOUBLE_AUCTION_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


class OrderBookSnapshot(BaseModel):
    """A frozen snapshot of one auction round's bids/asks/trades."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bids: NDArray[np.float64]
    asks: NDArray[np.float64]
    clearing_price: float


def _split_roles(n_traders: int, buyer_share: float, rng: np.random.Generator) -> NDArray[np.bool_]:
    is_buyer = rng.random(size=n_traders) < buyer_share
    return is_buyer


def _draw_values(*, n_traders: int, ceiling: float, rng: np.random.Generator) -> NDArray[np.float64]:
    return rng.uniform(0.0, ceiling, size=n_traders)


def _clear_round(
    *,
    values: NDArray[np.float64],
    is_buyer: NDArray[np.bool_],
    shading: float,
    ceiling: float,
) -> tuple[NDArray[np.float64], NDArray[np.float64], float, NDArray[np.float64]]:
    bids = np.where(is_buyer, values * (1.0 - shading), 0.0)
    asks = np.where(~is_buyer, values + (ceiling - values) * shading, ceiling)
    sorted_bids = np.sort(bids[is_buyer])[::-1]
    sorted_asks = np.sort(asks[~is_buyer])
    quantity = min(sorted_bids.size, sorted_asks.size)
    surplus = np.zeros(values.size, dtype=np.float64)
    if quantity == 0 or sorted_bids[0] < sorted_asks[0]:
        return bids, asks, 0.0, surplus
    matched = int(min(np.count_nonzero(sorted_bids[:quantity] >= sorted_asks[:quantity]), quantity))
    clearing_price = float((sorted_bids[matched - 1] + sorted_asks[matched - 1]) / 2.0)
    buyer_indices = np.argsort(bids)[::-1][:matched]
    seller_indices = np.argsort(np.where(is_buyer, ceiling + 1.0, asks))[:matched]
    surplus[buyer_indices] = np.maximum(values[buyer_indices] - clearing_price, 0.0)
    surplus[seller_indices] = np.maximum(clearing_price - values[seller_indices], 0.0)
    return bids, asks, clearing_price, surplus


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """Run one CDA replicate, returning the cumulative-surplus panel.

    Returns
    -------
    ReplicateResult
        ``focal_panel[t, i]`` is trader ``i``'s cumulative surplus after step ``t``.
    """
    cumulative = np.zeros(params.n_traders, dtype=np.float64)
    panel = np.empty((params.n_steps + 1, params.n_traders), dtype=np.float64)
    panel[0] = cumulative
    for step in range(1, params.n_steps + 1):
        is_buyer = _split_roles(params.n_traders, params.buyer_share, rng)
        values = _draw_values(n_traders=params.n_traders, ceiling=params.value_ceiling, rng=rng)
        _, _, _, surplus = _clear_round(
            values=values,
            is_buyer=is_buyer,
            shading=params.shading,
            ceiling=params.value_ceiling,
        )
        cumulative += surplus
        panel[step] = cumulative
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )


def final_orderbook(params: AdvancedParams, rng: np.random.Generator) -> OrderBookSnapshot:
    """Replay one replicate and capture the very last auction round.

    Returns
    -------
    OrderBookSnapshot
        Bids, asks, and clearing price for the final step.
    """
    snapshot = OrderBookSnapshot(
        bids=np.empty(0, dtype=np.float64),
        asks=np.empty(0, dtype=np.float64),
        clearing_price=0.0,
    )
    for _ in range(params.n_steps):
        is_buyer = _split_roles(params.n_traders, params.buyer_share, rng)
        values = _draw_values(n_traders=params.n_traders, ceiling=params.value_ceiling, rng=rng)
        bids, asks, clearing_price, _ = _clear_round(
            values=values,
            is_buyer=is_buyer,
            shading=params.shading,
            ceiling=params.value_ceiling,
        )
        snapshot = OrderBookSnapshot(
            bids=bids[is_buyer],
            asks=asks[~is_buyer],
            clearing_price=clearing_price,
        )
    return snapshot


__all__ = [
    "DOUBLE_AUCTION_DEFAULT_SEED",
    "DOUBLE_AUCTION_DEFAULT_SHADING",
    "DOUBLE_AUCTION_DEFAULT_STEPS",
    "DOUBLE_AUCTION_DEFAULT_TRADERS",
    "DOUBLE_AUCTION_DEFAULT_VALUE_CEILING",
    "DOUBLE_AUCTION_FEATURE",
    "AdvancedParams",
    "DoubleAuctionConfig",
    "OrderBookSnapshot",
    "SimpleParams",
    "final_orderbook",
    "simulate_once",
]
