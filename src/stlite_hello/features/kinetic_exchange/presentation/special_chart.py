"""Wealth vs savings-rate scatter special chart for Kinetic Exchange."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle

from ..model import AdvancedParams, savings_per_agent

_DEFAULT_HEIGHT = 320


class SavingsWealthData(pa.DataFrameModel):
    """One row per (run, agent) pairing savings rate with final wealth."""

    run: int = pa.Field(ge=0)
    agent: int = pa.Field(ge=0)
    savings_rate: float = pa.Field(ge=0.0, le=1.0)
    final_wealth: float = pa.Field(ge=0.0)


class SavingsWealthHeading(BaseModel):
    """Title and axis labels for the savings/wealth scatter."""

    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    rolling_label: str


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    params: AdvancedParams
    seed: int
    runs: int
    heading: SavingsWealthHeading


def build_savings_wealth_panel(
    *,
    bundle: RunBundle,
    params: AdvancedParams,
    seed: int,
    runs: int,
) -> DataFrame[SavingsWealthData]:
    """Combine per-replicate savings draws with final wealth.

    Returns
    -------
    DataFrame[SavingsWealthData]
        One row per (run, agent) suitable for a scatter chart.
    """
    parent = np.random.SeedSequence(seed)
    child_seeds = parent.spawn(runs)
    pieces: list[pd.DataFrame] = []
    for run_index, seed_seq in enumerate(child_seeds):
        rng = np.random.default_rng(seed_seq)
        savings = savings_per_agent(params, rng)
        run_frame = bundle.final_population[bundle.final_population["run"] == run_index]
        pieces.append(
            pd.DataFrame(
                {
                    "run": run_frame["run"].astype(np.int64).to_numpy(),
                    "agent": run_frame["agent"].astype(np.int64).to_numpy(),
                    "savings_rate": savings.astype(np.float64),
                    "final_wealth": run_frame["value"].astype(np.float64).to_numpy(),
                },
            ),
        )
    combined = pd.concat(pieces, ignore_index=True)
    return DataFrame[SavingsWealthData](combined)


def build_savings_wealth_chart(
    data: DataFrame[SavingsWealthData],
    heading: SavingsWealthHeading,
) -> alt.TopLevelMixin:
    """Scatter of agents in (savings, wealth) space with a rolling-mean line."""
    base = alt.Chart(data).encode(
        x=alt.X("savings_rate:Q", title=heading.x_label),
        y=alt.Y("final_wealth:Q", title=heading.y_label),
    )
    points = base.mark_circle(opacity=0.4).encode(
        tooltip=["run", "agent", "savings_rate", "final_wealth"],
    )
    rolling = (
        alt
        .Chart(data)
        .transform_window(
            sort=[{"field": "savings_rate"}],
            mean_wealth="mean(final_wealth)",
            frame=[-15, 15],
        )
        .mark_line(color="#ff7f0e")
        .encode(
            x=alt.X("savings_rate:Q"),
            y=alt.Y("mean_wealth:Q", title=heading.rolling_label),
        )
    )
    return alt.layer(points, rolling).properties(title=heading.title, height=_DEFAULT_HEIGHT)


def render_special_chart(inputs: SpecialChartInputs) -> None:
    panel = build_savings_wealth_panel(
        bundle=inputs.bundle,
        params=inputs.params,
        seed=inputs.seed,
        runs=inputs.runs,
    )
    chart = build_savings_wealth_chart(panel, inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "SavingsWealthData",
    "SavingsWealthHeading",
    "SpecialChartInputs",
    "build_savings_wealth_chart",
    "build_savings_wealth_panel",
    "render_special_chart",
]
