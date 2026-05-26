"""Run a simulation N times with independent seeds and pack the result.

A simulation is any callable ``simulate_once(params, rng) -> ReplicateResult``.
The aggregator spawns ``runs`` independent child seeds from
``np.random.SeedSequence(seed)`` so every replicate is fully reproducible
and uncorrelated with the others.
"""

from collections.abc import Callable
from typing import Any

import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .config import AggregationConfig
from .schemas import FinalPopulation, FocalPanel

_EXPECTED_PANEL_DIMS = 2


class ReplicateResult(BaseModel):
    """Output of one replicate.

    ``focal_panel`` has shape ``(n_steps, n_agents)`` -- agents that drop out
    in the middle of the run still get a value in every step (typically
    ``0`` once they exit), so the matrix is dense and reasoning over time
    is straightforward.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    focal_panel: NDArray[np.float64]
    step_index: NDArray[np.int_]


type ParamsProtocol = BaseModel
"""Alias for simulation parameter models (any frozen Pydantic BaseModel)."""


SimulateOnce = Callable[[Any, np.random.Generator], ReplicateResult]
"""A simulation callable: ``simulate_once(params, rng) -> ReplicateResult``.

``params`` is typed ``Any`` so each feature can pass its own frozen
``BaseModel`` subclass without a contravariance error; the runtime
contract is enforced by the per-feature signature on ``simulate_once``.
"""


class RunBundle(BaseModel):
    """All N replicate outputs, packed for downstream consumption.

    Holds both the per-replicate numpy panels (cheap to compute on) and the
    long-form Pandera-validated DataFrames (used by exports and a few
    feature-specific charts). The numpy view exists so ``summarize`` does
    not pay the cost of re-pivoting millions of rows back out of the
    DataFrame on every run.
    """

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    final_population: DataFrame[FinalPopulation]
    focal_panel: DataFrame[FocalPanel]
    panels: tuple[NDArray[np.float64], ...]
    step_indices: tuple[NDArray[np.int_], ...]


def _build_final_population(panels: list[NDArray[np.float64]]) -> DataFrame[FinalPopulation]:
    rows: list[dict[str, int | float]] = []
    for run_index, panel in enumerate(panels):
        last = panel[-1, :]
        for agent_index, value in enumerate(last):
            rows.append({"run": run_index, "agent": agent_index, "value": float(value)})
    frame = pd.DataFrame(rows, columns=["run", "agent", "value"])
    frame["run"] = frame["run"].astype("int64")
    frame["agent"] = frame["agent"].astype("int64")
    frame["value"] = frame["value"].astype("float64")
    return DataFrame[FinalPopulation](frame)


def _build_focal_panel(
    panels: list[NDArray[np.float64]],
    step_indices: list[NDArray[np.int_]],
) -> DataFrame[FocalPanel]:
    n_agents = panels[0].shape[1]
    agent_template = np.arange(n_agents, dtype=np.int64)
    runs: list[NDArray[np.int64]] = []
    steps_out: list[NDArray[np.int64]] = []
    agents_out: list[NDArray[np.int64]] = []
    values_out: list[NDArray[np.float64]] = []
    for run_index, (panel, steps) in enumerate(zip(panels, step_indices, strict=True)):
        n_steps = panel.shape[0]
        runs.append(np.full(panel.size, run_index, dtype=np.int64))
        steps_out.append(np.repeat(steps.astype(np.int64), n_agents))
        agents_out.append(np.tile(agent_template, n_steps))
        values_out.append(panel.astype(np.float64, copy=False).ravel())
    frame = pd.DataFrame(
        {
            "run": np.concatenate(runs),
            "step": np.concatenate(steps_out),
            "agent": np.concatenate(agents_out),
            "value": np.concatenate(values_out),
        },
    )
    return DataFrame[FocalPanel](frame)


def run_replicates(
    *,
    simulate_once: SimulateOnce,
    params: ParamsProtocol,
    config: AggregationConfig,
) -> RunBundle:
    """Run ``config.runs`` independent replicates with seeded RNGs.

    Returns
    -------
    RunBundle
        Bundle carrying the final population and the focal-quantity panel
        across every replicate, validated through Pandera schemas.
    """
    parent = np.random.SeedSequence(config.seed)
    child_seeds = parent.spawn(config.runs)
    panels: list[NDArray[np.float64]] = []
    step_indices: list[NDArray[np.int_]] = []
    for seed_seq in child_seeds:
        rng = np.random.default_rng(seed_seq)
        result = simulate_once(params, rng)
        if result.focal_panel.ndim != _EXPECTED_PANEL_DIMS:
            msg = "ReplicateResult.focal_panel must be 2-D (steps, agents)"
            raise ValueError(msg)
        if result.focal_panel.shape[0] != result.step_index.size:
            msg = "ReplicateResult.focal_panel rows must match step_index length"
            raise ValueError(msg)
        panels.append(result.focal_panel)
        step_indices.append(result.step_index)

    n_agents = {panel.shape[1] for panel in panels}
    if len(n_agents) > 1:
        msg = "All replicates must have the same number of agents"
        raise ValueError(msg)
    return RunBundle(
        final_population=_build_final_population(panels),
        focal_panel=_build_focal_panel(panels, step_indices),
        panels=tuple(panels),
        step_indices=tuple(step_indices),
    )


__all__ = [
    "ParamsProtocol",
    "ReplicateResult",
    "RunBundle",
    "SimulateOnce",
    "run_replicates",
]
