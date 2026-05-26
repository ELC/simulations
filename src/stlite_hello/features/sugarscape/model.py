import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

SUGARSCAPE_DEFAULT_SEED = 1_000_047
SUGARSCAPE_FEATURE = "sugarscape"
SUGARSCAPE_DEFAULT_GRID = 20
SUGARSCAPE_DEFAULT_AGENTS = 60
SUGARSCAPE_DEFAULT_STEPS = 50
SUGARSCAPE_DEFAULT_VISION = 4
SUGARSCAPE_DEFAULT_METABOLISM = 1.0
SUGARSCAPE_DEFAULT_REGROWTH = 1.0
SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT = 5.0


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_agents: int = Field(default=SUGARSCAPE_DEFAULT_AGENTS, ge=4, le=400)
    n_steps: int = Field(default=SUGARSCAPE_DEFAULT_STEPS, ge=5, le=500)
    vision: int = Field(default=SUGARSCAPE_DEFAULT_VISION, ge=1, le=10)


class AdvancedParams(SimpleParams):
    grid_size: int = Field(default=SUGARSCAPE_DEFAULT_GRID, ge=5, le=60)
    regrowth_rate: float = Field(default=SUGARSCAPE_DEFAULT_REGROWTH, gt=0.0)
    metabolism_mean: float = Field(default=SUGARSCAPE_DEFAULT_METABOLISM, gt=0.0)
    initial_endowment: float = Field(default=SUGARSCAPE_DEFAULT_INITIAL_ENDOWMENT, ge=0.0)


class SugarscapeConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=SUGARSCAPE_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


class SpatialSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    sugar_grid: NDArray[np.float64]
    agent_rows: NDArray[np.int_]
    agent_cols: NDArray[np.int_]
    agent_wealth: NDArray[np.float64]
