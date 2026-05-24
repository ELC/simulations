import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def stlite_main_app() -> AppTest:
    return AppTest.from_file("stlite_hello/presentation/app.py")


@pytest.fixture
def stlite_home_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.presentation.pages import home_page\nhome_page()\n",
    )


@pytest.fixture
def stlite_charts_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.presentation.pages import charts_page\ncharts_page()\n",
    )


@pytest.fixture
def stlite_about_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.presentation.pages import about_page\nabout_page()\n",
    )
