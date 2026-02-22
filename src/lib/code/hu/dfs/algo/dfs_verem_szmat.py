from copy import deepcopy

class stack(list):
  push = list.append
  pop = list.pop
  def is_empty(self): return len(self) == 0

BEJARANDO=1
BEFEJEZENDO=2

def dfs(G, s):
  n = len(G)
  elozo = [None]*n
  mszam = [None]*n
  bszam = [None]*n
  kovetkezo = stack()
  
  MSZAM=0
  BSZAM=0
  
  def honnan(s):
    nonlocal MSZAM, BSZAM
    
    kovetkezo.push((s, None, BEJARANDO))
    while not kovetkezo.is_empty():
      aktiv_csucs, szulo_csucs, tipus = kovetkezo.pop()

      if tipus == BEJARANDO and mszam[aktiv_csucs] is None:
        elozo[aktiv_csucs] = szulo_csucs
        MSZAM += 1; mszam[aktiv_csucs] = MSZAM
        
        kovetkezo.push((aktiv_csucs, None, BEFEJEZENDO))
        for v in range(n-1, -1, -1):
          if G[aktiv_csucs][v]:
            kovetkezo.push((v, aktiv_csucs, BEJARANDO))

      elif tipus == BEFEJEZENDO:
        BSZAM += 1; bszam[aktiv_csucs] = BSZAM
  
  honnan(s)
  for v in range(n):
    if mszam[v] is None:
      honnan(v)
  
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