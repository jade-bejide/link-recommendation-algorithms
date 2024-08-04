import networkx as nx
from copy import deepcopy


def detect_bridge_nodes(graph: nx.DiGraph, agent: int, candidates: list[int]) -> list[int]:
    bridge_nodes = []

    for candidate in candidates:
        if graph.has_edge(agent, candidate) and graph.has_edge(candidate, agent):
            graph_ = deepcopy(graph)
            graph_.remove_edge(agent, candidate)
            graph_.remove_edge(candidate, agent)

            if not nx.is_strongly_connected(graph_):
                bridge_nodes.append(candidate)

    return bridge_nodes
