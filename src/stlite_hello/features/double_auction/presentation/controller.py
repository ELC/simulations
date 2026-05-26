"""Orchestrator: sidebar -> gated run -> sections, all typed."""

from typing import TYPE_CHECKING, cast

import streamlit as st

from stlite_hello.analysis import (
    RunBundle,
    SimulationReport,
    run_replicates,
    summarize,
)
from stlite_hello.features.double_auction.model import (
    DOUBLE_AUCTION_FEATURE,
    DoubleAuctionConfig,
    simulate_once,
)
from stlite_hello.presentation import RunControlInputs, render_run_control

from . import sections
from .sidebar import SidebarInputs, build_config
from .special_chart import SpecialChartInputs, render_special_chart
from .view_models import DOUBLE_AUCTION_COPY, DOUBLE_AUCTION_SPECIAL_HEADING

if TYPE_CHECKING:
    from stlite_hello.features.double_auction.model import AdvancedParams


def _run(config: DoubleAuctionConfig) -> RunBundle:
    return run_replicates(
        simulate_once=simulate_once,
        params=config.params,
        config=config,
    )


def _summarize(*, config: DoubleAuctionConfig, bundle: RunBundle) -> SimulationReport:
    return summarize(bundle=bundle, config=config)


def render() -> None:
    """Render the Double Auction page end-to-end."""
    copy = DOUBLE_AUCTION_COPY
    sections.render_page_header(copy.page_header)
    sections.render_example_callout(copy.example)
    defaults = DoubleAuctionConfig()
    config = build_config(SidebarInputs(defaults=defaults))
    outcome = render_run_control(
        RunControlInputs(
            feature=DOUBLE_AUCTION_FEATURE,
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
    render_special_chart(
        SpecialChartInputs(
            params=cast("AdvancedParams", outcome.params),
            seed=outcome.config.seed,
            heading=DOUBLE_AUCTION_SPECIAL_HEADING,
        ),
    )


__all__ = ["render"]
