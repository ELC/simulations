from streamlit.testing.v1 import AppTest


def test_yard_sale_main_renders_without_exception() -> None:
    test = AppTest.from_string("from stlite_hello.features.yard_sale import main\nmain()\n")

    test.run(timeout=10)

    assert not test.exception


def test_yard_sale_run_button_executes_simulation_and_renders_sections() -> None:
    test = AppTest.from_string("from stlite_hello.features.yard_sale import main\nmain()\n")
    test.session_state["yard_sale_runs"] = 2
    test.session_state["yard_sale_trajectory_samples"] = 4
    test.session_state["yard_sale_resamples"] = 200
    test.session_state["yard_sale_simple_agents"] = 12
    test.session_state["yard_sale_simple_steps"] = 20
    test.run(timeout=10)
    test.button(key="run_outcome::yard_sale::button").click()

    test.run(timeout=120)

    assert not test.exception
