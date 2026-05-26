"""Orchestrator: sidebar -> analysis -> sections, all typed."""

import streamlit as st

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    run_replicates,
    summarize,
)
from stlite_hello.features.preferential_attachment.model import (
    PREFERENTIAL_ATTACHMENT_FEATURE,
    PreferentialAttachmentConfig,
    simulate_once,
)
from stlite_hello.presentation import DownloadInputs

from . import sections
from .sidebar import SidebarInputs, build_config
from .special_chart import SpecialChartInputs, render_special_chart
from .view_models import PREFERENTIAL_ATTACHMENT_COPY, PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING


def _run(config: PreferentialAttachmentConfig) -> RunBundle:
    return run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )


def _summarize(*, config: PreferentialAttachmentConfig, bundle: RunBundle) -> SimulationReport:
    return summarize(bundle=bundle, config=config)


def render() -> None:
    """Render the preferential-attachment page end-to-end."""
    copy = PREFERENTIAL_ATTACHMENT_COPY
    sections.render_page_header(copy.page_header)
    defaults = PreferentialAttachmentConfig()
    config = build_config(SidebarInputs(defaults=defaults))
    with st.spinner(f"Running {config.runs} replicates..."):
        bundle = _run(config)
        report = _summarize(config=config, bundle=bundle)
    sections.render_example_callout(copy.example)
    sections.render_metrics_table(report.metrics_ci, copy.headings.metrics_table)
    sections.render_metric_trajectories(
        report.metrics_ci_over_time,
        copy.headings.metric_trajectories,
    )
    sections.render_lorenz(report.lorenz, copy.headings.lorenz)
    sections.render_kde_and_fits(report.kde, report.fitted_densities, copy.headings.kde_fits)
    sections.render_aic_ranking(report.fits, copy.headings.aic_ranking)
    sections.render_decile_transitions(report.decile_transitions, copy.headings.decile_transitions)
    st.subheader(copy.special_chart_title)
    render_special_chart(
        SpecialChartInputs(
            params=config.params,
            seed=config.seed,
            heading=PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING,
        ),
    )
    sections.render_download(
        DownloadInputs(
            feature=PREFERENTIAL_ATTACHMENT_FEATURE,
            config=config,
            params=config.params,
            bundle=bundle,
            report=report,
            heading=copy.download,
        ),
    )


__all__ = ["render"]
