"""Wealth-condensation heatmap special chart for Yard-Sale."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle

_DEFAULT_HEIGHT = 320
_RANK_BINS = 40
_MAX_STEPS = 60


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


def _sample_sorted_shares(
    bundle: RunBundle,
) -> tuple[NDArray[np.int64], NDArray[np.float64]]:
    stacked = np.stack(bundle.panels, axis=0)
    sorted_desc = -np.sort(-stacked, axis=2)
    n_steps_full = sorted_desc.shape[1]
    step_indices = np.linspace(0, n_steps_full - 1, num=min(_MAX_STEPS, n_steps_full), dtype=np.int64)
    sampled = sorted_desc[:, step_indices, :]
    totals = sampled.sum(axis=2, keepdims=True)
    shares = sampled / np.where(totals > 0.0, totals, 1.0)
    return step_indices, shares.astype(np.float64, copy=False)


def _mean_shares_per_bin(shares: NDArray[np.float64]) -> NDArray[np.float64]:
    n_runs, n_steps_sampled, n_agents = shares.shape
    bucket = np.minimum(np.arange(n_agents) // max(1, n_agents // _RANK_BINS) + 1, _RANK_BINS)
    aggregated = np.zeros((n_steps_sampled, _RANK_BINS), dtype=np.float64)
    for rank_bin in range(1, _RANK_BINS + 1):
        mask = bucket == rank_bin
        if not mask.any():
            continue
        aggregated[:, rank_bin - 1] = shares[:, :, mask].sum(axis=(0, 2)) / float(
            mask.sum() * n_runs,
        )
    return aggregated


def aggregate_wealth_condensation(bundle: RunBundle) -> DataFrame[WealthCondensationData]:
    """Average per-step rank-binned wealth share across replicates.

    Returns
    -------
    DataFrame[WealthCondensationData]
        Long-form heatmap data ready for Altair.
    """
    step_indices, shares = _sample_sorted_shares(bundle)
    mean_share = _mean_shares_per_bin(shares)
    step_grid, rank_grid = np.meshgrid(step_indices, np.arange(1, _RANK_BINS + 1), indexing="ij")
    frame = pd.DataFrame(
        {
            "step": step_grid.ravel().astype(np.int64),
            "rank": rank_grid.ravel().astype(np.int64),
            "wealth_share": mean_share.ravel().astype(np.float64),
        },
    )
    return DataFrame[WealthCondensationData](frame)


def build_wealth_condensation_chart(
    data: DataFrame[WealthCondensationData],
    heading: WealthCondensationHeading,
) -> alt.TopLevelMixin:
    """Build the rank-vs-step wealth-condensation heatmap.

    Returns
    -------
    alt.TopLevelMixin
        Altair heatmap layered chart ready for ``st.altair_chart``.
    """
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
    aggregated = aggregate_wealth_condensation(inputs.bundle)
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
