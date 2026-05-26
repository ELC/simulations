import pytest
from streamlit.testing.v1 import AppTest

_EXPECTED_SEED = 77
_EXPECTED_RUNS = 3
_EXPECTED_SHADING = 0.35
_EXPECTED_BUYER_SHARE = 0.6

_ADVANCED_SCRIPT = """
import streamlit as st
from stlite_hello.features.double_auction import DoubleAuctionConfig
from stlite_hello.features.double_auction.presentation.sidebar import (
    SidebarInputs,
    build_config,
)

config = build_config(SidebarInputs(defaults=DoubleAuctionConfig()))
st.session_state["resolved_seed"] = config.seed
st.session_state["resolved_runs"] = config.runs
st.session_state["resolved_shading"] = config.params.shading
st.session_state["resolved_buyer_share"] = config.params.buyer_share
"""


def test_sidebar_advanced_view_collects_full_advanced_params() -> None:
    test = AppTest.from_string(_ADVANCED_SCRIPT)
    test.session_state["double_auction_view_choice"] = "Advanced"
    test.session_state["double_auction_simple_traders"] = 30
    test.session_state["double_auction_simple_steps"] = 25
    test.session_state["double_auction_simple_ceiling"] = 50.0
    test.session_state["double_auction_advanced_shading"] = _EXPECTED_SHADING
    test.session_state["double_auction_advanced_buyer_share"] = _EXPECTED_BUYER_SHARE
    test.session_state["double_auction_seed_input"] = _EXPECTED_SEED
    test.session_state["double_auction_runs"] = _EXPECTED_RUNS
    test.session_state["double_auction_trajectory_samples"] = 5
    test.session_state["double_auction_resamples"] = 200
    test.session_state["double_auction_confidence"] = 0.9

    test.run(timeout=30)

    assert not test.exception
    assert test.session_state["resolved_seed"] == _EXPECTED_SEED
    assert test.session_state["resolved_runs"] == _EXPECTED_RUNS
    assert test.session_state["resolved_shading"] == pytest.approx(_EXPECTED_SHADING)
    assert test.session_state["resolved_buyer_share"] == pytest.approx(_EXPECTED_BUYER_SHARE)
