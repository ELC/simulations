from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

COURNOT_DEFAULT_SEED = 1_000_039
COURNOT_FEATURE = "cournot"
COURNOT_DEFAULT_FIRMS = 6
COURNOT_DEFAULT_STEPS = 60
COURNOT_DEFAULT_INTERCEPT = 100.0
COURNOT_DEFAULT_SLOPE = 1.0
COURNOT_DEFAULT_COST_MEAN = 20.0
COURNOT_DEFAULT_COST_SPREAD = 10.0
COURNOT_DEFAULT_INERTIA = 0.5


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_firms: int = Field(default=COURNOT_DEFAULT_FIRMS, ge=2, le=50)
    n_steps: int = Field(default=COURNOT_DEFAULT_STEPS, ge=5, le=1_000)
    inertia: float = Field(default=COURNOT_DEFAULT_INERTIA, ge=0.0, le=0.99)


class AdvancedParams(SimpleParams):
    intercept: float = Field(default=COURNOT_DEFAULT_INTERCEPT, gt=0.0)
    slope: float = Field(default=COURNOT_DEFAULT_SLOPE, gt=0.0)
    cost_mean: float = Field(default=COURNOT_DEFAULT_COST_MEAN, ge=0.0)
    cost_spread: float = Field(default=COURNOT_DEFAULT_COST_SPREAD, ge=0.0)


class CournotConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=COURNOT_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)
