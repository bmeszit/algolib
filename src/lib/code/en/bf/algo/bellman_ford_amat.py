from copy import deepcopy
infinity = float('inf')

def bellman_ford(G, s):
  n = len(G)
  dist = [infinity] * n; dist[s] = 0
  prev = [None] * n

  for _ in range(n-1):
    dist_new = [None] * n; dist_new[s] = 0
    prev_new = [None] * n
    for v in range(n):
      if v == s: continue
      dist_new[v] = dist[v]
      prev_new[v] = prev[v]
      for u in range(n):
        if dist[u] + G[u][v] < dist_new[v]:
          dist_new[v] = dist[u] + G[u][v]
          prev_new[v] = u
    dist = dist_new
    prev = prev_new

  return dist, prev

n, m = map(int, input().split())
G = [[infinity]*n for _ in range(n)]
for i in range(m):
  u, v, weight = map(int, input().split())
  G[u][v] = weight
s = int(input())

MEASURE_START()
dist, prev = bellman_ford(deepcopy(G), s)
MEASURE_STOP()

print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(prev); print()
