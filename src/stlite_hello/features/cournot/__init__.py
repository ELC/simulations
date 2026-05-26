"""Cournot oligopoly simulation slice."""

import streamlit as st

from .model import (
    COURNOT_DEFAULT_COST_MEAN,
    COURNOT_DEFAULT_COST_SPREAD,
    COURNOT_DEFAULT_FIRMS,
    COURNOT_DEFAULT_INERTIA,
    COURNOT_DEFAULT_INTERCEPT,
    COURNOT_DEFAULT_SEED,
    COURNOT_DEFAULT_SLOPE,
    COURNOT_DEFAULT_STEPS,
    COURNOT_FEATURE,
    AdvancedParams,
    CournotConfig,
    SimpleParams,
    costs_for_seed,
    quantity_trajectory,
    simulate_once,
)
from .page import pages
from .presentation import (
    COURNOT_COPY,
    COURNOT_SPECIAL_HEADING,
    BestResponseHeading,
    BestResponseLinesData,
    BestResponseTrajectoryData,
    SpecialChartInputs,
    build_best_response_chart,
    build_trajectory_data,
    render,
    render_special_chart,
)


def main() -> None:
    st.set_page_config(page_title="Cournot oligopoly", layout="wide")
    page = st.navigation(pages(), position="sidebar")
    page.run()


__all__ = [
    "COURNOT_COPY",
    "COURNOT_DEFAULT_COST_MEAN",
    "COURNOT_DEFAULT_COST_SPREAD",
    "COURNOT_DEFAULT_FIRMS",
    "COURNOT_DEFAULT_INERTIA",
    "COURNOT_DEFAULT_INTERCEPT",
    "COURNOT_DEFAULT_SEED",
    "COURNOT_DEFAULT_SLOPE",
    "COURNOT_DEFAULT_STEPS",
    "COURNOT_FEATURE",
    "COURNOT_SPECIAL_HEADING",
    "AdvancedParams",
    "BestResponseHeading",
    "BestResponseLinesData",
    "BestResponseTrajectoryData",
    "CournotConfig",
    "SimpleParams",
    "SpecialChartInputs",
    "build_best_response_chart",
    "build_trajectory_data",
    "costs_for_seed",
    "main",
    "pages",
    "quantity_trajectory",
    "render",
    "render_special_chart",
    "simulate_once",
]
