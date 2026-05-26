import pandera.pandas as pa


class SupplyDemandData(pa.DataFrameModel):
    side: str
    quantity: int = pa.Field(ge=0)
    price: float = pa.Field(ge=0.0)
