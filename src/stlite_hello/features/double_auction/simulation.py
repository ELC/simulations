import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams, OrderBookSnapshot


def _split_roles(n_traders: int, buyer_share: float, rng: np.random.Generator) -> NDArray[np.bool_]:
    return rng.random(size=n_traders) < buyer_share


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
