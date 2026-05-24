from streamlit.testing.v1 import AppTest


def test_home_page_renders_greeting(stlite_home_page: AppTest) -> None:
    stlite_home_page.run()

    assert not stlite_home_page.exception
    assert stlite_home_page.title[0].value == "Hello, Stlite!"
    assert stlite_home_page.text_input[0].value == "world"
