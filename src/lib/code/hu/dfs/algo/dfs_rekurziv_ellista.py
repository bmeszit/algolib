def dfs(G, s):
  n = len(G)
  MSZAM=0; BSZAM=0

  elozo=[None]*n
  mszam=[None]*n
  bszam=[None]*n

  def honnan(v):
    nonlocal MSZAM
    nonlocal BSZAM
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
  u, v = map(int, input().split())
  G[u].append(v)
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(G, s)
MERES_VEG()

print("Szülő csúcsok:"); print(elozo); print()
print("Mélységi számok:"); print(mszam); print()
print("Befejezési számok:"); print(bszam); print()