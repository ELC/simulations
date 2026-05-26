import altair as alt
import numpy as np
import pandas as pd
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .model import AdvancedParams
from .schemas import SupplyDemandData
from .simulation import final_orderbook

_DEFAULT_HEIGHT = 320


class SupplyDemandHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    clearing_label: str


def build_supply_demand_frame(
    *,
    params: AdvancedParams,
    seed: int,
) -> tuple[DataFrame[SupplyDemandData], float]:
    """Replay one replicate to extract the final-round supply / demand curves."""
    parent = np.random.SeedSequence(seed)
    first_child = parent.spawn(1)[0]
    rng = np.random.default_rng(first_child)
    snapshot = final_orderbook(params, rng)
    bids_desc = np.sort(snapshot.bids)[::-1]
    asks_asc = np.sort(snapshot.asks)
    demand = pd.DataFrame(
        {
            "side": np.full(bids_desc.size, "Demand"),
            "quantity": np.arange(1, bids_desc.size + 1, dtype=np.int64),
            "price": bids_desc.astype(np.float64),
        },
    )
    supply = pd.DataFrame(
        {
            "side": np.full(asks_asc.size, "Supply"),
            "quantity": np.arange(1, asks_asc.size + 1, dtype=np.int64),
            "price": asks_asc.astype(np.float64),
        },
    )
    combined = pd.concat([demand, supply], ignore_index=True)
    return DataFrame[SupplyDemandData](combined), snapshot.clearing_price


def build_supply_demand_chart(
    *,
    data: DataFrame[SupplyDemandData],
    clearing_price: float,
    heading: SupplyDemandHeading,
) -> alt.TopLevelMixin:
    curves = (
        alt.Chart(data)
        .mark_line(interpolate="step-after")
        .encode(
            x=alt.X("quantity:Q", title=heading.x_label),
            y=alt.Y("price:Q", title=heading.y_label),
            color=alt.Color("side:N"),
        )
    )
    rule = (
        alt.Chart(pd.DataFrame({"clearing": [clearing_price]}))
        .mark_rule(strokeDash=[4, 4], color="gray")
        .encode(y=alt.Y("clearing:Q", title=heading.clearing_label))
    )
    return alt.layer(curves, rule).properties(title=heading.title, height=_DEFAULT_HEIGHT)
