import numpy as np
import pytest
from numpy.typing import NDArray

from stlite_hello.analysis.adapters import (
    BootstrapCIResult,
    BootstrapSettings,
    KDESample,
    bootstrap_ci,
    fit_distribution,
    gaussian_kde_grid,
    pdf_values,
    rvs_distribution,
)


@pytest.fixture
def bootstrap_settings(
    bootstrap_resamples: int,
    confidence_level: float,
    bootstrap_seed: int,
) -> BootstrapSettings:
    return BootstrapSettings(
        n_resamples=bootstrap_resamples,
        confidence_level=confidence_level,
        seed=bootstrap_seed,
    )


def test_bootstrap_ci_brackets_mean_of_standard_normal(
    standard_normal_samples: NDArray[np.float64],
    bootstrap_settings: BootstrapSettings,
) -> None:
    result: BootstrapCIResult = bootstrap_ci(
        standard_normal_samples,
        statistic=lambda data: float(np.mean(data)),
        settings=bootstrap_settings,
    )

    assert result.ci_low < result.estimate < result.ci_high
    assert result.ci_low < 0.0 < result.ci_high
    assert result.confidence_level == bootstrap_settings.confidence_level
    assert result.method == "BCa"
    assert result.standard_error >= 0.0


def test_bootstrap_ci_is_reproducible_under_same_seed(
    standard_normal_samples: NDArray[np.float64],
    bootstrap_settings: BootstrapSettings,
) -> None:
    first = bootstrap_ci(
        standard_normal_samples,
        statistic=lambda data: float(np.mean(data)),
        settings=bootstrap_settings,
    )
    second = bootstrap_ci(
        standard_normal_samples,
        statistic=lambda data: float(np.mean(data)),
        settings=bootstrap_settings,
    )

    assert first == second


def test_gaussian_kde_grid_returns_pdf_like_curve(
    standard_normal_samples: NDArray[np.float64],
    kde_grid_size: int,
) -> None:
    kde: KDESample = gaussian_kde_grid(standard_normal_samples, grid_size=kde_grid_size)

    assert kde.x.shape == (kde_grid_size,)
    assert kde.density.shape == (kde_grid_size,)
    assert np.all(kde.density >= 0.0)
    integral = float(np.trapezoid(kde.density, kde.x))
    assert integral == pytest.approx(1.0, rel=0.05)


def test_gaussian_kde_grid_rejects_singleton_sample() -> None:
    with pytest.raises(ValueError, match="at least 2 samples"):
        gaussian_kde_grid(np.array([1.0]), grid_size=8)


def test_fit_distribution_recovers_exponential_scale(
    exponential_samples: NDArray[np.float64],
) -> None:
    fitted = fit_distribution(exponential_samples, name="expon")

    loc, scale = fitted.params
    assert loc == pytest.approx(0.0, abs=0.1)
    assert scale == pytest.approx(2.0, rel=0.1)
    assert fitted.loglik < 0.0
    assert fitted.name == "expon"


def test_pdf_values_integrates_to_one(
    exponential_samples: NDArray[np.float64],
) -> None:
    fitted = fit_distribution(exponential_samples, name="expon")
    grid = np.linspace(0.0, 30.0, 4_096, dtype=np.float64)

    density = pdf_values(fitted, grid)

    assert density.shape == grid.shape
    integral = float(np.trapezoid(density, grid))
    assert integral == pytest.approx(1.0, rel=0.05)


def test_rvs_distribution_is_reproducible(
    bootstrap_seed: int,
) -> None:
    first = rvs_distribution("norm", (0.0, 1.0), size=128, seed=bootstrap_seed)
    second = rvs_distribution("norm", (0.0, 1.0), size=128, seed=bootstrap_seed)

    assert np.array_equal(first, second)


def test_rvs_distribution_pareto_returns_finite_values() -> None:
    drawn = rvs_distribution("pareto", (2.5,), size=512, seed=7)

    assert drawn.shape == (512,)
    assert np.all(np.isfinite(drawn))
    assert np.all(drawn >= 1.0)
