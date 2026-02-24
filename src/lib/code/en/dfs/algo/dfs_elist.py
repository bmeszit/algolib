from copy import deepcopy

def dfs(G, s):
  n = len(G)
  dtime = [None]*n; ftime = [None]*n; prev = [None]*n; nextu = [0]*n
  dtime[s] = 1; DTIME = 1; FTIME = 0; v = s; nextv = 0
  while True:
    for i in range(nextu[v], len(G[v])):
      u = G[v][i]; nextu[v] = i+1
      if dtime[u] is None:
        DTIME += 1; dtime[u] = DTIME; prev[u] = v; v = u; break
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
  v, u = map(int, input().split())
  G[v].append(u)
s = int(input())

MEASURE_START()
prev, dtime, ftime = dfs(deepcopy(G), s)
MEASURE_STOP()

print("Parent vertices:"); print(prev); print()
print("Discovery times:"); print(dtime); print()
print("Finishing times:"); print(ftime); print()
