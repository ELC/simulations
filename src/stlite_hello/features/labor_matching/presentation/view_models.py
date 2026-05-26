"""Frozen view-model singletons holding labor-matching UI text."""

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

from .special_chart import BeveridgeHeading

LABOR_MATCHING_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Labor search-and-matching dynamics",
        icon=":material/work:",
        caption=(
            "Workers and vacancies meet through a Cobb-Douglas matching function. "
            "Separations dissolve jobs at a constant rate while new vacancies open every period; "
            "earnings accrue only while employed."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **seasonal hospitality hiring in a tourist town** - inns post "
            "vacancies, prospective workers search, separations spike at the end of each season, "
            "and lifetime earnings hinge on how quickly each worker can be re-matched."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on cumulative wage income.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Step",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final wage income",
            x_label="Cumulative share of workers",
            y_label="Cumulative share of income",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-income KDE with top-3 fitted PDFs",
            x_label="Cumulative wage income",
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
        label="Labor-matching seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    special_chart_title="Beveridge curve",
)

LABOR_MATCHING_SPECIAL_HEADING = BeveridgeHeading(
    title="Beveridge curve traced through the simulation",
    x_label="Unemployment rate",
    y_label="Vacancy rate",
    step_label="Step",
)


__all__ = ["LABOR_MATCHING_COPY", "LABOR_MATCHING_SPECIAL_HEADING"]
