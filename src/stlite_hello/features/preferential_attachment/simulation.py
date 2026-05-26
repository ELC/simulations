import networkx as nx
import numpy as np
from numpy.typing import NDArray

from stlite_hello.analysis import ReplicateResult

from .model import AdvancedParams


def _validate(params: AdvancedParams) -> None:
    if params.initial_clique > params.n_nodes:
        msg = "initial_clique must be <= n_nodes."
        raise ValueError(msg)
    if params.m_attach >= params.initial_clique:
        msg = "m_attach must be strictly less than initial_clique."
        raise ValueError(msg)


def _pick_targets(
    *,
    existing: int,
    degree: NDArray[np.int64],
    m: int,
    rng: np.random.Generator,
) -> NDArray[np.int_]:
    weights = degree[:existing].astype(np.float64)
    total = float(weights.sum())
    probabilities: NDArray[np.float64] = (
        np.full(existing, 1.0 / existing, dtype=np.float64) if total <= 0.0 else weights / total
    )
    return rng.choice(existing, size=m, replace=False, p=probabilities)


def _grow_graph(params: AdvancedParams, rng: np.random.Generator) -> NDArray[np.float64]:
    panel = np.zeros((params.n_nodes - params.initial_clique + 1, params.n_nodes), dtype=np.float64)
    degree = np.zeros(params.n_nodes, dtype=np.int64)
    for left in range(params.initial_clique):
        for right in range(left + 1, params.initial_clique):
            degree[left] += 1
            degree[right] += 1
    panel[0, : params.initial_clique] = degree[: params.initial_clique]
    for step, new_node in enumerate(range(params.initial_clique, params.n_nodes), start=1):
        targets = _pick_targets(existing=new_node, degree=degree, m=params.m_attach, rng=rng)
        for target in targets:
            degree[target] += 1
        degree[new_node] = params.m_attach
        panel[step] = degree
    return panel


def simulate_once(params: AdvancedParams, rng: np.random.Generator) -> ReplicateResult:
    _validate(params)
    panel = _grow_graph(params, rng)
    return ReplicateResult(
        focal_panel=panel,
        step_index=np.arange(panel.shape[0], dtype=np.int_),
    )


def final_graph(params: AdvancedParams, rng: np.random.Generator) -> nx.Graph:  # type: ignore[no-any-unimported]
    _validate(params)
    graph = nx.Graph()
    for left in range(params.initial_clique):
        for right in range(left + 1, params.initial_clique):
            graph.add_edge(left, right)
    degree = np.zeros(params.n_nodes, dtype=np.int64)
    for left, right in graph.edges():
        degree[left] += 1
        degree[right] += 1
    for new_node in range(params.initial_clique, params.n_nodes):
        targets = _pick_targets(existing=new_node, degree=degree, m=params.m_attach, rng=rng)
        for target in targets:
            graph.add_edge(new_node, int(target))
            degree[target] += 1
        degree[new_node] = params.m_attach
    return graph
