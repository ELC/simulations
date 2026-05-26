import numpy as np
import pytest

from stlite_hello.analysis import (
    AggregationConfig,
    ReplicateResult,
    SimulateOnce,
    SimulationReport,
    run_replicates,
    summarize,
)
from stlite_hello.analysis.aggregation import ParamsProtocol

_EXPECTED_HEADLINE_METRICS = 11
_EXPECTED_KDE_GRID_SIZE = 200
_TOP_FITS_OVERLAID = 3
_EMPTY_DENSITY_ROWS = 0
_ZERO = 0.0


def test_summarize_emits_eleven_headline_metrics(
    exponential_report: SimulationReport,
) -> None:
    metrics = list(exponential_report.metrics_ci["metric"])

    expected = {
        "gini",
        "top_1pct_share",
        "hill_alpha",
        "coefficient_of_variation",
        "shannon_entropy",
        "convergence_half_life",
        "top_1pct_turnover",
        "top_1pct_persistence",
        "mean_top_1pct_tenure",
        "bottom_to_top_rise_count",
        "median_time_to_rise",
    }
    assert set(metrics) == expected
    assert len(metrics) == _EXPECTED_HEADLINE_METRICS


def test_summarize_metrics_have_valid_ci_band(exponential_report: SimulationReport) -> None:
    frame = exponential_report.metrics_ci
    assert bool((frame["ci_low"] <= frame["estimate"]).all())
    assert bool((frame["estimate"] <= frame["ci_high"]).all())


def test_summarize_kde_grid_is_dense(exponential_report: SimulationReport) -> None:
    assert exponential_report.kde.shape[0] == _EXPECTED_KDE_GRID_SIZE
    assert bool((exponential_report.kde["density"] >= _ZERO).all())


def test_summarize_ranks_an_exponential_family_first_on_exponential_data(
    exponential_report: SimulationReport,
) -> None:
    top_fit = exponential_report.fits.sort_values("rank").iloc[0]

    assert top_fit["name"] in {"expon", "gamma", "weibull_min"}
    assert top_fit["delta_aic"] == pytest.approx(_ZERO)


def test_summarize_includes_top_three_densities(exponential_report: SimulationReport) -> None:
    unique_names = sorted(exponential_report.fitted_densities["name"].unique())
    assert len(unique_names) == _TOP_FITS_OVERLAID


def test_summarize_decile_transitions_form_a_probability_matrix(
    exponential_report: SimulationReport,
) -> None:
    matrix = exponential_report.decile_transitions.pivot(
        index="from_decile",
        columns="to_decile",
        values="probability",
    ).to_numpy()
    row_sums = matrix.sum(axis=1)
    assert bool(np.all((row_sums == pytest.approx(_ZERO)) | (row_sums == pytest.approx(1.0, rel=0.01))))


def test_summarize_top_pct_spells_are_non_empty(exponential_report: SimulationReport) -> None:
    assert exponential_report.top_pct_spells.shape[0] > 0
    assert bool((exponential_report.top_pct_spells["duration"] >= 1).all())


def test_summarize_metrics_over_time_includes_concentration_and_mobility(
    exponential_report: SimulationReport,
) -> None:
    metrics = set(exponential_report.metrics_ci_over_time["metric"])
    assert "gini" in metrics
    assert "top_1pct_turnover" in metrics
    assert "top_1pct_persistence" in metrics


def test_summarize_handles_empty_bundle(
    trivial_params: ParamsProtocol,
    aggregation_config: AggregationConfig,
) -> None:
    def empty_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        return ReplicateResult(
            focal_panel=np.zeros((2, 0), dtype=np.float64),
            step_index=np.arange(2, dtype=np.int_),
        )

    bundle = run_replicates(simulate_once=empty_sim, params=trivial_params, config=aggregation_config)
    report = summarize(bundle=bundle, config=aggregation_config)

    assert report.metrics_ci.shape[0] == _EXPECTED_HEADLINE_METRICS
    assert report.decile_transitions["probability"].sum() == pytest.approx(_ZERO)


def test_summarize_handles_zero_only_focal_quantity(
    trivial_params: ParamsProtocol,
    aggregation_config: AggregationConfig,
) -> None:
    def zeros_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        return ReplicateResult(
            focal_panel=np.zeros((3, 5), dtype=np.float64),
            step_index=np.arange(3, dtype=np.int_),
        )

    bundle = run_replicates(simulate_once=zeros_sim, params=trivial_params, config=aggregation_config)
    report = summarize(bundle=bundle, config=aggregation_config)

    assert bool(np.allclose(report.fits["delta_aic"].to_numpy(), _ZERO))
    assert report.fitted_densities.shape[0] == _EMPTY_DENSITY_ROWS


def test_summarize_handles_degenerate_constant_panel(
    trivial_params: ParamsProtocol,
    aggregation_config: AggregationConfig,
    exponential_simulate_once: SimulateOnce,
) -> None:
    def constant_sim(_params: ParamsProtocol, _rng: np.random.Generator) -> ReplicateResult:
        panel = np.full((6, 4), 2.0, dtype=np.float64)
        return ReplicateResult(focal_panel=panel, step_index=np.arange(6, dtype=np.int_))

    bundle = run_replicates(simulate_once=constant_sim, params=trivial_params, config=aggregation_config)
    report = summarize(bundle=bundle, config=aggregation_config)

    gini_row = report.metrics_ci[report.metrics_ci["metric"] == "gini"].iloc[0]
    assert float(gini_row["estimate"]) == pytest.approx(_ZERO)
    _ = summarize(
        bundle=run_replicates(
            simulate_once=exponential_simulate_once,
            params=trivial_params,
            config=aggregation_config,
        ),
        config=aggregation_config,
    )
