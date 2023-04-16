# Number of vertices
nV = 6
INF = 999

# Algorithm 
def floyd(G):
    dist = list(map(lambda p: list(map(lambda q: q, p)), G))

    # Adding vertices individually
    for r in range(nV):
        for p in range(nV):
            for q in range(nV):
                dist[p][q] = min(dist[p][q], dist[p][r] + dist[r][q])

    length = INF
    for i in range(nV):
        length = min(length, dist[i][i])
    
    if length == INF:
        return "Acyclic"
    else:
        return length


G = [[INF, 4, INF, INF, INF, INF],
         [INF, INF, 5, 2, INF, INF],
         [3, INF, INF, 7, INF, INF],
         [10, INF, INF, INF, 2, INF],
         [INF, INF, INF, INF, INF, 6],
         [INF, INF, INF, INF, INF, INF]]

print(floyd(G))