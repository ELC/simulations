from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle
from stlite_hello.features.kinetic_exchange.charts import (
    SavingsWealthHeading,
    build_savings_wealth_chart,
    build_savings_wealth_panel,
)
from stlite_hello.features.kinetic_exchange.model import AdvancedParams

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bundle: RunBundle
    params: AdvancedParams
    seed: int
    runs: int
    heading: SavingsWealthHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    panel = build_savings_wealth_panel(
        bundle=inputs.bundle,
        params=inputs.params,
        seed=inputs.seed,
        runs=inputs.runs,
    )
    chart = build_savings_wealth_chart(panel, inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
