# Link Recommendation Algorithms

## About
This repository encapsulates part of my undergraduate dissertation: **Link Recommendation Algorithms Affect the Virality of Social Media Influencers**. It implements a range of _link_ recommendation algorithms (where recommendations are made based on the link structure of a directed social network graph). 

Agents of the social network model are made recommendations in a random asynchronous order. During each recommendation round, an agent 'unfollows' its weakest connection with probability $1-d(i)$ and accepts each of its recommendations with probability $1/d(i)$. $d(i)$ is the number of outlinks for agent $i$. Justifications for these design choices are detailed within my undergraduate dissertation.

To simulate each recommendation algorithm, a connected and weighted directed graph is required. Within my dissertation, I decided to use a minimally connected Erdos-Renyi graph as the initial topology of the social network however, any connected, weighted and directed graph can be used.


### Note

The exact implementation of a '_Circle of Trust_' in Twitter's Who To Follow algorithm is ambiguous and in this implementation, it is interpreted as an egocentric random walk starting at the node whom recommendations are being generated for. The implementation of Twitter's Who To Follow Algorithm also assumes that the fundamental theorem of Markov Chains can be applied to the produced bipartite graph to reduce the computation time.

## Packages
- NetworkX
- [graph-walker](https://github.com/kerighan/graph-walker)
- gensim
- NumPy

## Algorithms
- Jaccard Coefficient
- Adamic Coefficient
- Preferential Attachment
- Common Neighbours
- Two Hops
- Common Followed
- Homophilic Node2Vec
- Structural Node2Vec
- Twitter's Who To Follow Service

## How To Use
Run `python src/main.py`

## References
- Grover, A. and Leskovec, J., 2016, August. node2vec: Scalable feature learning for networks. In Proceedings of the 22nd ACM SIGKDD international conference on Knowledge discovery and data mining (pp. 855-864).

- Gupta, P., Goel, A., Lin, J., Sharma, A., Wang, D. and Zadeh, R., 2013, May. Wtf: The who to follow service at twitter. In Proceedings of the 22nd international conference on World Wide Web (pp. 505-514).

- Liben-Nowell, D. and Kleinberg, J., 2003, November. The link prediction problem for social networks. In Proceedings of the twelfth international conference on Information and knowledge management (pp. 556-559).