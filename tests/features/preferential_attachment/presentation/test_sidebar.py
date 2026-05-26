from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 123
_EXPECTED_RUNS = 3
_EXPECTED_NODES = 50
_EXPECTED_ATTACH = 3
_EXPECTED_CLIQUE = 6

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.preferential_attachment import PreferentialAttachmentConfig
from stlite_hello.features.preferential_attachment.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=PreferentialAttachmentConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_nodes"] = config.params.n_nodes
st.session_state["resolved_attach"] = config.params.m_attach
st.session_state["resolved_clique"] = config.params.initial_clique
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["preferential_attachment_view_choice"] = "Advanced"
    test.session_state["preferential_attachment_simple_nodes"] = _EXPECTED_NODES
    test.session_state["preferential_attachment_simple_attach"] = _EXPECTED_ATTACH
    test.session_state["preferential_attachment_advanced_clique"] = _EXPECTED_CLIQUE
    test.session_state["preferential_attachment_seed_input"] = _EXPECTED_SEED
    test.session_state["preferential_attachment_runs"] = _EXPECTED_RUNS
    test.session_state["preferential_attachment_trajectory_samples"] = 5
    test.session_state["preferential_attachment_resamples"] = 200
    test.session_state["preferential_attachment_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_nodes"] == _EXPECTED_NODES
    assert test.session_state["resolved_attach"] == _EXPECTED_ATTACH
    assert test.session_state["resolved_clique"] == _EXPECTED_CLIQUE
