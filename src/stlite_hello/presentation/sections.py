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


class Reference(BaseModel):
    """A seminal paper / book / chapter associated with a simulation."""

    model_config = ConfigDict(frozen=True)

    citation: str
    title: str
    venue: str
    url: str


class ExampleCallout(BaseModel):
    """Rich real-world analogue narrative with seminal-paper references.

    Rendered as a highlight card at the top of every simulation page so the
    reader understands *what the abstract model maps to* before touching any
    parameter, and can dive into the original sources from a single
    expander.
    """

    model_config = ConfigDict(frozen=True)

    headline: str
    summary: str
    mechanism: str
    references_title: str
    references: tuple[Reference, ...]


class MetricsTableHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    title: str
    caption: str


class DownloadHeading(BaseModel):
    model_config = ConfigDict(frozen=True)

    label: str
    help: str
    mime: str = "application/json"


class ChartExplainer(BaseModel):
    """How-to-read narrative attached to a chart or table.

    Rendered as a collapsible expander immediately below the chart so the
    page stays scannable while still teaching the reader what to look for.
    """

    model_config = ConfigDict(frozen=True)

    expander_title: str
    how_to_read: str
    what_it_means: str


def render_page_header(header: PageHeader) -> None:
    st.title(f"{header.icon} {header.title}")
    st.caption(header.caption)


def render_example_callout(copy: ExampleCallout) -> None:
    st.info(copy.headline, icon=":material/lightbulb:")
    st.markdown(f"**The story.** {copy.summary}")
    st.markdown(f"**Why the mapping works.** {copy.mechanism}")
    with st.expander(copy.references_title):
        for reference in copy.references:
            st.markdown(
                f"- **{reference.citation}.** [{reference.title}]({reference.url}) — *{reference.venue}*.",
            )


def _render_explainer(explainer: ChartExplainer) -> None:
    with st.expander(explainer.expander_title):
        st.markdown(f"**How to read it.** {explainer.how_to_read}")
        st.markdown(f"**What it tells you.** {explainer.what_it_means}")


def render_metrics_table(
    metrics: DataFrame[MetricCI],
    heading: MetricsTableHeading,
    explainer: ChartExplainer,
) -> None:
    st.subheader(heading.title)
    st.caption(heading.caption)
    st.dataframe(metrics, width="stretch")
    _render_explainer(explainer)


def _show(chart: alt.TopLevelMixin, explainer: ChartExplainer) -> None:
    st.altair_chart(cast("alt.Chart", chart), width="stretch")
    _render_explainer(explainer)


def render_metric_trajectories(
    metrics_over_time: DataFrame[MetricCIOverTime],
    heading: ChartHeading,
    explainer: ChartExplainer,
) -> None:
    _show(build_metric_trajectories(metrics_over_time, heading), explainer)


def render_lorenz(
    lorenz: DataFrame[LorenzCurve],
    heading: ChartHeading,
    explainer: ChartExplainer,
) -> None:
    _show(build_lorenz(lorenz, heading), explainer)


def render_kde_and_fits(
    kde: DataFrame[KDECurve],
    fitted: DataFrame[FittedDensity],
    heading: KdeFitsHeading,
    explainer: ChartExplainer,
) -> None:
    _show(build_kde_with_fits(kde, fitted, heading), explainer)


def render_aic_ranking(
    fits: DataFrame[DistributionFit],
    heading: ChartHeading,
    explainer: ChartExplainer,
) -> None:
    _show(build_aic_ranking(fits, heading), explainer)


def render_decile_transitions(
    transitions: DataFrame[DecileTransition],
    heading: DecileHeatmapHeading,
    explainer: ChartExplainer,
) -> None:
    _show(build_decile_transitions(transitions, heading), explainer)


def render_special_chart_explainer(explainer: ChartExplainer) -> None:
    """Render an explainer expander below a per-feature special chart."""
    _render_explainer(explainer)


__all__ = [
    "ChartExplainer",
    "DownloadHeading",
    "ExampleCallout",
    "MetricsTableHeading",
    "PageHeader",
    "Reference",
    "render_aic_ranking",
    "render_decile_transitions",
    "render_example_callout",
    "render_kde_and_fits",
    "render_lorenz",
    "render_metric_trajectories",
    "render_metrics_table",
    "render_page_header",
    "render_special_chart_explainer",
]
