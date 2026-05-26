"""Sugarscape spatial harvest-and-metabolism model."""

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

SUGARSCAPE_DEFAULT_SEED = 1_000_047
SUGARSCAPE_FEATURE = "sugarscape"
SUGARSCAPE_DEFAULT_GRID = 20
SUGARSCAPE_DEFAULT_AGENTS = 100
SUGARSCAPE_DEFAULT_STEPS = 80
SUGARSCAPE_DEFAULT_VISION = 4
SUGARSCAPE_DEFAULT_METABOLISM = 1.0
SUGARSCAPE_DEFAULT_REGROWTH = 1.0
SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT = 5.0


class SimpleParams(BaseModel):
    """Three knobs: agents, vision and steps. Grid size stays fixed."""

    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=SUGARSCAPE_DEFAULT_AGENTS, ge=4, le=400)
    n_steps: int = Field(default=SUGARSCAPE_DEFAULT_STEPS, ge=5, le=500)
    vision: int = Field(default=SUGARSCAPE_DEFAULT_VISION, ge=1, le=10)


class AdvancedParams(SimpleParams):
    """Adds the grid edge, sugar regrowth, metabolism and endowment."""

    grid_size: int = Field(default=SUGARSCAPE_DEFAULT_GRID, ge=5, le=60)
    regrowth_rate: float = Field(default=SUGARSCAPE_DEFAULT_REGROWTH, gt=0.0)
    metabolism_mean: float = Field(default=SUGARSCAPE_DEFAULT_METABOLISM, gt=0.0)
    initial_endowment: float = Field(default=SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT, ge=0.0)


class SugarscapeConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=SUGARSCAPE_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


class SpatialSnapshot(BaseModel):
    """Final state of one replicate for the spatial heatmap."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    sugar_grid: NDArray[np.float64]
    agent_rows: NDArray[np.int_]
    agent_cols: NDArray[np.int_]
    agent_wealth: NDArray[np.float64]


class _ReplicateState(BaseModel):
    """Mutable replicate state bundled to keep helper arities small."""

    model_config = ConfigDict(arbitrary_types_allowed=True)

    sugar: NDArray[np.float64]
    capacity: NDArray[np.float64]
    rows: NDArray[np.int_]
    cols: NDArray[np.int_]
    wealth: NDArray[np.float64]
    metabolism: NDArray[np.float64]


class _LookupContext(BaseModel):
    """Read-only neighbourhood lookup context for a single agent move."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    sugar: NDArray[np.float64]
    occupied: NDArray[np.bool_]
    grid_size: int
    vision: int


def _build_capacity(grid_size: int) -> NDArray[np.float64]:
    coords = np.arange(grid_size, dtype=np.float64)
    rr, cc = np.meshgrid(coords, coords, indexing="ij")
    center = (grid_size - 1) / 2.0
    distance = np.sqrt((rr - center) ** 2 + (cc - center) ** 2)
    radius = center if center > 0.0 else 1.0
    return np.maximum(4.0 * (1.0 - distance / radius), 0.0) + 1.0


