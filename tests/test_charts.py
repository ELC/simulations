import altair as alt
import pandas as pd
import pandera.pandas as pa
import pytest

from stlite_hello.charts import (
    WaveChartParams,
    build_sine_wave_chart,
    wave_dataframe,
)


class WaveData(pa.DataFrameModel):
    x: float
    y: float


@pytest.fixture
def default_params() -> WaveChartParams:
    return WaveChartParams(waves=3, amplitude=1.0, points=120)


@pytest.fixture
def default_wave_data(default_params: WaveChartParams) -> pd.DataFrame:
    return wave_dataframe(default_params)


def test_wave_data_rejects_invalid_columns() -> None:
    with pytest.raises(pa.errors.SchemaError):
        WaveData.validate(pd.DataFrame({"a": [1.0]}))


def test_wave_dataframe_matches_schema(default_params: WaveChartParams) -> None:
    frame = wave_dataframe(default_params)

    WaveData.validate(frame)


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


def test_build_sine_wave_chart_returns_altair_chart(
    default_params: WaveChartParams,
    default_wave_data: pd.DataFrame,
) -> None:
    chart = build_sine_wave_chart(default_wave_data, params=default_params)

    assert isinstance(chart, alt.Chart)
    mark = chart.to_dict()["mark"]
    assert mark == "line" or mark == {"type": "line", "point": True}


def test_build_sine_wave_chart_title_reflects_params() -> None:
    params = WaveChartParams(waves=5, amplitude=1.5)

    chart = build_sine_wave_chart(wave_dataframe(params), params=params)

    title = chart.to_dict()["title"]
    assert isinstance(title, str)
    assert "5 cycles" in title
    assert "1.5" in title
