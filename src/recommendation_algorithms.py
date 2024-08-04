import networkx as nx
import numpy as np
from walker import random_walks
from gensim.models import Word2Vec
from gensim.utils import effective_n_jobs


def get_in_neighbours(graph: nx.DiGraph, agent: int) -> list[int]:
    return list(filter(lambda node: graph[node][agent]["weight"] > 0, graph.predecessors(agent)))


def get_out_neighbours(graph: nx.DiGraph, agent: int) -> list[int]:
    return list(filter(lambda node: graph[agent][node]["weight"] > 0, graph.successors(agent)))


def get_neighbours(graph: nx.DiGraph, agent: int) -> list[int]:
    return list(set(get_in_neighbours(graph, agent)).union(set(get_out_neighbours(graph, agent))))


def compute_jaccard_coefficient(graph: nx.DiGraph, agent: int, candidate: int) -> float:
    # get neighbours
    agent_neighbours = get_neighbours(graph, agent)
    candidate_neighbours = get_neighbours(graph, candidate)

    numerator = set(agent_neighbours).intersection(candidate_neighbours)
    denominator = set(agent_neighbours).union(candidate_neighbours)

    try:
        return len(numerator) / len(denominator)
    except ZeroDivisionError:
        return 0.0

def compute_adamic_coefficient(graph: nx.DiGraph, agent: int, candidate: int) -> float:
    # get neighbours
    agent_neighbours = get_neighbours(graph, agent)
    candidate_neighbours = get_neighbours(graph, candidate)

    common_neighbours = set(agent_neighbours).intersection(candidate_neighbours)

    total: float = 0.0

    for node in common_neighbours:
        node_neighbours = get_neighbours(graph, node)

        try:
            subtotal = 1/np.log10(len(node_neighbours))
        except ZeroDivisionError:
            subtotal = 0.0
        total += subtotal

    return total

def compute_preferential_attachment(graph: nx.DiGraph, agent: int, candidate: int) -> float:
    # get neighbours
    agent_neighbours = get_neighbours(graph, agent)
    candidate_neighbours = get_neighbours(graph, candidate)

    return len(agent_neighbours) * len(candidate_neighbours)


def compute_common_neighbours(graph: nx.DiGraph, agent: int, candidate: int) -> float:
    # get neighbours
    agent_neighbours = get_neighbours(graph, agent)
    candidate_neighbours = get_neighbours(graph, candidate)

    return len(set(agent_neighbours).intersection(set(candidate_neighbours)))

def compute_two_hops(graph: nx.DiGraph, agent: int, candidate: int) -> int:
    agent_in_neighbours = get_in_neighbours(graph, agent)
    candidate_out_neighbours = get_out_neighbours(graph, candidate)

    return len(set(agent_in_neighbours).intersection(candidate_out_neighbours))

def compute_common_followed(graph: nx.DiGraph, agent: int, candidate: int) -> int:
    agent_in_neighbours = get_in_neighbours(graph, agent)
    candidate_in_neighbours = get_in_neighbours(graph, candidate)

    return len(set(agent_in_neighbours).intersection(candidate_in_neighbours))


def compute_homophilic_node2vec(graph: nx.DiGraph, agent: int, c: int):
    p = 1
    q = 0.5
    return compute_node2vec(graph, agent, c, p, q)


def compute_structural_node2vec(graph: nx.DiGraph, agent: int, c: int):
    p = 1
    q = 2
    return compute_node2vec(graph, agent, c, p, q)


def compute_node2vec(graph: nx.DiGraph, agent: int, c: int, p: float, q: float):
    walk_length: int = 10
    dimensions: int = 64
    num_walks: int = 10
    window_size: int = 10
    # use the optimal number of workers
    workers: int = effective_n_jobs(-1)

    walks = random_walks(graph, n_walks=num_walks, walk_len=walk_length, p=p, q=q, start_nodes=[agent]).astype(int)
    walks = [list(map(str, walk)) for walk in walks]

    model = Word2Vec(walks, vector_size=dimensions, window=window_size, min_count=1, sg=1, workers=workers)
    followings = list(graph.predecessors(agent))
    return list(set(map(lambda node: int(node[0]), model.wv.most_similar(f'{agent}', topn=c))).difference([agent]+followings))


