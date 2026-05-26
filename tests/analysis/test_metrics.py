import numpy as np
import pytest
from numpy.typing import NDArray

from stlite_hello.analysis.metrics import (
    bottom_to_top_rise_count,
    coefficient_of_variation,
    convergence_half_life,
    decile_transition_matrix,
    gini,
    hill_alpha,
    lorenz_curve,
    mean_tenure_from_spells,
    median_time_to_rise,
    shannon_entropy,
    top_pct_persistence_rate,
    top_pct_spells,
    top_pct_turnover_per_step,
    top_pct_turnover_rate,
    top_share,
)

_ZERO = 0.0
_ONE = 1.0
_HALF_LIFE_INDEX = 3.0
_ELEVEN_AGENT_PARETO_ALPHA = 2.5
_EXPONENTIAL_CV = 1.0
_TEN = 10
_LAST_INDEX = 2.0
_LAST_TRANSITION_INDEX = 4


def test_gini_of_equal_distribution_is_zero() -> None:
    assert gini(np.ones(10, dtype=np.float64)) == pytest.approx(_ZERO)


def test_gini_of_single_winner_is_close_to_one() -> None:
    values = np.zeros(100, dtype=np.float64)
    values[-1] = 100.0
    assert gini(values) == pytest.approx(0.99, abs=0.01)


def test_gini_returns_zero_for_empty_array() -> None:
    assert gini(np.array([], dtype=np.float64)) == pytest.approx(_ZERO)


def test_gini_returns_zero_when_total_is_zero() -> None:
    assert gini(np.zeros(5, dtype=np.float64)) == pytest.approx(_ZERO)


def test_gini_rejects_negative_values() -> None:
    with pytest.raises(ValueError, match="non-negative"):
        gini(np.array([-1.0, 2.0], dtype=np.float64))


def test_top_share_full_population_is_one() -> None:
    assert top_share(np.arange(1, 11, dtype=np.float64), fraction=1.0) == pytest.approx(_ONE)


def test_top_share_single_winner() -> None:
    values = np.zeros(100, dtype=np.float64)
    values[-1] = 50.0
    assert top_share(values, fraction=0.01) == pytest.approx(_ONE)


def test_top_share_returns_zero_for_empty() -> None:
    assert top_share(np.array([], dtype=np.float64), fraction=0.1) == pytest.approx(_ZERO)


def test_top_share_returns_zero_for_zero_total() -> None:
    assert top_share(np.zeros(10, dtype=np.float64), fraction=0.1) == pytest.approx(_ZERO)


def test_top_share_rejects_invalid_fraction() -> None:
    with pytest.raises(ValueError, match="fraction"):
        top_share(np.ones(5, dtype=np.float64), fraction=0.0)


def test_hill_alpha_recovers_pareto_index() -> None:
    rng = np.random.default_rng(0)
    samples = rng.pareto(a=_ELEVEN_AGENT_PARETO_ALPHA, size=20_000) + 1.0

    alpha = hill_alpha(samples, tail_fraction=0.05)

    assert alpha == pytest.approx(_ELEVEN_AGENT_PARETO_ALPHA, rel=0.2)


def test_hill_alpha_short_input_returns_zero() -> None:
    assert hill_alpha(np.array([1.0], dtype=np.float64)) == pytest.approx(_ZERO)


def test_hill_alpha_zero_threshold_returns_zero() -> None:
    values = np.array([0.0] * 100, dtype=np.float64)
    assert hill_alpha(values) == pytest.approx(_ZERO)


def test_hill_alpha_returns_zero_when_all_top_equal_to_threshold() -> None:
    values = np.ones(20, dtype=np.float64)
    assert hill_alpha(values) == pytest.approx(_ZERO)


def test_coefficient_of_variation_unit_normal_about_one() -> None:
    rng = np.random.default_rng(0)
    samples = rng.exponential(scale=1.0, size=5_000)

    cv = coefficient_of_variation(samples)

    assert cv == pytest.approx(_EXPONENTIAL_CV, rel=0.1)


def test_coefficient_of_variation_zero_mean_returns_zero() -> None:
    assert coefficient_of_variation(np.zeros(10, dtype=np.float64)) == pytest.approx(_ZERO)


def test_coefficient_of_variation_empty_returns_zero() -> None:
    assert coefficient_of_variation(np.array([], dtype=np.float64)) == pytest.approx(_ZERO)


def test_shannon_entropy_uniform_maximises_entropy() -> None:
    values = np.ones(10, dtype=np.float64)
    assert shannon_entropy(values) == pytest.approx(float(np.log(_TEN)), rel=1e-6)


