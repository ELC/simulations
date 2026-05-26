"""Presentation layer for the labor-matching feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    BeveridgeData,
    BeveridgeHeading,
    SpecialChartInputs,
    build_beveridge_chart,
    build_beveridge_frame,
    render_special_chart,
)
from .view_models import LABOR_MATCHING_COPY, LABOR_MATCHING_SPECIAL_HEADING

__all__ = [
    "LABOR_MATCHING_COPY",
    "LABOR_MATCHING_SPECIAL_HEADING",
    "BeveridgeData",
    "BeveridgeHeading",
    "SidebarInputs",
    "SpecialChartInputs",
    "build_beveridge_chart",
    "build_beveridge_frame",
    "build_config",
    "render",
    "render_special_chart",
]
