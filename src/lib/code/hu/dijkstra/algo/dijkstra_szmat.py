vegtelen = float('inf')

def dijkstra(G, s):
  n = len(G)
  tav = [vegtelen] * n; tav[s] = 0
  elozo = [None] * n; kesz = [False] * n
  v = s

  for _ in range(n-1):
    kesz[v] = True
    for u in range(n):
      if not kesz[u]:
        if tav[v] + G[v][u] < tav[u]:
          tav[u] = tav[v] + G[v][u]
          elozo[u] = v

    v = None
    for u in range(n):
      if not kesz[u] and tav[u] < vegtelen:
        if v is None or tav[u] < tav[v]:
          v = u
    if v is None:
      break

  return tav, elozo

n, m = map(int, input().split())
G = [[vegtelen]*n for _ in range(n)]
for i in range(m):
  u, v, suly = map(int, input().split())
  G[u][v] = suly
s = int(input())

MERES_KEZD()
tav, elozo = dijkstra(G, s)
MERES_VEG()

print("Legrövidebb utak:"); print(tav); print()
print("Legrövidebb utak szülői:"); print(elozo); print()
