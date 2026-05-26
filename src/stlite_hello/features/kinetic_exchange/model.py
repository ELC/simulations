from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

KINETIC_DEFAULT_SEED = 1_000_033
KINETIC_FEATURE = "kinetic_exchange"
KINETIC_DEFAULT_AGENTS = 200
KINETIC_DEFAULT_STEPS = 250
KINETIC_DEFAULT_LAMBDA_MEAN = 0.5
KINETIC_DEFAULT_LAMBDA_SPREAD = 0.3
KINETIC_DEFAULT_INITIAL_WEALTH = 100.0


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=KINETIC_DEFAULT_AGENTS, ge=10, le=2_000)
    n_steps: int = Field(default=KINETIC_DEFAULT_STEPS, ge=10, le=5_000)
    lambda_mean: float = Field(default=KINETIC_DEFAULT_LAMBDA_MEAN, ge=0.0, le=1.0)


class AdvancedParams(SimpleParams):
    lambda_spread: float = Field(default=KINETIC_DEFAULT_LAMBDA_SPREAD, ge=0.0, le=1.0)
    initial_wealth: float = Field(default=KINETIC_DEFAULT_INITIAL_WEALTH, gt=0.0)


class KineticExchangeConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=KINETIC_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)
