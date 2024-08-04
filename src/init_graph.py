import networkx as nx
import random
import numpy as np

def connected_erdos_renyi_graph(size: int):
    p_c = lambda n: np.log(n)/n # critical probability to maximise probability of connectedness
    graph: nx.Graph = nx.erdos_renyi_graph(n=size, p=p_c(size))
    components = list(nx.connected_components(graph))
    components = list(map(lambda component: list(component), components))
    n_components = len(components)

    if not nx.is_connected(graph):
        for i in range(1, n_components):
            base_node = np.random.choice(components[0])
            connect_node = np.random.choice(components[i])
            graph.add_edge(base_node, connect_node)

    assert nx.is_connected(graph)
    digraph: nx.DiGraph = graph.to_directed()

    for i, j in digraph.edges:
        digraph[i][j]["weight"] = np.random.uniform()
        digraph[j][i]["weight"] = np.random.uniform()

    return digraph