"""Cross-model concentration and mobility metrics.

All functions operate on numpy arrays so they can be wrapped with
``scipy.stats.bootstrap`` for CIs. Public helpers (``lorenz_curve``,
``decile_transition_matrix``, ``top_pct_spells``) return Pandera-validated
dataframes so the rest of the analysis layer never touches raw pandas.
"""

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame

from .adapters import KaplanMeierEstimate, kaplan_meier_mean_lifetime
from .schemas import DecileTransition, LorenzCurve, TopPctSpell


def gini(values: NDArray[np.float64]) -> float:
    """Gini coefficient of a non-negative 1-D array."""
    if values.size == 0:
        return 0.0
    if np.any(values < 0):
        msg = "gini requires non-negative values"
        raise ValueError(msg)
    sorted_values = np.sort(values)
    n = sorted_values.size
    total = float(sorted_values.sum())
    if total == 0.0:
        return 0.0
    cumulative = np.cumsum(sorted_values, dtype=np.float64)
    return float((n + 1 - 2 * np.sum(cumulative) / total) / n)


def top_share(values: NDArray[np.float64], *, fraction: float) -> float:
    """Share of the total held by the top ``fraction`` of the population."""
    if values.size == 0:
        return 0.0
    if not 0.0 < fraction <= 1.0:
        msg = "fraction must be in (0, 1]"
        raise ValueError(msg)
    total = float(values.sum())
    if total == 0.0:
        return 0.0
    k = max(1, int(np.ceil(values.size * fraction)))
    top = np.partition(values, -k)[-k:]
    return float(top.sum() / total)


def hill_alpha(values: NDArray[np.float64], *, tail_fraction: float = 0.1) -> float:
    """Hill estimator of the Pareto tail index on the top ``tail_fraction``."""
    if values.size < 2:
        return 0.0
    k = max(2, int(np.ceil(values.size * tail_fraction)))
    sorted_values = np.sort(values)
    threshold = sorted_values[-k]
    if threshold <= 0.0:
        return 0.0
    top = sorted_values[-k + 1 :]
    log_ratios = np.log(top / threshold)
    mean_log = float(np.mean(log_ratios))
    if mean_log == 0.0:
        return 0.0
    return float(1.0 / mean_log)


def coefficient_of_variation(values: NDArray[np.float64]) -> float:
    """σ / μ — undefined when μ == 0 (returns 0.0)."""
    if values.size == 0:
        return 0.0
    mean = float(np.mean(values))
    if mean == 0.0:
        return 0.0
    return float(np.std(values, ddof=0) / mean)


def shannon_entropy(values: NDArray[np.float64]) -> float:
    """Shannon entropy of the population's normalised shares (nats)."""
    if values.size == 0:
        return 0.0
    total = float(values.sum())
    if total == 0.0:
        return 0.0
    shares = values / total
    nonzero = shares[shares > 0.0]
    return float(-np.sum(nonzero * np.log(nonzero)))


def convergence_half_life(
    trajectory: NDArray[np.float64],
    *,
    initial: float,
    final: float,
) -> float:
    """Step at which ``trajectory`` first crosses half-way between initial and final."""
    if trajectory.size == 0:
        return 0.0
    delta = final - initial
    if delta == 0.0:
        return 0.0
    target = initial + 0.5 * delta
    if delta > 0:
        crossings = np.where(trajectory >= target)[0]
    else:
        crossings = np.where(trajectory <= target)[0]
    if crossings.size == 0:
        return float(trajectory.size - 1)
    return float(crossings[0])


def _top_set_indices(values: NDArray[np.float64], *, fraction: float) -> set[int]:
    if values.size == 0:
        return set()
    k = max(1, int(np.ceil(values.size * fraction)))
    return {int(idx) for idx in np.argpartition(values, -k)[-k:]}


