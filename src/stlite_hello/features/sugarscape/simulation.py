from dataclasses import dataclass

import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams, SpatialSnapshot


@dataclass(slots=True)
class _ReplicateState:
    """Mutable replicate state bundled to keep helper arities small."""

    sugar: NDArray[np.float64]
    capacity: NDArray[np.float64]
    rows: NDArray[np.int_]
    cols: NDArray[np.int_]
    wealth: NDArray[np.float64]
    metabolism: NDArray[np.float64]


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


def _best_visible_cell(  # noqa: PLR0913, PLR0917 - hot loop, positional args avoid Pydantic overhead
    row: int,
    col: int,
    sugar: NDArray[np.float64],
    occupied: NDArray[np.bool_],
    deltas: NDArray[np.int_],
    grid_size: int,
) -> tuple[int, int]:
    rr = (row + deltas) % grid_size
    cc = (col + deltas) % grid_size
    row_values = np.where(occupied[rr, col], -np.inf, sugar[rr, col])
    col_values = np.where(occupied[row, cc], -np.inf, sugar[row, cc])
    self_value = sugar[row, col]
    row_max = float(row_values.max())
    col_max = float(col_values.max())
    if max(row_max, col_max) <= self_value:
        return row, col
    if row_max >= col_max:
        idx = int(np.argmax(row_values))
        return int(rr[idx]), col
    idx = int(np.argmax(col_values))
    return row, int(cc[idx])


def _move_agent(
    agent: int,
    state: _ReplicateState,
    occupied: NDArray[np.bool_],
    deltas: NDArray[np.int_],
    grid_size: int,
) -> None:
    r0, c0 = int(state.rows[agent]), int(state.cols[agent])
    occupied[r0, c0] = False
    new_row, new_col = _best_visible_cell(r0, c0, state.sugar, occupied, deltas, grid_size)
    state.rows[agent] = new_row
    state.cols[agent] = new_col
    occupied[new_row, new_col] = True
    state.wealth[agent] += state.sugar[new_row, new_col]
    state.sugar[new_row, new_col] = 0.0


def _sugarscape_step(
    *,
    state: _ReplicateState,
    params: AdvancedParams,
    rng: np.random.Generator,
) -> None:
    occupied = np.zeros_like(state.sugar, dtype=np.bool_)
    occupied[state.rows, state.cols] = True
    deltas = np.array(
        [d for d in range(-params.vision, params.vision + 1) if d != 0],
        dtype=np.int_,
    )
    for agent in rng.permutation(state.rows.size):
        _move_agent(int(agent), state, occupied, deltas, params.grid_size)
    state.wealth -= state.metabolism
    np.maximum(state.wealth, 0.0, out=state.wealth)
    np.minimum(state.sugar + params.regrowth_rate, state.capacity, out=state.sugar)


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


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    snapshot = _run_replicate(params, rng)
    return ReplicateResult(focal_panel=snapshot[0], step_index=snapshot[1])


def final_snapshot(params: AdvancedParams, rng: np.random.Generator) -> SpatialSnapshot:
    return _run_replicate_snapshot(params, rng)
