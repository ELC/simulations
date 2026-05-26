"""Presentation layer for the Kinetic Exchange feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    SavingsWealthData,
    SavingsWealthHeading,
    SpecialChartInputs,
    build_savings_wealth_chart,
    build_savings_wealth_panel,
    render_special_chart,
)
from .view_models import KINETIC_COPY, KINETIC_SPECIAL_HEADING

__all__ = [
    "KINETIC_COPY",
    "KINETIC_SPECIAL_HEADING",
    "SavingsWealthData",
    "SavingsWealthHeading",
    "SidebarInputs",
    "SpecialChartInputs",
    "build_config",
    "build_savings_wealth_chart",
    "build_savings_wealth_panel",
    "render",
    "render_special_chart",
]