def test_shannon_entropy_concentrated_is_zero() -> None:
    values = np.zeros(10, dtype=np.float64)
    values[0] = 1.0
    assert shannon_entropy(values) == pytest.approx(_ZERO)


def test_shannon_entropy_empty_returns_zero() -> None:
    assert shannon_entropy(np.array([], dtype=np.float64)) == pytest.approx(_ZERO)


def test_shannon_entropy_zero_total_returns_zero() -> None:
    assert shannon_entropy(np.zeros(5, dtype=np.float64)) == pytest.approx(_ZERO)


def test_convergence_half_life_hits_midpoint_index() -> None:
    trajectory = np.array([0.0, 0.2, 0.4, 0.5, 0.6, 0.8, 1.0], dtype=np.float64)
    assert convergence_half_life(trajectory, initial=0.0, final=1.0) == pytest.approx(_HALF_LIFE_INDEX)


def test_convergence_half_life_decreasing_metric() -> None:
    trajectory = np.array([1.0, 0.9, 0.7, 0.5, 0.3, 0.1, 0.0], dtype=np.float64)
    assert convergence_half_life(trajectory, initial=1.0, final=0.0) == pytest.approx(_HALF_LIFE_INDEX)


def test_convergence_half_life_no_crossing_returns_last_index() -> None:
    trajectory = np.array([0.0, 0.1, 0.2], dtype=np.float64)
    assert convergence_half_life(trajectory, initial=0.0, final=1.0) == pytest.approx(_LAST_INDEX)


def test_convergence_half_life_no_change_returns_zero() -> None:
    trajectory = np.array([0.5, 0.5, 0.5], dtype=np.float64)
    assert convergence_half_life(trajectory, initial=0.5, final=0.5) == pytest.approx(_ZERO)


def test_convergence_half_life_empty_returns_zero() -> None:
    assert convergence_half_life(np.array([], dtype=np.float64), initial=0.0, final=1.0) == pytest.approx(_ZERO)


def _winner_panel() -> NDArray[np.float64]:
    panel = np.zeros((5, 10), dtype=np.float64)
    panel[0, 0] = 1.0
    panel[1, 0] = 2.0
    panel[2, 0] = 3.0
    panel[3, 0] = 4.0
    panel[4, 0] = 5.0
    return panel


def test_top_pct_turnover_per_step_stable_winner_returns_zero() -> None:
    rates = top_pct_turnover_per_step(_winner_panel())
    assert np.array_equal(rates, np.zeros(4, dtype=np.float64))


def test_top_pct_turnover_rate_stable_winner_returns_zero() -> None:
    assert top_pct_turnover_rate(_winner_panel()) == pytest.approx(_ZERO)


def test_top_pct_persistence_rate_stable_winner_returns_one() -> None:
    assert top_pct_persistence_rate(_winner_panel()) == pytest.approx(_ONE)


def test_top_pct_turnover_per_step_single_step_returns_empty() -> None:
    panel = np.array([[1.0, 2.0, 3.0]], dtype=np.float64)
    assert top_pct_turnover_per_step(panel).size == 0


def test_top_pct_turnover_rate_single_step_returns_zero() -> None:
    panel = np.array([[1.0, 2.0]], dtype=np.float64)
    assert top_pct_turnover_rate(panel) == pytest.approx(_ZERO)


def test_top_pct_turnover_per_step_zero_agent_panel_returns_zero_rates() -> None:
    panel = np.zeros((3, 0), dtype=np.float64)

    rates = top_pct_turnover_per_step(panel)

    assert rates.shape == (2,)
    assert bool(np.all(rates == _ZERO))


def test_top_pct_turnover_per_step_full_rotation() -> None:
    panel = np.array(
        [
            [10.0, 1.0, 1.0, 1.0],
            [1.0, 10.0, 1.0, 1.0],
            [1.0, 1.0, 10.0, 1.0],
        ],
        dtype=np.float64,
    )

    rates = top_pct_turnover_per_step(panel)

    assert bool(np.all(rates == _ONE))


def test_top_pct_spells_on_empty_panel_returns_no_spells() -> None:
    spells = top_pct_spells(np.zeros((3, 0), dtype=np.float64))
    assert spells.shape[0] == 0


def test_top_pct_spells_records_durations_and_censoring() -> None:
    panel = np.array(
        [
            [5.0, 1.0],
            [4.0, 1.0],
            [1.0, 5.0],
        ],
        dtype=np.float64,
    )

    spells = top_pct_spells(panel, run_index=2)

    assert list(spells["run"]) == [2, 2]
    assert sorted(spells["agent"].tolist()) == [0, 1]
    assert spells["censored"].any()


