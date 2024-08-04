import heapq
import networkx as nx
import numpy as np
from walker import random_walks
from random_rewiring import generate_recommendations

def egocentric_random_walk(graph: nx.DiGraph, node: int, c: int) -> dict[int, float]:
    walks = random_walks(graph, n_walks=15, walk_len=10, start_nodes=[node], verbose=False)
    appearances = {}

    for walk in walks:
        for agent in walk:
            if agent != node:
                if agent not in appearances: appearances[agent] = 0
                appearances[agent] += 1

    for agent in appearances:
        appearances[agent] = appearances[agent] / (15*c*2)

    return appearances


def get_circle_of_trust(graph: nx.DiGraph, node: int, c: int) -> list[int]:
    egocentric_pq = egocentric_random_walk(graph, node, c)
    return heapq.nlargest(c, egocentric_pq, key=lambda agent: egocentric_pq[agent])


def get_authorities(graph: nx.DiGraph, hubs: list[int]) -> list[int]:
    authorities = set()

    for hub in hubs:
        followings = list(filter(lambda node: graph[node][hub]["weight"] > 0, graph.predecessors(hub)))
        authorities = authorities.union(followings)

    return list(authorities)

def create_twitter_bipartite(graph: nx.DiGraph, node: int):
    c = 50

    hubs = get_circle_of_trust(graph, node, c)
    authorities = get_authorities(graph, hubs)

    bipartite = nx.DiGraph()
    node_h: int = 0
    hubs_ = set()
    auths_ = set()

    for hub in hubs:
        node_a = graph.number_of_nodes()+1
        hubs_.add(node_h)
        for authority in authorities:
            auths_.add(node_a)
            bipartite.add_nodes_from([node_h, node_a])
            bipartite.nodes[node_h]["node-id"] = hub
            bipartite.nodes[node_a]["node-id"] = authority
            bipartite.add_edge(node_h, node_a)
            bipartite.add_edge(node_a, node_h)
            if graph.has_edge(hub, authority):
                bipartite[node_h][node_a]["weight"] = graph[hub][authority]["weight"]
                bipartite[node_a][node_h]["weight"] = graph[authority][hub]["weight"]

            node_a += 1
        node_h += 1

    return bipartite, list(hubs_), list(auths_)

def get_W(graph: nx.DiGraph, group: list[int], hubs:bool=False) -> float:
    if hubs:
        return sum(graph.out_degree(node, weight="weight") for node in group)

    return sum(graph.in_degree(node, weight="weight") for node in group)


def get_stationary_distribution(graph: nx.DiGraph, group: list[int], hubs:bool=False) -> dict[int, float]:
    W = get_W(graph, group, hubs)

    if W == 0: return {node: 0.0 for node in group}

    if hubs:
        pi = {node: graph.out_degree(node, weight="weight")/W for node in group}
    else:
        pi = {node: graph.in_degree(node, weight="weight")/W for node in group}

    return pi


def wtf(graph: nx.DiGraph, node: int, c: int) -> list[int]:
    bipartite, hubs, authorities = create_twitter_bipartite(graph, node)
    followings = list(graph.predecessors(node))

    # if the bipartite graph is not well-defined switch to random recommendations (cold-start)
    if nx.is_empty(bipartite): return generate_recommendations(graph, node, followings, c)

    # use unique stationary distribution
    pi_hubs = get_stationary_distribution(bipartite, hubs, True)
    pi_auths = get_stationary_distribution(bipartite, authorities)

    top_hubs = heapq.nlargest(c, pi_hubs.keys(), key=lambda hub: pi_hubs[hub])
    top_auths = heapq.nlargest(c, pi_auths.keys(), key=lambda auth: pi_auths[auth])

    top_hubs = list(map(lambda hub: bipartite.nodes[hub]["node-id"], top_hubs))
    top_auths = list(map(lambda auth: bipartite.nodes[auth]["node-id"], top_auths))
    top_hubs = list(filter(lambda h: h not in followings and h != node, top_hubs))
    top_auths = list(filter(lambda a: a not in followings and a != node, top_auths))
    return list(set(top_hubs).union(top_auths))





