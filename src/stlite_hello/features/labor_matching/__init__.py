import streamlit as st

from .charts import (
    BeveridgeHeading,
    build_beveridge_chart,
    build_beveridge_frame,
)
from .model import (
    LABOR_MATCHING_DEFAULT_ALPHA,
    LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT,
    LABOR_MATCHING_DEFAULT_MU,
    LABOR_MATCHING_DEFAULT_PRODUCTIVITY,
    LABOR_MATCHING_DEFAULT_SEED,
    LABOR_MATCHING_DEFAULT_SEPARATION,
    LABOR_MATCHING_DEFAULT_STEPS,
    LABOR_MATCHING_DEFAULT_VACANCY_RATE,
    LABOR_MATCHING_DEFAULT_WAGE_SHARE,
    LABOR_MATCHING_DEFAULT_WORKERS,
    LABOR_MATCHING_FEATURE,
    AdvancedParams,
    LaborMarketHistory,
    LaborMatchingConfig,
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
from .schemas import BeveridgeData
from .simulation import labor_market_history, simulate_once
from .view_models import LABOR_MATCHING_COPY, LABOR_MATCHING_SPECIAL_HEADING


def main() -> None:
    st.set_page_config(page_title="Labor matching", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "LABOR_MATCHING_COPY",
    "LABOR_MATCHING_DEFAULT_ALPHA",
    "LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT",
    "LABOR_MATCHING_DEFAULT_MU",
    "LABOR_MATCHING_DEFAULT_PRODUCTIVITY",
    "LABOR_MATCHING_DEFAULT_SEED",
    "LABOR_MATCHING_DEFAULT_SEPARATION",
    "LABOR_MATCHING_DEFAULT_STEPS",
    "LABOR_MATCHING_DEFAULT_VACANCY_RATE",
    "LABOR_MATCHING_DEFAULT_WAGE_SHARE",
    "LABOR_MATCHING_DEFAULT_WORKERS",
    "LABOR_MATCHING_FEATURE",
    "LABOR_MATCHING_SPECIAL_HEADING",
    "AdvancedParams",
    "BeveridgeData",
    "BeveridgeHeading",
    "LaborMarketHistory",
    "LaborMatchingConfig",
    "SidebarInputs",
    "SimpleParams",
    "SpecialChartInputs",
    "build_beveridge_chart",
    "build_beveridge_frame",
    "build_config",
    "labor_market_history",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
