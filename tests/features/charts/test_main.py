from streamlit.testing.v1 import AppTest


def test_charts_main_renders_charts_page(stlite_charts_main: AppTest) -> None:
    stlite_charts_main.run()

    assert not stlite_charts_main.exception
    assert stlite_charts_main.title[0].value == "Wave charts"
