import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def stlite_main_app() -> AppTest:
    return AppTest.from_file("src/stlite_hello/app.py")


def test_main_renders_default_home_page(stlite_main_app: AppTest) -> None:
    stlite_main_app.run()

    assert not stlite_main_app.exception
    assert stlite_main_app.title[0].value == "Hello, Stlite!"
    assert stlite_main_app.text_input[0].value == "world"
