import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 99
_EXPECTED_RUNS = 3
_EXPECTED_SPREAD = 0.25
_EXPECTED_WEALTH = 300.0

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.kinetic_exchange import KineticExchangeConfig
from stlite_hello.features.kinetic_exchange.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=KineticExchangeConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_spread"] = config.params.lambda_spread
st.session_state["resolved_wealth"] = config.params.initial_wealth
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["kinetic_exchange_view_choice"] = "Advanced"
    test.session_state["kinetic_exchange_simple_agents"] = 30
    test.session_state["kinetic_exchange_simple_steps"] = 25
    test.session_state["kinetic_exchange_simple_lambda_mean"] = 0.4
    test.session_state["kinetic_exchange_advanced_spread"] = 0.25
    test.session_state["kinetic_exchange_advanced_wealth"] = 300.0
    test.session_state["kinetic_exchange_seed_input"] = 99
    test.session_state["kinetic_exchange_runs"] = 3
    test.session_state["kinetic_exchange_trajectory_samples"] = 5
    test.session_state["kinetic_exchange_resamples"] = 200
    test.session_state["kinetic_exchange_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_spread"] == pytest.approx(_EXPECTED_SPREAD)
    assert test.session_state["resolved_wealth"] == pytest.approx(_EXPECTED_WEALTH)
