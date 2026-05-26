"""Frozen view-model singletons holding preferential-attachment UI text."""

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

from .special_chart import ZipfHeading

PREFERENTIAL_ATTACHMENT_COPY = FeatureCopy(
    page_header=PageHeader(
        title="Preferential attachment growth dynamics",
        icon=":material/hub:",
        caption=(
            "Each new node attaches to existing nodes with probability proportional to current "
            "degree. The resulting degree distribution is heavy-tailed; concentration metrics "
            "track the emergence of a few dominant hubs."
        ),
    ),
    example=ExampleCallout(
        body=(
            "Real-world analogue: **academic citation networks** where new papers cite "
            "well-cited classics with high probability, producing a small number of "
            "ultra-influential references and a long tail of niche work."
        ),
    ),
    headings=CommonChartHeadings(
        metrics_table=MetricsTableHeading(
            title="Headline metrics with bootstrap CI",
            caption="Six concentration + five mobility metrics on per-node degree.",
        ),
        metric_trajectories=ChartHeading(
            title="Metric trajectories with 95% CI band",
            x_label="Node arrivals",
            y_label="Estimate",
        ),
        lorenz=ChartHeading(
            title="Lorenz curve of final degree",
            x_label="Cumulative share of nodes",
            y_label="Cumulative share of degree",
        ),
        kde_fits=KdeFitsHeading(
            title="Final-degree KDE with top-3 fitted PDFs",
            x_label="Degree",
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
        label="Preferential-attachment seed",
        help="Deterministic seed for this simulation only.",
    ),
    special_chart_title="Zipf log-log degree-rank plot",
)

PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING = ZipfHeading(
    title="Degree vs rank on log-log axes",
    x_label="Rank (log)",
    y_label="Degree (log)",
)


__all__ = ["PREFERENTIAL_ATTACHMENT_COPY", "PREFERENTIAL_ATTACHMENT_SPECIAL_HEADING"]
