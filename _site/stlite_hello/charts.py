import altair as alt
import numpy as np
import pandas as pd
from pydantic import BaseModel, ConfigDict, Field


class WaveChartParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    waves: int
    amplitude: float
    points: int = Field(default=120)


def wave_dataframe(params: WaveChartParams) -> pd.DataFrame:
    x = np.linspace(0, 2 * np.pi, params.points)
    y = params.amplitude * np.sin(params.waves * x)
    return pd.DataFrame({"x": x, "y": y})


def build_sine_wave_chart(
    data: pd.DataFrame,
    *,
    params: WaveChartParams,
) -> alt.Chart:
    return (
        alt
        .Chart(data)
        .mark_line(point=True)
        .encode(
            x=alt.X("x:Q", title="Angle (radians)"),
            y=alt.Y("y:Q", title="Value"),
            tooltip=["x:Q", "y:Q"],
        )
        .properties(
            title=f"Sine wave ({params.waves} cycles, amplitude {params.amplitude})",
            width="container",
            height=320,
        )
        .interactive()
    )
