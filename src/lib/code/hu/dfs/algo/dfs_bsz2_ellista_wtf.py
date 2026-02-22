from copy import deepcopy

def dfs(G, s):
  n = len(G)
  hol = [0]*n
  globhol = 0
  mszam = [None]*n; mszam[s] = 1
  bszam = [None]*n
  elozo = [None]*n
  MSZAM = 1; BSZAM = 0; aktiv_csucs = s
  while True:
    while hol[aktiv_csucs] < len(G[aktiv_csucs]):
      v = G[aktiv_csucs][hol[aktiv_csucs]]
      hol[aktiv_csucs]+=1
      if mszam[v] is None:
        MSZAM += 1; mszam[v] = MSZAM
        elozo[v] = aktiv_csucs
        aktiv_csucs = v
        break
    else:
      BSZAM += 1; bszam[aktiv_csucs] = BSZAM
      if elozo[aktiv_csucs] != None:
        aktiv_csucs = elozo[aktiv_csucs]
      else:
        while globhol < n:
          v = globhol
          globhol+=1
          if mszam[v] == None:
            aktiv_csucs = v
            MSZAM += 1; mszam[aktiv_csucs] = MSZAM
            break
            
        else:
          break
  return elozo, mszam, bszam

n, m = map(int, input().split())
G = [[] for i in range(n)]
for i in range(m):
  u, v = map(int, input().split())
  G[u].append(v)
s = int(input())

MERES_KEZD()
elozo, mszam, bszam = dfs(deepcopy(G), s)
MERES_VEG()

print("Szülő csúcsok:"); print(elozo); print()
print("Mélységi számok:"); print(mszam); print()
print("Befejezési számok:"); print(bszam); print()