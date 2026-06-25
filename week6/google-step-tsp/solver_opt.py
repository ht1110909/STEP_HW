#!/usr/bin/env python3

import sys
import math
from common import print_tour, read_input

def solve(cities):
    """
    Solves the TSP using a Christofides-inspired algorithm,
    followed by the 2-Opt optimization to further refine the route.
    """
    if not cities:
        return []
    if len(cities) == 1:
        return [0]

    christofides_path = christofides(cities)
    return opt_2(christofides_path, cities)

def build_distance_matrix(cities):
    """Pre-calculates distances to avoid redundant math.sqrt calls."""
    n = len(cities)
    dist = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(i + 1, n):
            d = calculate_distance(cities[i], cities[j])
            dist[i][j] = d
            dist[j][i] = d
    return dist

def calculate_distance(start, end):
    """Calculates Euclidean distance."""
    x1, y1 = start
    x2, y2 = end
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# ==========================================
# Christofides Algorithm Steps
# ==========================================

def christofides(cities):
    """Orchestrates the steps of the Christofides algorithm."""
    n = len(cities)
    dist_matrix = build_distance_matrix(cities)

    # Step 1: Minimum Spanning Tree
    mst_adj = build_mst(n, dist_matrix)

    # Step 2: Find Odd Degree Vertices
    odd_vertices = get_odd_vertices(mst_adj)

    # Step 3: Greedy Perfect Matching
    matching = greedy_perfect_matching(odd_vertices, dist_matrix)

    # Step 4: Create Multigraph
    multigraph = create_multigraph(mst_adj, matching)

    # Step 5: Eulerian Circuit
    circuit = find_eulerian_circuit(multigraph)

    # Step 6: Make Hamiltonian (Shortcutting)
    path = shortcut_circuit(circuit)

    return path

def build_mst(n, dist_matrix):
    """Step 1: Uses Prim's Algorithm to build a Minimum Spanning Tree."""
    mst_adj = [[] for _ in range(n)]
    #keeps track of the shortest distance each node can offer
    key = [float('inf')] * n
    #keeps track of the connection between node n and node parent[n] that offers the shortest dist
    parent = [-1] * n
    #keeps track of which node is alrady in the tree
    in_mst = [False] * n

    #start from node 0
    key[0] = 0
    for _ in range(n):
        u = -1
        min_val = float('inf')
        #find the shortest cost node
        for i in range(n):
            if not in_mst[i] and key[i] < min_val:
                min_val = key[i]
                u = i

        in_mst[u] = True

        #update the key list with shortest distance they can offer
        for v in range(n):
            if not in_mst[v] and dist_matrix[u][v] < key[v]:
                key[v] = dist_matrix[u][v]
                parent[v] = u

    #create an adjacency list to make a tree
    for v in range(1, n):
        u = parent[v]
        mst_adj[u].append(v)
        mst_adj[v].append(u)

    return mst_adj

def get_odd_vertices(mst_adj):
    """Step 2: Finds vertices with an odd number of edges in the MST."""
    return [v for v, edges in enumerate(mst_adj) if len(edges) % 2 != 0]

def greedy_perfect_matching(odd_vertices, dist_matrix):
    """Step 3: Pairs up odd vertices using a greedy proximity approach."""
    odd_unmatched = set(odd_vertices)
    matching = []

    #until all of them get matched
    while odd_unmatched:
        #select arbituary node
        v = odd_unmatched.pop()
        best_u = None
        min_dist = float('inf')

        #find the closest node
        for u in odd_unmatched:
            if dist_matrix[v][u] < min_dist:
                min_dist = dist_matrix[v][u]
                best_u = u

        #match them if the closest node exists
        if best_u is not None:
            matching.append((v, best_u))
            odd_unmatched.remove(best_u)

    return matching

def create_multigraph(mst_adj, matching):
    """Step 4: Combines the MST and the matching edges into a single graph."""
    multigraph = [list(edges) for edges in mst_adj]
    for u, v in matching:
        multigraph[u].append(v)
        multigraph[v].append(u)
    return multigraph

def find_eulerian_circuit(multigraph):
    """Step 5: Uses Hierholzer's Algorithm to find an Eulerian circuit."""
    #current path it is walking
    curr_path = [0]
    circuit = []

    while curr_path:
        #current node
        curr_v = curr_path[-1]
        #if current node still has unused edges
        if multigraph[curr_v]:
            #get the next unused edge and push on to the path
            next_v = multigraph[curr_v].pop()
            multigraph[next_v].remove(curr_v)
            curr_path.append(next_v)
        #no unused edges mean you are stack, so there is a sub-circuit 
        else:
            circuit.append(curr_path.pop())

    return circuit

def shortcut_circuit(circuit):
    """Step 6: Removes duplicate city visits to create a Hamiltonian path."""
    visited = set()
    path = []
    # Reverse circuit because Hierholzer's builds it backwards
    for v in circuit[::-1]:
        if v not in visited:
            visited.add(v)
            path.append(v)
    return path

# ==========================================
# Optimization
# ==========================================

def opt_2(path, cities):
    """2-Opt Optimization for refining the path."""
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(path)):
            for j in range(i + 2, len(path)):
                if i == 0 and j == len(path) - 1:
                    continue

                c_i, c_next_i = cities[path[i]], cities[path[(i + 1) % len(path)]]
                c_j, c_next_j = cities[path[j]], cities[path[(j + 1) % len(path)]]

                pre_dist = calculate_distance(c_i, c_next_i) + calculate_distance(c_j, c_next_j)
                post_dist = calculate_distance(c_i, c_j) + calculate_distance(c_next_i, c_next_j)

                if pre_dist > post_dist:
                    path[i + 1:j + 1] = path[i + 1:j + 1][::-1]
                    swapped = True
    return path

if __name__ == '__main__':
    assert len(sys.argv) > 1
    tour = solve(read_input(sys.argv[1]))
    print_tour(tour)
