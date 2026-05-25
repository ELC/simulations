from streamlit.testing.v1 import AppTest


def test_home_main_renders_home_page(stlite_home_main: AppTest) -> None:
    stlite_home_main.run()

    assert not stlite_home_main.exception
    assert stlite_home_main.title[0].value == "Hello, Stlite!"
