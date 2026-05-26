import pandera.pandas as pa

WEALTH_CONDENSATION_RANK_BINS = 40


class WealthCondensationData(pa.DataFrameModel):
    step: int = pa.Field(ge=0)
    rank: int = pa.Field(ge=1, le=WEALTH_CONDENSATION_RANK_BINS)
    wealth_share: float = pa.Field(ge=0.0)
