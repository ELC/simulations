import pandera.pandas as pa


class BestResponseTrajectoryData(pa.DataFrameModel):
    step: int = pa.Field(ge=0)
    q1: float = pa.Field(ge=0.0)
    q2: float = pa.Field(ge=0.0)


class BestResponseLinesData(pa.DataFrameModel):
    firm: str
    q_self: float = pa.Field(ge=0.0)
    q_other: float = pa.Field(ge=0.0)
