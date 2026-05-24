from streamlit.testing.v1 import AppTest


def test_main_renders_hello_world(stlite_main_app: AppTest) -> None:
    stlite_main_app.run()

    assert not stlite_main_app.exception
    assert stlite_main_app.title[0].value == "Hello, Stlite!"
    assert stlite_main_app.text_input[0].value == "world"
