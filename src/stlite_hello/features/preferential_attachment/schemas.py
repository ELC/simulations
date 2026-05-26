import pandera.pandas as pa


class ZipfData(pa.DataFrameModel):
    rank: int = pa.Field(ge=1)
    degree: float = pa.Field(ge=0.0)
