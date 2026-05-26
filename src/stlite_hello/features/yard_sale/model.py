from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

YARD_SALE_DEFAULT_SEED = 1_000_003
YARD_SALE_FEATURE = "yard_sale"
YARD_SALE_DEFAULT_AGENTS = 200
YARD_SALE_DEFAULT_STEPS = 250
YARD_SALE_DEFAULT_FRACTION = 0.10
YARD_SALE_DEFAULT_INITIAL_WEALTH = 100.0


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=YARD_SALE_DEFAULT_AGENTS, ge=10, le=2_000)
    n_steps: int = Field(default=YARD_SALE_DEFAULT_STEPS, ge=10, le=5_000)
    transfer_fraction: float = Field(default=YARD_SALE_DEFAULT_FRACTION, gt=0.0, lt=1.0)


class AdvancedParams(SimpleParams):
    initial_wealth: float = Field(default=YARD_SALE_DEFAULT_INITIAL_WEALTH, gt=0.0)
    win_probability: float = Field(default=0.5, gt=0.0, lt=1.0)


class YardSaleConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=YARD_SALE_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)
