import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 91
_EXPECTED_RUNS = 3
_EXPECTED_REGROWTH = 0.5
_EXPECTED_METABOLISM = 1.2
_EXPECTED_ENDOWMENT = 2.0
_EXPECTED_GRID = 12

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.sugarscape import SugarscapeConfig
from stlite_hello.features.sugarscape.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=SugarscapeConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_grid"] = config.params.grid_size
st.session_state["resolved_regrowth"] = config.params.regrowth_rate
st.session_state["resolved_metabolism"] = config.params.metabolism_mean
st.session_state["resolved_endowment"] = config.params.initial_endowment
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["sugarscape_view_choice"] = "Advanced"
    test.session_state["sugarscape_simple_agents"] = 16
    test.session_state["sugarscape_simple_steps"] = 20
    test.session_state["sugarscape_simple_vision"] = 3
    test.session_state["sugarscape_advanced_grid"] = _EXPECTED_GRID
    test.session_state["sugarscape_advanced_regrowth"] = _EXPECTED_REGROWTH
    test.session_state["sugarscape_advanced_metabolism"] = _EXPECTED_METABOLISM
    test.session_state["sugarscape_advanced_endowment"] = _EXPECTED_ENDOWMENT
    test.session_state["sugarscape_seed_input"] = _EXPECTED_SEED
    test.session_state["sugarscape_runs"] = _EXPECTED_RUNS
    test.session_state["sugarscape_trajectory_samples"] = 5
    test.session_state["sugarscape_resamples"] = 200
    test.session_state["sugarscape_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_grid"] == _EXPECTED_GRID
    assert test.session_state["resolved_regrowth"] == pytest.approx(_EXPECTED_REGROWTH)
    assert test.session_state["resolved_metabolism"] == pytest.approx(_EXPECTED_METABOLISM)
    assert test.session_state["resolved_endowment"] == pytest.approx(_EXPECTED_ENDOWMENT)
