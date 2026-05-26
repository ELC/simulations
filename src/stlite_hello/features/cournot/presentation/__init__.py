"""Presentation layer for the Cournot feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    BestResponseHeading,
    BestResponseLinesData,
    BestResponseTrajectoryData,
    SpecialChartInputs,
    build_best_response_chart,
    build_trajectory_data,
    render_special_chart,
)
from .view_models import COURNOT_COPY, COURNOT_SPECIAL_HEADING

__all__ = [
    "COURNOT_COPY",
    "COURNOT_SPECIAL_HEADING",
    "BestResponseHeading",
    "BestResponseLinesData",
    "BestResponseTrajectoryData",
    "SidebarInputs",
    "SpecialChartInputs",
    "build_best_response_chart",
    "build_config",
    "build_trajectory_data",
    "render",
    "render_special_chart",
]
