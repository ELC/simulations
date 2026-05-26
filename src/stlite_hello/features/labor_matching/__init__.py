"""Labor search-and-matching simulation slice."""

import streamlit as st

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
    labor_market_history,
    simulate_once,
)
from .page import pages
from .presentation import (
    LABOR_MATCHING_COPY,
    LABOR_MATCHING_SPECIAL_HEADING,
    BeveridgeData,
    BeveridgeHeading,
    SpecialChartInputs,
    build_beveridge_chart,
    build_beveridge_frame,
    render,
    render_special_chart,
)


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
    "SimpleParams",
    "SpecialChartInputs",
    "build_beveridge_chart",
    "build_beveridge_frame",
    "labor_market_history",
    "main",
    "pages",
    "render",
    "render_special_chart",
    "simulate_once",
]
