"""Sidebar widgets that turn user input into typed Pydantic configs."""

import streamlit as st
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

_MIN_RUNS = 1
_MAX_RUNS = 500
_MIN_BOOTSTRAP = 200
_MAX_BOOTSTRAP = 5000
_MIN_TRAJECTORY_SAMPLES = 5
_MAX_TRAJECTORY_SAMPLES = 200


class AggregationSidebarLabels(BaseModel):
    """Labels for the aggregation expander in the sidebar."""

    model_config = ConfigDict(frozen=True)

    expander_title: str
    runs_label: str
    seed_label: str
    confidence_label: str
    bootstrap_resamples_label: str
    trajectory_samples_label: str


class AggregationSidebarInputs(BaseModel):
    """Bundle of typed inputs for :func:`build_aggregation_config`."""

    model_config = ConfigDict(frozen=True)

    defaults: AggregationConfig
    labels: AggregationSidebarLabels
    key_prefix: str = Field(min_length=1)


def build_aggregation_config(inputs: AggregationSidebarInputs) -> AggregationConfig:
    """Render the aggregation expander and return a fresh :class:`AggregationConfig`.

    Returns
    -------
    AggregationConfig
        Frozen Pydantic config reflecting the current widget state.
    """
    defaults = inputs.defaults
    labels = inputs.labels
    with st.sidebar.expander(labels.expander_title, expanded=False):
        runs = st.slider(
            labels.runs_label,
            min_value=_MIN_RUNS,
            max_value=_MAX_RUNS,
            value=defaults.runs,
            key=f"{inputs.key_prefix}_runs",
        )
        seed = st.number_input(
            labels.seed_label,
            min_value=0,
            value=defaults.seed,
            step=1,
            key=f"{inputs.key_prefix}_seed",
        )
        confidence = st.slider(
            labels.confidence_label,
            min_value=0.5,
            max_value=0.99,
            value=defaults.confidence_level,
            step=0.01,
            key=f"{inputs.key_prefix}_confidence",
        )
        resamples = st.slider(
            labels.bootstrap_resamples_label,
            min_value=_MIN_BOOTSTRAP,
            max_value=_MAX_BOOTSTRAP,
            value=defaults.bootstrap_resamples,
            step=100,
            key=f"{inputs.key_prefix}_resamples",
        )
        trajectory_samples = st.slider(
            labels.trajectory_samples_label,
            min_value=_MIN_TRAJECTORY_SAMPLES,
            max_value=_MAX_TRAJECTORY_SAMPLES,
            value=defaults.trajectory_step_samples,
            step=1,
            key=f"{inputs.key_prefix}_trajectory_samples",
        )
    return AggregationConfig(
        runs=int(runs),
        seed=int(seed),
        confidence_level=float(confidence),
        bootstrap_resamples=int(resamples),
        trajectory_step_samples=int(trajectory_samples),
    )


__all__ = [
    "AggregationSidebarInputs",
    "AggregationSidebarLabels",
    "build_aggregation_config",
]
