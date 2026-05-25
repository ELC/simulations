import pytest
from pandera.typing import DataFrame

from stlite_hello.features.charts import (
    WaveChartParams,
    WaveData,
    build_sine_wave_chart,
    wave_dataframe,
)


def test_wave_dataframe_has_expected_shape(default_params: WaveChartParams) -> None:
    frame = wave_dataframe(default_params)

    assert list(frame.columns) == ["x", "y"]
    assert len(frame) == default_params.points


def test_wave_dataframe_endpoints_match_sine(default_params: WaveChartParams) -> None:
    frame = wave_dataframe(default_params)

    assert frame["x"].iloc[0] == pytest.approx(0.0)
    assert frame["y"].iloc[0] == pytest.approx(0.0)
    assert frame["y"].min() == pytest.approx(-default_params.amplitude, abs=0.01)
    assert frame["y"].max() == pytest.approx(default_params.amplitude, abs=0.01)


def test_build_sine_wave_chart_embeds_wave_data(
    default_params: WaveChartParams,
    default_wave_data: DataFrame[WaveData],
) -> None:
    spec = build_sine_wave_chart(default_wave_data, params=default_params).to_dict()

    rows = spec["datasets"][spec["data"]["name"]]

    assert spec["mark"] == {"type": "line", "point": True}
    assert spec["encoding"]["x"]["field"] == "x"
    assert spec["encoding"]["y"]["field"] == "y"
    assert len(rows) == len(default_wave_data)
    assert rows[0]["y"] == pytest.approx(0.0)


def test_build_sine_wave_chart_title_reflects_params(
    title_params: WaveChartParams,
    title_wave_data: DataFrame[WaveData],
) -> None:
    chart = build_sine_wave_chart(title_wave_data, params=title_params)

    assert chart.to_dict()["title"] == (f"Sine wave ({title_params.waves} cycles, amplitude {title_params.amplitude})")
