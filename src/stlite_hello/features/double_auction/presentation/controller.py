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
)
from stlite_hello.features.double_auction.simulation import simulate_once
from stlite_hello.features.double_auction.view_models import (
    DOUBLE_AUCTION_COPY,
    DOUBLE_AUCTION_SPECIAL_HEADING,
)
from stlite_hello.presentation import (
    render_aic_ranking,
    render_decile_transitions,
    render_example_callout,
    render_kde_and_fits,
    render_lorenz,
    render_metric_trajectories,
    render_metrics_table,
    render_page_header,
    render_run_control,
    render_special_chart_explainer,
)
from stlite_hello.view_models import RunControlInputs

from .sidebar import SidebarInputs, build_config
from .special_chart import SpecialChartInputs, render_special_chart

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
    copy = DOUBLE_AUCTION_COPY
    render_page_header(copy.page_header)
    render_example_callout(copy.example)
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
    headings = copy.headings
    explainers = copy.explainers
    render_metrics_table(report.metrics_ci, headings.metrics_table, explainers.metrics_table)
    render_metric_trajectories(
        report.metrics_ci_over_time,
        headings.metric_trajectories,
        explainers.metric_trajectories,
    )
    render_lorenz(report.lorenz, headings.lorenz, explainers.lorenz)
    render_kde_and_fits(
        report.kde,
        report.fitted_densities,
        headings.kde_fits,
        explainers.kde_fits,
    )
    render_aic_ranking(report.fits, headings.aic_ranking, explainers.aic_ranking)
    render_decile_transitions(
        report.decile_transitions,
        headings.decile_transitions,
        explainers.decile_transitions,
    )
    st.subheader(copy.special_chart_title)
    render_special_chart(
        SpecialChartInputs(
            params=cast("AdvancedParams", outcome.params),
            seed=outcome.config.seed,
            heading=DOUBLE_AUCTION_SPECIAL_HEADING,
        ),
    )
    render_special_chart_explainer(copy.special_chart_explainer)
