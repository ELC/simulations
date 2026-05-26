import numpy as np
import pytest
from numpy.typing import NDArray


@pytest.fixture
def standard_normal_samples() -> NDArray[np.float64]:
    return np.random.default_rng(0).standard_normal(size=1_000)


@pytest.fixture
def exponential_samples() -> NDArray[np.float64]:
    return np.random.default_rng(1).exponential(scale=2.0, size=2_000)


@pytest.fixture
def bootstrap_seed() -> int:
    return 42


@pytest.fixture
def bootstrap_resamples() -> int:
    return 200


@pytest.fixture
def confidence_level() -> float:
    return 0.95


@pytest.fixture
def kde_grid_size() -> int:
    return 64
