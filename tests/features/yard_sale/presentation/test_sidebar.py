import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 42
_EXPECTED_RUNS = 3
_EXPECTED_INITIAL_WEALTH = 250.0
_EXPECTED_WIN = 0.6

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.yard_sale import YardSaleConfig
from stlite_hello.features.yard_sale.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=YardSaleConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_initial_wealth"] = config.params.initial_wealth
st.session_state["resolved_win"] = config.params.win_probability
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["yard_sale_view_choice"] = "Advanced"
    test.session_state["yard_sale_simple_agents"] = 30
    test.session_state["yard_sale_simple_steps"] = 25
    test.session_state["yard_sale_simple_fraction"] = 0.2
    test.session_state["yard_sale_advanced_wealth"] = 250.0
    test.session_state["yard_sale_advanced_win"] = 0.6
    test.session_state["yard_sale_seed_input"] = 42
    test.session_state["yard_sale_runs"] = 3
    test.session_state["yard_sale_trajectory_samples"] = 5
    test.session_state["yard_sale_resamples"] = 200
    test.session_state["yard_sale_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_initial_wealth"] == pytest.approx(_EXPECTED_INITIAL_WEALTH)
    assert test.session_state["resolved_win"] == pytest.approx(_EXPECTED_WIN)
