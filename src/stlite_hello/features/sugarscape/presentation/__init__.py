"""Presentation layer for the Sugarscape feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    AgentLocationData,
    SpatialCellData,
    SpatialHeading,
    SpecialChartInputs,
    build_spatial_chart,
    build_spatial_frames,
    render_special_chart,
)
from .view_models import SUGARSCAPE_COPY, SUGARSCAPE_SPECIAL_HEADING

__all__ = [
    "SUGARSCAPE_COPY",
    "SUGARSCAPE_SPECIAL_HEADING",
    "AgentLocationData",
    "SidebarInputs",
    "SpatialCellData",
    "SpatialHeading",
    "SpecialChartInputs",
    "build_config",
    "build_spatial_chart",
    "build_spatial_frames",
    "render",
    "render_special_chart",
]
