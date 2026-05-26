import streamlit as st

from .charts import (
    SavingsWealthHeading,
    build_savings_wealth_chart,
    build_savings_wealth_panel,
)
from .model import (
    KINETIC_DEFAULT_AGENTS,
    KINETIC_DEFAULT_INITIAL_WEALTH,
    KINETIC_DEFAULT_LAMBDA_MEAN,
    KINETIC_DEFAULT_LAMBDA_SPREAD,
    KINETIC_DEFAULT_SEED,
    KINETIC_DEFAULT_STEPS,
    KINETIC_FEATURE,
    AdvancedParams,
    KineticExchangeConfig,
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
from .schemas import SavingsWealthData
from .simulation import savings_per_agent, simulate_once
from .view_models import KINETIC_COPY, KINETIC_SPECIAL_HEADING


def main() -> None:
    st.set_page_config(page_title="Kinetic wealth exchange", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "KINETIC_COPY",
    "KINETIC_DEFAULT_AGENTS",
    "KINETIC_DEFAULT_INITIAL_WEALTH",
    "KINETIC_DEFAULT_LAMBDA_MEAN",
    "KINETIC_DEFAULT_LAMBDA_SPREAD",
    "KINETIC_DEFAULT_SEED",
    "KINETIC_DEFAULT_STEPS",
    "KINETIC_FEATURE",
    "KINETIC_SPECIAL_HEADING",
    "AdvancedParams",
    "KineticExchangeConfig",
    "SavingsWealthData",
    "SavingsWealthHeading",
    "SidebarInputs",
    "SimpleParams",
    "SpecialChartInputs",
    "build_config",
    "build_savings_wealth_chart",
    "build_savings_wealth_panel",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "savings_per_agent",
    "simulate_once",
]
