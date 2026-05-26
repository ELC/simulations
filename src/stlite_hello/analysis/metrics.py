"""Cross-model concentration and mobility metrics.

All functions operate on numpy arrays so they can be wrapped with
``scipy.stats.bootstrap`` for CIs. Public helpers (``lorenz_curve``,
``decile_transition_matrix``, ``top_pct_spells``) return Pandera-validated
dataframes so the rest of the analysis layer never touches raw pandas.
"""

from typing import cast

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame

from .adapters import KaplanMeierEstimate, kaplan_meier_mean_lifetime
from .schemas import DecileTransition, LorenzCurve, TopPctSpell

_DEFAULT_TAIL_FRACTION = 0.1
_DEFAULT_TOP_FRACTION = 0.01
_DEFAULT_BOTTOM_DECILE = 1
_DEFAULT_TOP_DECILE = 10
_NUM_DECILES = 10
_MINIMUM_SAMPLES_FOR_HILL = 2
_MINIMUM_STEPS_FOR_MOBILITY = 2


def gini(values: NDArray[np.float64]) -> float:
    if values.size == 0:
        return 0.0
    if np.any(values < 0):
        msg = "gini requires non-negative values"
        raise ValueError(msg)
    sorted_values = np.sort(values)
    n = sorted_values.size
    total = float(sorted_values.sum())
    if not total:
        return 0.0
    cumulative = np.cumsum(sorted_values, dtype=np.float64)
    return float((n + 1 - 2 * np.sum(cumulative) / total) / n)


def top_share(values: NDArray[np.float64], *, fraction: float) -> float:
    if values.size == 0:
        return 0.0
    if not 0.0 < fraction <= 1.0:
        msg = "fraction must be in (0, 1]"
        raise ValueError(msg)
    total = float(values.sum())
    if not total:
        return 0.0
    k = max(1, int(np.ceil(values.size * fraction)))
    top = np.partition(values, -k)[-k:]
    return float(top.sum() / total)


def hill_alpha(values: NDArray[np.float64], *, tail_fraction: float = _DEFAULT_TAIL_FRACTION) -> float:
    if values.size < _MINIMUM_SAMPLES_FOR_HILL:
        return 0.0
    k = max(_MINIMUM_SAMPLES_FOR_HILL, int(np.ceil(values.size * tail_fraction)))
    sorted_values = np.sort(values)
    threshold = sorted_values[-k]
    if threshold <= 0.0:
        return 0.0
    top = sorted_values[-k + 1 :]
    log_ratios = np.log(top / threshold)
    mean_log = float(np.mean(log_ratios))
    if not mean_log:
        return 0.0
    return float(1.0 / mean_log)


def coefficient_of_variation(values: NDArray[np.float64]) -> float:
    if values.size == 0:
        return 0.0
    mean = float(np.mean(values))
    if not mean:
        return 0.0
    return float(np.std(values, ddof=0) / mean)


def shannon_entropy(values: NDArray[np.float64]) -> float:
    if values.size == 0:
        return 0.0
    total = float(values.sum())
    if not total:
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
    if trajectory.size == 0:
        return 0.0
    delta = final - initial
    if not delta:
        return 0.0
    target = initial + 0.5 * delta
    crossings = np.where(trajectory >= target)[0] if delta > 0 else np.where(trajectory <= target)[0]
    if crossings.size == 0:
        return float(trajectory.size - 1)
    return float(crossings[0])


def _in_top_matrix(panel: NDArray[np.float64], *, fraction: float) -> NDArray[np.bool_]:
    """Boolean ``(n_steps, n_agents)`` mask marking each agent's top-fraction membership.

    Returns
    -------
    NDArray[np.bool_]
        ``True`` at ``(step, agent)`` iff that agent sits in the top
        ``fraction`` of the population at that step.
    """
    n_steps, n_agents = panel.shape
    in_top = np.zeros(panel.shape, dtype=bool)
    k = max(1, int(np.ceil(n_agents * fraction)))
    for step in range(n_steps):
        idx = np.argpartition(panel[step, :], -k)[-k:]
        in_top[step, idx] = True
    return in_top


def top_pct_turnover_per_step(
    panel: NDArray[np.float64],
    *,
    fraction: float = _DEFAULT_TOP_FRACTION,
) -> NDArray[np.float64]:
    if panel.shape[0] < _MINIMUM_STEPS_FOR_MOBILITY:
        return np.zeros(0, dtype=np.float64)
    if panel.shape[1] == 0:
        return np.zeros(panel.shape[0] - 1, dtype=np.float64)
    in_top = _in_top_matrix(panel, fraction=fraction)
    overlap = np.logical_and(in_top[:-1, :], in_top[1:, :]).sum(axis=1).astype(np.float64)
    denom = float(max(1, in_top[0, :].sum()))
    rates = 1.0 - overlap / denom
    return cast("NDArray[np.float64]", rates)


def top_pct_turnover_rate(panel: NDArray[np.float64], *, fraction: float = _DEFAULT_TOP_FRACTION) -> float:
    rates = top_pct_turnover_per_step(panel, fraction=fraction)
    return float(rates.mean()) if rates.size > 0 else 0.0


