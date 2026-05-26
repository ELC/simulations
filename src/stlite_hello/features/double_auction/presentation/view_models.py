"""Frozen view-model singletons holding Double Auction UI text."""

from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading
from stlite_hello.presentation import (
    DEFAULT_RUN_CONTROL_LABELS,
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

from .special_chart import SupplyDemandHeading

DOUBLE_AUCTION_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Continuous double-auction price discovery",
        icon=":material/storefront:",
        caption=(
            "Buyers and sellers post bids and asks with private values; matching is "
            "price-time-priority. Price converges to the Walrasian crossing as agents arrive."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **wholesale day-ahead electricity pools** where generators "
            "submit ask offers and retailers submit demand bids, and the market clears at the "
            "intersection price."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on cumulative trader surplus.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final trader surplus",
            x_label="Cumulative share of traders",
            y_label="Cumulative share of surplus",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-surplus KDE with top-3 fitted PDFs",
            x_label="Cumulative surplus",
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
        label="Double Auction seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    special_chart_title="Marshallian supply-demand cross (final round)",
)

DOUBLE_AUCTION_SPECIAL_HEADING = SupplyDemandHeading(
    title="Final-round supply and demand curves",
    x_label="Quantity",
    y_label="Price",
    clearing_label="Clearing price",
)


__all__ = ["DOUBLE_AUCTION_COPY", "DOUBLE_AUCTION_SPECIAL_HEADING"]
