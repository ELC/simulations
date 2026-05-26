from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.labor_matching.model import (
    AdvancedParams,
    LaborMatchingConfig,
    SimpleParams,
)
from stlite_hello.features.labor_matching.view_models import LABOR_MATCHING_COPY
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "labor_matching"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_workers = st.slider(
        "Number of workers",
        min_value=10,
        max_value=2_000,
        value=defaults.n_workers,
        step=10,
        key=f"{_KEY_PREFIX}_simple_workers",
    )
    n_steps = st.slider(
        "Simulation steps",
        min_value=5,
        max_value=500,
        value=defaults.n_steps,
        step=5,
        key=f"{_KEY_PREFIX}_simple_steps",
    )
    separation_rate = st.slider(
        "Separation rate",
        min_value=0.005,
        max_value=0.5,
        value=defaults.separation_rate,
        step=0.005,
        key=f"{_KEY_PREFIX}_simple_separation",
    )
    matching_efficiency = st.slider(
        "Matching efficiency",
        min_value=0.05,
        max_value=2.0,
        value=defaults.matching_efficiency,
        step=0.05,
        key=f"{_KEY_PREFIX}_simple_efficiency",
    )
    return AdvancedParams(
        n_workers=int(n_workers),
        n_steps=int(n_steps),
        separation_rate=float(separation_rate),
        matching_efficiency=float(matching_efficiency),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    alpha = st.slider(
        "Matching elasticity alpha",
        min_value=0.05,
        max_value=0.95,
        value=defaults.alpha,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_alpha",
    )
    vacancy_rate = st.slider(
        "Vacancy creation rate",
        min_value=0.0,
        max_value=1.0,
        value=defaults.vacancy_creation_rate,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_vacancy",
    )
    wage_share = st.slider(
        "Worker wage share",
        min_value=0.01,
        max_value=0.99,
        value=defaults.wage_share,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_wage",
    )
    productivity = st.number_input(
        "Productivity per filled job",
        min_value=0.01,
        value=defaults.productivity,
        step=0.1,
        key=f"{_KEY_PREFIX}_advanced_productivity",
    )
    initial_employment = st.slider(
        "Initial employment rate",
        min_value=0.0,
        max_value=1.0,
        value=defaults.initial_employment,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_initial",
    )
    return AdvancedParams(
        n_workers=simple.n_workers,
        n_steps=simple.n_steps,
        separation_rate=simple.separation_rate,
        matching_efficiency=simple.matching_efficiency,
        alpha=float(alpha),
        vacancy_creation_rate=float(vacancy_rate),
        wage_share=float(wage_share),
        productivity=float(productivity),
        initial_employment=float(initial_employment),
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
                n_workers=defaults.n_workers,
                n_steps=defaults.n_steps,
                separation_rate=defaults.separation_rate,
                matching_efficiency=defaults.matching_efficiency,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: LaborMatchingConfig


def build_config(inputs: SidebarInputs) -> LaborMatchingConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, LABOR_MATCHING_COPY.view_toggle)
    seed = _render_seed(LABOR_MATCHING_COPY.seed, defaults.seed)
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
            labels=LABOR_MATCHING_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return LaborMatchingConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
