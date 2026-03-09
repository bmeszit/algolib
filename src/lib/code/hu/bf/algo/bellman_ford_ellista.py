from copy import deepcopy
vegtelen = float('inf')

def grafot_megfordit(G):
  n = len(G)
  G_ford = [[] for v in range(n)]
  for u in range(n):
    for v, suly in G[u]:
      G_ford[v].append((u, suly))
  return G_ford

def bellman_ford(G_be, s):
  n = len(G_be)
  tav = [vegtelen] * n; tav[s] = 0
  elozo = [None] * n

  for _ in range(n-1):
    tav_uj = [None] * n; tav_uj[s] = 0
    elozo_uj = [None] * n
    for v in range(n):
      if v == s: continue
      tav_uj[v] = tav[v]
      elozo_uj[v] = elozo[v]
      for u, suly in G_be[v]:
        if tav[u] + suly < tav_uj[v]:
          tav_uj[v] = tav[u] + suly
          elozo_uj[v] = u
    tav = tav_uj
    elozo = elozo_uj

  return tav, elozo

n, m = map(int, input().split())
G = [[] for _ in range(n)]
for i in range(m):
  u, v, suly = map(int, input().split())
  G[u].append((v, suly))
s = int(input())

G_be = grafot_megfordit(G)

MERES_KEZD()
tav, elozo = bellman_ford(deepcopy(G_be), s)
MERES_VEG()

print("Legrövidebb utak:"); print(tav); print()
print("Legrövidebb utak szülői:"); print(elozo); print()
