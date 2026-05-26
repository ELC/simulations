from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class AggregationConfig(BaseModel):
    """Knobs shared across every simulation (runs, seed, bootstrap, snapshots).
    Each feature subclasses this with its own ``params`` payload and a
    feature-specific default seed (distinct from every other feature).
    """

    model_config = ConfigDict(frozen=True)

    runs: int = Field(default=30, ge=1, le=500)
    seed: int = Field(default=...)
    trajectory_step_samples: int = Field(default=15, ge=2, le=500)
    bootstrap_resamples: int = Field(default=500, ge=200, le=20_000)
    confidence_level: float = Field(default=0.95, gt=0.0, lt=1.0)
    bootstrap_method: Literal["BCa", "percentile", "basic"] = "BCa"
