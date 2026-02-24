from copy import deepcopy

class stack(list):
  push = list.append
  pop = list.pop
  def peek(self): return self[-1]
  def is_empty(self): return len(self) == 0

def dfs(G, s):
  n = len(G)
  elozo = [None]*n
  mszam = [None]*n
  bszam = [None]*n
  
  kcsucs = stack()
  kszom = [0]*n
  
  MSZAM=0
  BSZAM=0
  
  def honnan(s):
    nonlocal MSZAM, BSZAM
    
    MSZAM += 1; mszam[s]=MSZAM
    kcsucs.push(s)
    
    while not kcsucs.is_empty():
      v = kcsucs.peek()
      while kszom[v]<n:
        u = kszom[v]
        if G[v][u] and mszam[u] is None:
          elozo[u] = v
          MSZAM += 1; mszam[u] = MSZAM
          kcsucs.push(u)
          break
        else: kszom[v] += 1
      else:
        BSZAM += 1; bszam[v]=BSZAM
        kcsucs.pop()
          
  honnan(s)
  for v in range(n):
    if mszam[v] is None:
      honnan(v)
  
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
