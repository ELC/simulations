"""Yard-Sale wealth-exchange model (vectorised, deterministic per seed)."""

import numpy as np
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

YARD_SALE_DEFAULT_SEED = 1_000_003
YARD_SALE_FEATURE = "yard_sale"
YARD_SALE_DEFAULT_AGENTS = 200
YARD_SALE_DEFAULT_STEPS = 500
YARD_SALE_DEFAULT_FRACTION = 0.10
YARD_SALE_DEFAULT_INITIAL_WEALTH = 100.0


class SimpleParams(BaseModel):
    """Two-knob view: how big the random transfer is, and population size."""

    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=YARD_SALE_DEFAULT_AGENTS, ge=10, le=2_000)
    n_steps: int = Field(default=YARD_SALE_DEFAULT_STEPS, ge=10, le=5_000)
    transfer_fraction: float = Field(default=YARD_SALE_DEFAULT_FRACTION, gt=0.0, lt=1.0)


class AdvancedParams(SimpleParams):
    """Full parametrisation including initial wealth and win probability."""

    initial_wealth: float = Field(default=YARD_SALE_DEFAULT_INITIAL_WEALTH, gt=0.0)
    win_probability: float = Field(default=0.5, gt=0.0, lt=1.0)


class YardSaleConfig(AggregationConfig):
    """Frozen aggregation + per-sim params for Yard-Sale."""

    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=YARD_SALE_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """Run one Yard-Sale replicate; return the per-step wealth panel.

    Returns
    -------
    ReplicateResult
        ``focal_panel`` shape ``(n_steps + 1, n_agents)`` (step 0 is the
        initial endowment).
    """
    n_agents = params.n_agents
    n_steps = params.n_steps
    wealth = np.full(n_agents, params.initial_wealth, dtype=np.float64)
    panel = np.empty((n_steps + 1, n_agents), dtype=np.float64)
    panel[0] = wealth
    half = n_agents - (n_agents % 2)
    for step in range(1, n_steps + 1):
        order = rng.permutation(n_agents)
        pairs = order[:half].reshape(-1, 2)
        a, b = pairs[:, 0], pairs[:, 1]
        stake = params.transfer_fraction * np.minimum(wealth[a], wealth[b])
        a_wins = rng.random(size=pairs.shape[0]) < params.win_probability
        transfer = np.where(a_wins, stake, -stake)
        wealth[a] += transfer
        wealth[b] -= transfer
        panel[step] = wealth
    step_index = np.arange(n_steps + 1, dtype=np.int_)
    return ReplicateResult(focal_panel=panel, step_index=step_index)


__all__ = [
    "YARD_SALE_DEFAULT_AGENTS",
    "YARD_SALE_DEFAULT_FRACTION",
    "YARD_SALE_DEFAULT_INITIAL_WEALTH",
    "YARD_SALE_DEFAULT_SEED",
    "YARD_SALE_DEFAULT_STEPS",
    "YARD_SALE_FEATURE",
    "AdvancedParams",
    "SimpleParams",
    "YardSaleConfig",
    "simulate_once",
]
