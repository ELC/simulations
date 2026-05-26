from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.features.preferential_attachment.model import (
    AdvancedParams,
    PreferentialAttachmentConfig,
    SimpleParams,
)
from stlite_hello.features.preferential_attachment.view_models import (
    PREFERENTIAL_ATTACHMENT_COPY,
)
from stlite_hello.presentation import build_aggregation_config
from stlite_hello.view_models import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
)

_KEY_PREFIX = "preferential_attachment"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_nodes = st.slider(
        "Number of nodes",
        min_value=10,
        max_value=2_000,
        value=defaults.n_nodes,
        step=10,
        key=f"{_KEY_PREFIX}_simple_nodes",
    )
    m_attach = st.slider(
        "Attachments per arrival",
        min_value=1,
        max_value=20,
        value=defaults.m_attach,
        step=1,
        key=f"{_KEY_PREFIX}_simple_attach",
    )
    return AdvancedParams(n_nodes=int(n_nodes), m_attach=int(m_attach))


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    initial_clique = st.slider(
        "Initial seed clique size",
        min_value=max(simple.m_attach + 1, 2),
        max_value=50,
        value=max(defaults.initial_clique, simple.m_attach + 1),
        step=1,
        key=f"{_KEY_PREFIX}_advanced_clique",
    )
    return AdvancedParams(
        n_nodes=simple.n_nodes,
        m_attach=simple.m_attach,
        initial_clique=int(initial_clique),
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
            simple_defaults = SimpleParams(n_nodes=defaults.n_nodes, m_attach=defaults.m_attach)
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: PreferentialAttachmentConfig


def build_config(inputs: SidebarInputs) -> PreferentialAttachmentConfig:
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, PREFERENTIAL_ATTACHMENT_COPY.view_toggle)
    seed = _render_seed(PREFERENTIAL_ATTACHMENT_COPY.seed, defaults.seed)
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
            labels=PREFERENTIAL_ATTACHMENT_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return PreferentialAttachmentConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )
