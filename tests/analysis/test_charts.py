import pytest

from stlite_hello.analysis import (
    ChartHeading,
    DecileHeatmapHeading,
    KdeFitsHeading,
    SimulationReport,
    build_aic_ranking,
    build_decile_transitions,
    build_kde_with_fits,
    build_lorenz,
    build_metric_trajectories,
)


@pytest.fixture
def trajectories_heading() -> ChartHeading:
    return ChartHeading(title="Trajectories", x_label="Step", y_label="Metric")


@pytest.fixture
def lorenz_heading() -> ChartHeading:
    return ChartHeading(
        title="Lorenz",
        x_label="Cumulative population share",
        y_label="Cumulative value share",
    )


@pytest.fixture
def kde_heading() -> KdeFitsHeading:
    return KdeFitsHeading(
        title="KDE",
        x_label="Focal quantity",
        density_label="Density",
        fit_legend_label="Distribution",
    )


@pytest.fixture
def aic_heading() -> ChartHeading:
    return ChartHeading(title="AIC", x_label="Δ AIC", y_label="Distribution")


@pytest.fixture
def decile_heading() -> DecileHeatmapHeading:
    return DecileHeatmapHeading(
        title="Transitions",
        from_label="Initial decile",
        to_label="Final decile",
        probability_label="Probability",
    )


def test_metric_trajectories_chart_spec_contains_data(
    exponential_report: SimulationReport,
    trajectories_heading: ChartHeading,
) -> None:
    chart = build_metric_trajectories(exponential_report.metrics_ci_over_time, trajectories_heading)

    spec = chart.to_dict()
    assert spec["title"] == trajectories_heading.title
    assert "facet" in spec


def test_lorenz_chart_includes_equality_line(
    exponential_report: SimulationReport,
    lorenz_heading: ChartHeading,
) -> None:
    chart = build_lorenz(exponential_report.lorenz, lorenz_heading)

    spec = chart.to_dict()
    assert spec["title"] == lorenz_heading.title
    assert len(spec["layer"]) == 3


def test_kde_chart_overlays_kde_and_fits(
    exponential_report: SimulationReport,
    kde_heading: KdeFitsHeading,
) -> None:
    chart = build_kde_with_fits(exponential_report.kde, exponential_report.fitted_densities, kde_heading)

    spec = chart.to_dict()
    assert spec["title"] == kde_heading.title
    assert len(spec["layer"]) == 2


def test_aic_chart_uses_delta_aic_on_x(
    exponential_report: SimulationReport,
    aic_heading: ChartHeading,
) -> None:
    chart = build_aic_ranking(exponential_report.fits, aic_heading)

    spec = chart.to_dict()
    assert spec["title"] == aic_heading.title
    assert spec["encoding"]["x"]["field"] == "delta_aic"


def test_decile_transitions_chart_renders_heatmap(
    exponential_report: SimulationReport,
    decile_heading: DecileHeatmapHeading,
) -> None:
    chart = build_decile_transitions(exponential_report.decile_transitions, decile_heading)

    spec = chart.to_dict()
    assert spec["mark"]["type"] == "rect"
    assert spec["encoding"]["color"]["field"] == "probability"
