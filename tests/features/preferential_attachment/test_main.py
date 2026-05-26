from streamlit.testing.v1 import AppTest


def test_preferential_attachment_main_renders_without_exception() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.preferential_attachment import main\nmain()\n",
    )

    test.run(timeout=10)

    assert not test.exception


def test_preferential_attachment_run_button_executes_simulation_and_renders_sections() -> None:
    test = AppTest.from_string(
        "from stlite_hello.features.preferential_attachment import main\nmain()\n",
    )
    test.session_state["preferential_attachment_runs"] = 2
    test.session_state["preferential_attachment_trajectory_samples"] = 4
    test.session_state["preferential_attachment_resamples"] = 200
    test.session_state["preferential_attachment_simple_nodes"] = 40
    test.session_state["preferential_attachment_simple_attach"] = 2
    test.run(timeout=10)
    test.button(key="run_outcome::preferential_attachment::button").click()

    test.run(timeout=120)

    assert not test.exception
