import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

LABOR_MATCHING_DEFAULT_SEED = 1_000_053
LABOR_MATCHING_FEATURE = "labor_matching"
LABOR_MATCHING_DEFAULT_WORKERS = 200
LABOR_MATCHING_DEFAULT_STEPS = 60
LABOR_MATCHING_DEFAULT_MU = 0.5
LABOR_MATCHING_DEFAULT_ALPHA = 0.5
LABOR_MATCHING_DEFAULT_SEPARATION = 0.05
LABOR_MATCHING_DEFAULT_VACANCY_RATE = 0.1
LABOR_MATCHING_DEFAULT_WAGE_SHARE = 0.5
LABOR_MATCHING_DEFAULT_PRODUCTIVITY = 1.0
LABOR_MATCHING_DEFAULT_INITIAL_EMPLOYMENT = 0.5


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_workers: int = Field(default=LABOR_MATCHING_DEFAULT_WORKERS, ge=10, le=2_000)
    n_steps: int = Field(default=LABOR_MATCHING_DEFAULT_STEPS, ge=5, le=500)
    separation_rate: float = Field(default=LABOR_MATCHING_DEFAULT_SEPARATION, gt=0.0, lt=1.0)
    matching_efficiency: float = Field(default=LABOR_MATCHING_DEFAULT_MU, gt=0.0, le=2.0)


class AdvancedParams(SimpleParams):
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
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    unemployment_rate: NDArray[np.float64]
    vacancy_rate: NDArray[np.float64]
