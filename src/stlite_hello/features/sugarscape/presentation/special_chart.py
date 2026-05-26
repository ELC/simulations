from typing import TYPE_CHECKING, cast

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.features.sugarscape.charts import (
    SpatialHeading,
    build_spatial_chart,
    build_spatial_frames,
)
from stlite_hello.features.sugarscape.model import AdvancedParams

if TYPE_CHECKING:
    import altair as alt


class SpecialChartInputs(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    params: AdvancedParams
    seed: int
    heading: SpatialHeading


def render_special_chart(inputs: SpecialChartInputs) -> None:
    cells, agents = build_spatial_frames(params=inputs.params, seed=inputs.seed)
    chart = build_spatial_chart(cells=cells, agents=agents, heading=inputs.heading)
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
