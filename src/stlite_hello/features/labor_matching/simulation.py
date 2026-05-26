import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams, LaborMarketHistory


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


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    """One labor-matching replicate; focal quantity is per-worker cumulative wage income."""
    panel, _ = _run_replicate(params, rng)
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(params.n_steps + 1, dtype=np.int_),
    )


def labor_market_history(params: AdvancedParams, rng: np.random.Generator) -> LaborMarketHistory:
    """Replay one replicate and return the per-step unemployment and vacancy rates."""
    _, history = _run_replicate(params, rng)
    return history
