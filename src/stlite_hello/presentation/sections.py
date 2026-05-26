from typing import cast

import altair as alt
import streamlit as st
from pandera.typing import DataFrame

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
from stlite_hello.view_models import (
    ChartExplainer,
    ExampleCallout,
    MetricsTableHeading,
    PageHeader,
)


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
    _render_explainer(explainer)
