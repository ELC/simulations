"""Continuous double-auction simulation slice."""

import streamlit as st

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
    final_orderbook,
    simulate_once,
)
from .page import pages
from .presentation import (
    DOUBLE_AUCTION_COPY,
    DOUBLE_AUCTION_SPECIAL_HEADING,
    SpecialChartInputs,
    SupplyDemandData,
    SupplyDemandHeading,
    build_supply_demand_chart,
    build_supply_demand_frame,
    render,
    render_special_chart,
)


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
    "SimpleParams",
    "SpecialChartInputs",
    "SupplyDemandData",
    "SupplyDemandHeading",
    "build_supply_demand_chart",
    "build_supply_demand_frame",
    "final_orderbook",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
