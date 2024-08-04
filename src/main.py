import networkx as nx
from recommendations import rewiring, ra_enums
from init_graph import connected_erdos_renyi_graph
from copy import deepcopy


def simulate_recommendations(graph: nx.DiGraph) -> nx.DiGraph:
    # number of recommendations for each agent in the social network
    C = 5
    final_graphs = []
    for algorithm in ra_enums:
        graph_: nx.DiGraph = deepcopy(graph)
        graph_ = rewiring(graph_, algorithm, C)
        final_graphs.append(graph_)
    return final_graphs

GRAPH = connected_erdos_renyi_graph(1000)
graph_configs = simulate_recommendations(GRAPH)

