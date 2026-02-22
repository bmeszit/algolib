class stack(list):
  push = list.append
  pop = list.pop
  def peek(self): return self[-1]
  def is_empty(self): return len(self) == 0

from enum import Enum
class csucs_tipus(Enum):
  bejarando = 1
  befejezendo = 2

def dfs(G, s):
  n = len(G)
  elozo = [None]*n
  mszam = [None]*n
  bszam = [None]*n
  kovetkezo = stack()
  
  kovetkezo.push((s, csucs_tipus.bejarando))
  mszam[s] = 1
  
  MSZAM=1
  BSZAM=0
  
  while not kovetkezo.is_empty():
    aktiv_csucs, tipus = kovetkezo.pop()
    
    if tipus == csucs_tipus.bejarando:
      kovetkezo.push((aktiv_csucs, csucs_tipus.befejezendo))
      for v, van_el in reversed(list(enumerate((G[aktiv_csucs])))):
        if van_el and mszam[v] is None:
          MSZAM += 1
          mszam[v] = MSZAM
          elozo[v] = aktiv_csucs
          kovetkezo.push((v, csucs_tipus.bejarando))
      
    elif tipus == csucs_tipus.befejezendo:
      BSZAM += 1
      bszam[aktiv_csucs] = BSZAM
  
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

print("Szülő csúcsok:"); print(elozo)
print("Mélységi számok:"); print(mszam)
print("Befejezési számok:"); print(bszam)