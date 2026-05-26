import numpy as np
import pytest
from pydantic import ValidationError

from stlite_hello.features.preferential_attachment import (
    PREFERENTIAL_ATTACHMENT_DEFAULT_NODES,
    PREFERENTIAL_ATTACHMENT_DEFAULT_SEED,
    AdvancedParams,
    PreferentialAttachmentConfig,
    SimpleParams,
    final_graph,
    simulate_once,
)

_DEFAULT_ATTACH = 3


def test_simple_params_defaults_are_valid() -> None:
    params = SimpleParams()

    assert params.n_nodes == PREFERENTIAL_ATTACHMENT_DEFAULT_NODES
    assert params.m_attach == _DEFAULT_ATTACH


def test_advanced_params_rejects_zero_attach() -> None:
    with pytest.raises(ValidationError):
        AdvancedParams(m_attach=0)


def test_preferential_attachment_config_default_seed_is_distinct() -> None:
    assert PreferentialAttachmentConfig().seed == PREFERENTIAL_ATTACHMENT_DEFAULT_SEED


def test_simulate_once_panel_grows_one_row_per_arrival() -> None:
    params = AdvancedParams(n_nodes=30, m_attach=2, initial_clique=3)
    rng = np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)

    result = simulate_once(params, rng)

    expected_rows = params.n_nodes - params.initial_clique + 1
    assert result.focal_panel.shape == (expected_rows, params.n_nodes)


def test_simulate_once_is_deterministic_for_same_seed() -> None:
    params = AdvancedParams(n_nodes=30, m_attach=2, initial_clique=3)

    first = simulate_once(params, np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED))
    second = simulate_once(params, np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED))

    assert np.array_equal(first.focal_panel, second.focal_panel)


def test_simulate_once_total_degree_equals_twice_total_edges() -> None:
    params = AdvancedParams(n_nodes=30, m_attach=2, initial_clique=3)
    rng = np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)
    arrivals = params.n_nodes - params.initial_clique
    initial_edges = params.initial_clique * (params.initial_clique - 1) // 2
    expected_edges = initial_edges + arrivals * params.m_attach

    result = simulate_once(params, rng)

    final_total_degree = float(result.focal_panel[-1].sum())
    assert final_total_degree == pytest.approx(2.0 * expected_edges)


def test_final_graph_has_expected_node_and_edge_count() -> None:
    params = AdvancedParams(n_nodes=30, m_attach=2, initial_clique=3)
    rng = np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)

    graph = final_graph(params, rng)

    arrivals = params.n_nodes - params.initial_clique
    initial_edges = params.initial_clique * (params.initial_clique - 1) // 2
    expected_edges = initial_edges + arrivals * params.m_attach
    assert graph.number_of_nodes() == params.n_nodes
    assert graph.number_of_edges() == expected_edges


def test_simulate_once_rejects_attach_at_least_clique() -> None:
    params = AdvancedParams(n_nodes=20, m_attach=5, initial_clique=5)
    rng = np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)

    with pytest.raises(ValueError, match="m_attach"):
        simulate_once(params, rng)


def test_simulate_once_rejects_clique_above_node_count() -> None:
    params = AdvancedParams(n_nodes=10, m_attach=2, initial_clique=20)
    rng = np.random.default_rng(seed=PREFERENTIAL_ATTACHMENT_DEFAULT_SEED)

    with pytest.raises(ValueError, match="initial_clique"):
        simulate_once(params, rng)
