"""Sidebar: turn user input into a frozen :class:`DoubleAuctionConfig`."""

from typing import Literal

import streamlit as st
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import AggregationConfig
from stlite_hello.presentation import (
    AdvancedToggleLabels,
    AggregationSidebarInputs,
    SeedSliderLabels,
    build_aggregation_config,
)

from ..model import AdvancedParams, DoubleAuctionConfig, SimpleParams
from .view_models import DOUBLE_AUCTION_COPY

_KEY_PREFIX = "double_auction"


class _SidebarParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    view: Literal["simple", "advanced"]
    params: AdvancedParams


def _render_simple_form(defaults: SimpleParams) -> AdvancedParams:
    n_traders = st.slider(
        "Number of traders",
        min_value=4,
        max_value=1_000,
        value=defaults.n_traders,
        step=2,
        key=f"{_KEY_PREFIX}_simple_traders",
    )
    n_steps = st.slider(
        "Auction rounds",
        min_value=10,
        max_value=2_000,
        value=defaults.n_steps,
        step=10,
        key=f"{_KEY_PREFIX}_simple_steps",
    )
    value_ceiling = st.number_input(
        "Maximum private value",
        min_value=1.0,
        value=defaults.value_ceiling,
        step=1.0,
        key=f"{_KEY_PREFIX}_simple_ceiling",
    )
    return AdvancedParams(
        n_traders=int(n_traders),
        n_steps=int(n_steps),
        value_ceiling=float(value_ceiling),
    )


def _render_advanced_form(defaults: AdvancedParams) -> AdvancedParams:
    simple = _render_simple_form(defaults)
    shading = st.slider(
        "Strategic shading (0 = truthful)",
        min_value=0.0,
        max_value=0.9,
        value=defaults.shading,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_shading",
    )
    buyer_share = st.slider(
        "Fraction of buyers",
        min_value=0.05,
        max_value=0.95,
        value=defaults.buyer_share,
        step=0.01,
        key=f"{_KEY_PREFIX}_advanced_buyer_share",
    )
    return AdvancedParams(
        n_traders=simple.n_traders,
        n_steps=simple.n_steps,
        value_ceiling=simple.value_ceiling,
        shading=float(shading),
        buyer_share=float(buyer_share),
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
                n_traders=defaults.n_traders,
                n_steps=defaults.n_steps,
                value_ceiling=defaults.value_ceiling,
            )
            params = _render_simple_form(simple_defaults)
            view = "simple"
    return _SidebarParams(view=view, params=params)


class SidebarInputs(BaseModel):
    model_config = ConfigDict(frozen=True)

    defaults: DoubleAuctionConfig


def build_config(inputs: SidebarInputs) -> DoubleAuctionConfig:
    """Render the sidebar and return a frozen :class:`DoubleAuctionConfig`.

    Returns
    -------
    DoubleAuctionConfig
        Fully validated, no primitives in the public signature.
    """
    defaults = inputs.defaults
    sidebar_params = _render_params(defaults.params, DOUBLE_AUCTION_COPY.view_toggle)
    seed = _render_seed(DOUBLE_AUCTION_COPY.seed, defaults.seed)
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
            labels=DOUBLE_AUCTION_COPY.sidebar,
            key_prefix=_KEY_PREFIX,
        ),
    )
    return DoubleAuctionConfig(
        runs=aggregation.runs,
        seed=aggregation.seed,
        trajectory_step_samples=aggregation.trajectory_step_samples,
        bootstrap_resamples=aggregation.bootstrap_resamples,
        confidence_level=aggregation.confidence_level,
        bootstrap_method=aggregation.bootstrap_method,
        params=sidebar_params.params,
    )


__all__ = ["SidebarInputs", "build_config"]
