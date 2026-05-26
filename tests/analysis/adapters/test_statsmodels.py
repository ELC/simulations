import numpy as np
import pytest
from numpy.typing import NDArray

from stlite_hello.analysis.adapters import (
    KaplanMeierEstimate,
    kaplan_meier_mean_lifetime,
)


@pytest.fixture
def fully_observed_durations() -> NDArray[np.float64]:
    return np.array([1.0, 2.0, 3.0, 4.0, 5.0], dtype=np.float64)


@pytest.fixture
def fully_observed_events(fully_observed_durations: NDArray[np.float64]) -> NDArray[np.int_]:
    return np.ones_like(fully_observed_durations, dtype=np.int_)


@pytest.fixture
def censored_durations() -> NDArray[np.float64]:
    return np.array([2.0, 4.0, 6.0, 8.0, 10.0], dtype=np.float64)


@pytest.fixture
def censored_events() -> NDArray[np.int_]:
    return np.array([1, 1, 0, 1, 0], dtype=np.int_)


def test_kaplan_meier_recovers_mean_of_fully_observed_data(
    fully_observed_durations: NDArray[np.float64],
    fully_observed_events: NDArray[np.int_],
) -> None:
    estimate: KaplanMeierEstimate = kaplan_meier_mean_lifetime(
        durations=fully_observed_durations,
        event_observed=fully_observed_events,
    )

    assert estimate.observed_events == fully_observed_durations.size
    assert estimate.censored_events == 0
    assert estimate.mean_lifetime == pytest.approx(float(np.mean(fully_observed_durations)), abs=0.5)
    assert estimate.median_lifetime > 0.0


def test_kaplan_meier_handles_censoring(
    censored_durations: NDArray[np.float64],
    censored_events: NDArray[np.int_],
) -> None:
    expected_observed = int(censored_events.sum())
    expected_censored = censored_events.size - expected_observed

    estimate = kaplan_meier_mean_lifetime(
        durations=censored_durations,
        event_observed=censored_events,
    )

    assert estimate.observed_events == expected_observed
    assert estimate.censored_events == expected_censored
    assert estimate.mean_lifetime > 0.0


def test_kaplan_meier_with_empty_input_returns_zero() -> None:
    estimate = kaplan_meier_mean_lifetime(
        durations=np.array([], dtype=np.float64),
        event_observed=np.array([], dtype=np.int_),
    )

    assert estimate == KaplanMeierEstimate(
        mean_lifetime=0.0,
        median_lifetime=0.0,
        observed_events=0,
        censored_events=0,
    )


def test_kaplan_meier_rejects_mismatched_shapes() -> None:
    with pytest.raises(ValueError, match="same shape"):
        kaplan_meier_mean_lifetime(
            durations=np.array([1.0, 2.0], dtype=np.float64),
            event_observed=np.array([1], dtype=np.int_),
        )
