import streamlit as st

from .charts import (
    SupplyDemandHeading,
    build_supply_demand_chart,
    build_supply_demand_frame,
)
from .model import (
    DOUBLE_AUCTION_DEFAULT_SEED,
    DOUBLE_AUCTION_DEFAULT_SHADING,
    DOUBLE_AUCTION_DEFAULT_STEPS,
    DOUBLE_AUCTION_DEFAULT_TRADERS,
    DOUBLE_AUCTION_DEFAULT_VALUE_CEILING,
    DOUBLE_AUCTION_FEATURE,
    AdvancedParams,
    DoubleAuctionConfig,
    OrderBookSnapshot,
    SimpleParams,
)
from .presentation import (
    SidebarInputs,
    SpecialChartInputs,
    build_config,
    pages,
    render,
    render_special_chart,
)
from .schemas import SupplyDemandData
from .simulation import final_orderbook, simulate_once
from .view_models import DOUBLE_AUCTION_COPY, DOUBLE_AUCTION_SPECIAL_HEADING


def main() -> None:
    st.set_page_config(page_title="Double auction simulation", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "DOUBLE_AUCTION_COPY",
    "DOUBLE_AUCTION_DEFAULT_SEED",
    "DOUBLE_AUCTION_DEFAULT_SHADING",
    "DOUBLE_AUCTION_DEFAULT_STEPS",
    "DOUBLE_AUCTION_DEFAULT_TRADERS",
    "DOUBLE_AUCTION_DEFAULT_VALUE_CEILING",
    "DOUBLE_AUCTION_FEATURE",
    "DOUBLE_AUCTION_SPECIAL_HEADING",
    "AdvancedParams",
    "DoubleAuctionConfig",
    "OrderBookSnapshot",
    "SidebarInputs",
    "SimpleParams",
    "SpecialChartInputs",
    "SupplyDemandData",
    "SupplyDemandHeading",
    "build_config",
    "build_supply_demand_chart",
    "build_supply_demand_frame",
    "final_orderbook",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
