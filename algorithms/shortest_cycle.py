"""
The length of the shortest cycle in graph G
"""

import heapq

def dijkstra_shortest_cycle(graph,source):
    # initialize distance and visited arrays
    distance = {v: float('inf') for v in graph}
    visited = set()

    # set distance of source node to 0
    distance[source] = 0

    # create heap and push source node onto it
    heap = [(0, source)]

    while heap:
        # extract node with smallest distance from heap
        dist, node = heapq.heappop(heap)
        # mark node as visited
        visited.add(node)
        if distance[node] < dist:
            continue
        # update distances for all neighbors of node
        for neighbor, weight in graph[node]:
            # if node has already been visited, skip it
            if neighbor in visited and neighbor != source:
                continue

            new_dist = distance[node] + weight
            if new_dist < distance[neighbor] or distance[source] == 0:
                distance[neighbor] = new_dist
                if neighbor not in heap:
                    heapq.heappush(heap, (new_dist, neighbor))

    return distance[source]

def find_shortest_cycle(graph):
    lengthMinCycle = float("inf")
    for v in G:
        lengthCycle = dijkstra_shortest_cycle(graph, v)
        if lengthCycle < lengthMinCycle and lengthCycle != 0:
            lengthMinCycle = lengthCycle

    if lengthMinCycle == float("inf"):
        return "Acyclic"
    else:
        return lengthMinCycle

# graphs = [{
#     1: [(3,6),(4,3)],
#     2: [(1,3)],
#     3: [(4,2)],
#     4: [(2,1),(3,1)],
#     5: [(2,4),(4,2)]
# },{
#     0: [(1,4),(2,3)],
#     1: [(2,5),(3,2)],
#     2: [(3,7)],
#     3: [(4,2)],
#     4: [(5,6)]
# }
# ]

G = {
    0: [(1,4)],
    1: [(2,5),(3,2)],
    2: [(0,3),(3,7)],
    3: [(0,10),(4,2)],
    4: [(5,6)],
    5: []
}

print(find_shortest_cycle(G))