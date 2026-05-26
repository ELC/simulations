from streamlit.testing.v1 import AppTest


def test_sugarscape_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.sugarscape import main\nmain()\n",
    )
    test.session_state["sugarscape_runs"] = 2
    test.session_state["sugarscape_trajectory_samples"] = 4
    test.session_state["sugarscape_resamples"] = 200
    test.session_state["sugarscape_simple_agents"] = 12
    test.session_state["sugarscape_simple_steps"] = 10
    test.session_state["sugarscape_simple_vision"] = 3

    test.run(timeout=120)

    assert not test.exception
