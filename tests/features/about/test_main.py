from streamlit.testing.v1 import AppTest


def test_about_main_renders_about_page(stlite_about_main: AppTest) -> None:
    stlite_about_main.run()

    assert not stlite_about_main.exception
    assert stlite_about_main.title[0].value == "About this demo"
