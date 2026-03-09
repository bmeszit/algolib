from copy import deepcopy
infinity = float('inf')

def dfs(G, s):
  n = len(G)
  dtime = [None]*n; ftime = [None]*n; prev = [None]*n; nextu = [0]*n
  dtime[s] = 1; DTIME = 1; FTIME = 0; v = s; nextv = 0
  while True:
    for i in range(nextu[v], n):
      nextu[v] = i+1
      if G[v][i] != infinity:
        u = i
        if dtime[u] is None:
          DTIME += 1; dtime[u] = DTIME; prev[u] = v; v = u; break
        elif dtime[v] > dtime[u] and ftime[u] is None:
          raise Exception(f"Graph is not acyclic! Found back edge: {v} -> {u}.")
    else:
      FTIME += 1; ftime[v] = FTIME
      if prev[v] != None: v = prev[v]
      else:
        for w in range(nextv, n):
          nextv = w+1
          if dtime[w] is None:
            DTIME += 1; dtime[w] = DTIME; v = w; break
        else: break
  return prev, dtime, ftime

n, m = map(int, input().split())
G = [[infinity]*n for _ in range(n)]
for i in range(m):
  v, u, weight = map(int, input().split())
  G[v][u] = weight
s = int(input())

MEASURE_START()
prev, dtime, ftime = dfs(deepcopy(G), s)
topo_order = [None] * n
for v in range(n):
  topo_order[n - ftime[v]] = v

dist = [infinity]*n; dist_prev = [None]*n
dist[s] = 0

for v in topo_order:
  for u in range(n):
    if G[v][u] != infinity:
      if dist[v] + G[v][u] < dist[u]:
        dist[u] = dist[v] + G[v][u]; dist_prev[u] = v

MEASURE_STOP()

print("Topological order:"); print(topo_order); print()
print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(dist_prev); print()
