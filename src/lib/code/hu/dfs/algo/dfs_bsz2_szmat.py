from copy import deepcopy

def dfs(G, s):
  n = len(G)
  mszam = [None]*n; mszam[s] = 1
  bszam = [None]*n
  elozo = [None]*n
  MSZAM = 1; BSZAM = 0; aktiv_csucs = s
  while True:
    for v in range(n):
      if G[aktiv_csucs][v] and mszam[v] is None:
        MSZAM += 1; mszam[v] = MSZAM
        elozo[v] = aktiv_csucs
        aktiv_csucs = v
        break
    else:
      BSZAM += 1; bszam[aktiv_csucs] = BSZAM
      if elozo[aktiv_csucs] != None:
        aktiv_csucs = elozo[aktiv_csucs]
      else:
        for v in range(n):
          if mszam[v] == None:
            aktiv_csucs = v
            MSZAM += 1; mszam[aktiv_csucs] = MSZAM
            break
        else:
          break
  return elozo, mszam, bszam

n, m = map(int, input().split())
elek = []
G = [[False] * n for i in range(n)]
for i in range(m):
  u, v = map(int, input().split())
  elek.append((u, v))
  G[u][v] = True
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