import altair as alt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .model import AdvancedParams
from .schemas import BestResponseLinesData, BestResponseTrajectoryData
from .simulation import costs_for_seed, quantity_trajectory

_DEFAULT_HEIGHT = 360


class BestResponseHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    line_legend_label: str


def _select_firms(costs: NDArray[np.float64]) -> tuple[int, int]:
    order = np.argsort(costs)
    return int(order[0]), int(order[-1])


def _best_response_endpoints(
    *,
    cost: float,
    intercept: float,
    slope: float,
    max_q: float,
) -> tuple[float, float]:
    at_zero = max(0.0, (intercept - cost) / (2.0 * slope))
    at_max = max(0.0, (intercept - cost - slope * max_q) / (2.0 * slope))
    return at_zero, at_max


def build_trajectory_data(
    *,
    params: AdvancedParams,
    seed: int,
) -> tuple[DataFrame[BestResponseTrajectoryData], DataFrame[BestResponseLinesData]]:
    first_child = np.random.SeedSequence(seed).spawn(1)[0]
    trajectory = quantity_trajectory(params, np.random.default_rng(first_child))
    costs = costs_for_seed(params, np.random.default_rng(first_child))
    firm_a, firm_b = _select_firms(costs)
    trace = pd.DataFrame(
        {
            "step": np.arange(trajectory.shape[0], dtype=np.int64),
            "q1": trajectory[:, firm_a].astype(np.float64),
            "q2": trajectory[:, firm_b].astype(np.float64),
        },
    )
    max_q = float(max(trajectory.max(), params.intercept / params.slope))
    a_zero, a_max = _best_response_endpoints(
        cost=float(costs[firm_a]),
        intercept=params.intercept,
        slope=params.slope,
        max_q=max_q,
    )
    b_zero, b_max = _best_response_endpoints(
        cost=float(costs[firm_b]),
        intercept=params.intercept,
        slope=params.slope,
        max_q=max_q,
    )
    lines = pd.DataFrame(
        {
            "firm": ["Firm A", "Firm A", "Firm B", "Firm B"],
            "q_self": [a_zero, a_max, b_zero, b_max],
            "q_other": [0.0, max_q, 0.0, max_q],
        },
    )
    return DataFrame[BestResponseTrajectoryData](trace), DataFrame[BestResponseLinesData](lines)


def build_best_response_chart(
    *,
    trajectory: DataFrame[BestResponseTrajectoryData],
    lines: DataFrame[BestResponseLinesData],
    heading: BestResponseHeading,
) -> alt.TopLevelMixin:
    trace = (
        alt
        .Chart(trajectory)
        .mark_line(point=True, opacity=0.7)
        .encode(
            x=alt.X("q1:Q", title=heading.x_label),
            y=alt.Y("q2:Q", title=heading.y_label),
            order=alt.Order("step:Q"),
            color=alt.Color("step:Q", scale=alt.Scale(scheme="viridis")),
            tooltip=["step", "q1", "q2"],
        )
    )
    best_lines_a = (
        alt
        .Chart(lines[lines["firm"] == "Firm A"])
        .mark_line(color="#d62728")
        .encode(
            x=alt.X("q_self:Q"),
            y=alt.Y("q_other:Q"),
        )
    )
    best_lines_b = (
        alt
        .Chart(lines[lines["firm"] == "Firm B"])
        .mark_line(color="#2ca02c")
        .encode(
            x=alt.X("q_other:Q"),
            y=alt.Y("q_self:Q", title=heading.line_legend_label),
        )
    )
    return alt.layer(best_lines_a, best_lines_b, trace).properties(
        title=heading.title,
        height=_DEFAULT_HEIGHT,
    )
