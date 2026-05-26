from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.sugarscape.model import AdvancedParams, SimpleParams, SugarscapeConfig
from stlite_hello.features.sugarscape.view_models import SUGARSCAPE_COPY
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "sugarscape"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_agents = st.slider(
        "Number of agents",
        min_value=4,
        max_value=400,
        value=defaults.n_agents,
        step=1,
        key=f"{_KEY_PREFIX}_simple_agents",
    )
    n_steps = st.slider(
        "Simulation steps",
        min_value=5,
        max_value=500,
        value=defaults.n_steps,
        step=5,
        key=f"{_KEY_PREFIX}_simple_steps",
    )
    vision = st.slider(
        "Vision radius",
        min_value=1,
        max_value=10,
        value=defaults.vision,
        step=1,
        key=f"{_KEY_PREFIX}_simple_vision",
    )
    return AdvancedParams(
        n_agents=int(n_agents),
        n_steps=int(n_steps),
        vision=int(vision),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    grid_size = st.slider(
        "Grid edge length",
        min_value=5,
        max_value=60,
        value=defaults.grid_size,
        step=1,
        key=f"{_KEY_PREFIX}_advanced_grid",
    )
    regrowth_rate = st.number_input(
        "Sugar regrowth per step",
        min_value=0.01,
        value=defaults.regrowth_rate,
        step=0.1,
        key=f"{_KEY_PREFIX}_advanced_regrowth",
    )
    metabolism_mean = st.number_input(
        "Mean metabolism per step",
        min_value=0.01,
        value=defaults.metabolism_mean,
        step=0.1,
        key=f"{_KEY_PREFIX}_advanced_metabolism",
    )
    initial_endowment = st.number_input(
        "Initial sugar endowment",
        min_value=0.0,
        value=defaults.initial_endowment,
        step=1.0,
        key=f"{_KEY_PREFIX}_advanced_endowment",
    )
    return AdvancedParams(
        n_agents=simple.n_agents,
        n_steps=simple.n_steps,
        vision=simple.vision,
        grid_size=int(grid_size),
        regrowth_rate=float(regrowth_rate),
        metabolism_mean=float(metabolism_mean),
        initial_endowment=float(initial_endowment),
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
                vision=defaults.vision,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: SugarscapeConfig


def build_config(inputs: SidebarInputs) -> SugarscapeConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, SUGARSCAPE_COPY.view_toggle)
    seed = _render_seed(SUGARSCAPE_COPY.seed, defaults.seed)
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
            labels=SUGARSCAPE_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return SugarscapeConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
