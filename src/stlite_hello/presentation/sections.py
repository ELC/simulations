"""Streamlit-only glue for the seven body sections every simulation renders."""

from typing import cast

import altair as alt
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import (
    ChartHeading,
    DecileHeatmapHeading,
    DecileTransition,
    DistributionFit,
    FittedDensity,
    KDECurve,
    KdeFitsHeading,
    LorenzCurve,
    MetricCI,
    MetricCIOverTime,
    build_aic_ranking,
    build_decile_transitions,
    build_kde_with_fits,
    build_lorenz,
    build_metric_trajectories,
)


class PageHeader(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    icon: str
    caption: str


class ExampleCallout(BaseModel):
    model_config = ConfigDict(frozen=True)

    body: str


class MetricsTableHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    caption: str


class DownloadHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    help: str
    mime: str = "application/json"


def render_page_header(header: PageHeader) -> None:
    st.title(f"{header.icon} {header.title}")
    st.caption(header.caption)


def render_example_callout(copy: ExampleCallout) -> None:
    st.info(copy.body, icon=":material/info:")


def render_metrics_table(
    metrics: DataFrame[MetricCI],
    heading: MetricsTableHeading,
) -> None:
    st.subheader(heading.title)
    st.caption(heading.caption)
    st.dataframe(metrics, width="stretch")


def _show(chart: alt.TopLevelMixin) -> None:
    st.altair_chart(cast("alt.Chart", chart), width="stretch")


def render_metric_trajectories(
    metrics_over_time: DataFrame[MetricCIOverTime],
    heading: ChartHeading,
) -> None:
    _show(build_metric_trajectories(metrics_over_time, heading))


def render_lorenz(lorenz: DataFrame[LorenzCurve], heading: ChartHeading) -> None:
    _show(build_lorenz(lorenz, heading))


def render_kde_and_fits(
    kde: DataFrame[KDECurve],
    fitted: DataFrame[FittedDensity],
    heading: KdeFitsHeading,
) -> None:
    _show(build_kde_with_fits(kde, fitted, heading))


def render_aic_ranking(fits: DataFrame[DistributionFit], heading: ChartHeading) -> None:
    _show(build_aic_ranking(fits, heading))


def render_decile_transitions(
    transitions: DataFrame[DecileTransition],
    heading: DecileHeatmapHeading,
) -> None:
    _show(build_decile_transitions(transitions, heading))


__all__ = [
    "DownloadHeading",
    "ExampleCallout",
    "MetricsTableHeading",
    "PageHeader",
    "render_aic_ranking",
    "render_decile_transitions",
    "render_example_callout",
    "render_kde_and_fits",
    "render_lorenz",
    "render_metric_trajectories",
    "render_metrics_table",
    "render_page_header",
]
