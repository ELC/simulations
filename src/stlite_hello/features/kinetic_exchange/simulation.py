import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams


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
    return _sample_savings(rng, params)
