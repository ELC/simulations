"""Marshallian supply-demand cross for the double auction's final round."""

from typing import cast

import altair as alt
import numpy as np
import pandas as pd
import pandera.pandas as pa
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from ..model import AdvancedParams, final_orderbook

_DEFAULT_HEIGHT = 320


class SupplyDemandData(pa.DataFrameModel):
    """Long-form supply/demand curves for the final auction round."""

    side: str
    quantity: int = pa.Field(ge=0)
    price: float = pa.Field(ge=0.0)


class SupplyDemandHeading(BaseModel):
    """Title and labels for the Marshallian S/D chart."""

    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    clearing_label: str


class SpecialChartInputs(BaseModel):
    """Typed inputs for :func:`render_special_chart`."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: SupplyDemandHeading


def build_supply_demand_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> tuple[DataFrame[SupplyDemandData], float]:
    """Replay one replicate to extract the final-round S/D curves.

    Returns
    -------
    tuple[DataFrame[SupplyDemandData], float]
        Long-form S/D data and the clearing price.
    """
    parent = np.random.SeedSequence(seed)
    first_child = parent.spawn(1)[0]
    rng = np.random.default_rng(first_child)
    snapshot = final_orderbook(params, rng)
    bids_desc = np.sort(snapshot.bids)[::-1]
    asks_asc = np.sort(snapshot.asks)
    demand = pd.DataFrame(
        {
            "side": np.full(bids_desc.size, "Demand"),
            "quantity": np.arange(1, bids_desc.size + 1, dtype=np.int64),
            "price": bids_desc.astype(np.float64),
        },
    )
    supply = pd.DataFrame(
        {
            "side": np.full(asks_asc.size, "Supply"),
            "quantity": np.arange(1, asks_asc.size + 1, dtype=np.int64),
            "price": asks_asc.astype(np.float64),
        },
    )
    combined = pd.concat([demand, supply], ignore_index=True)
    return DataFrame[SupplyDemandData](combined), snapshot.clearing_price


def build_supply_demand_chart(
    *,
    data: DataFrame[SupplyDemandData],
    clearing_price: float,
    heading: SupplyDemandHeading,
) -> alt.TopLevelMixin:
    """Build the layered Marshallian S/D step-line chart.

    Returns
    -------
    alt.TopLevelMixin
        Layered Altair chart with step lines and a clearing-price rule.
    """
    curves = (
        alt
        .Chart(data)
        .mark_line(interpolate="step-after")
        .encode(
            x=alt.X("quantity:Q", title=heading.x_label),
            y=alt.Y("price:Q", title=heading.y_label),
            color=alt.Color("side:N"),
        )
    )
    rule = (
        alt
        .Chart(pd.DataFrame({"clearing": [clearing_price]}))
        .mark_rule(strokeDash=[4, 4], color="gray")
        .encode(y=alt.Y("clearing:Q", title=heading.clearing_label))
    )
    return alt.layer(curves, rule).properties(title=heading.title, height=_DEFAULT_HEIGHT)


def render_special_chart(inputs: SpecialChartInputs) -> None:
    data, clearing = build_supply_demand_frame(params=inputs.params, seed=inputs.seed)
    chart = build_supply_demand_chart(
        data=data,
        clearing_price=clearing,
        heading=inputs.heading,
    )
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


__all__ = [
    "SpecialChartInputs",
    "SupplyDemandData",
    "SupplyDemandHeading",
    "build_supply_demand_chart",
    "build_supply_demand_frame",
    "render_special_chart",
]
