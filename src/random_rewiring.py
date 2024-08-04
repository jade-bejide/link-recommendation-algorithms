import networkx as nx
import numpy as np
import random

from bridge_detection import detect_bridge_nodes
from rewiring import add_edges


def generate_recommendations(graph: nx.DiGraph, agent: int, predecessors: list[int], c:int):
    not_connected = set(graph.nodes)-set(predecessors+[agent])
    n = min(c, len(not_connected))
    potential_connections = list(np.random.choice(list(not_connected), size=n, replace=False))
    return potential_connections


def accept_recommendations(graph: nx.DiGraph, agent: int, p: float, recommendations: list[int]):
    accepted_recommendations = set()
    for candidate in recommendations:
        if np.random.uniform() < p:
            accepted_recommendations.add(candidate)
            graph = add_edges(graph, agent, candidate)

    return graph, accepted_recommendations


def disconnect(graph: nx.DiGraph, agent: int, new_connections: set[int], p: float):
    neighbours = list(set(graph.neighbors(agent)).difference(new_connections))

    bridge_nodes = detect_bridge_nodes(graph, agent, neighbours)
    neighbours = list(filter(lambda node: node not in bridge_nodes, neighbours))

    if neighbours:
        if np.random.uniform() < (1-p):
            disconnection_candidate = min(neighbours, key=lambda node: graph[agent][node]["weight"])
            graph.remove_edge(agent, disconnection_candidate)
            graph.remove_edge(disconnection_candidate, agent)

    assert nx.is_strongly_connected(graph)
    return graph


# k defines the number of nodes to attempt to connect to (synonymous to the number of recommendations to accept)
def random_rewire(graph: nx.DiGraph, c:int=5) -> nx.DiGraph:
    nodes = list(graph.nodes)
    random.shuffle(nodes)
    for agent in nodes:
        predecessors = list(graph.predecessors(agent))

        recommendations = generate_recommendations(graph, agent, predecessors, c)

        p = 1/len(predecessors)

        graph, accepted_recommendations = accept_recommendations(graph, agent, p, recommendations)
        # Disconnection candidates are the neighbours of agent who are not bridges
        graph = disconnect(graph, agent, accepted_recommendations, p)

    return graph

