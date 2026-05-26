import pytest

from stlite_hello.features.preferential_attachment import (
    AdvancedParams,
    PreferentialAttachmentConfig,
)

_FAST_NODES = 40
_FAST_ATTACH = 2
_FAST_CLIQUE = 3
_FAST_RUNS = 4
_FAST_TRAJECTORY = 8
_FAST_RESAMPLES = 200


@pytest.fixture
def preferential_attachment_fast_params() -> AdvancedParams:
    return AdvancedParams(
        n_nodes=_FAST_NODES,
        m_attach=_FAST_ATTACH,
        initial_clique=_FAST_CLIQUE,
    )


@pytest.fixture
def preferential_attachment_fast_config(
    preferential_attachment_fast_params: AdvancedParams,
) -> PreferentialAttachmentConfig:
    return PreferentialAttachmentConfig(
        runs=_FAST_RUNS,
        trajectory_step_samples=_FAST_TRAJECTORY,
        bootstrap_resamples=_FAST_RESAMPLES,
        params=preferential_attachment_fast_params,
    )
