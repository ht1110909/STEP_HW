## Christofides algorithm
build MST -> Find odd degree nodes -> Min-weight matching -> Eulerian circuit  -> Shortcut

# MST
MST is short for minimum spanning tree. A spanning tree connects all n nodes with exactly n-1 edges and no cycles. The minimum one does this with the least total edge weight. Think of it as the cheapest way to wire all cities together without any loops. Cost here just refers to the distance between two nodes.
I will use Prim's algorithm to implement MST. The core idea of this is at each step, look at all edges that connect a node already in my tree to a node not yet in my tree, and pick the cheapest one. Repeat until all nodes are in the tree.

# odd node + min-weight matching
Find all odd-degree nodes in order to create a Eulerian graph later (condition for Eulerian is that all nodes have even-degree). We want Eulerian graph because it visits every node once, which make it possible for me to do shortcutting.
Min-weight matching is hard to implement so I implemented the greedy approximation version.The following is how it works:
- Picks an arbitrary unmatched node v
- Finds v's nearest unmatched neighbor
- Matches them, removes both, repeat
We know that there are even numbers of odd-degree nodes based on handshaking lemma

# Eulerian circuit
Now that we know there exists an Eulerian circuit in the tree, we will find one using Hierholzer's Algorithm.
Currently, we have a multigraph so we want to get a compelete cycle. We start at any node, keep walking unused edges until you return to start (sub-circuit) If unused edges remain, find a node on the circuit that still has unused edges and start exploring a new sub-circuit from there. We repeat this until all edges are used.

# Shortcut
After finding all Eulerian circuits (guranteed that all nodes are in the returned list), return a path that drops any repeatedly visited city. Based on the trinagle inequality, the direct path is always shorter than going through another city

# remaining question
I still don't really understand why we can always come back to the starting node in the EUlerian circuit. I know it is becasue all nodes have even-degree but what does that do with always have a path to come back...?
Why is it guranteed that all nodes are in the returned list of Eulerian circuit???
