"""Shared Streamlit presentation primitives.

Every per-feature ``presentation/`` package consumes these helpers so the
seven simulation slices stay 1:1 in behaviour and minimal in glue.
"""

from .runner import (
    RunControlInputs,
    RunControlLabels,
    SimulationOutcome,
    render_run_control,
)
from .sections import (
    DownloadHeading,
    ExampleCallout,
    MetricsTableHeading,
    PageHeader,
    render_aic_ranking,
    render_decile_transitions,
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
    DEFAULT_RUN_CONTROL_LABELS,
    AdvancedToggleLabels,
    CommonChartHeadings,
    FeatureCopy,
    SeedSliderLabels,
)

__all__ = [
    "DEFAULT_RUN_CONTROL_LABELS",
    "AdvancedToggleLabels",
    "AggregationSidebarInputs",
    "AggregationSidebarLabels",
    "CommonChartHeadings",
    "DownloadHeading",
    "ExampleCallout",
    "FeatureCopy",
    "MetricsTableHeading",
    "PageHeader",
    "RunControlInputs",
    "RunControlLabels",
    "SeedSliderLabels",
    "SimulationOutcome",
    "build_aggregation_config",
    "render_aic_ranking",
    "render_decile_transitions",
    "render_example_callout",
    "render_kde_and_fits",
    "render_lorenz",
    "render_metric_trajectories",
    "render_metrics_table",
    "render_page_header",
    "render_run_control",
]
