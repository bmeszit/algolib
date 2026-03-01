from copy import deepcopy
def dfs(G, s):
  n = len(G)
  mszam = [None]*n; bszam = [None]*n; elozo = [None]*n; kszom = [0]*n
  mszam[s] = 1; MSZAM = 1; BSZAM = 0; v = s; kcsucs = 0
  print(f"kezdő csúcs: {v}")
  print(f"mszam[{v}] = {mszam[v]}")
  while True:
    for i in range(kszom[v], len(G[v])):
      u = G[v][i]; kszom[v] = i+1
      if mszam[u] is None:
          MSZAM += 1; mszam[u] = MSZAM
          print(f"faél: {v} -> {u}")
          print(f"elozo[{u}] = {v}")
          print(f"mszam[{u}] = {mszam[u]}")
          elozo[u] = v; v = u
          break
      elif mszam[v] < mszam[u]:
          print(f"előreél: {v} -> {u}")
      elif mszam[v] > mszam[u] and bszam[u] is None:
          print(f"visszaél: {v} -> {u}")
      elif mszam[v] > mszam[u] and bszam[u] is not None:
          print(f"keresztél: {v} -> {u}")
    else:
      BSZAM += 1; bszam[v] = BSZAM
      print(f"bszam[{v}] = {bszam[v]}")
      if elozo[v] != None:
        v = elozo[v]
        print(f"felfele lépés, aktuális csúcs: {v}")
      else:
        for w in range(kcsucs, n):
          kcsucs = w+1
          if mszam[w] is None:
            MSZAM += 1; mszam[w] = MSZAM; v = w
            print(f"új komponens, aktuális csúcs: {v}")
            print(f"mszam[{v}] = {mszam[v]}")
            break
        else: break
  return elozo, mszam, bszam

n, m = map(int, input().split())
G = [[] for i in range(n)]
for i in range(m):
    v, u = map(int, input().split())
    G[v].append(u)
s = int(input())

elozo, mszam, bszam = dfs(G, s)
