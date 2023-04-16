import heapq as hq

def shortest_cycle(G):
    path = {}
    for u in G:
        for v in G:
            path[(u,v)] = float("inf")
    
    for s in G:
        dist = {v: float("inf") for v in G}
        dist[s] = 0
        # path[(s,s)] = 0
        H = [(0,s)]
        print(s)
        while H:
            curr_distance, curr_vertex = hq.heappop(H)
            # if curr_distance > path[(s,curr_vertex)]:
            #     continue
            if curr_distance > dist[curr_vertex]:
                continue

            for neighbor, weight in G[curr_vertex]:
                distance = curr_distance + weight
                # if distance < path[(s,neighbor)] or path[(s,s)] == 0:
                #     path[(s,neighbor)] = distance
                #     hq.heappush(H, (distance,neighbor))
                if distance < dist[neighbor] or dist[s] == 0:
                    dist[neighbor] = distance
                    hq.heappush(H, (distance, neighbor))
        print(s)
        print(dist)
        print("\n")
    # for s in G:
    #     if path[(s,s)] < lengthMin and path[(s,s)] != 0:
    #         lengthMin = path[(s,s)]
    
    # if lengthMin == float("inf"):
    #     print("Acyclic")
    # else:
    #     print(lengthMin)


G = {
    1: [(3,6),(4,3)],
    2: [(1,3)],
    3: [(4,2)],
    4: [(2,1),(3,1)],
    5: [(2,4),(4,2)]
}

shortest_cycle(G)