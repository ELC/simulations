"""Frozen view-model singletons holding Yard-Sale UI text."""

from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading
from stlite_hello.presentation import (
    AdvancedToggleLabels,
    AggregationSidebarLabels,
    CommonChartHeadings,
    DownloadHeading,
    ExampleCallout,
    FeatureCopy,
    MetricsTableHeading,
    PageHeader,
    SeedSliderLabels,
)

from .special_chart import WealthCondensationHeading

YARD_SALE_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Yard-Sale wealth exchange",
        icon=":material/savings:",
        caption=(
            "Random pairwise transfers of a fraction of the loser's wealth — a fair coin still "
            "produces emergent wealth condensation (Pareto / oligarchy)."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **commission-pool redistribution in high-turnover sales teams** "
            "where the winner of each deal absorbs a slice of the prospect's future commission, "
            "concentrating commissions among a few rainmakers over time."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics aggregated across replicates.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final wealth",
            x_label="Cumulative share of agents",
            y_label="Cumulative share of wealth",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-wealth KDE with top-3 fitted PDFs",
            x_label="Wealth",
            density_label="Density",
            fit_legend_label="Best-AIC fit",
        ),
        aic_ranking=ChartHeading(
            title="Candidate distribution AIC ranking",
            x_label="ΔAIC (lower is better)",
            y_label="Distribution",
        ),
        decile_transitions=DecileHeatmapHeading(
            title="Decile transition heatmap (initial → final)",
            from_label="Initial decile",
            to_label="Final decile",
            probability_label="Transition probability",
        ),
    ),
    download=DownloadHeading(
        label="Download run as JSON",
        help="Includes the run bundle and the full simulation report.",
    ),
    sidebar=AggregationSidebarLabels(
        expander_title="Aggregation",
        runs_label="Replicates",
        seed_label="Seed",
        confidence_label="Confidence level",
        bootstrap_resamples_label="Bootstrap resamples",
        trajectory_samples_label="Trajectory snapshots",
    ),
    view_toggle=AdvancedToggleLabels(
        label="View",
        simple_option="Simple",
        advanced_option="Advanced",
    ),
    seed=SeedSliderLabels(
        label="Yard-Sale seed",
        help="Deterministic seed for this simulation only.",
    ),
    special_chart_title="Wealth-condensation heatmap",
)

YARD_SALE_SPECIAL_HEADING = WealthCondensationHeading(
    title="Wealth-condensation heatmap (rank vs step)",
    x_label="Step",
    y_label="Rank (1 = richest)",
    color_label="Mean wealth share",
)


__all__ = ["YARD_SALE_COPY", "YARD_SALE_SPECIAL_HEADING"]
