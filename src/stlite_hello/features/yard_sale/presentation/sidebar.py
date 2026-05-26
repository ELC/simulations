from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.yard_sale.model import AdvancedParams, SimpleParams, YardSaleConfig
from stlite_hello.features.yard_sale.view_models import YARD_SALE_COPY
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "yard_sale"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _advanced_label(labels: AdvancedToggleLabels) -> tuple[str, str]:
    return labels.simple_option, labels.advanced_option


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
    transfer_fraction = st.slider(
        "Transfer fraction",
        min_value=0.01,
        max_value=0.99,
        value=defaults.transfer_fraction,
        step=0.01,
        key=f"{_KEY_PREFIX}_simple_fraction",
    )
    return AdvancedParams(
        n_agents=int(n_agents),
        n_steps=int(n_steps),
        transfer_fraction=float(transfer_fraction),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    initial_wealth = st.number_input(
        "Initial wealth per agent",
        min_value=0.01,
        value=defaults.initial_wealth,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_wealth",
    )
    win_probability = st.slider(
        "Win probability for agent A",
        min_value=0.01,
        max_value=0.99,
        value=defaults.win_probability,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_win",
    )
    return AdvancedParams(
        n_agents=simple.n_agents,
        n_steps=simple.n_steps,
        transfer_fraction=simple.transfer_fraction,
        initial_wealth=float(initial_wealth),
        win_probability=float(win_probability),
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
    simple_option, advanced_option = _advanced_label(labels)
    with st.sidebar.expander("Parameters", expanded=True):
        choice = st.radio(
            labels.label,
            options=[simple_option, advanced_option],
            key=f"{_KEY_PREFIX}_view_choice",
            horizontal=True,
        )
        if choice == advanced_option:
            params = _render_advanced_form(defaults)
            view: Literal["simple", "advanced"] = "advanced"
        else:
            simple_defaults = SimpleParams(
                n_agents=defaults.n_agents,
                n_steps=defaults.n_steps,
                transfer_fraction=defaults.transfer_fraction,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: YardSaleConfig


def build_config(inputs: SidebarInputs) -> YardSaleConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, YARD_SALE_COPY.view_toggle)
    seed = _render_seed(YARD_SALE_COPY.seed, defaults.seed)
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
            labels=YARD_SALE_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return YardSaleConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
