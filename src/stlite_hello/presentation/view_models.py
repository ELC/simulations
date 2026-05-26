"""Frozen view-model BaseModels for UI text and labels."""

from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading

from .runner import RunControlLabels
from .sections import DownloadHeading, ExampleCallout, MetricsTableHeading, PageHeader
from .sidebar import AggregationSidebarLabels

DEFAULT_RUN_CONTROL_LABELS = RunControlLabels(
    run_button="Run simulation",
    idle_message="Adjust parameters in the sidebar, then click *Run simulation* to start.",
    spinner_template="Running {runs} replicates...",
    elapsed_template="Last run: {runs} replicates in {elapsed:.2f}s.",
)


class CommonChartHeadings(BaseModel):
    """Bundle of headings shared by every simulation page."""

    model_config = ConfigDict(frozen=True)

    metrics_table: MetricsTableHeading
    metric_trajectories: ChartHeading
    lorenz: ChartHeading
    kde_fits: KdeFitsHeading
    aic_ranking: ChartHeading
    decile_transitions: DecileHeatmapHeading


class SeedSliderLabels(BaseModel):
    """Labels for the per-feature seed input."""

    model_config = ConfigDict(frozen=True)

    label: str
    help: str


class AdvancedToggleLabels(BaseModel):
    """Labels for the Simple/Advanced radio."""

    model_config = ConfigDict(frozen=True)

    label: str
    simple_option: str
    advanced_option: str


class FeatureCopy(BaseModel):
    """All text shown on a single simulation page."""

    model_config = ConfigDict(frozen=True)

    page_header: PageHeader
    example: ExampleCallout
    headings: CommonChartHeadings
    download: DownloadHeading
    sidebar: AggregationSidebarLabels
    view_toggle: AdvancedToggleLabels
    seed: SeedSliderLabels
    run_control: RunControlLabels
    special_chart_title: str


__all__ = [
    "DEFAULT_RUN_CONTROL_LABELS",
    "AdvancedToggleLabels",
    "CommonChartHeadings",
    "FeatureCopy",
    "SeedSliderLabels",
]
