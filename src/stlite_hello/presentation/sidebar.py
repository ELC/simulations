import streamlit as st

from stlite_hello.analysis import AggregationConfig
from stlite_hello.view_models import AggregationSidebarInputs

_MIN_RUNS = 1
_MAX_RUNS = 500
_MIN_BOOTSTRAP = 200
_MAX_BOOTSTRAP = 5000
_MIN_TRAJECTORY_SAMPLES = 5
_MAX_TRAJECTORY_SAMPLES = 200


def build_aggregation_config(inputs: AggregationSidebarInputs) -> AggregationConfig:
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
