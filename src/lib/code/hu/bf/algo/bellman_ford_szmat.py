vegtelen = float('inf')

def bellman_ford(G, s):
  n = len(G)
  tav = [vegtelen] * n; tav[s] = 0
  elozo = [None] * n

  for _ in range(n-1):
    tav_uj = [None] * n; tav_uj[s] = 0
    elozo_uj = [None] * n
    for v in range(n):
      if v == s: continue
      tav_uj[v] = tav[v]
      elozo_uj[v] = elozo[v]
      for u in range(n):
        if tav[u] + G[u][v] < tav_uj[v]:
          tav_uj[v] = tav[u] + G[u][v]
          elozo_uj[v] = u
    tav = tav_uj
    elozo = elozo_uj

  return tav, elozo

n, m = map(int, input().split())
G = [[vegtelen]*n for _ in range(n)]
for i in range(m):
  u, v, suly = map(int, input().split())
  G[u][v] = suly
s = int(input())

MERES_KEZD()
tav, elozo = bellman_ford(G, s)
MERES_VEG()

print("Legrövidebb utak:"); print(tav); print()
print("Legrövidebb utak szülői:"); print(elozo); print()
