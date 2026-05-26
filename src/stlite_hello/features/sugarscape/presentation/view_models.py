"""Frozen view-model singletons holding Sugarscape UI text."""

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

from .special_chart import SpatialHeading

SUGARSCAPE_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Sugarscape resource-foraging dynamics",
        icon=":material/grass:",
        caption=(
            "Agents on a toroidal sugar landscape search within their visual range, harvest, and "
            "pay metabolism each step. Heterogeneous metabolisms and birth positions seed the "
            "emergence of a heavy-tailed wealth distribution."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **artisanal gold panning along a watershed** - prospectors "
            "diffuse across rich seams and depleted sections; nearby deposits regenerate slowly "
            "while a few claim-holders accumulate disproportionate yields."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-agent wealth.",
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
        label="Sugarscape seed",
        help="Deterministic seed for this simulation only.",
    ),
    run_control=DEFAULT_RUN_CONTROL_LABELS,
    special_chart_title="Spatial wealth heatmap",
)

SUGARSCAPE_SPECIAL_HEADING = SpatialHeading(
    title="Final sugar landscape and agent wealth",
    row_label="Row",
    col_label="Column",
    sugar_label="Remaining sugar",
    agent_label="Agent wealth",
)


__all__ = ["SUGARSCAPE_COPY", "SUGARSCAPE_SPECIAL_HEADING"]
