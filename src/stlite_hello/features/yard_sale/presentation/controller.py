"""Orchestrator: sidebar -> gated run -> sections, all typed."""

import streamlit as st

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    run_replicates,
    summarize,
)
from stlite_hello.features.yard_sale.model import YARD_SALE_FEATURE, YardSaleConfig, simulate_once
from stlite_hello.presentation import RunControlInputs, render_run_control

from . import sections
from .sidebar import SidebarInputs, build_config
from .special_chart import SpecialChartInputs, render_special_chart
from .view_models import YARD_SALE_COPY, YARD_SALE_SPECIAL_HEADING


def _run(config: YardSaleConfig) -> RunBundle:
    return run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )


def _summarize(*, config: YardSaleConfig, bundle: RunBundle) -> SimulationReport:
    return summarize(bundle=bundle, config=config)


def render() -> None:
    """Render the Yard-Sale page end-to-end."""
    copy = YARD_SALE_COPY
    sections.render_page_header(copy.page_header)
    sections.render_example_callout(copy.example)
    defaults = YardSaleConfig()
    config = build_config(SidebarInputs(defaults=defaults))
    outcome = render_run_control(
        RunControlInputs(
            feature=YARD_SALE_FEATURE,
            config=config,
            params=config.params,
            run=lambda: _run(config),
            summarize=lambda bundle: _summarize(config=config, bundle=bundle),
            labels=copy.run_control,
            download=copy.download,
        ),
    )
    if outcome is None:
        return
    bundle = outcome.bundle
    report = outcome.report
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
    render_special_chart(SpecialChartInputs(bundle=bundle, heading=YARD_SALE_SPECIAL_HEADING))


__all__ = ["render"]
