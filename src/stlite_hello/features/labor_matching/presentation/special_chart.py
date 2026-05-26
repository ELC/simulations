"""Beveridge-curve special chart for the labor matching model."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.labor_matching.model import AdvancedParams, labor_market_history

_DEFAULT_HEIGHT = 360


class BeveridgeData(pa.DataFrameModel):
    """One row per step with the unemployment and vacancy rates."""

    step: int = pa.Field(ge=0)
    unemployment_rate: float = pa.Field(ge=0.0, le=1.0)
    vacancy_rate: float = pa.Field(ge=0.0)


class BeveridgeHeading(BaseModel):
    """Title and axis labels for the Beveridge curve chart."""

    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    step_label: str


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: BeveridgeHeading


def build_beveridge_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> DataFrame[BeveridgeData]:
    """Replay one replicate and project the (U, V) time series to a frame.

    Returns
    -------
    DataFrame[BeveridgeData]
        One row per step with the validated rates.
    """
    rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    history = labor_market_history(params, rng)
    frame = pd.DataFrame(
        {
            "step": np.arange(history.unemployment_rate.size, dtype=np.int64),
            "unemployment_rate": history.unemployment_rate.astype(np.float64),
            "vacancy_rate": history.vacancy_rate.astype(np.float64),
        },
    )
    return DataFrame[BeveridgeData](frame)


def build_beveridge_chart(
    *,
    data: DataFrame[BeveridgeData],
    heading: BeveridgeHeading,
) -> alt.TopLevelMixin:
    """Layered Altair chart: connected (U, V) trace + colored time points.

    Returns
    -------
    alt.TopLevelMixin
        The composed chart.
    """
    line = (
        alt
        .Chart(data)
        .mark_line(opacity=0.5)
        .encode(
            x=alt.X("unemployment_rate:Q", title=heading.x_label),
            y=alt.Y("vacancy_rate:Q", title=heading.y_label),
            order=alt.Order("step:Q"),
        )
    )
    points = (
        alt
        .Chart(data)
        .mark_circle(size=60)
        .encode(
            x=alt.X("unemployment_rate:Q"),
            y=alt.Y("vacancy_rate:Q"),
            color=alt.Color("step:Q", title=heading.step_label, scale=alt.Scale(scheme="viridis")),
            tooltip=["step", "unemployment_rate", "vacancy_rate"],
        )
    )
    return alt.layer(line, points).properties(title=heading.title, height=_DEFAULT_HEIGHT)


def render_special_chart(inputs: SpecialChartInputs) -> None:
    data = build_beveridge_frame(params=inputs.params, seed=inputs.seed)
    chart = build_beveridge_chart(data=data, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "BeveridgeData",
    "BeveridgeHeading",
    "SpecialChartInputs",
    "build_beveridge_chart",
    "build_beveridge_frame",
    "render_special_chart",
]
