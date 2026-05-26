import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 88
_EXPECTED_RUNS = 3
_EXPECTED_ALPHA = 0.6
_EXPECTED_VACANCY = 0.2
_EXPECTED_WAGE = 0.45
_EXPECTED_PRODUCTIVITY = 1.5
_EXPECTED_INITIAL = 0.7

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.labor_matching import LaborMatchingConfig
from stlite_hello.features.labor_matching.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=LaborMatchingConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_alpha"] = config.params.alpha
st.session_state["resolved_vacancy"] = config.params.vacancy_creation_rate
st.session_state["resolved_wage"] = config.params.wage_share
st.session_state["resolved_productivity"] = config.params.productivity
st.session_state["resolved_initial"] = config.params.initial_employment
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["labor_matching_view_choice"] = "Advanced"
    test.session_state["labor_matching_simple_workers"] = 50
    test.session_state["labor_matching_simple_steps"] = 30
    test.session_state["labor_matching_simple_separation"] = 0.05
    test.session_state["labor_matching_simple_efficiency"] = 0.5
    test.session_state["labor_matching_advanced_alpha"] = _EXPECTED_ALPHA
    test.session_state["labor_matching_advanced_vacancy"] = _EXPECTED_VACANCY
    test.session_state["labor_matching_advanced_wage"] = _EXPECTED_WAGE
    test.session_state["labor_matching_advanced_productivity"] = _EXPECTED_PRODUCTIVITY
    test.session_state["labor_matching_advanced_initial"] = _EXPECTED_INITIAL
    test.session_state["labor_matching_seed_input"] = _EXPECTED_SEED
    test.session_state["labor_matching_runs"] = _EXPECTED_RUNS
    test.session_state["labor_matching_trajectory_samples"] = 5
    test.session_state["labor_matching_resamples"] = 200
    test.session_state["labor_matching_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_alpha"] == pytest.approx(_EXPECTED_ALPHA)
    assert test.session_state["resolved_vacancy"] == pytest.approx(_EXPECTED_VACANCY)
    assert test.session_state["resolved_wage"] == pytest.approx(_EXPECTED_WAGE)
    assert test.session_state["resolved_productivity"] == pytest.approx(_EXPECTED_PRODUCTIVITY)
    assert test.session_state["resolved_initial"] == pytest.approx(_EXPECTED_INITIAL)
