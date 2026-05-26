from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.cournot.charts import (
    BestResponseHeading,
    build_best_response_chart,
    build_trajectory_data,
)
from stlite_hello.features.cournot.model import AdvancedParams

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: BestResponseHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    trace, lines = build_trajectory_data(params=inputs.params, seed=inputs.seed)
    chart = build_best_response_chart(trajectory=trace, lines=lines, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
