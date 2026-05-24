import pytest
from pandera.typing import DataFrame

from stlite_hello.charts import WaveChartParams, WaveData, wave_dataframe


@pytest.fixture
def default_params() -> WaveChartParams:
    return WaveChartParams(waves=3, amplitude=1.0, points=120)


@pytest.fixture
def default_wave_data(default_params: WaveChartParams) -> DataFrame[WaveData]:
    return wave_dataframe(default_params)
