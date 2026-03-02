from copy import deepcopy
vegtelen = float('inf')

def grafot_megfordit(G):
  n = len(G)
  G_ford = [[] for v in range(n)]
  for v in range(n):
    for u, suly in G[v]:
      G_ford[u].append((v, suly))
  return G_ford

def dfs(G, s):
  n = len(G)
  mszam = [None]*n; bszam = [None]*n; elozo = [None]*n; kszom = [0]*n
  mszam[s] = 1; MSZAM = 1; BSZAM = 0; v = s; kcsucs = 0
  while True:
    for i in range(kszom[v], len(G[v])):
      u, _ = G[v][i]; kszom[v] = i+1
      if mszam[u] is None:
        MSZAM += 1; mszam[u] = MSZAM; elozo[u] = v; v = u; break
      elif mszam[v] > mszam[u] and bszam[u] is None:
        raise Exception(f"Nem aciklikus a gráf! Megtalált visszaél: {v} -> {u}.")
    else:
      BSZAM += 1; bszam[v] = BSZAM
      if elozo[v] != None: v = elozo[v]
      else:
        for w in range(kcsucs, n):
          kcsucs = w+1
          if mszam[w] is None:
            MSZAM += 1; mszam[w] = MSZAM; v = w; break
        else: break
  return elozo, mszam, bszam

n, m = map(int, input().split())
G = [[] for i in range(n)]
for i in range(m):
  v, u, suly = map(int, input().split())
  G[v].append((u, suly))
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(deepcopy(G), s)
topo_sorrend = sorted(range(n), key=lambda i: bszam[i], reverse=True)

G_beelek = grafot_megfordit(G)

# Legrövidebb utak
tav = [vegtelen]*n; tav_elozo = [None]*n
tav[s] = 0

for v in topo_sorrend:
  for u, suly in G_beelek[v]:
    if tav[u] + suly < tav[v]:
      tav[v] = tav[u] + suly; tav_elozo[v] = u

# Leghosszabb utak
maxut = [-vegtelen]*n; maxut_elozo = [None]*n
maxut[s] = 0

for v in topo_sorrend:
  for u, suly in G_beelek[v]:
    if maxut[u] + suly > maxut[v]:
      maxut[v] = maxut[u] + suly; maxut_elozo[v] = u

MERES_VEG()

print("Topologikus sorrend:"); print(topo_sorrend); print()
print("Legrövidebb utak:"); print(tav); print()
print("Legrövidebb utak szülői:"); print(tav_elozo); print()
print("Leghosszabb utak:"); print(maxut); print()
print("Leghosszabb utak szülői:"); print(maxut_elozo); print()
