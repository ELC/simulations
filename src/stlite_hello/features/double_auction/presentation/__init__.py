"""Presentation layer for the Double Auction feature."""

from .controller import render
from .sidebar import SidebarInputs, build_config
from .special_chart import (
    SpecialChartInputs,
    SupplyDemandData,
    SupplyDemandHeading,
    build_supply_demand_chart,
    build_supply_demand_frame,
    render_special_chart,
)
from .view_models import DOUBLE_AUCTION_COPY, DOUBLE_AUCTION_SPECIAL_HEADING

__all__ = [
    "DOUBLE_AUCTION_COPY",
    "DOUBLE_AUCTION_SPECIAL_HEADING",
    "SidebarInputs",
    "SpecialChartInputs",
    "SupplyDemandData",
    "SupplyDemandHeading",
    "build_config",
    "build_supply_demand_chart",
    "build_supply_demand_frame",
    "render",
    "render_special_chart",
]
