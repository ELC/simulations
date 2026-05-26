"""Local stub for :mod:`scipy.stats`.

Covers only the surface used by ``stlite_hello.analysis.adapters``.
"""

from collections.abc import Callable, Sequence
from typing import Any, Protocol

import numpy as np
from numpy.typing import NDArray

class _FrozenDistribution(Protocol):
    def pdf(self, x: NDArray[np.float64]) -> NDArray[np.float64]: ...
    def cdf(self, x: NDArray[np.float64]) -> NDArray[np.float64]: ...
    def rvs(
        self,
        size: int | tuple[int, ...] | None = ...,
        random_state: np.random.Generator | int | None = ...,
    ) -> NDArray[np.float64]: ...

class _Distribution(Protocol):
    name: str
    def __call__(self, *args: float, **kwargs: float) -> _FrozenDistribution: ...
    def pdf(self, x: NDArray[np.float64], *args: float, **kwargs: float) -> NDArray[np.float64]: ...
    def cdf(self, x: NDArray[np.float64], *args: float, **kwargs: float) -> NDArray[np.float64]: ...
    def logpdf(self, x: NDArray[np.float64], *args: float, **kwargs: float) -> NDArray[np.float64]: ...
    def fit(
        self,
        data: NDArray[np.float64],
        *args: float,
        **kwargs: Any,
    ) -> tuple[float, ...]: ...
    def rvs(
        self,
        *args: float,
        size: int | tuple[int, ...] | None = ...,
        random_state: np.random.Generator | int | None = ...,
        **kwargs: float,
    ) -> NDArray[np.float64]: ...
    @property
    def numargs(self) -> int: ...

norm: _Distribution
lognorm: _Distribution
expon: _Distribution
pareto: _Distribution
gamma: _Distribution
weibull_min: _Distribution

class _BootstrapResult(Protocol):
    @property
    def confidence_interval(self) -> tuple[float, float]: ...
    @property
    def bootstrap_distribution(self) -> NDArray[np.float64]: ...
    @property
    def standard_error(self) -> float: ...

def bootstrap(
    data: tuple[NDArray[np.float64], ...] | Sequence[NDArray[np.float64]],
    statistic: Callable[..., float] | Callable[..., NDArray[np.float64]],
    *,
    n_resamples: int = ...,
    batch: int | None = ...,
    vectorized: bool | None = ...,
    paired: bool = ...,
    confidence_level: float = ...,
    alternative: str = ...,
    method: str = ...,
    random_state: np.random.Generator | int | None = ...,
) -> _BootstrapResult: ...

class gaussian_kde:  # noqa: N801 — match scipy's class name
    def __init__(
        self,
        dataset: NDArray[np.float64],
        bw_method: str | float | Callable[["gaussian_kde"], float] | None = ...,
        weights: NDArray[np.float64] | None = ...,
    ) -> None: ...
    def __call__(self, points: NDArray[np.float64]) -> NDArray[np.float64]: ...
    def evaluate(self, points: NDArray[np.float64]) -> NDArray[np.float64]: ...
    @property
    def factor(self) -> float: ...
    @property
    def n(self) -> int: ...
