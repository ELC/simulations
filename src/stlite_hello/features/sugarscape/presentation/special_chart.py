"""Spatial wealth heatmap special chart for the Sugarscape model."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from ..model import AdvancedParams, final_snapshot

_DEFAULT_HEIGHT = 360


class SpatialCellData(pa.DataFrameModel):
    """One row per grid cell describing remaining sugar."""

    row: int = pa.Field(ge=0)
    col: int = pa.Field(ge=0)
    sugar: float = pa.Field(ge=0.0)


class AgentLocationData(pa.DataFrameModel):
    """One row per agent: location and accumulated wealth."""

    row: int = pa.Field(ge=0)
    col: int = pa.Field(ge=0)
    wealth: float = pa.Field(ge=0.0)


class SpatialHeading(BaseModel):
    """Title and axis labels for the spatial-wealth heatmap."""

    model_config = ConfigDict(frozen=True)

    title: str
    row_label: str
    col_label: str
    sugar_label: str
    agent_label: str


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: SpatialHeading


def build_spatial_frames(
    *,
    params: AdvancedParams,
    seed: int,
) -> tuple[DataFrame[SpatialCellData], DataFrame[AgentLocationData]]:
    """Replay one replicate and project sugar grid + agent locations to dataframes.

    Returns
    -------
    tuple[DataFrame[SpatialCellData], DataFrame[AgentLocationData]]
        First entry holds the sugar grid; second holds per-agent positions.
    """
    parent = np.random.SeedSequence(seed)
    rng = np.random.default_rng(parent.spawn(1)[0])
    snapshot = final_snapshot(params, rng)
    coords = np.arange(params.grid_size, dtype=np.int64)
    rr, cc = np.meshgrid(coords, coords, indexing="ij")
    cell_frame = pd.DataFrame(
        {
            "row": rr.ravel().astype(np.int64),
            "col": cc.ravel().astype(np.int64),
            "sugar": snapshot.sugar_grid.ravel().astype(np.float64),
        },
    )
    agent_frame = pd.DataFrame(
        {
            "row": snapshot.agent_rows.astype(np.int64),
            "col": snapshot.agent_cols.astype(np.int64),
            "wealth": snapshot.agent_wealth.astype(np.float64),
        },
    )
    return (
        DataFrame[SpatialCellData](cell_frame),
        DataFrame[AgentLocationData](agent_frame),
    )


def build_spatial_chart(
    *,
    cells: DataFrame[SpatialCellData],
    agents: DataFrame[AgentLocationData],
    heading: SpatialHeading,
) -> alt.TopLevelMixin:
    """Layer the sugar heatmap with per-agent wealth bubbles.

    Returns
    -------
    alt.TopLevelMixin
        Layered Altair chart ready to render.
    """
    heatmap = (
        alt
        .Chart(cells)
        .mark_rect()
        .encode(
            x=alt.X("col:O", title=heading.col_label),
            y=alt.Y("row:O", title=heading.row_label),
            color=alt.Color(
                "sugar:Q",
                title=heading.sugar_label,
                scale=alt.Scale(scheme="yelloworangebrown"),
            ),
            tooltip=["row", "col", "sugar"],
        )
    )
    bubbles = (
        alt
        .Chart(agents)
        .mark_circle(stroke="white", strokeWidth=0.5)
        .encode(
            x=alt.X("col:O"),
            y=alt.Y("row:O"),
            size=alt.Size("wealth:Q", title=heading.agent_label),
            color=alt.value("#1f77b4"),
            tooltip=["row", "col", "wealth"],
        )
    )
    return alt.layer(heatmap, bubbles).properties(title=heading.title, height=_DEFAULT_HEIGHT)


def render_special_chart(inputs: SpecialChartInputs) -> None:
    cells, agents = build_spatial_frames(params=inputs.params, seed=inputs.seed)
    chart = build_spatial_chart(cells=cells, agents=agents, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "AgentLocationData",
    "SpatialCellData",
    "SpatialHeading",
    "SpecialChartInputs",
    "build_spatial_chart",
    "build_spatial_frames",
    "render_special_chart",
]