def top_pct_turnover_per_step(
    panel: NDArray[np.float64],
    *,
    fraction: float = 0.01,
) -> NDArray[np.float64]:
    """Per-step replacement rate of the top-``fraction`` set across the panel.

    Returns an array of shape ``(n_steps - 1,)``; entry ``t`` is the share
    of the top set at step ``t`` that is *not* in the top set at step
    ``t + 1``.
    """
    if panel.shape[0] < 2:
        return np.zeros(0, dtype=np.float64)
    rates = np.empty(panel.shape[0] - 1, dtype=np.float64)
    for step in range(panel.shape[0] - 1):
        previous = _top_set_indices(panel[step, :], fraction=fraction)
        following = _top_set_indices(panel[step + 1, :], fraction=fraction)
        denom = max(1, len(previous))
        rates[step] = (len(previous - following)) / denom
    return rates


def top_pct_turnover_rate(panel: NDArray[np.float64], *, fraction: float = 0.01) -> float:
    """Mean per-step turnover of the top-``fraction`` set."""
    rates = top_pct_turnover_per_step(panel, fraction=fraction)
    return float(rates.mean()) if rates.size > 0 else 0.0


def top_pct_persistence_rate(panel: NDArray[np.float64], *, fraction: float = 0.01) -> float:
    """``1 - top_pct_turnover_rate``."""
    return 1.0 - top_pct_turnover_rate(panel, fraction=fraction)


def top_pct_spells(
    panel: NDArray[np.float64],
    *,
    fraction: float = 0.01,
    run_index: int = 0,
) -> DataFrame[TopPctSpell]:
    """One row per contiguous spell of an agent inside the top-``fraction`` set."""
    rows: list[dict[str, int | bool]] = []
    n_steps, n_agents = panel.shape
    for agent in range(n_agents):
        in_top_top = np.zeros(n_steps, dtype=bool)
        for step in range(n_steps):
            in_top_top[step] = agent in _top_set_indices(panel[step, :], fraction=fraction)
        spell_id = 0
        step = 0
        while step < n_steps:
            if not in_top_top[step]:
                step += 1
                continue
            start = step
            while step < n_steps and in_top_top[step]:
                step += 1
            duration = step - start
            censored = step == n_steps
            rows.append(
                {
                    "run": int(run_index),
                    "agent": int(agent),
                    "spell": int(spell_id),
                    "duration": int(duration),
                    "censored": bool(censored),
                },
            )
            spell_id += 1
    frame = pd.DataFrame(
        rows,
        columns=["run", "agent", "spell", "duration", "censored"],
    )
    frame["run"] = frame["run"].astype("int64")
    frame["agent"] = frame["agent"].astype("int64")
    frame["spell"] = frame["spell"].astype("int64")
    frame["duration"] = frame["duration"].astype("int64")
    frame["censored"] = frame["censored"].astype("bool")
    return DataFrame[TopPctSpell](frame)


def mean_tenure_from_spells(spells: DataFrame[TopPctSpell]) -> KaplanMeierEstimate:
    """Restricted mean tenure across spells, with right-censoring."""
    if spells.shape[0] == 0:
        return KaplanMeierEstimate(
            mean_lifetime=0.0,
            median_lifetime=0.0,
            observed_events=0,
            censored_events=0,
        )
    durations = spells["duration"].to_numpy(dtype=np.float64)
    censored = spells["censored"].to_numpy(dtype=bool)
    event_observed = (~censored).astype(np.int_)
    return kaplan_meier_mean_lifetime(durations=durations, event_observed=event_observed)


