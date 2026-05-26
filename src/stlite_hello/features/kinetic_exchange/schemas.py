import pandera.pandas as pa


class SavingsWealthData(pa.DataFrameModel):
    run: int = pa.Field(ge=0)
    agent: int = pa.Field(ge=0)
    savings_rate: float = pa.Field(ge=0.0, le=1.0)
    final_wealth: float = pa.Field(ge=0.0)
