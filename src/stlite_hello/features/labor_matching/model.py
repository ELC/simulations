"""Mortensen-Pissarides style labor search-and-matching model."""

import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig, ReplicateResult

LABOR_MATCHING_DEFAULT_SEED = 1_000_053
LABOR_MATCHING_FEATURE = "labor_matching"
LABOR_MATCHING_DEFAULT_WORKERS = 200
LABOR_MATCHING_DEFAULT_STEPS = 80
LABOR_MATCHING_DEFAULT_MU = 0.5
LABOR_MATCHING_DEFAULT_ALPHA = 0.5
LABOR_MATCHING_DEFAULT_SEPARATION = 0.05
LABOR_MATCHING_DEFAULT_VACANCY_RATE = 0.1
LABOR_MATCHING_DEFAULT_WAGE_SHARE = 0.5
LABOR_MATCHING_DEFAULT_PRODUCTIVITY = 1.0
LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT = 0.5


class SimpleParams(BaseModel):
    """Three knobs: workers, separation rate, matching efficiency."""

    model_config = ConfigDict(frozen=True)

    n_workers: int = Field(default=LABOR_MATCHING_DEFAULT_WORKERS, ge=10, le=2_000)
    n_steps: int = Field(default=LABOR_MATCHING_DEFAULT_STEPS, ge=5, le=500)
    separation_rate: float = Field(default=LABOR_MATCHING_DEFAULT_SEPARATION, gt=0.0, lt=1.0)
    matching_efficiency: float = Field(default=LABOR_MATCHING_DEFAULT_MU, gt=0.0, le=2.0)


class AdvancedParams(SimpleParams):
    """Adds the matching elasticity, vacancy creation, wages and productivity."""

    alpha: float = Field(default=LABOR_MATCHING_DEFAULT_ALPHA, gt=0.0, lt=1.0)
    vacancy_creation_rate: float = Field(default=LABOR_MATCHING_DEFAULT_VACANCY_RATE, ge=0.0, le=1.0)
    wage_share: float = Field(default=LABOR_MATCHING_DEFAULT_WAGE_SHARE, gt=0.0, lt=1.0)
    productivity: float = Field(default=LABOR_MATCHING_DEFAULT_PRODUCTIVITY, gt=0.0)
    initial_employment: float = Field(default=LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT, ge=0.0, le=1.0)


class LaborMatchingConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=LABOR_MATCHING_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


class LaborMarketHistory(BaseModel):
    """Per-step aggregate counts used to draw the Beveridge curve."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    unemployment_rate: NDArray[np.float64]
    vacancy_rate: NDArray[np.float64]


def _initial_employment(
    *,
    n_workers: int,
    initial_employment: float,
    rng: np.random.Generator,
) -> NDArray[np.bool_]:
    target = round(initial_employment * n_workers)
    employed = np.zeros(n_workers, dtype=np.bool_)
    if target > 0:
        indices = rng.choice(n_workers, size=target, replace=False)
        employed[indices] = True
    return employed


def _step(
    *,
    employed: NDArray[np.bool_],
    earnings: NDArray[np.float64],
    vacancies: int,
    params: AdvancedParams,
    rng: np.random.Generator,
) -> int:
    unemployed_count = int(np.sum(~employed))
    if unemployed_count > 0 and vacancies > 0:
        flow = params.matching_efficiency * (unemployed_count**params.alpha) * (vacancies ** (1.0 - params.alpha))
        matches = int(min(flow, float(unemployed_count), float(vacancies)))
        if matches > 0:
            unemployed_idx = np.flatnonzero(~employed)
            chosen = rng.choice(unemployed_idx, size=matches, replace=False)
            employed[chosen] = True
            vacancies -= matches
    wage = params.wage_share * params.productivity
    earnings[employed] += wage
    separations = rng.random(size=employed.size) < params.separation_rate
    fired = employed & separations
    employed[fired] = False
    vacancies += int(np.sum(fired))
    new_vacancies = round(params.vacancy_creation_rate * employed.size)
    vacancies += new_vacancies
    return vacancies


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """One labor-matching replicate; focal quantity is per-worker cumulative wage income.

    Returns
    -------
    ReplicateResult
        Earnings panel of shape ``(n_steps + 1, n_workers)``.
    """
    panel, _ = _run_replicate(params, rng)
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )


def labor_market_history(params: AdvancedParams, rng: np.random.Generator) -> LaborMarketHistory:
    """Replay the simulation and return per-step unemployment and vacancy rates.

    Returns
    -------
    LaborMarketHistory
        Two arrays of length ``n_steps + 1`` with the aggregate rates.
    """
    _, history = _run_replicate(params, rng)
    return history


def _run_replicate(
    params: AdvancedParams,
    rng: np.random.Generator,
) -> tuple[NDArray[np.float64], LaborMarketHistory]:
    employed = _initial_employment(
        n_workers=params.n_workers,
        initial_employment=params.initial_employment,
        rng=rng,
    )
    earnings = np.zeros(params.n_workers, dtype=np.float64)
    initial_vacancies = round(params.vacancy_creation_rate * params.n_workers)
    vacancies = max(initial_vacancies, 1)
    panel = np.empty((params.n_steps + 1, params.n_workers), dtype=np.float64)
    panel[0] = earnings
    unemployment_rate = np.empty(params.n_steps + 1, dtype=np.float64)
    vacancy_rate = np.empty(params.n_steps + 1, dtype=np.float64)
    unemployment_rate[0] = 1.0 - float(employed.mean())
    vacancy_rate[0] = vacancies / params.n_workers
    for step in range(1, params.n_steps + 1):
        vacancies = _step(
            employed=employed,
            earnings=earnings,
            vacancies=vacancies,
            params=params,
            rng=rng,
        )
        panel[step] = earnings
        unemployment_rate[step] = 1.0 - float(employed.mean())
        vacancy_rate[step] = vacancies / params.n_workers
    return panel, LaborMarketHistory(
        unemployment_rate=unemployment_rate,
        vacancy_rate=vacancy_rate,
    )


__all__ = [
    "LABOR_MATCHING_DEFAULT_ALPHA",
    "LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT",
    "LABOR_MATCHING_DEFAULT_MU",
    "LABOR_MATCHING_DEFAULT_PRODUCTIVITY",
    "LABOR_MATCHING_DEFAULT_SEED",
    "LABOR_MATCHING_DEFAULT_SEPARATION",
    "LABOR_MATCHING_DEFAULT_STEPS",
    "LABOR_MATCHING_DEFAULT_VACANCY_RATE",
    "LABOR_MATCHING_DEFAULT_WAGE_SHARE",
    "LABOR_MATCHING_DEFAULT_WORKERS",
    "LABOR_MATCHING_FEATURE",
    "AdvancedParams",
    "LaborMarketHistory",
    "LaborMatchingConfig",
    "SimpleParams",
    "labor_market_history",
    "simulate_once",
]
