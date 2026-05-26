import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 77
_EXPECTED_RUNS = 3
_EXPECTED_INTERCEPT = 80.0
_EXPECTED_SLOPE = 1.5
_EXPECTED_COST_MEAN = 15.0
_EXPECTED_COST_SPREAD = 5.0

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.cournot import CournotConfig
from stlite_hello.features.cournot.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=CournotConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_intercept"] = config.params.intercept
st.session_state["resolved_slope"] = config.params.slope
st.session_state["resolved_cost_mean"] = config.params.cost_mean
st.session_state["resolved_cost_spread"] = config.params.cost_spread
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["cournot_view_choice"] = "Advanced"
    test.session_state["cournot_simple_firms"] = 4
    test.session_state["cournot_simple_steps"] = 30
    test.session_state["cournot_simple_inertia"] = 0.4
    test.session_state["cournot_advanced_intercept"] = _EXPECTED_INTERCEPT
    test.session_state["cournot_advanced_slope"] = _EXPECTED_SLOPE
    test.session_state["cournot_advanced_cost_mean"] = _EXPECTED_COST_MEAN
    test.session_state["cournot_advanced_cost_spread"] = _EXPECTED_COST_SPREAD
    test.session_state["cournot_seed_input"] = _EXPECTED_SEED
    test.session_state["cournot_runs"] = _EXPECTED_RUNS
    test.session_state["cournot_trajectory_samples"] = 5
    test.session_state["cournot_resamples"] = 200
    test.session_state["cournot_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_intercept"] == pytest.approx(_EXPECTED_INTERCEPT)
    assert test.session_state["resolved_slope"] == pytest.approx(_EXPECTED_SLOPE)
    assert test.session_state["resolved_cost_mean"] == pytest.approx(_EXPECTED_COST_MEAN)
    assert test.session_state["resolved_cost_spread"] == pytest.approx(_EXPECTED_COST_SPREAD)
