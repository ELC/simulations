"""Thin re-exports of the shared section renderers, scoped to labor matching."""

from stlite_hello.presentation import (
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

__all__ = [
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
