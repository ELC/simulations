import pytest
from streamlit.testing.v1 import AppTest

from stlite_hello.charts import WaveChartParams


def test_charts_page_renders_wave_controls(
    stlite_charts_page: AppTest,
    default_params: WaveChartParams,
) -> None:
    stlite_charts_page.run()

    assert not stlite_charts_page.exception
    assert stlite_charts_page.title[0].value == "Wave charts"
    assert stlite_charts_page.slider[0].value == default_params.waves
    assert stlite_charts_page.slider[1].value == pytest.approx(default_params.amplitude)
