from pydantic import BaseModel, ConfigDict, Field

from stlite_hello.analysis import AggregationConfig

PREFERENTIAL_ATTACHMENT_DEFAULT_SEED = 1_000_061
PREFERENTIAL_ATTACHMENT_FEATURE = "preferential_attachment"
PREFERENTIAL_ATTACHMENT_DEFAULT_NODES = 200
PREFERENTIAL_ATTACHMENT_DEFAULT_ATTACHMENTS = 3
PREFERENTIAL_ATTACHMENT_DEFAULT_INITIAL_CLIQUE = 5


class SimpleParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    n_nodes: int = Field(default=PREFERENTIAL_ATTACHMENT_DEFAULT_NODES, ge=10, le=2_000)
    m_attach: int = Field(default=PREFERENTIAL_ATTACHMENT_DEFAULT_ATTACHMENTS, ge=1, le=20)


class AdvancedParams(SimpleParams):
    initial_clique: int = Field(default=PREFERENTIAL_ATTACHMENT_DEFAULT_INITIAL_CLIQUE, ge=2, le=50)


class PreferentialAttachmentConfig(AggregationConfig):
    model_config = ConfigDict(frozen=True)

    seed: int = Field(default=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)
    params: AdvancedParams = Field(default_factory=AdvancedParams)
