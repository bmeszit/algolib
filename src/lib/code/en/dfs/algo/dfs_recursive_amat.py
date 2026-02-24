from copy import deepcopy

def dfs(G, s):
  n = len(G)
  DTIME=0; FTIME=0

  prev=[None]*n
  dtime=[None]*n
  ftime=[None]*n

  def dfs_from(v):
    nonlocal DTIME, FTIME
    DTIME+=1; dtime[v]=DTIME
    for u in range(n):
      if G[v][u] and dtime[u] is None:
        prev[u] = v
        dfs_from(u)
    FTIME+=1; ftime[v]=FTIME
  
  dfs_from(s)
  for v in range(n):
    if dtime[v] is None:
      dfs_from(v)

  return prev, dtime, ftime

n, m = map(int, input().split())
G = [[False] * n for i in range(n)]
for i in range(m):
  v, u = map(int, input().split())
  G[v][u] = True
s = int(input())

MEASURE_START()
prev, dtime, ftime = dfs(deepcopy(G), s)
MEASURE_STOP()

print("Parent vertices:"); print(prev); print()
print("Discovery times:"); print(dtime); print()
print("Finishing times:"); print(ftime); print()
