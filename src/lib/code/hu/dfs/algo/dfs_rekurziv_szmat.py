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
    for u, van_el in enumerate(G[v]):
      if van_el and mszam[u] is None:
        elozo[u] = v
        honnan(u)
    BSZAM+=1; bszam[v]=BSZAM
  
  honnan(s)
  for v in range(n):
    if mszam[v] is None:
      honnan(v)
  return elozo, mszam, bszam

n, m = map(int, input().split())
G = [[False] * n for i in range(n)]
for i in range(m):
  u, v = map(int, input().split())
  G[u][v] = True
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(G, s)
MERES_VEG()

print("Szülő csúcsok:")
print(elozo)

print("Mélységi számok:")
print(mszam)

print("Befejezési számok:")
print(bszam)
