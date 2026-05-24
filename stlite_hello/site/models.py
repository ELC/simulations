from pydantic import BaseModel, ConfigDict


class FrozenSiteModel(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)
