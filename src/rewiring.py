import networkx as nx
import random

def add_edges(graph: nx.DiGraph, u, v):
    if not graph.has_edge(u, v):
        forward_edge = (u, v, {"weight": 0})
        backward_edge = (v, u, {"weight": random.uniform(0, 1)})
    else:
        forward_edge = (u, v, {"weight": graph[u][v]["weight"]})
        backward_edge = (v, u, {"weight": graph[v][u]["weight"]})

    graph.add_edges_from([forward_edge, backward_edge])
    return graph


def get_ego_graph(graph: nx.DiGraph, agent: int, hops: int) -> nx.DiGraph:
    # reverse graph and make undirected
    reversed_graph = graph.reverse(copy=True)
    return nx.ego_graph(reversed_graph, agent, radius=hops, undirected=True)
