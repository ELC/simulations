import pandera.pandas as pa


class SpatialCellData(pa.DataFrameModel):
    row: int = pa.Field(ge=0)
    col: int = pa.Field(ge=0)
    sugar: float = pa.Field(ge=0.0)


class AgentLocationData(pa.DataFrameModel):
    row: int = pa.Field(ge=0)
    col: int = pa.Field(ge=0)
    wealth: float = pa.Field(ge=0.0)
