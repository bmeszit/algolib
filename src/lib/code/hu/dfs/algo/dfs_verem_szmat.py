from copy import deepcopy

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
  
  MSZAM=0
  BSZAM=0
  
  def honnan(s):
    nonlocal MSZAM, BSZAM, elozo, mszam, bszam, kovetkezo
    
    kovetkezo.push((s, csucs_tipus.bejarando))
    MSZAM+=1; mszam[s] = MSZAM
  
    while not kovetkezo.is_empty():
      aktiv_csucs, tipus = kovetkezo.pop()
      
      if tipus == csucs_tipus.bejarando:
        kovetkezo.push((aktiv_csucs, csucs_tipus.befejezendo))
        for v in range(n-1, -1, -1):
          if G[aktiv_csucs][v] and mszam[v] is None:
            MSZAM += 1
            mszam[v] = MSZAM
            elozo[v] = aktiv_csucs
            kovetkezo.push((v, csucs_tipus.bejarando))
        
      elif tipus == csucs_tipus.befejezendo:
        BSZAM += 1
        bszam[aktiv_csucs] = BSZAM
   
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
elozo, mszam, bszam = dfs(deepcopy(G), s)
MERES_VEG()

print("Szülő csúcsok:"); print(elozo); print()
print("Mélységi számok:"); print(mszam); print()
print("Befejezési számok:"); print(bszam); print()