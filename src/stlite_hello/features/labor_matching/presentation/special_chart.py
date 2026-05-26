from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.labor_matching.charts import (
    BeveridgeHeading,
    build_beveridge_chart,
    build_beveridge_frame,
)
from stlite_hello.features.labor_matching.model import AdvancedParams

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: BeveridgeHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    data = build_beveridge_frame(params=inputs.params, seed=inputs.seed)
    chart = build_beveridge_chart(data=data, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
