from copy import deepcopy

def dfs(G, s):
  n = len(G)
  mszam = [None]*n; bszam = [None]*n; elozo = [None]*n; kszom = [0]*n
  mszam[s] = 1; MSZAM = 1; BSZAM = 0; v = s; kcsucs = 0
  while True:
    while kszom[v]<n:
      u = kszom[v]
      if G[v][u] and mszam[u] is None:
        MSZAM += 1; mszam[u] = MSZAM; elozo[u] = v; v = u; break
      else: kszom[v] += 1
    else:
      BSZAM += 1; bszam[v] = BSZAM
      if elozo[v] != None: v = elozo[v]
      else:
        while kcsucs<n:
          if mszam[kcsucs] is None:
            MSZAM += 1; mszam[kcsucs] = MSZAM; v = kcsucs; break
          else: kcsucs+=1
        else: break
  return elozo, mszam, bszam

n, m = map(int, input().split())
elek = []
G = [[False] * n for i in range(n)]
for i in range(m):
  v, u = map(int, input().split())
  elek.append((v, u))
  G[v][u] = True
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(deepcopy(G), s)
MERES_VEG()

print("Szülő csúcsok:"); print(elozo); print()
print("Mélységi számok:"); print(mszam); print()
print("Befejezési számok:"); print(bszam); print()

for u, v in elek:
  if  mszam[u] < mszam[v] and bszam[u] > bszam[v]:
    if elozo[v] == u:
      print(f"{u} -> {v}: Faél")
    else:
      print(f"{u} -> {v}: Előreél")
  elif mszam[u] > mszam[v] and bszam[u] < bszam[v]:
    print(f"{u} -> {v}: Visszaél")
  elif mszam[u] > mszam[v] and bszam[u] > bszam[v]:
    print(f"{u} -> {v}: Keresztél")
  else:
    print(f"{u} -> {v}: ??? Hibás a kód!")