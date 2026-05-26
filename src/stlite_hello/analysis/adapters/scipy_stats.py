"""Narrow, typed wrappers around the small ``scipy.stats`` surface we use.

This module is the **only** place in the codebase that may import
:mod:`scipy`. Callers consume the typed Pydantic models exposed below.
"""

from collections.abc import Callable, Sequence
from typing import Literal, Protocol, cast

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field
from scipy import stats as _stats

DistributionName = Literal[
    "norm",
    "lognorm",
    "expon",
    "pareto",
    "gamma",
    "weibull_min",
]


class _ScipyDistribution(Protocol):
    """Structural type for the scipy distribution objects we touch."""

    def fit(self, data: NDArray[np.float64]) -> tuple[float, ...]: ...
    def logpdf(self, x: NDArray[np.float64], *args: float) -> NDArray[np.float64]: ...
    def pdf(self, x: NDArray[np.float64], *args: float) -> NDArray[np.float64]: ...
    def rvs(
        self,
        *args: float,
        size: int,
        random_state: np.random.Generator,
    ) -> NDArray[np.float64]: ...


class BootstrapCIResult(BaseModel):
    model_config = ConfigDict(frozen=True)

    estimate: float
    ci_low: float
    ci_high: float
    confidence_level: float = Field(gt=0.0, lt=1.0)
    method: Literal["BCa", "percentile", "basic"]
    standard_error: float = Field(ge=0.0)


class KDESample(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    x: NDArray[np.float64]
    density: NDArray[np.float64]


class FittedDistribution(BaseModel):
    model_config = ConfigDict(frozen=True)

    name: DistributionName
    params: tuple[float, ...]
    loglik: float


_DISTRIBUTIONS: dict[DistributionName, _ScipyDistribution] = {
    "norm": cast("_ScipyDistribution", _stats.norm),
    "lognorm": cast("_ScipyDistribution", _stats.lognorm),
    "expon": cast("_ScipyDistribution", _stats.expon),
    "pareto": cast("_ScipyDistribution", _stats.pareto),
    "gamma": cast("_ScipyDistribution", _stats.gamma),
    "weibull_min": cast("_ScipyDistribution", _stats.weibull_min),
}


def _distribution(name: DistributionName) -> _ScipyDistribution:
    return _DISTRIBUTIONS[name]


def bootstrap_ci(
    samples: NDArray[np.float64],
    statistic: Callable[[NDArray[np.float64]], float],
    *,
    n_resamples: int,
    confidence_level: float,
    method: Literal["BCa", "percentile", "basic"] = "BCa",
    seed: int,
) -> BootstrapCIResult:
    """Bootstrap CI for ``statistic(samples)`` using ``scipy.stats.bootstrap``.

    The estimate is the statistic evaluated on the original sample; the CI is
    derived from ``n_resamples`` bootstrap replicates with the given method.
    The ``seed`` makes the resampling deterministic.
    """
    random_state = np.random.default_rng(seed)
    estimate = float(statistic(samples))
    result = _stats.bootstrap(
        (samples,),
        cast("Callable[..., float]", statistic),
        n_resamples=n_resamples,
        confidence_level=confidence_level,
        method=method,
        vectorized=False,
        random_state=random_state,
    )
    low, high = result.confidence_interval
    return BootstrapCIResult(
        estimate=estimate,
        ci_low=float(low),
        ci_high=float(high),
        confidence_level=confidence_level,
        method=method,
        standard_error=float(result.standard_error),
    )


def gaussian_kde_grid(
    samples: NDArray[np.float64],
    *,
    grid_size: int,
    pad_fraction: float = 0.1,
) -> KDESample:
    """Evaluate a Gaussian KDE of ``samples`` on a uniform grid.

    Bandwidth uses Scott's rule (scipy's default). The grid spans
    ``[min - pad*range, max + pad*range]`` so the tails are visible.
    """
    if samples.size < 2:
        msg = "gaussian_kde_grid requires at least 2 samples"
        raise ValueError(msg)
    estimator = _stats.gaussian_kde(samples)
    lo = float(samples.min())
    hi = float(samples.max())
    span = hi - lo
    pad = pad_fraction * span if span > 0 else 1.0
    grid = np.linspace(lo - pad, hi + pad, grid_size, dtype=np.float64)
    density = estimator(grid)
    return KDESample(x=grid, density=density)


def fit_distribution(
    samples: NDArray[np.float64],
    *,
    name: DistributionName,
) -> FittedDistribution:
    """Fit ``samples`` to the named distribution via MLE.

    Wraps ``dist.fit`` and computes the log-likelihood for downstream AIC.
    """
    dist = _distribution(name)
    params = tuple(float(p) for p in dist.fit(samples))
    loglik = float(np.sum(dist.logpdf(samples, *params)))
    return FittedDistribution(name=name, params=params, loglik=loglik)


def pdf_values(
    fitted: FittedDistribution,
    grid: NDArray[np.float64],
) -> NDArray[np.float64]:
    """Evaluate the fitted distribution's PDF on the given grid."""
    dist = _distribution(fitted.name)
    return np.asarray(dist.pdf(grid, *fitted.params), dtype=np.float64)


def rvs_distribution(
    name: DistributionName,
    params: Sequence[float],
    *,
    size: int,
    seed: int,
) -> NDArray[np.float64]:
    """Draw ``size`` random variates from the named distribution."""
    dist = _distribution(name)
    rng = np.random.default_rng(seed)
    drawn = dist.rvs(*params, size=size, random_state=rng)
    return np.asarray(drawn, dtype=np.float64)