def top_pct_persistence_rate(panel: NDArray[np.float64], *, fraction: float = _DEFAULT_TOP_FRACTION) -> float:
    return 1.0 - top_pct_turnover_rate(panel, fraction=fraction)


def _spell_rows(
    panel: NDArray[np.float64],
    *,
    fraction: float,
    run_index: int,
) -> list[dict[str, int | bool]]:
    n_steps, n_agents = panel.shape
    if n_steps == 0 or n_agents == 0:
        return []
    in_top = _in_top_matrix(panel, fraction=fraction)
    padded = np.pad(in_top.astype(np.int8), pad_width=((1, 1), (0, 0)))
    edges = np.diff(padded, axis=0)
    rows: list[dict[str, int | bool]] = []
    for agent in range(n_agents):
        starts = np.where(edges[:, agent] == 1)[0]
        ends = np.where(edges[:, agent] == -1)[0]
        for spell_id, (start, end) in enumerate(zip(starts, ends, strict=True)):
            rows.append(
                {
                    "run": int(run_index),
                    "agent": int(agent),
                    "spell": int(spell_id),
                    "duration": int(end - start),
                    "censored": bool(end == n_steps),
                },
            )
    return rows


def top_pct_spells(
    panel: NDArray[np.float64],
    *,
    fraction: float = _DEFAULT_TOP_FRACTION,
    run_index: int = 0,
) -> DataFrame[TopPctSpell]:
    rows = _spell_rows(panel, fraction=fraction, run_index=run_index)
    frame = pd.DataFrame(rows, columns=["run", "agent", "spell", "duration", "censored"])
    frame["run"] = frame["run"].astype("int64")
    frame["agent"] = frame["agent"].astype("int64")
    frame["spell"] = frame["spell"].astype("int64")
    frame["duration"] = frame["duration"].astype("int64")
    frame["censored"] = frame["censored"].astype("bool")
    return DataFrame[TopPctSpell](frame)


def mean_tenure_from_spells(spells: DataFrame[TopPctSpell]) -> KaplanMeierEstimate:
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
    order = np.argsort(panel, axis=1, kind="stable")
    ranks = np.argsort(order, axis=1, kind="stable")
    return np.minimum(_NUM_DECILES, (ranks * _NUM_DECILES // panel.shape[1]) + 1).astype(np.int_)


def bottom_to_top_rise_count(
    panel: NDArray[np.float64],
    *,
    bottom_decile: int = _DEFAULT_BOTTOM_DECILE,
    top_decile: int = _DEFAULT_TOP_DECILE,
) -> float:
    if panel.shape[0] < _MINIMUM_STEPS_FOR_MOBILITY or panel.shape[1] == 0:
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
    bottom_decile: int = _DEFAULT_BOTTOM_DECILE,
    top_decile: int = _DEFAULT_TOP_DECILE,
) -> float:
    if panel.shape[0] < _MINIMUM_STEPS_FOR_MOBILITY or panel.shape[1] == 0:
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
    if values.size == 0:
        frame = pd.DataFrame({"population_share": [0.0], "value_share": [0.0]})
        return DataFrame[LorenzCurve](frame)
    sorted_values = np.sort(values)
    total = float(sorted_values.sum())
    n = sorted_values.size
    population_share = np.concatenate(([0.0], np.arange(1, n + 1, dtype=np.float64) / n))
    if not total:
        value_share = np.zeros_like(population_share)
    else:
        cumulative = np.concatenate(([0.0], np.cumsum(sorted_values, dtype=np.float64) / total))
        value_share = np.clip(cumulative, 0.0, 1.0)
    population_share = np.clip(population_share, 0.0, 1.0)
    frame = pd.DataFrame({"population_share": population_share, "value_share": value_share})
    return DataFrame[LorenzCurve](frame)


def _empty_transition_frame() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "from_decile": np.repeat(np.arange(1, _NUM_DECILES + 1, dtype=np.int64), _NUM_DECILES),
            "to_decile": np.tile(np.arange(1, _NUM_DECILES + 1, dtype=np.int64), _NUM_DECILES),
            "probability": np.zeros(_NUM_DECILES * _NUM_DECILES, dtype=np.float64),
        },
    )


def decile_transition_matrix(panel: NDArray[np.float64]) -> DataFrame[DecileTransition]:
    if panel.shape[0] < _MINIMUM_STEPS_FOR_MOBILITY or panel.shape[1] == 0:
        return DataFrame[DecileTransition](_empty_transition_frame())
    decile = _agent_decile(panel)
    initial = decile[0, :]
    final = decile[-1, :]
    counts = np.zeros((_NUM_DECILES, _NUM_DECILES), dtype=np.float64)
    for start, end in zip(initial, final, strict=True):
        counts[start - 1, end - 1] += 1.0
    row_sums = counts.sum(axis=1, keepdims=True)
    safe_rows = np.where(row_sums > 0, row_sums, 1.0)
    probabilities = counts / safe_rows
    from_grid, to_grid = np.meshgrid(
        np.arange(1, _NUM_DECILES + 1, dtype=np.int64),
        np.arange(1, _NUM_DECILES + 1, dtype=np.int64),
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
