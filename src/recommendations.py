import random

import networkx as nx

from priority_queue import PriorityQueue
from salsa import wtf
from recommendation_algorithms import *
from recommendations_enum import RecommendationAlgorithm as RA
from bridge_detection import detect_bridge_nodes
from rewiring import add_edges
from random_rewiring import generate_recommendations



def get_recommendation_algorithm(algorithm: str):
    try:
        return recommendation_algorithms[algorithm]
    except KeyError:
        raise RuntimeError(f'Algorithm {algorithm} is not recognised.')

def add_to_pq(graph: nx.DiGraph, agent: int, candidate: int, pq: PriorityQueue, recommendation_algorithm):
    if candidate != agent:
        pq.enqueue(candidate, recommendation_algorithm(graph, agent, candidate))

# returns a dictionary of the top k recommendations for a user
def get_recommendations(graph: nx.DiGraph, agent: int, algorithm:str, c: int=5, hops:int=4) -> list:
    recommendation_algorithm = get_recommendation_algorithm(algorithm)
    priority_queue = PriorityQueue()
    # candidates are members of the ego graph excluding the agent and its immediate neighbours
    candidates = set(graph.nodes).difference([agent]+get_neighbours(graph, agent))

    list(map(lambda candidate: add_to_pq(graph, agent, candidate, priority_queue, recommendation_algorithm), candidates))

    recommendations = priority_queue.get_top_n(c)
    return recommendations


def accept_recommendations(graph: nx.DiGraph, agent: int, recommendations: list, p) -> list[int]:
    new_connections: list[int] = []
    for candidate in recommendations:
        # accept recommendation
        if np.random.uniform() < p:
            new_connections.append(candidate)
            graph = add_edges(graph, agent, candidate)

    return new_connections


# the probability of accepting a recommendation should be decreasing in the size of a node's neighbourhood
def get_rewiring_p(graph: nx.DiGraph, agent: int) -> float:
    return 1/len(list(graph.predecessors(agent)))


# randomly disconnect two agents, given that the graph remains weakly connected
def disconnect(graph: nx.DiGraph, agent: int, p: float, new_connections:list[int]):
    neighbours: list[int] = get_neighbours(graph, agent)
    bridge_nodes = detect_bridge_nodes(graph, agent, neighbours)
    candidates = set(neighbours).difference(bridge_nodes+new_connections+[agent])

    if candidates:
        if np.random.uniform() < (1-p):
            # disconnect the weakest connection
            candidate = min(candidates, key=lambda node: graph[agent][node]["weight"])
            graph.remove_edge(agent, candidate)
            graph.remove_edge(candidate, agent)

    assert nx.is_weakly_connected(graph)


def get_num_followings(graph: nx.DiGraph, agent: int):
    return len(list(filter(lambda node: graph[node][agent]["weight"] > 0, graph.predecessors(agent))))


def rewiring(graph: nx.DiGraph, algorithm: str="test", c:int=5) -> nx.DiGraph:
    hops = 5
    nodes = list(graph.nodes)
    random.shuffle(nodes)
    for agent in nodes:
        p = get_rewiring_p(graph, agent)

        match algorithm:
            case 'wtf':
                no_followings = get_num_followings(graph, agent)
                if no_followings < 1:
                    # Address Cold Start Problem
                    recommendations = generate_recommendations(graph, agent, list(graph.predecessors(agent)), c)
                else:
                    recommendations = wtf(graph, agent, c)
            case 'homophilic_node2vec':
                no_followings = get_num_followings(graph, agent)
                if no_followings < 1:
                    recommendations = generate_recommendations(graph, agent, list(graph.predecessors(agent)), c)
                else:
                    recommendations = compute_homophilic_node2vec(graph, agent, c)
            case 'structural_node2vec':
                no_followings = get_num_followings(graph, agent)
                if no_followings < 1:
                    recommendations = generate_recommendations(graph, agent, list(graph.predecessors(agent)), c)
                else:
                    recommendations = compute_structural_node2vec(graph, agent, c)
            case _:
                recommendations = get_recommendations(graph, agent, algorithm, c, hops)

        new_connections = accept_recommendations(graph, agent, recommendations, p)
        disconnect(graph, agent, p, new_connections)

    return graph


recommendation_algorithms = {
    'jaccard_coefficient': compute_jaccard_coefficient,
    'adamic_coefficient': compute_adamic_coefficient,
    'preferential_attachment': compute_preferential_attachment,
    'common_neighbours': compute_common_neighbours,
    'two_hops': compute_two_hops,
    'common_followed': compute_common_followed,
    'node2vec': compute_node2vec
}

ra_enums = {
    'ordinary': RA.ORDINARY,
    'random': RA.RANDOM,
    'jaccard_coefficient': RA.JACCARD,
    'adamic_coefficient': RA.ADAMIC,
    'preferential_attachment': RA.PREFERENTIAL_ATTACHMENT,
    'common_neighbours': RA.COMMON_NEIGHBOURS,
    'two_hops': RA.TWO_HOPS,
    'common_followed': RA.COMMON_FOLLOWED,
    'homophilic_node2vec': RA.HOMOPHILIC_NODE2VEC,
    'structural_node2vec': RA.STRUCTURAL_EQUIVALENCE_NODE2VEC,
    'wtf': RA.TWITTER_WTF,
}
