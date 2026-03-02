from copy import deepcopy
infinity = float('inf')

def reverse_graph(G):
  n = len(G)
  G_rev = [[] for v in range(n)]
  for v in range(n):
    for u, weight in G[v]:
      G_rev[u].append((v, weight))
  return G_rev

def dfs(G, s):
  n = len(G)
  dtime = [None]*n; ftime = [None]*n; prev = [None]*n; nextu = [0]*n
  dtime[s] = 1; DTIME = 1; FTIME = 0; v = s; nextv = 0
  while True:
    for i in range(nextu[v], len(G[v])):
      u, _ = G[v][i]; nextu[v] = i+1
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
G = [[] for i in range(n)]
for i in range(m):
  v, u, weight = map(int, input().split())
  G[v].append((u, weight))
s = int(input())

MEASURE_START()
prev, dtime, ftime = dfs(deepcopy(G), s)
topo_order = sorted(range(n), key=lambda i: ftime[i], reverse=True)

G_inedges = reverse_graph(G)

# Shortest paths
dist = [infinity]*n; dist_prev = [None]*n
dist[s] = 0

for v in topo_order:
  for u, weight in G_inedges[v]:
    if dist[u] + weight < dist[v]:
      dist[v] = dist[u] + weight; dist_prev[v] = u

# Longest paths
maxpath = [-infinity]*n; maxpath_prev = [None]*n
maxpath[s] = 0

for v in topo_order:
  for u, weight in G_inedges[v]:
    if maxpath[u] + weight > maxpath[v]:
      maxpath[v] = maxpath[u] + weight; maxpath_prev[v] = u

MEASURE_STOP()

print("Topological order:"); print(topo_order); print()
print("Shortest paths:"); print(dist); print()
print("Parents for the shortest paths:"); print(dist_prev); print()
print("Longest paths:"); print(maxpath); print()
print("Parents for the longest paths:"); print(maxpath_prev); print()