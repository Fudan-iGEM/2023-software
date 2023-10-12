Fudan iGEM 2022 witnessed the success of [PartHub](https://2022.igem.wiki/fudan/software), so this year we gathered feedback from PartHub users (Fudan iGEM 2022 team members and other iGEMers and some judges in 2022 Grand Jamboree), resolved known issues, and launched the brand new PartHub 2! Compared to Parthub, PartHub 2 has several new features:

- Update with 2022 iGEM Registry of Standard Biological Parts. Parthub 2 contains over 60,000 Parts, which is a huge leap up from Parthub.
- Improve the user interaction interface to further simplify the process of usage. PartHub 2 incorporates feedback and suggestions from PartHub users, removes unnecessary options and starts developing recommendation algorithms.
- Design a diversified recommendation algorithm based on graph algorithm. We developed a diversified recommendation algorithm based on PageRank and [Louvain method](https://en.wikipedia.org/wiki/Louvain_method) to prioritize the appearance of more significant parts in the search results and avoid the recurrence of similar parts.

The core of PartHub 2 is the graph model based on the Registry of Standard Biological Parts. For each Part, in addition to the attributes (like name, sequence etc.) it carries, there are two types of relationships with other nodes: "twins" and "refers to". The "twins" are undirected, while the "refers to" are directed; each is a data structure known as graph, and their relationships may be represented by an adjacency matrix. PageRank and [Louvain method](https://en.wikipedia.org/wiki/Louvain_method) is based on this graph model. [PageRank](https://en.wikipedia.org/wiki/PageRank) reflects how actively a Part is used and Louvain enables community detection of similar Parts.

We provide a summary of the notation.

| Variable  | Description                                                  |
| --------- | ------------------------------------------------------------ |
| $d$       | damping factor which can be set between 0 (inclusive) and 1 (exclusive) |
| $Q$       | modularity of a graph                                        |
| $k_i,k_j$ | the sum of the weights of the edges attached to $community_i$ and $community_j$ |
| $m$       | sum of all of the edge weights in the graph                  |
| $c_i,c_j$ | communities of the nodes                                     |

## PageRank

The PageRank algorithm[^1] evaluates the relevance of each node in the network based on the number of incoming relationships and the importance of the associated source nodes. In general, the underlying notion is that a node is only as important as the nodes that link to it. We assume that a node $A$ has node $T_1$ to $T_n$ which point to it. PageRank is introduced as a function that solves the following equation:

$$
PageRank(A) = (1-d)+d\sum_{i=1}^n \frac{PageRank(T_i)}{C(T_i)}
$$

where $C(A)$ is the number of links going out of node *A*. This equation is used to update a candidate solution iteratively and arrive at an approximate solution. By calculating the PageRank of each node, the centrality of each Part can be defined and represented.

## Louvain Method

The Louvain method[^2] is a community detection method suitable for huge networks. It maximizes a modularity score for each community, where modularity measures the quality of node assignment. This entails determining how much more densely connected nodes within a community are in comparison to how connected they would be in a random network.

In [Louvain method](https://en.wikipedia.org/wiki/Louvain_method), modularity $Q$ of a graph is defined as:

$$
Q = \frac{1}{2m}\sum_{i,j}[A_{i,j}-\frac{k_ik_j}{2m}]\delta(c_i,c_j)
$$

where $A_{i,j}$ is the edge weight between $community_i$ and $community_j$ and $\delta(x,y)$ is Kronecker delta function ($\delta(x,y)=1$ if $x=y$ else $0$).

Louvain algorithm needs to be repeated for two phases to greedily maximize modularity. Phase 1 will put each node in a graph into a distinct community and optimize modularity by allowing only local changes to node-communities memberships. Phase 2 will aggregate communities into super-nodes to build a new network. The new network of super-nodes will then run Phase 1. Phase 1 and Phase 2 will be repeated until no movement yields a gain on the sum of modularity of all communities.

## Referenecs
[^1]: Brin, S., & Page, L. (1998). The anatomy of a large-scale hypertextual Web search engine. *Computer Networks and ISDN Systems*, *30*(1), 107–117. https://doi.org/10.1016/S0169-7552(98)00110-X
[^2]: Blondel, V. D., Guillaume, J.-L., Lambiotte, R., & Lefebvre, E. (2008). Fast unfolding of communities in large networks. *Journal of Statistical Mechanics: Theory and Experiment*, *2008*(10), P10008. https://doi.org/10.1088/1742-5468/2008/10/P10008