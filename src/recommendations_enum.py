from enum import IntEnum, auto

class RecommendationAlgorithm(IntEnum):
    ORDINARY = 0
    RANDOM = auto()
    JACCARD = auto()
    ADAMIC = auto()
    PREFERENTIAL_ATTACHMENT = auto()
    COMMON_NEIGHBOURS = auto()
    GRAPH_DISTANCE = auto()
    TWO_HOPS = auto()
    COMMON_FOLLOWED = auto()
    HOMOPHILIC_NODE2VEC = auto()
    STRUCTURAL_EQUIVALENCE_NODE2VEC = auto()
    TWITTER_WTF = auto()
    TEST = auto()

