from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.cournot.model import AdvancedParams, CournotConfig, SimpleParams
from stlite_hello.features.cournot.view_models import COURNOT_COPY
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "cournot"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_firms = st.slider(
        "Number of firms",
        min_value=2,
        max_value=50,
        value=defaults.n_firms,
        step=1,
        key=f"{_KEY_PREFIX}_simple_firms",
    )
    n_steps = st.slider(
        "Best-response iterations",
        min_value=5,
        max_value=1_000,
        value=defaults.n_steps,
        step=5,
        key=f"{_KEY_PREFIX}_simple_steps",
    )
    inertia = st.slider(
        "Adjustment inertia",
        min_value=0.0,
        max_value=0.99,
        value=defaults.inertia,
        step=0.01,
        key=f"{_KEY_PREFIX}_simple_inertia",
    )
    return AdvancedParams(
        n_firms=int(n_firms),
        n_steps=int(n_steps),
        inertia=float(inertia),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    intercept = st.number_input(
        "Demand intercept a",
        min_value=1.0,
        value=defaults.intercept,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_intercept",
    )
    slope = st.number_input(
        "Demand slope b",
        min_value=0.01,
        value=defaults.slope,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_slope",
    )
    cost_mean = st.number_input(
        "Mean marginal cost",
        min_value=0.0,
        value=defaults.cost_mean,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_cost_mean",
    )
    cost_spread = st.number_input(
        "Cost spread (half-width)",
        min_value=0.0,
        value=defaults.cost_spread,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_cost_spread",
    )
    return AdvancedParams(
        n_firms=simple.n_firms,
        n_steps=simple.n_steps,
        inertia=simple.inertia,
        intercept=float(intercept),
        slope=float(slope),
        cost_mean=float(cost_mean),
        cost_spread=float(cost_spread),
    )


def _render_seed(labels: SeedSliderLabels, default: int) -> int:
    value = st.sidebar.number_input(
        labels.label,
        min_value=0,
        value=default,
        step=1,
        help=labels.help,
        key=f"{_KEY_PREFIX}_seed_input",
    )
    return int(value)


def _render_params(defaults: AdvancedParams, labels: AdvancedToggleLabels) -> _SidebarParams:
    with st.sidebar.expander("Parameters", expanded=True):
        choice = st.radio(
            labels.label,
            options=[labels.simple_option, labels.advanced_option],
            key=f"{_KEY_PREFIX}_view_choice",
            horizontal=True,
        )
        if choice == labels.advanced_option:
            params = _render_advanced_form(defaults)
            view: Literal["simple", "advanced"] = "advanced"
        else:
            simple_defaults = SimpleParams(
                n_firms=defaults.n_firms,
                n_steps=defaults.n_steps,
                inertia=defaults.inertia,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: CournotConfig


def build_config(inputs: SidebarInputs) -> CournotConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, COURNOT_COPY.view_toggle)
    seed = _render_seed(COURNOT_COPY.seed, defaults.seed)
    aggregation = build_aggregation_config(
        AggregationSidebarInputs(
            defaults=AggregationConfig(
                runs=defaults.runs,
                seed=seed,
                trajectory_step_samples=defaults.trajectory_step_samples,
                bootstrap_resamples=defaults.bootstrap_resamples,
                confidence_level=defaults.confidence_level,
                bootstrap_method=defaults.bootstrap_method,
            ),
            labels=COURNOT_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return CournotConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
