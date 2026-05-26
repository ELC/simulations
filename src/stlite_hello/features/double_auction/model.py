import numpy as np
from numpy.typing import NDArray
from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

DOUBLE_AUCTION_DEFAULT_SEED = 1_000_037
DOUBLE_AUCTION_FEATURE = "double_auction"
DOUBLE_AUCTION_DEFAULT_TRADERS = 80
DOUBLE_AUCTION_DEFAULT_STEPS = 120
DOUBLE_AUCTION_DEFAULT_VALUE_CEILING = 100.0
DOUBLE_AUCTION_DEFAULT_SHADING = 0.2


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_traders: int = Field(default=DOUBLE_AUCTION_DEFAULT_TRADERS, ge=4, le=1_000)
    n_steps: int = Field(default=DOUBLE_AUCTION_DEFAULT_STEPS, ge=10, le=2_000)
    value_ceiling: float = Field(default=DOUBLE_AUCTION_DEFAULT_VALUE_CEILING, gt=0.0)


class AdvancedParams(SimpleParams):
    shading: float = Field(default=DOUBLE_AUCTION_DEFAULT_SHADING, ge=0.0, le=0.9)
    buyer_share: float = Field(default=0.5, gt=0.0, lt=1.0)


class DoubleAuctionConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=DOUBLE_AUCTION_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)


class OrderBookSnapshot(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    bids: NDArray[np.float64]
    asks: NDArray[np.float64]
    clearing_price: float
