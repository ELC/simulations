"""Shared Streamlit presentation primitives.

Every per-feature ``presentation/`` package consumes these helpers so the
seven simulation slices stay 1:1 in behaviour and minimal in glue.
"""

from .sections import (
    DownloadHeading,
    DownloadInputs,
    ExampleCallout,
    MetricsTableHeading,
    PageHeader,
    render_aic_ranking,
    render_decile_transitions,
    render_download,
    render_example_callout,
    render_kde_and_fits,
    render_lorenz,
    render_metric_trajectories,
    render_metrics_table,
    render_page_header,
)
from .sidebar import (
    AggregationSidebarInputs,
    AggregationSidebarLabels,
    build_aggregation_config,
)
from .view_models import (
    AdvancedToggleLabels,
    CommonChartHeadings,
    FeatureCopy,
    SeedSliderLabels,
)

__all__ = [
    "AdvancedToggleLabels",
    "AggregationSidebarInputs",
    "AggregationSidebarLabels",
    "CommonChartHeadings",
    "DownloadHeading",
    "DownloadInputs",
    "ExampleCallout",
    "FeatureCopy",
    "MetricsTableHeading",
    "PageHeader",
    "SeedSliderLabels",
    "build_aggregation_config",
    "render_aic_ranking",
    "render_decile_transitions",
    "render_download",
    "render_example_callout",
    "render_kde_and_fits",
    "render_lorenz",
    "render_metric_trajectories",
    "render_metrics_table",
    "render_page_header",
]
