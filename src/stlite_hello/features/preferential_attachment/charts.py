from typing import cast

import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .model import AdvancedParams
from .schemas import ZipfData
from .simulation import final_graph

_DEFAULT_HEIGHT = 360


class ZipfHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str


def build_zipf_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> DataFrame[ZipfData]:
    rng = np.random.default_rng(np.random.SeedSequence(seed).spawn(1)[0])
    graph = final_graph(params, rng)
    degrees = np.array(sorted((deg for _, deg in graph.degree()), reverse=True), dtype=np.float64)
    frame = pd.DataFrame(
        {
            "rank": np.arange(1, degrees.size + 1, dtype=np.int64),
            "degree": degrees,
        },
    )
    return DataFrame[ZipfData](frame)


def build_zipf_chart(
    *,
    data: DataFrame[ZipfData],
    heading: ZipfHeading,
) -> alt.TopLevelMixin:
    base = (
        alt
        .Chart(data)
        .mark_circle(size=40, opacity=0.7)
        .encode(
            x=alt.X("rank:Q", title=heading.x_label, scale=alt.Scale(type="log")),
            y=alt.Y("degree:Q", title=heading.y_label, scale=alt.Scale(type="log")),
            tooltip=["rank", "degree"],
        )
    )
    return cast(
        "alt.TopLevelMixin",
        base.properties(title=heading.title, height=_DEFAULT_HEIGHT),
    )
