def dfs(i, curr_node, visited, order, G):
    visited.add(curr_node)
    for neighbour in G[curr_node]:
        if neighbour not in visited:
            i = dfs(i, neighbour, visited, order, G)
    
    order[i] = curr_node
    return i - 1

def topological_sort(G):
    order = [0] * len(G)
    visited = set()
    i = len(G) - 1
    for node in G:
        if node not in visited:
            i = dfs(i, node, visited, order, G)

    return order

G = {
    'a': ['b', 'c'],
    'b': ['d'],
    'c': ['d'],
    'd': ['e'],
    'e': []
}

print(topological_sort(G))
