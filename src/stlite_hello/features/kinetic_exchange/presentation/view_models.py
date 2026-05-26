"""Frozen view-model singletons holding Kinetic Exchange UI text."""

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

from .special_chart import SavingsWealthHeading

KINETIC_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Kinetic wealth exchange (with savings)",
        icon=":material/payments:",
        caption=(
            "Chakraborti-Chakrabarti pairwise updates with per-agent savings rates. "
            "Homogeneous savings produce a Gamma body; heterogeneous savings grow a Pareto tail."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **rotating-savings clubs (ROSCAs / tandas)** where each cycle a "
            "random member pockets the pooled contributions while the rest save a fixed fraction "
            "of their endowment."
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
        label="Kinetic Exchange seed",
        help="Deterministic seed for this simulation only.",
    ),
    special_chart_title="Wealth vs savings rate scatter",
)

KINETIC_SPECIAL_HEADING = SavingsWealthHeading(
    title="Final wealth vs saving propensity (with rolling mean)",
    x_label="Saving propensity λ",
    y_label="Final wealth",
    rolling_label="Rolling-mean wealth",
)


__all__ = ["KINETIC_COPY", "KINETIC_SPECIAL_HEADING"]
