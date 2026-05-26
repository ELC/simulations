from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.double_auction.charts import (
    SupplyDemandHeading,
    build_supply_demand_chart,
    build_supply_demand_frame,
)
from stlite_hello.features.double_auction.model import AdvancedParams

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: SupplyDemandHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    data, clearing = build_supply_demand_frame(params=inputs.params, seed=inputs.seed)
    chart = build_supply_demand_chart(
        data=data,
        clearing_price=clearing,
        heading=inputs.heading,
    )
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
