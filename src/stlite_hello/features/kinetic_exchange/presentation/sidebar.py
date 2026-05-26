from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.kinetic_exchange.model import AdvancedParams, KineticExchangeConfig, SimpleParams
from stlite_hello.features.kinetic_exchange.view_models import KINETIC_COPY
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "kinetic_exchange"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_agents = st.slider(
        "Number of agents",
        min_value=10,
        max_value=2_000,
        value=defaults.n_agents,
        step=10,
        key=f"{_KEY_PREFIX}_simple_agents",
    )
    n_steps = st.slider(
        "Steps per replicate",
        min_value=10,
        max_value=5_000,
        value=defaults.n_steps,
        step=10,
        key=f"{_KEY_PREFIX}_simple_steps",
    )
    lambda_mean = st.slider(
        "Mean savings propensity",
        min_value=0.0,
        max_value=1.0,
        value=defaults.lambda_mean,
        step=0.01,
        key=f"{_KEY_PREFIX}_simple_lambda_mean",
    )
    return AdvancedParams(
        n_agents=int(n_agents),
        n_steps=int(n_steps),
        lambda_mean=float(lambda_mean),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    lambda_spread = st.slider(
        "Savings dispersion (half-width)",
        min_value=0.0,
        max_value=1.0,
        value=defaults.lambda_spread,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_spread",
    )
    initial_wealth = st.number_input(
        "Initial wealth per agent",
        min_value=0.01,
        value=defaults.initial_wealth,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_wealth",
    )
    return AdvancedParams(
        n_agents=simple.n_agents,
        n_steps=simple.n_steps,
        lambda_mean=simple.lambda_mean,
        lambda_spread=float(lambda_spread),
        initial_wealth=float(initial_wealth),
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
                n_agents=defaults.n_agents,
                n_steps=defaults.n_steps,
                lambda_mean=defaults.lambda_mean,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: KineticExchangeConfig


def build_config(inputs: SidebarInputs) -> KineticExchangeConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, KINETIC_COPY.view_toggle)
    seed = _render_seed(KINETIC_COPY.seed, defaults.seed)
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
            labels=KINETIC_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return KineticExchangeConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
