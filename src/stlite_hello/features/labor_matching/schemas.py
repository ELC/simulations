import pandera.pandas as pa


class BeveridgeData(pa.DataFrameModel):
    step: int = pa.Field(ge=0)
    unemployment_rate: float = pa.Field(ge=0.0, le=1.0)
    vacancy_rate: float = pa.Field(ge=0.0)
