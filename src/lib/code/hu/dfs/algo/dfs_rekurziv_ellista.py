from copy import deepcopy

def dfs(G, s):
  n = len(G)
  MSZAM=0; BSZAM=0

  elozo=[None]*n
  mszam=[None]*n
  bszam=[None]*n

  def honnan(v):
    nonlocal MSZAM, BSZAM
    MSZAM+=1; mszam[v]=MSZAM
    for u in G[v]:
      if mszam[u] is None:
        elozo[u] = v
        honnan(u)
    BSZAM+=1; bszam[v]=BSZAM
  
  honnan(s)
  for v in range(n):
    if mszam[v] is None:
      honnan(v)

  return elozo, mszam, bszam

n, m = map(int, input().split())
elek = []
G = [[] for i in range(n)]
for i in range(m):
  u, v = map(int, input().split())
  elek.append((u, v))
  G[u].append(v)
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