def _place_agents(
    *,
    n_agents: int,
    grid_size: int,
    rng: np.random.Generator,
) -> tuple[NDArray[np.int_], NDArray[np.int_]]:
    total_cells = grid_size * grid_size
    if n_agents > total_cells:
        msg = "More agents than cells; pick a larger grid or fewer agents."
        raise ValueError(msg)
    cells = rng.choice(total_cells, size=n_agents, replace=False)
    rows = (cells // grid_size).astype(np.int_)
    cols = (cells % grid_size).astype(np.int_)
    return rows, cols


def _draw_metabolism(
    *,
    n_agents: int,
    metabolism_mean: float,
    rng: np.random.Generator,
) -> NDArray[np.float64]:
    return rng.uniform(0.5 * metabolism_mean, 1.5 * metabolism_mean, size=n_agents)


def _best_visible_cell(*, row: int, col: int, context: _LookupContext) -> tuple[int, int]:
    sugar = context.sugar
    best_value = sugar[row, col]
    best_row, best_col = row, col
    for delta in range(-context.vision, context.vision + 1):
        if delta == 0:
            continue
        candidate_row = (row + delta) % context.grid_size
        if not context.occupied[candidate_row, col] and sugar[candidate_row, col] > best_value:
            best_value = sugar[candidate_row, col]
            best_row, best_col = candidate_row, col
        candidate_col = (col + delta) % context.grid_size
        if not context.occupied[row, candidate_col] and sugar[row, candidate_col] > best_value:
            best_value = sugar[row, candidate_col]
            best_row, best_col = row, candidate_col
    return best_row, best_col


def _sugarscape_step(
    *,
    state: _ReplicateState,
    params: AdvancedParams,
    rng: np.random.Generator,
) -> None:
    occupied = np.zeros_like(state.sugar, dtype=np.bool_)
    occupied[state.rows, state.cols] = True
    order = rng.permutation(state.rows.size)
    for agent in order:
        r0, c0 = int(state.rows[agent]), int(state.cols[agent])
        occupied[r0, c0] = False
        new_row, new_col = _best_visible_cell(
            row=r0,
            col=c0,
            context=_LookupContext(
                sugar=state.sugar,
                occupied=occupied,
                grid_size=params.grid_size,
                vision=params.vision,
            ),
        )
        state.rows[agent] = new_row
        state.cols[agent] = new_col
        occupied[new_row, new_col] = True
        state.wealth[agent] += state.sugar[new_row, new_col]
        state.sugar[new_row, new_col] = 0.0
    state.wealth -= state.metabolism
    np.maximum(state.wealth, 0.0, out=state.wealth)
    np.minimum(state.sugar + params.regrowth_rate, state.capacity, out=state.sugar)


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """One Sugarscape replicate; focal quantity is per-agent wealth at each step.

    Returns
    -------
    ReplicateResult
        Wealth panel of shape ``(n_steps + 1, n_agents)``.
    """
    snapshot = _run_replicate(params, rng)
    return ReplicateResult(focal_panel=snapshot[0], step_index=snapshot[1])


def final_snapshot(params: AdvancedParams, rng: np.random.Generator) -> SpatialSnapshot:
    """Replay one replicate and capture grid + per-agent positions at the end.

    Returns
    -------
    SpatialSnapshot
        The final sugar grid plus the location and wealth of every agent.
    """
    return _run_replicate_snapshot(params, rng)


def _initial_state(params: AdvancedParams, rng: np.random.Generator) -> _ReplicateState:
    capacity = _build_capacity(params.grid_size)
    rows, cols = _place_agents(n_agents=params.n_agents, grid_size=params.grid_size, rng=rng)
    metabolism = _draw_metabolism(
        n_agents=params.n_agents,
        metabolism_mean=params.metabolism_mean,
        rng=rng,
    )
    return _ReplicateState(
        sugar=capacity.copy(),
        capacity=capacity,
        rows=rows,
        cols=cols,
        wealth=np.full(params.n_agents, params.initial_endowment, dtype=np.float64),
        metabolism=metabolism,
    )


def _run_replicate(
    params: AdvancedParams,
    rng: np.random.Generator,
) -> tuple[NDArray[np.float64], NDArray[np.int_]]:
    state = _initial_state(params, rng)
    panel = np.empty((params.n_steps + 1, params.n_agents), dtype=np.float64)
    panel[0] = state.wealth
    for step in range(1, params.n_steps + 1):
        _sugarscape_step(state=state, params=params, rng=rng)
        panel[step] = state.wealth
    return panel, np.arange(params.n_steps + 1, dtype=np.int_)


def _run_replicate_snapshot(
    params: AdvancedParams,
    rng: np.random.Generator,
) -> SpatialSnapshot:
    state = _initial_state(params, rng)
    for _ in range(1, params.n_steps + 1):
        _sugarscape_step(state=state, params=params, rng=rng)
    return SpatialSnapshot(
        sugar_grid=state.sugar,
        agent_rows=state.rows,
        agent_cols=state.cols,
        agent_wealth=state.wealth,
    )


__all__ = [
    "SUGARSCAPE_DEFAULT_AGENTS",
    "SUGARSCAPE_DEFAULT_GRID",
    "SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT",
    "SUGARSCAPE_DEFAULT_METABOLISM",
    "SUGARSCAPE_DEFAULT_REGROWTH",
    "SUGARSCAPE_DEFAULT_SEED",
    "SUGARSCAPE_DEFAULT_STEPS",
    "SUGARSCAPE_DEFAULT_VISION",
    "SUGARSCAPE_FEATURE",
    "AdvancedParams",
    "SimpleParams",
    "SpatialSnapshot",
    "SugarscapeConfig",
    "final_snapshot",
    "simulate_once",
]
