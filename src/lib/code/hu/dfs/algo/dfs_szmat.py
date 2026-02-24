from copy import deepcopy

def dfs(G, s):
  n = len(G)
  mszam = [None]*n; bszam = [None]*n; elozo = [None]*n; kszom = [0]*n
  mszam[s] = 1; MSZAM = 1; BSZAM = 0; v = s; kcsucs = 0
  while True:
    for u in range(kszom[v], n):
      kszom[v]=u+1
      if G[v][u] and mszam[u] is None:
        MSZAM += 1; mszam[u] = MSZAM; elozo[u] = v; v = u; break
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
