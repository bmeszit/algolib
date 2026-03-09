infinity = float('inf')

def dijkstra(G, s):
  n = len(G)
  dist = [infinity] * n; dist[s] = 0
  prev = [None] * n; done = [False] * n
  v = s

  for _ in range(n-1):
    done[v] = True
    for u in range(n):
      if not done[u]:
        if dist[v] + G[v][u] < dist[u]:
          dist[u] = dist[v] + G[v][u]
          prev[u] = v

    v = None
    for u in range(n):
      if not done[u] and dist[u] < infinity:
        if v is None or dist[u] < dist[v]:
          v = u
    if v is None:
      break

  return dist, prev

n, m = map(int, input().split())
G = [[infinity]*n for _ in range(n)]
for i in range(m):
  u, v, weight = map(int, input().split())
  G[u][v] = weight
s = int(input())

MEASURE_START()
dist, prev = dijkstra(G, s)
MEASURE_STOP()

print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(prev); print()
