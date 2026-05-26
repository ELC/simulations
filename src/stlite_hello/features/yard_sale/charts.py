from typing import cast

import altair as alt
import numpy as np
import pandas as pd
from numpy.typing import NDArray
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import RunBundle

from .schemas import WEALTH_CONDENSATION_RANK_BINS, WealthCondensationData

_DEFAULT_HEIGHT = 320
_MAX_STEPS = 60


class WealthCondensationHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str
    color_label: str


def _sample_sorted_shares(
    bundle: RunBundle,
) -> tuple[NDArray[np.int64], NDArray[np.float64]]:
    stacked = np.stack(bundle.panels, axis=0)
    sorted_desc = -np.sort(-stacked, axis=2)
    n_steps_full = sorted_desc.shape[1]
    step_indices = np.linspace(0, n_steps_full - 1, num=min(_MAX_STEPS, n_steps_full), dtype=np.int64)
    sampled = sorted_desc[:, step_indices, :]
    totals = sampled.sum(axis=2, keepdims=True)
    shares = sampled / np.where(totals > 0.0, totals, 1.0)
    return step_indices, shares.astype(np.float64, copy=False)


def _mean_shares_per_bin(shares: NDArray[np.float64]) -> NDArray[np.float64]:
    n_runs, n_steps_sampled, n_agents = shares.shape
    bucket = np.minimum(
        np.arange(n_agents) // max(1, n_agents // WEALTH_CONDENSATION_RANK_BINS) + 1,
        WEALTH_CONDENSATION_RANK_BINS,
    )
    aggregated = np.zeros((n_steps_sampled, WEALTH_CONDENSATION_RANK_BINS), dtype=np.float64)
    for rank_bin in range(1, WEALTH_CONDENSATION_RANK_BINS + 1):
        mask = bucket == rank_bin
        if not mask.any():
            continue
        aggregated[:, rank_bin - 1] = shares[:, :, mask].sum(axis=(0, 2)) / float(
            mask.sum() * n_runs,
        )
    return aggregated


def aggregate_wealth_condensation(bundle: RunBundle) -> DataFrame[WealthCondensationData]:
    step_indices, shares = _sample_sorted_shares(bundle)
    mean_share = _mean_shares_per_bin(shares)
    step_grid, rank_grid = np.meshgrid(
        step_indices,
        np.arange(1, WEALTH_CONDENSATION_RANK_BINS + 1),
        indexing="ij",
    )
    frame = pd.DataFrame(
        {
            "step": step_grid.ravel().astype(np.int64),
            "rank": rank_grid.ravel().astype(np.int64),
            "wealth_share": mean_share.ravel().astype(np.float64),
        },
    )
    return DataFrame[WealthCondensationData](frame)


def build_wealth_condensation_chart(
    data: DataFrame[WealthCondensationData],
    heading: WealthCondensationHeading,
) -> alt.TopLevelMixin:
    chart = (
        alt
        .Chart(data)
        .mark_rect()
        .encode(
            x=alt.X("step:O", title=heading.x_label),
            y=alt.Y("rank:O", title=heading.y_label, sort="ascending"),
            color=alt.Color(
                "wealth_share:Q",
                title=heading.color_label,
                scale=alt.Scale(scheme="magma"),
            ),
            tooltip=["step", "rank", "wealth_share"],
        )
        .properties(title=heading.title, height=_DEFAULT_HEIGHT)
    )
    return cast("alt.TopLevelMixin", chart)
