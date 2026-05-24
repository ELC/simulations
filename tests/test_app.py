from streamlit.testing.v1 import AppTest


def test_main_renders_hello_world() -> None:
    app = AppTest.from_file("stlite_hello/__main__.py")
    app.run()

    assert not app.exception
    assert app.title[0].value == "Hello, Stlite!"
    assert app.text_input[0].value == "world"
