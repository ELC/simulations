from streamlit.testing.v1 import AppTest


def test_about_page_renders_demo_description(stlite_about_page: AppTest) -> None:
    stlite_about_page.run()

    assert not stlite_about_page.exception
    assert stlite_about_page.title[0].value == "About this demo"
