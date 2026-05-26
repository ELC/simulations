"""Frozen view-model singletons holding Cournot UI text."""

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

from .special_chart import BestResponseHeading

COURNOT_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Cournot oligopoly best-response dynamics",
        icon=":material/oil_barrel:",
        caption=(
            "N firms with heterogeneous marginal costs iterate best responses on linear inverse "
            "demand. Quantities converge to the Nash equilibrium; metrics track distance to Nash "
            "and profit dispersion."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **OPEC+ crude-oil quota negotiations** where each member sets "
            "output knowing rivals will react, sliding toward a Nash equilibrium of producer share."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-firm profit.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Iteration",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final firm profit",
            x_label="Cumulative share of firms",
            y_label="Cumulative share of profit",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-profit KDE with top-3 fitted PDFs",
            x_label="Profit",
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
        label="Cournot seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    special_chart_title="Best-response trajectory in (q1, q2) space",
)

COURNOT_SPECIAL_HEADING = BestResponseHeading(
    title="Best-response iterates and analytic lines",
    x_label="Firm A quantity",
    y_label="Firm B quantity",
    line_legend_label="Best response",
)


__all__ = ["COURNOT_COPY", "COURNOT_SPECIAL_HEADING"]