def _agent_decile(panel: NDArray[np.float64]) -> NDArray[np.int_]:
    """Decile (1..10) of each agent at each step."""
    decile = np.empty(panel.shape, dtype=np.int_)
    for step in range(panel.shape[0]):
        ranks = np.argsort(np.argsort(panel[step, :]))
        decile[step, :] = np.minimum(10, (ranks * 10 // panel.shape[1]) + 1)
    return decile


def bottom_to_top_rise_count(
    panel: NDArray[np.float64],
    *,
    bottom_decile: int = 1,
    top_decile: int = 10,
) -> float:
    """Fraction of agents that move from ``bottom_decile`` to ``top_decile`` later in time."""
    if panel.shape[0] < 2 or panel.shape[1] == 0:
        return 0.0
    decile = _agent_decile(panel)
    risers = 0
    for agent in range(panel.shape[1]):
        bottom_steps = np.where(decile[:, agent] <= bottom_decile)[0]
        top_steps = np.where(decile[:, agent] >= top_decile)[0]
        if bottom_steps.size == 0 or top_steps.size == 0:
            continue
        first_bottom = int(bottom_steps[0])
        later_top = top_steps[top_steps > first_bottom]
        if later_top.size > 0:
            risers += 1
    return float(risers / panel.shape[1])


def median_time_to_rise(
    panel: NDArray[np.float64],
    *,
    bottom_decile: int = 1,
    top_decile: int = 10,
) -> float:
    """Median number of steps from first bottom-decile to first top-decile observation."""
    if panel.shape[0] < 2 or panel.shape[1] == 0:
        return 0.0
    decile = _agent_decile(panel)
    delays: list[int] = []
    for agent in range(panel.shape[1]):
        bottom_steps = np.where(decile[:, agent] <= bottom_decile)[0]
        top_steps = np.where(decile[:, agent] >= top_decile)[0]
        if bottom_steps.size == 0 or top_steps.size == 0:
            continue
        first_bottom = int(bottom_steps[0])
        later_top = top_steps[top_steps > first_bottom]
        if later_top.size > 0:
            delays.append(int(later_top[0] - first_bottom))
    if not delays:
        return 0.0
    return float(np.median(delays))


def lorenz_curve(values: NDArray[np.float64]) -> DataFrame[LorenzCurve]:
    """Lorenz curve points (population share, value share) including (0, 0)."""
    if values.size == 0:
        frame = pd.DataFrame({"population_share": [0.0], "value_share": [0.0]})
        return DataFrame[LorenzCurve](frame)
    sorted_values = np.sort(values)
    total = float(sorted_values.sum())
    n = sorted_values.size
    population_share = np.concatenate(([0.0], np.arange(1, n + 1, dtype=np.float64) / n))
    if total == 0.0:
        value_share = np.zeros_like(population_share)
    else:
        cumulative = np.concatenate(([0.0], np.cumsum(sorted_values, dtype=np.float64) / total))
        value_share = np.clip(cumulative, 0.0, 1.0)
    population_share = np.clip(population_share, 0.0, 1.0)
    frame = pd.DataFrame({"population_share": population_share, "value_share": value_share})
    return DataFrame[LorenzCurve](frame)


def decile_transition_matrix(panel: NDArray[np.float64]) -> DataFrame[DecileTransition]:
    """Long-form 10×10 transition matrix from the first to the last sampled step."""
    if panel.shape[0] < 2 or panel.shape[1] == 0:
        empty = pd.DataFrame(
            {
                "from_decile": np.repeat(np.arange(1, 11, dtype=np.int64), 10),
                "to_decile": np.tile(np.arange(1, 11, dtype=np.int64), 10),
                "probability": np.zeros(100, dtype=np.float64),
            },
        )
        return DataFrame[DecileTransition](empty)
    decile = _agent_decile(panel)
    initial = decile[0, :]
    final = decile[-1, :]
    counts = np.zeros((10, 10), dtype=np.float64)
    for start, end in zip(initial, final, strict=True):
        counts[start - 1, end - 1] += 1.0
    row_sums = counts.sum(axis=1, keepdims=True)
    safe_rows = np.where(row_sums > 0, row_sums, 1.0)
    probabilities = counts / safe_rows
    from_grid, to_grid = np.meshgrid(
        np.arange(1, 11, dtype=np.int64),
        np.arange(1, 11, dtype=np.int64),
        indexing="ij",
    )
    frame = pd.DataFrame(
        {
            "from_decile": from_grid.ravel(),
            "to_decile": to_grid.ravel(),
            "probability": probabilities.ravel(),
        },
    )
    return DataFrame[DecileTransition](frame)


__all__ = [
    "bottom_to_top_rise_count",
    "coefficient_of_variation",
    "convergence_half_life",
    "decile_transition_matrix",
    "gini",
    "hill_alpha",
    "lorenz_curve",
    "mean_tenure_from_spells",
    "median_time_to_rise",
    "shannon_entropy",
    "top_pct_persistence_rate",
    "top_pct_spells",
    "top_pct_turnover_per_step",
    "top_pct_turnover_rate",
    "top_share",
]
