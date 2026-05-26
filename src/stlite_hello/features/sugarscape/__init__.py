import streamlit as st

from .charts import (
    SpatialHeading,
    build_spatial_chart,
    build_spatial_frames,
)
from .model import (
    SUGARSCAPE_DEFAULT_AGENTS,
    SUGARSCAPE_DEFAULT_GRID,
    SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT,
    SUGARSCAPE_DEFAULT_METABOLISM,
    SUGARSCAPE_DEFAULT_REGROWTH,
    SUGARSCAPE_DEFAULT_SEED,
    SUGARSCAPE_DEFAULT_STEPS,
    SUGARSCAPE_DEFAULT_VISION,
    SUGARSCAPE_FEATURE,
    AdvancedParams,
    SimpleParams,
    SpatialSnapshot,
    SugarscapeConfig,
)
from .presentation import (
    SidebarInputs,
    SpecialChartInputs,
    build_config,
    pages,
    render,
    render_special_chart,
)
from .schemas import AgentLocationData, SpatialCellData
from .simulation import final_snapshot, simulate_once
from .view_models import SUGARSCAPE_COPY, SUGARSCAPE_SPECIAL_HEADING


def main() -> None:
    st.set_page_config(page_title="Sugarscape", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "SUGARSCAPE_COPY",
    "SUGARSCAPE_DEFAULT_AGENTS",
    "SUGARSCAPE_DEFAULT_GRID",
    "SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT",
    "SUGARSCAPE_DEFAULT_METABOLISM",
    "SUGARSCAPE_DEFAULT_REGROWTH",
    "SUGARSCAPE_DEFAULT_SEED",
    "SUGARSCAPE_DEFAULT_STEPS",
    "SUGARSCAPE_DEFAULT_VISION",
    "SUGARSCAPE_FEATURE",
    "SUGARSCAPE_SPECIAL_HEADING",
    "AdvancedParams",
    "AgentLocationData",
    "SidebarInputs",
    "SimpleParams",
    "SpatialCellData",
    "SpatialHeading",
    "SpatialSnapshot",
    "SpecialChartInputs",
    "SugarscapeConfig",
    "build_config",
    "build_spatial_chart",
    "build_spatial_frames",
    "final_snapshot",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
