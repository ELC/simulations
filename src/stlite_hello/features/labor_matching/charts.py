import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .model import AdvancedParams
from .schemas import BeveridgeData
from .simulation import labor_market_history

_DEFAULT_HEIGHT = 360


class BeveridgeHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    step_label: str


def build_beveridge_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> DataFrame[BeveridgeData]:
    rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    history = labor_market_history(params, rng)
    frame = pd.DataFrame(
        {
            "step": np.arange(history.unemployment_rate.size, dtype=np.int64),
            "unemployment_rate": history.unemployment_rate.astype(np.float64),
            "vacancy_rate": history.vacancy_rate.astype(np.float64),
        },
    )
    return DataFrame[BeveridgeData](frame)


def build_beveridge_chart(
    *,
    data: DataFrame[BeveridgeData],
    heading: BeveridgeHeading,
) -> alt.TopLevelMixin:
    line = (
        alt
        .Chart(data)
        .mark_line(opacity=0.5)
        .encode(
            x=alt.X("unemployment_rate:Q", title=heading.x_label),
            y=alt.Y("vacancy_rate:Q", title=heading.y_label),
            order=alt.Order("step:Q"),
        )
    )
    points = (
        alt
        .Chart(data)
        .mark_circle(size=60)
        .encode(
            x=alt.X("unemployment_rate:Q"),
            y=alt.Y("vacancy_rate:Q"),
            color=alt.Color("step:Q", title=heading.step_label, scale=alt.Scale(scheme="viridis")),
            tooltip=["step", "unemployment_rate", "vacancy_rate"],
        )
    )
    return alt.layer(line, points).properties(title=heading.title, height=_DEFAULT_HEIGHT)
