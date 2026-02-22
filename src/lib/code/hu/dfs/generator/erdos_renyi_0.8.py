import random
rng = random.Random(42)

# Erdős-Rényi generátor
def grafot_general(n, p):
  elek = []
  for u in range(n):
    for v in range(n):
      if u==v:
        continue
      if rng.random() < p:
        elek.append((u, v))
  return(elek)

p = 0.8
meretek = [(i+1)*100 for i in range(5)]

for n in meretek:
  elek = grafot_general(n, p)
  m = len(elek)
  sorok = [f"{n} {m}"]
  for u, v in elek:
    sorok.append(f"{u} {v}")
  sorok.append(f"0")
  BEMENET("\n".join(sorok))
