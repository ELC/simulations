from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle
from stlite_hello.features.yard_sale.charts import (
    WealthCondensationHeading,
    aggregate_wealth_condensation,
    build_wealth_condensation_chart,
)

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    heading: WealthCondensationHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    aggregated = aggregate_wealth_condensation(inputs.bundle)
    chart = build_wealth_condensation_chart(aggregated, inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
