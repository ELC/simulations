from typing import cast

import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams


def _sample_costs(params: AdvancedParams, rng: np.random.Generator) -> NDArray[np.float64]:
    if params.cost_spread <= 0.0:
        return np.full(params.n_firms, params.cost_mean, dtype=np.float64)
    lo = max(0.0, params.cost_mean - params.cost_spread)
    hi = params.cost_mean + params.cost_spread
    return rng.uniform(lo, hi, size=params.n_firms)


def _best_response(
    *,
    quantities: NDArray[np.float64],
    costs: NDArray[np.float64],
    intercept: float,
    slope: float,
) -> NDArray[np.float64]:
    others = quantities.sum() - quantities
    raw = (intercept - costs - slope * others) / (2.0 * slope)
    return cast("NDArray[np.float64]", np.maximum(raw, 0.0))


def _profits(
    *,
    quantities: NDArray[np.float64],
    costs: NDArray[np.float64],
    intercept: float,
    slope: float,
) -> NDArray[np.float64]:
    price = max(intercept - slope * float(quantities.sum()), 0.0)
    return cast("NDArray[np.float64]", np.maximum((price - costs) * quantities, 0.0))


def costs_for_seed(params: AdvancedParams, rng: np.random.Generator) -> NDArray[np.float64]:
    return _sample_costs(params, rng)


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    costs = _sample_costs(params, rng)
    quantities: NDArray[np.float64] = np.full(
        params.n_firms,
        params.intercept / (2.0 * params.slope * params.n_firms),
        dtype=np.float64,
    )
    panel = np.empty((params.n_steps + 1, params.n_firms), dtype=np.float64)
    panel[0] = _profits(quantities=quantities, costs=costs, intercept=params.intercept, slope=params.slope)
    for step in range(1, params.n_steps + 1):
        target = _best_response(
            quantities=quantities,
            costs=costs,
            intercept=params.intercept,
            slope=params.slope,
        )
        quantities = params.inertia * quantities + (1.0 - params.inertia) * target
        panel[step] = _profits(
            quantities=quantities,
            costs=costs,
            intercept=params.intercept,
            slope=params.slope,
        )
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )


def quantity_trajectory(
    params: AdvancedParams,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    costs = _sample_costs(params, rng)
    quantities: NDArray[np.float64] = np.full(
        params.n_firms,
        params.intercept / (2.0 * params.slope * params.n_firms),
        dtype=np.float64,
    )
    trajectory = np.empty((params.n_steps + 1, params.n_firms), dtype=np.float64)
    trajectory[0] = quantities
    for step in range(1, params.n_steps + 1):
        target = _best_response(
            quantities=quantities,
            costs=costs,
            intercept=params.intercept,
            slope=params.slope,
        )
        quantities = params.inertia * quantities + (1.0 - params.inertia) * target
        trajectory[step] = quantities
    return trajectory
