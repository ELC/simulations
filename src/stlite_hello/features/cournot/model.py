"""Cournot oligopoly best-response dynamics."""

from typing import cast

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

COURNOT_DEFAULT_SEED = 1_000_039
COURNOT_FEATURE = "cournot"
COURNOT_DEFAULT_FIRMS = 6
COURNOT_DEFAULT_STEPS = 60
COURNOT_DEFAULT_INTERCEPT = 100.0
COURNOT_DEFAULT_SLOPE = 1.0
COURNOT_DEFAULT_COST_MEAN = 20.0
COURNOT_DEFAULT_COST_SPREAD = 10.0
COURNOT_DEFAULT_INERTIA = 0.5


class SimpleParams(BaseModel):
    """Two knobs: firms + best-response inertia."""

    model_config = ConfigDict(frozen=True)

    n_firms: int = Field(default=COURNOT_DEFAULT_FIRMS, ge=2, le=50)
    n_steps: int = Field(default=COURNOT_DEFAULT_STEPS, ge=5, le=1_000)
    inertia: float = Field(default=COURNOT_DEFAULT_INERTIA, ge=0.0, le=0.99)


class AdvancedParams(SimpleParams):
    """Adds the demand intercept/slope and the cost spread."""

    intercept: float = Field(default=COURNOT_DEFAULT_INTERCEPT, gt=0.0)
    slope: float = Field(default=COURNOT_DEFAULT_SLOPE, gt=0.0)
    cost_mean: float = Field(default=COURNOT_DEFAULT_COST_MEAN, ge=0.0)
    cost_spread: float = Field(default=COURNOT_DEFAULT_COST_SPREAD, ge=0.0)


class CournotConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=COURNOT_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


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


def costs_for_seed(params: AdvancedParams, rng: np.random.Generator) -> NDArray[np.float64]:
    """Replay the cost draw used inside ``simulate_once`` for a given RNG.

    Returns
    -------
    NDArray[np.float64]
        Per-firm marginal costs.
    """
    return _sample_costs(params, rng)


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """One Cournot replicate; focal quantity is per-firm profit at each step.

    Returns
    -------
    ReplicateResult
        ``focal_panel[t, i]`` is firm ``i``'s profit at iteration ``t``.
    """
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


def _profits(
    *,
    quantities: NDArray[np.float64],
    costs: NDArray[np.float64],
    intercept: float,
    slope: float,
) -> NDArray[np.float64]:
    price = max(intercept - slope * float(quantities.sum()), 0.0)
    return cast("NDArray[np.float64]", np.maximum((price - costs) * quantities, 0.0))


def quantity_trajectory(
    params: AdvancedParams,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    """Reconstruct the per-step quantity vector for the special chart.

    Returns
    -------
    NDArray[np.float64]
        Shape ``(n_steps + 1, n_firms)`` of quantities at every iteration.
    """
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


__all__ = [
    "COURNOT_DEFAULT_COST_MEAN",
    "COURNOT_DEFAULT_COST_SPREAD",
    "COURNOT_DEFAULT_FIRMS",
    "COURNOT_DEFAULT_INERTIA",
    "COURNOT_DEFAULT_INTERCEPT",
    "COURNOT_DEFAULT_SEED",
    "COURNOT_DEFAULT_SLOPE",
    "COURNOT_DEFAULT_STEPS",
    "COURNOT_FEATURE",
    "AdvancedParams",
    "CournotConfig",
    "SimpleParams",
    "costs_for_seed",
    "quantity_trajectory",
    "simulate_once",
]
