import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .model import AdvancedParams
from .schemas import AgentLocationData, SpatialCellData
from .simulation import final_snapshot

_DEFAULT_HEIGHT = 360


class SpatialHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    row_label: str
    col_label: str
    sugar_label: str
    agent_label: str


def build_spatial_frames(
    *,
    params: AdvancedParams,
    seed: int,
) -> tuple[DataFrame[SpatialCellData], DataFrame[AgentLocationData]]:
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
