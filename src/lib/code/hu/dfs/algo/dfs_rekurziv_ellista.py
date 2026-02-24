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
G = [[] for i in range(n)]
for i in range(m):
  v, u = map(int, input().split())
  G[v].append(u)
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(deepcopy(G), s)
MERES_VEG()

print("Szülő csúcsok:"); print(elozo); print()
print("Mélységi számok:"); print(mszam); print()
print("Befejezési számok:"); print(bszam); print()
