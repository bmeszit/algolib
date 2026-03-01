from copy import deepcopy

def dfs(G, s):
  n = len(G)
  dtime = [None]*n; ftime = [None]*n; prev = [None]*n; nextu = [0]*n
  dtime[s] = 1; DTIME = 1; FTIME = 0; v = s; nextv = 0
  print(f"start vertex: {v}")
  print(f"dtime[{v}] = {dtime[v]}")
  while True:
    for i in range(nextu[v], len(G[v])):
      u = G[v][i]; nextu[v] = i+1
      if dtime[u] is None:
          DTIME += 1; dtime[u] = DTIME
          print(f"tree edge: {v} -> {u}")
          print(f"prev[{u}] = {v}")
          print(f"dtime[{u}] = {dtime[u]}")
          prev[u] = v; v = u
          break
      elif dtime[v] < dtime[u]:
          print(f"forward edge: {v} -> {u}")
      elif dtime[v] > dtime[u] and ftime[u] is None:
          print(f"back edge: {v} -> {u}")
      elif dtime[v] > dtime[u] and ftime[u] is not None:
          print(f"cross edge: {v} -> {u}")
    else:
      FTIME += 1; ftime[v] = FTIME
      print(f"ftime[{v}] = {ftime[v]}")
      if prev[v] != None:
        v = prev[v]
        print(f"stepping up, current vertex: {v}")
      else:
        for w in range(nextv, n):
          nextv = w+1
          if dtime[w] is None:
            DTIME += 1; dtime[w] = DTIME; v = w
            print(f"new component, current vertex: {v}")
            print(f"dtime[{v}] = {dtime[v]}")
            break
        else: break
  return prev, dtime, ftime

n, m = map(int, input().split())
G = [[] for i in range(n)]
for i in range(m):
    v, u = map(int, input().split())
    G[v].append(u)
s = int(input())

prev, dtime, ftime = dfs(G, s)