def test_mean_tenure_from_empty_spells_returns_zero(
    equal_panel: NDArray[np.float64],
) -> None:
    empty_panel = equal_panel[:0, :]
    spells = top_pct_spells(empty_panel)

    estimate = mean_tenure_from_spells(spells)

    assert estimate.mean_lifetime == pytest.approx(_ZERO)
    assert estimate.observed_events == 0
    assert estimate.censored_events == 0


def test_mean_tenure_from_spells_uses_kaplan_meier() -> None:
    panel = np.array(
        [
            [10.0, 1.0, 1.0],
            [10.0, 1.0, 1.0],
            [1.0, 10.0, 1.0],
        ],
        dtype=np.float64,
    )
    spells = top_pct_spells(panel)

    estimate = mean_tenure_from_spells(spells)

    assert estimate.mean_lifetime > _ZERO


def _two_riser_panel() -> NDArray[np.float64]:
    initial = np.arange(1.0, 11.0, dtype=np.float64)
    after = initial.copy()
    after[0], after[-1] = after[-1], after[0]
    return np.stack([initial, after], axis=0)


def test_bottom_to_top_rise_count_detects_riser() -> None:
    assert bottom_to_top_rise_count(_two_riser_panel()) == pytest.approx(0.1)


def test_bottom_to_top_rise_count_empty_panel_returns_zero() -> None:
    assert bottom_to_top_rise_count(np.zeros((1, 5), dtype=np.float64)) == pytest.approx(_ZERO)


def test_median_time_to_rise_detects_delay() -> None:
    initial = np.arange(1.0, 11.0, dtype=np.float64)
    after = initial.copy()
    after[0], after[-1] = after[-1], after[0]
    panel = np.stack([initial, initial, after], axis=0)

    assert median_time_to_rise(panel) == pytest.approx(_LAST_INDEX)


def test_median_time_to_rise_empty_panel_returns_zero() -> None:
    assert median_time_to_rise(np.zeros((1, 5), dtype=np.float64)) == pytest.approx(_ZERO)


def test_median_time_to_rise_no_riser_returns_zero() -> None:
    panel = np.tile(np.arange(1.0, 11.0, dtype=np.float64), (3, 1))
    assert median_time_to_rise(panel) == pytest.approx(_ZERO)


def test_bottom_to_top_rise_count_no_riser_returns_zero() -> None:
    panel = np.tile(np.arange(1.0, 11.0, dtype=np.float64), (3, 1))
    assert bottom_to_top_rise_count(panel) == pytest.approx(_ZERO)


def test_lorenz_curve_equal_distribution_is_diagonal() -> None:
    lorenz = lorenz_curve(np.ones(5, dtype=np.float64))
    diagonal = lorenz["population_share"].to_numpy() == pytest.approx(lorenz["value_share"].to_numpy(), abs=1e-12)
    assert bool(np.all(diagonal))


def test_lorenz_curve_perfect_inequality_is_corner() -> None:
    values = np.zeros(100, dtype=np.float64)
    values[-1] = 100.0

    lorenz = lorenz_curve(values)

    assert lorenz["value_share"].iloc[-1] == pytest.approx(_ONE)
    assert lorenz["value_share"].iloc[-2] == pytest.approx(_ZERO)


def test_lorenz_curve_empty_returns_origin_only() -> None:
    lorenz = lorenz_curve(np.array([], dtype=np.float64))

    assert lorenz.shape[0] == 1
    assert float(lorenz["population_share"].iloc[0]) == pytest.approx(_ZERO)


def test_lorenz_curve_zero_total_has_flat_value_share() -> None:
    lorenz = lorenz_curve(np.zeros(5, dtype=np.float64))
    assert bool(np.all(lorenz["value_share"].to_numpy() == _ZERO))


def test_decile_transition_matrix_rows_sum_to_one_or_zero(
    linear_panel: NDArray[np.float64],
) -> None:
    transitions = decile_transition_matrix(linear_panel)
    matrix = transitions.pivot(index="from_decile", columns="to_decile", values="probability").to_numpy()
    row_sums = matrix.sum(axis=1)
    assert all(s == pytest.approx(_ZERO) or s == pytest.approx(_ONE) for s in row_sums)


def test_decile_transition_matrix_empty_panel_returns_zero_matrix() -> None:
    transitions = decile_transition_matrix(np.zeros((1, 0), dtype=np.float64))
    assert transitions["probability"].sum() == pytest.approx(_ZERO)


def test_top_pct_turnover_per_step_record_count_matches_steps_minus_one() -> None:
    panel = np.random.default_rng(0).exponential(1.0, size=(_LAST_TRANSITION_INDEX + 1, 50)).astype(np.float64)
    rates = top_pct_turnover_per_step(panel)
    assert rates.size == _LAST_TRANSITION_INDEX
