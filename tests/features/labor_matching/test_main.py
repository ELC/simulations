from streamlit.testing.v1 import AppTest


def test_labor_matching_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.labor_matching import main\nmain()\n",
    )
    test.session_state["labor_matching_runs"] = 2
    test.session_state["labor_matching_trajectory_samples"] = 4
    test.session_state["labor_matching_resamples"] = 200
    test.session_state["labor_matching_simple_workers"] = 40
    test.session_state["labor_matching_simple_steps"] = 15
    test.session_state["labor_matching_simple_separation"] = 0.05
    test.session_state["labor_matching_simple_efficiency"] = 0.5

    test.run(timeout=120)

    assert not test.exception
