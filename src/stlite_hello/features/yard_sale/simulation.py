import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams


def _yard_sale_step(
    *,
    wealth: NDArray[np.float64],
    rng: np.random.Generator,
    transfer_fraction: float,
    win_probability: float,
) -> None:
    n_agents = wealth.size
    half = n_agents - (n_agents % 2)
    order = rng.permutation(n_agents)
    pairs = order[:half].reshape(-1, 2)
    a, b = pairs[:, 0], pairs[:, 1]
    stake = transfer_fraction * np.minimum(wealth[a], wealth[b])
    transfer = np.where(rng.random(size=pairs.shape[0]) < win_probability, stake, -stake)
    wealth[a] += transfer
    wealth[b] -= transfer


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    wealth = np.full(params.n_agents, params.initial_wealth, dtype=np.float64)
    panel = np.empty((params.n_steps + 1, params.n_agents), dtype=np.float64)
    panel[0] = wealth
    for step in range(1, params.n_steps + 1):
        _yard_sale_step(
            wealth=wealth,
            rng=rng,
            transfer_fraction=params.transfer_fraction,
            win_probability=params.win_probability,
        )
        panel[step] = wealth
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )
