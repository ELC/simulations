"""Pure Altair chart builders shared by every simulation.

Each function takes a Pandera-typed dataframe plus a frozen Pydantic
heading view-model and returns an ``alt.Chart``. No Streamlit imports
here; the ``presentation/`` layer of each feature renders these charts.
"""

from typing import cast

import altair as alt
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from .schemas import (
    DecileTransition,
    DistributionFit,
    FittedDensity,
    KDECurve,
    LorenzCurve,
    MetricCIOverTime,
)

_DEFAULT_HEIGHT = 320


class ChartHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    y_label: str


class KdeFitsHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    x_label: str
    density_label: str
    fit_legend_label: str


class DecileHeatmapHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    from_label: str
    to_label: str
    probability_label: str


def build_metric_trajectories(
    metrics_over_time: DataFrame[MetricCIOverTime],
    heading: ChartHeading,
) -> alt.TopLevelMixin:
    base = alt.Chart(metrics_over_time).encode(
        x=alt.X("step:Q", title=heading.x_label),
        color=alt.Color("metric:N"),
    )
    band = base.mark_area(opacity=0.25).encode(
        y=alt.Y("ci_low:Q", title=heading.y_label),
        y2=alt.Y2("ci_high:Q"),
    )
    line = base.mark_line().encode(y=alt.Y("estimate:Q", title=heading.y_label))
    layered = alt.layer(band, line).facet(
        facet=alt.Facet("metric:N", title=None),
        columns=2,
    )
    return cast("alt.TopLevelMixin", layered.properties(title=heading.title).resolve_scale(y="independent"))


def build_lorenz(lorenz: DataFrame[LorenzCurve], heading: ChartHeading) -> alt.TopLevelMixin:
    base = alt.Chart(lorenz).encode(
        x=alt.X("population_share:Q", title=heading.x_label),
        y=alt.Y("value_share:Q", title=heading.y_label),
    )
    curve = base.mark_area(opacity=0.4)
    line = base.mark_line()
    equality_data = alt.Chart(lorenz).mark_line(strokeDash=[4, 2], color="gray").encode(
        x="population_share:Q",
        y=alt.Y("population_share:Q"),
    )
    return alt.layer(curve, line, equality_data).properties(
        title=heading.title,
        height=_DEFAULT_HEIGHT,
    )


def build_kde_with_fits(
    kde: DataFrame[KDECurve],
    fitted: DataFrame[FittedDensity],
    heading: KdeFitsHeading,
) -> alt.TopLevelMixin:
    kde_chart = alt.Chart(kde).mark_area(opacity=0.35).encode(
        x=alt.X("x:Q", title=heading.x_label),
        y=alt.Y("density:Q", title=heading.density_label),
    )
    fit_chart = alt.Chart(fitted).mark_line().encode(
        x=alt.X("x:Q"),
        y=alt.Y("density:Q"),
        color=alt.Color("name:N", title=heading.fit_legend_label),
    )
    return alt.layer(kde_chart, fit_chart).properties(
        title=heading.title,
        height=_DEFAULT_HEIGHT,
    )


def build_aic_ranking(fits: DataFrame[DistributionFit], heading: ChartHeading) -> alt.TopLevelMixin:
    chart = (
        alt.Chart(fits)
        .mark_bar()
        .encode(
            x=alt.X("delta_aic:Q", title=heading.x_label),
            y=alt.Y("name:N", sort="-x", title=heading.y_label),
            color=alt.Color("rank:O", scale=alt.Scale(scheme="viridis"), legend=None),
            tooltip=["name", "aic", "delta_aic", "rank"],
        )
        .properties(title=heading.title, height=_DEFAULT_HEIGHT)
    )
    return cast("alt.TopLevelMixin", chart)


def build_decile_transitions(
    transitions: DataFrame[DecileTransition],
    heading: DecileHeatmapHeading,
) -> alt.TopLevelMixin:
    chart = (
        alt.Chart(transitions)
        .mark_rect()
        .encode(
            x=alt.X("to_decile:O", title=heading.to_label),
            y=alt.Y("from_decile:O", title=heading.from_label, sort="descending"),
            color=alt.Color("probability:Q", scale=alt.Scale(scheme="viridis"), title=heading.probability_label),
            tooltip=["from_decile", "to_decile", "probability"],
        )
        .properties(title=heading.title, height=_DEFAULT_HEIGHT)
    )
    return cast("alt.TopLevelMixin", chart)


__all__ = [
    "ChartHeading",
    "DecileHeatmapHeading",
    "KdeFitsHeading",
    "build_aic_ranking",
    "build_decile_transitions",
    "build_kde_with_fits",
    "build_lorenz",
    "build_metric_trajectories",
]
