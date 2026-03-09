infinity = float('inf')

def reverse_graph(G):
  n = len(G)
  G_rev = [[] for v in range(n)]
  for u in range(n):
    for v, weight in G[u]:
      G_rev[v].append((u, weight))
  return G_rev

def bellman_ford(G_in, s):
  n = len(G_in)
  dist = [infinity] * n; dist[s] = 0
  prev = [None] * n

  for _ in range(n-1):
    dist_new = [None] * n; dist_new[s] = 0
    prev_new = [None] * n
    for v in range(n):
      if v == s: continue
      dist_new[v] = dist[v]
      prev_new[v] = prev[v]
      for u, weight in G_in[v]:
        if dist[u] + weight < dist_new[v]:
          dist_new[v] = dist[u] + weight
          prev_new[v] = u
    dist = dist_new
    prev = prev_new

  return dist, prev

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for i in range(m):
  u, v, weight = map(int, input().split())
  G[u].append((v, weight))
s = int(input())

G_in = reverse_graph(G)

MEASURE_START()
dist, prev = bellman_ford(G_in, s)
MEASURE_STOP()

print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(prev); print()
