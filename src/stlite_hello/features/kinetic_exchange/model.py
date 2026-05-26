"""Chakraborti-Chakrabarti kinetic wealth exchange with savings."""

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

KINETIC_DEFAULT_SEED = 1_000_033
KINETIC_FEATURE = "kinetic_exchange"
KINETIC_DEFAULT_AGENTS = 200
KINETIC_DEFAULT_STEPS = 500
KINETIC_DEFAULT_LAMBDA_MEAN = 0.5
KINETIC_DEFAULT_LAMBDA_SPREAD = 0.3
KINETIC_DEFAULT_INITIAL_WEALTH = 100.0


class SimpleParams(BaseModel):
    """Knob set for the simple view: how strongly agents save and how many they are."""

    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=KINETIC_DEFAULT_AGENTS, ge=10, le=2_000)
    n_steps: int = Field(default=KINETIC_DEFAULT_STEPS, ge=10, le=5_000)
    lambda_mean: float = Field(default=KINETIC_DEFAULT_LAMBDA_MEAN, ge=0.0, le=1.0)


class AdvancedParams(SimpleParams):
    """Full parametrisation including saving heterogeneity and seed wealth."""

    lambda_spread: float = Field(default=KINETIC_DEFAULT_LAMBDA_SPREAD, ge=0.0, le=1.0)
    initial_wealth: float = Field(default=KINETIC_DEFAULT_INITIAL_WEALTH, gt=0.0)


class KineticExchangeConfig(AggregationConfig):
    """Frozen aggregation + per-sim params for Kinetic Exchange."""

    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=KINETIC_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


def _sample_savings(rng: np.random.Generator, params: AdvancedParams) -> NDArray[np.float64]:
    lo = max(0.0, params.lambda_mean - params.lambda_spread)
    hi = min(1.0, params.lambda_mean + params.lambda_spread)
    if hi <= lo:
        return np.full(params.n_agents, params.lambda_mean, dtype=np.float64)
    return rng.uniform(lo, hi, size=params.n_agents)


def _kinetic_step(
    *,
    wealth: NDArray[np.float64],
    savings: NDArray[np.float64],
    rng: np.random.Generator,
) -> None:
    n_agents = wealth.size
    half = n_agents - (n_agents % 2)
    order = rng.permutation(n_agents)
    pairs = order[:half].reshape(-1, 2)
    i, j = pairs[:, 0], pairs[:, 1]
    epsilon = rng.random(size=pairs.shape[0])
    pot = (1.0 - savings[i]) * wealth[i] + (1.0 - savings[j]) * wealth[j]
    total = wealth[i] + wealth[j]
    share_i = savings[i] * wealth[i] + epsilon * pot
    wealth[i] = share_i
    wealth[j] = total - share_i


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """One Kinetic Exchange replicate.

    Returns
    -------
    ReplicateResult
        Wealth panel of shape ``(n_steps + 1, n_agents)`` with the initial
        endowment in row 0.
    """
    wealth = np.full(params.n_agents, params.initial_wealth, dtype=np.float64)
    savings = _sample_savings(rng, params)
    panel = np.empty((params.n_steps + 1, params.n_agents), dtype=np.float64)
    panel[0] = wealth
    for step in range(1, params.n_steps + 1):
        _kinetic_step(wealth=wealth, savings=savings, rng=rng)
        panel[step] = wealth
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )


def savings_per_agent(params: AdvancedParams, rng: np.random.Generator) -> NDArray[np.float64]:
    """Reproduce the per-agent savings draw used inside ``simulate_once``.

    Returns
    -------
    NDArray[np.float64]
        Array of saving fractions, one per agent.
    """
    return _sample_savings(rng, params)


__all__ = [
    "KINETIC_DEFAULT_AGENTS",
    "KINETIC_DEFAULT_INITIAL_WEALTH",
    "KINETIC_DEFAULT_LAMBDA_MEAN",
    "KINETIC_DEFAULT_LAMBDA_SPREAD",
    "KINETIC_DEFAULT_SEED",
    "KINETIC_DEFAULT_STEPS",
    "KINETIC_FEATURE",
    "AdvancedParams",
    "KineticExchangeConfig",
    "SimpleParams",
    "savings_per_agent",
    "simulate_once",
]
