from streamlit.testing.v1 import AppTest


def test_kinetic_exchange_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.kinetic_exchange import main\nmain()\n",
    )
    test.session_state["kinetic_exchange_runs"] = 2
    test.session_state["kinetic_exchange_trajectory_samples"] = 4
    test.session_state["kinetic_exchange_resamples"] = 200
    test.session_state["kinetic_exchange_simple_agents"] = 12
    test.session_state["kinetic_exchange_simple_steps"] = 20

    test.run(timeout=120)

    assert not test.exception
