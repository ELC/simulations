"""Frozen view-model BaseModels for UI text and labels."""

from pydantic import BaseModel, ConfigDict

from stlite_hello.analysis import ChartHeading, DecileHeatmapHeading, KdeFitsHeading

from .sections import DownloadHeading, ExampleCallout, MetricsTableHeading, PageHeader
from .sidebar import AggregationSidebarLabels


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
    special_chart_title: str


__all__ = [
    "AdvancedToggleLabels",
    "CommonChartHeadings",
    "FeatureCopy",
    "SeedSliderLabels",
]
