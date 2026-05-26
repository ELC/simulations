import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle

from .model import AdvancedParams
from .schemas import SavingsWealthData
from .simulation import savings_per_agent

_DEFAULT_HEIGHT = 320


class SavingsWealthHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    rolling_label: str


def build_savings_wealth_panel(
    *,
    bundle: RunBundle,
    params: AdvancedParams,
    seed: int,
    runs: int,
) -> DataFrame[SavingsWealthData]:
    """Combine per-replicate savings draws with final wealth."""
    parent = np.random.SeedSequence(seed)
    child_seeds = parent.spawn(runs)
    pieces: list[pd.DataFrame] = []
    for run_index, seed_seq in enumerate(child_seeds):
        rng = np.random.default_rng(seed_seq)
        savings = savings_per_agent(params, rng)
        run_frame = bundle.final_population[bundle.final_population["run"] == run_index]
        pieces.append(
            pd.DataFrame(
                {
                    "run": run_frame["run"].astype(np.int64).to_numpy(),
                    "agent": run_frame["agent"].astype(np.int64).to_numpy(),
                    "savings_rate": savings.astype(np.float64),
                    "final_wealth": run_frame["value"].astype(np.float64).to_numpy(),
                },
            ),
        )
    combined = pd.concat(pieces, ignore_index=True)
    return DataFrame[SavingsWealthData](combined)


def build_savings_wealth_chart(
    data: DataFrame[SavingsWealthData],
    heading: SavingsWealthHeading,
) -> alt.TopLevelMixin:
    base = alt.Chart(data).encode(
        x=alt.X("savings_rate:Q", title=heading.x_label),
        y=alt.Y("final_wealth:Q", title=heading.y_label),
    )
    points = base.mark_circle(opacity=0.4).encode(
        tooltip=["run", "agent", "savings_rate", "final_wealth"],
    )
    rolling = (
        alt.Chart(data)
        .transform_window(
            sort=[{"field": "savings_rate"}],
            mean_wealth="mean(final_wealth)",
            frame=[-15, 15],
        )
        .mark_line(color="#ff7f0e")
        .encode(
            x=alt.X("savings_rate:Q"),
            y=alt.Y("mean_wealth:Q", title=heading.rolling_label),
        )
    )
    return alt.layer(points, rolling).properties(title=heading.title, height=_DEFAULT_HEIGHT)
