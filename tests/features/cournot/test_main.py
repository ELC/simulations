from streamlit.testing.v1 import AppTest


def test_cournot_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.cournot import main\nmain()\n",
    )

    test.run(timeout=10)

    assert not test.exception


def test_cournot_run_button_executes_simulation_and_renders_sections() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.cournot import main\nmain()\n",
    )
    test.session_state["cournot_runs"] = 2
    test.session_state["cournot_trajectory_samples"] = 4
    test.session_state["cournot_resamples"] = 200
    test.session_state["cournot_simple_firms"] = 4
    test.session_state["cournot_simple_steps"] = 15
    test.session_state["cournot_simple_inertia"] = 0.5
    test.run(timeout=10)
    test.button(key="run_outcome::cournot::button").click()

    test.run(timeout=120)

    assert not test.exception
