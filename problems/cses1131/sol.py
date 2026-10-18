import sys
from collections import deque


def farthest(adj: list[list[int]], start: int) -> tuple[int, int]:
    """BFS desde start: (nodo más lejano, su distancia). Iterativo: sin límite de recursión."""
    dist = [-1] * len(adj)
    dist[start] = 0
    queue = deque([start])
    node = start
    while queue:
        node = queue.popleft()
        for nxt in adj[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1
                queue.append(nxt)
    return node, dist[node]  # el último en salir de la cola es de los más lejanos


def tree_diameter(n: int, edges: list[tuple[int, int]]) -> int:
    adj: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    endpoint, _ = farthest(adj, 1)  # un extremo de algún diámetro
    return farthest(adj, endpoint)[1]


def main() -> None:
    data = list(map(int, sys.stdin.buffer.read().split()))
    n = data[0]
    edges = list(zip(data[1::2], data[2::2]))
    print(tree_diameter(n, edges))


if __name__ == "__main__":
    main()
