import pytest
from streamlit.testing.v1 import AppTest

import stlite_hello.__main__ as package_main
from stlite_hello import presentation
from stlite_hello.charts import WaveChartParams
from stlite_hello.presentation.app import main as presentation_main


def test_package_main_imports_presentation_main() -> None:
    assert package_main.main is presentation_main


def test_presentation_rejects_unknown_attribute() -> None:
    with pytest.raises(AttributeError, match="has no attribute 'missing'"):
        _ = presentation.missing


def test_main_renders_hello_world(stlite_main_app: AppTest) -> None:
    stlite_main_app.run()

    assert not stlite_main_app.exception
    assert stlite_main_app.title[0].value == "Hello, Stlite!"
    assert stlite_main_app.text_input[0].value == "world"


def test_charts_page_renders_wave_controls(
    stlite_charts_page: AppTest,
    default_params: WaveChartParams,
) -> None:
    stlite_charts_page.run()

    assert not stlite_charts_page.exception
    assert stlite_charts_page.title[0].value == "Wave charts"
    assert stlite_charts_page.slider[0].value == default_params.waves
    assert stlite_charts_page.slider[1].value == pytest.approx(default_params.amplitude)


def test_about_page_renders_demo_description(stlite_about_page: AppTest) -> None:
    stlite_about_page.run()

    assert not stlite_about_page.exception
    assert stlite_about_page.title[0].value == "About this demo"
