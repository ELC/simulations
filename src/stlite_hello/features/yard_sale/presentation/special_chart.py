"""Wealth-condensation heatmap special chart for Yard-Sale."""

from typing import cast

import altair as alt
import numpy as np
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import FocalPanel, RunBundle

_DEFAULT_HEIGHT = 320
_RANK_BINS = 40


class WealthCondensationData(pa.DataFrameModel):
    """One row per (step, rank bin) carrying the bin's mean wealth share."""

    step: int = pa.Field(ge=0)
    rank: int = pa.Field(ge=1, le=_RANK_BINS)
    wealth_share: float = pa.Field(ge=0.0)


class WealthCondensationHeading(BaseModel):
    """Title and axis labels for the wealth-condensation heatmap."""

    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    color_label: str


def aggregate_wealth_condensation(panel: DataFrame[FocalPanel]) -> DataFrame[WealthCondensationData]:
    """Average per-step rank-binned wealth share across replicates.

    Returns
    -------
    DataFrame[WealthCondensationData]
        Long-form heatmap data ready for Altair.
    """
    frame = panel.copy()
    frame["rank"] = (
        frame
        .groupby(["run", "step"], sort=False)["value"]
        .rank(method="first", ascending=False)
        .astype(np.int64)
    )
    agents_per_step = frame.groupby(["run", "step"], sort=False)["agent"].transform("count")
    bucket_width = agents_per_step / _RANK_BINS
    frame["rank_bin"] = np.minimum(
        ((frame["rank"] - 1) // bucket_width).astype(np.int64) + 1,
        _RANK_BINS,
    )
    totals = frame.groupby(["run", "step"], sort=False)["value"].transform("sum")
    safe_totals = totals.where(totals > 0.0, 1.0)
    frame["share"] = frame["value"] / safe_totals
    aggregated = (
        frame
        .groupby(["step", "rank_bin"], sort=False)["share"]
        .mean()
        .reset_index()
        .rename(columns={"rank_bin": "rank", "share": "wealth_share"})
    )
    aggregated["step"] = aggregated["step"].astype(np.int64)
    aggregated["rank"] = aggregated["rank"].astype(np.int64)
    aggregated["wealth_share"] = aggregated["wealth_share"].astype(np.float64)
    return DataFrame[WealthCondensationData](aggregated)


def build_wealth_condensation_chart(
    data: DataFrame[WealthCondensationData],
    heading: WealthCondensationHeading,
) -> alt.TopLevelMixin:
    """Build the rank-vs-step wealth-condensation heatmap."""
    chart = (
        alt
        .Chart(data)
        .mark_rect()
        .encode(
            x=alt.X("step:O", title=heading.x_label),
            y=alt.Y("rank:O", title=heading.y_label, sort="ascending"),
            color=alt.Color(
                "wealth_share:Q",
                title=heading.color_label,
                scale=alt.Scale(scheme="magma"),
            ),
            tooltip=["step", "rank", "wealth_share"],
        )
        .properties(title=heading.title, height=_DEFAULT_HEIGHT)
    )
    return cast("alt.TopLevelMixin", chart)


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    heading: WealthCondensationHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    """Streamlit-glue: build and render the wealth-condensation heatmap."""
    aggregated = aggregate_wealth_condensation(inputs.bundle.focal_panel)
    chart = build_wealth_condensation_chart(aggregated, inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "SpecialChartInputs",
    "WealthCondensationData",
    "WealthCondensationHeading",
    "aggregate_wealth_condensation",
    "build_wealth_condensation_chart",
    "render_special_chart",
]
