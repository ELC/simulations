"""Streamlit-only glue for the seven body sections every simulation renders."""

from typing import cast

import altair as alt
import streamlit as st
from pandera.typing import DataFrame
from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import (
    AggregationConfig,
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
    RunBundle,
    SimulationReport,
    build_aic_ranking,
    build_decile_transitions,
    build_kde_with_fits,
    build_lorenz,
    build_metric_trajectories,
    export_filename,
    serialize_run,
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


class DownloadInputs(BaseModel):
    """Bundle of typed inputs for :func:`render_download` (avoids primitives)."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    feature: str
    config: AggregationConfig
    params: BaseModel
    bundle: RunBundle
    report: SimulationReport
    heading: DownloadHeading


def render_download(inputs: DownloadInputs) -> None:
    payload = serialize_run(
        feature=inputs.feature,
        config=inputs.config,
        params=inputs.params,
        bundle=inputs.bundle,
        report=inputs.report,
    )
    file_name = export_filename(feature=inputs.feature, config=inputs.config)
    st.download_button(
        label=inputs.heading.label,
        data=payload,
        file_name=file_name,
        mime=inputs.heading.mime,
        help=inputs.heading.help,
    )


__all__ = [
    "DownloadHeading",
    "DownloadInputs",
    "ExampleCallout",
    "MetricsTableHeading",
    "PageHeader",
    "render_aic_ranking",
    "render_decile_transitions",
    "render_download",
    "render_example_callout",
    "render_kde_and_fits",
    "render_lorenz",
    "render_metric_trajectories",
    "render_metrics_table",
    "render_page_header",
]
