from copy import deepcopy
infinity = float('inf')

def dijkstra(G, s):
  n = len(G)
  dist = [infinity] * n; dist[s] = 0
  prev = [None] * n; done = [False] * n; done[s] = True
  v = s

  while True:
    for u, weight in G[v]:
      if not done[u]:
        if dist[v] + weight < dist[u]:
          dist[u] = dist[v] + weight
          prev[u] = v

    min_dist = infinity; v = None
    for u in range(n):
      if not done[u] and dist[u] < min_dist:
        min_dist = dist[u]; v = u
    if v is None: break
    done[v] = True

  return dist, prev

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for i in range(m):
  u, v, weight = map(int, input().split())
  G[u].append((v, weight))
s = int(input())

MEASURE_START()
dist, prev = dijkstra(deepcopy(G), s)
MEASURE_STOP()

print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(prev); print()
