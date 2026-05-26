import streamlit as st

from .charts import (
    WealthCondensationHeading,
    aggregate_wealth_condensation,
    build_wealth_condensation_chart,
)
from .model import (
    YARD_SALE_DEFAULT_AGENTS,
    YARD_SALE_DEFAULT_FRACTION,
    YARD_SALE_DEFAULT_INITIAL_WEALTH,
    YARD_SALE_DEFAULT_SEED,
    YARD_SALE_DEFAULT_STEPS,
    YARD_SALE_FEATURE,
    AdvancedParams,
    SimpleParams,
    YardSaleConfig,
)
from .presentation import (
    SidebarInputs,
    SpecialChartInputs,
    build_config,
    pages,
    render,
    render_special_chart,
)
from .schemas import WealthCondensationData
from .simulation import simulate_once
from .view_models import YARD_SALE_COPY, YARD_SALE_SPECIAL_HEADING


def main() -> None:
    st.set_page_config(page_title="Yard-Sale simulation", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "YARD_SALE_COPY",
    "YARD_SALE_DEFAULT_AGENTS",
    "YARD_SALE_DEFAULT_FRACTION",
    "YARD_SALE_DEFAULT_INITIAL_WEALTH",
    "YARD_SALE_DEFAULT_SEED",
    "YARD_SALE_DEFAULT_STEPS",
    "YARD_SALE_FEATURE",
    "YARD_SALE_SPECIAL_HEADING",
    "AdvancedParams",
    "SidebarInputs",
    "SimpleParams",
    "SpecialChartInputs",
    "WealthCondensationData",
    "WealthCondensationHeading",
    "YardSaleConfig",
    "aggregate_wealth_condensation",
    "build_config",
    "build_wealth_condensation_chart",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
