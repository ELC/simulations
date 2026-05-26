"""Zipf log-log degree-rank special chart for preferential attachment."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.preferential_attachment.model import AdvancedParams, final_graph

_DEFAULT_HEIGHT = 360


class ZipfData(pa.DataFrameModel):
    """One row per node with its rank (1-indexed) and final degree."""

    rank: int = pa.Field(ge=1)
    degree: float = pa.Field(ge=0.0)


class ZipfHeading(BaseModel):
    """Title and axis labels for the Zipf log-log chart."""

    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: ZipfHeading


def build_zipf_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> DataFrame[ZipfData]:
    """Replay one replicate, sort nodes by degree, return rank-degree pairs.

    Returns
    -------
    DataFrame[ZipfData]
        Sorted degrees with rank 1 assigned to the highest-degree node.
    """
    rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    graph = final_graph(params, rng)
    degrees = np.array(sorted((deg for _, deg in graph.degree()), reverse=True), dtype=np.float64)
    frame = pd.DataFrame(
        {
            "rank": np.arange(1, degrees.size + 1, dtype=np.int64),
            "degree": degrees,
        },
    )
    return DataFrame[ZipfData](frame)


def build_zipf_chart(
    *,
    data: DataFrame[ZipfData],
    heading: ZipfHeading,
) -> alt.TopLevelMixin:
    """Log-log scatter showing the heavy-tailed degree distribution.

    Returns
    -------
    alt.TopLevelMixin
        The composed chart.
    """
    base = (
        alt
        .Chart(data)
        .mark_circle(size=40, opacity=0.7)
        .encode(
            x=alt.X("rank:Q", title=heading.x_label, scale=alt.Scale(type="log")),
            y=alt.Y("degree:Q", title=heading.y_label, scale=alt.Scale(type="log")),
            tooltip=["rank", "degree"],
        )
    )
    return cast(
        "alt.TopLevelMixin",
        base.properties(title=heading.title, height=_DEFAULT_HEIGHT),
    )


def render_special_chart(inputs: SpecialChartInputs) -> None:
    data = build_zipf_frame(params=inputs.params, seed=inputs.seed)
    chart = build_zipf_chart(data=data, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "SpecialChartInputs",
    "ZipfData",
    "ZipfHeading",
    "build_zipf_chart",
    "build_zipf_frame",
    "render_special_chart",
]
