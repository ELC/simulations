from streamlit.testing.v1 import AppTest


def test_double_auction_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.double_auction import main\nmain()\n",
    )
    test.session_state["double_auction_runs"] = 2
    test.session_state["double_auction_trajectory_samples"] = 4
    test.session_state["double_auction_resamples"] = 200
    test.session_state["double_auction_simple_traders"] = 12
    test.session_state["double_auction_simple_steps"] = 20

    test.run(timeout=120)

    assert not test.exception
