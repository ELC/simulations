import pytest
from streamlit.testing.v1 import AppTest


@pytest.fixture
def stlite_home_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.home import home_page\nhome_page()\n",
    )


@pytest.fixture
def stlite_charts_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.charts import charts_page\ncharts_page()\n",
    )


@pytest.fixture
def stlite_about_page() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.about import about_page\nabout_page()\n",
    )


@pytest.fixture
def stlite_home_main() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.home import main\nmain()\n",
    )


@pytest.fixture
def stlite_charts_main() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.charts import main\nmain()\n",
    )


@pytest.fixture
def stlite_about_main() -> AppTest:
    return AppTest.from_string(
        "from stlite_hello.features.about import main\nmain()\n",
    )
