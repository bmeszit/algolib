import random
rng = random.Random(42)

# Erdős-Rényi DAG generátor
def grafot_general(n, p):
  elek = []
  topo_sorrend = list(range(n))
  rng.shuffle(topo_sorrend)
  for i, u in enumerate(topo_sorrend):
    for v in topo_sorrend[i+1:]:
      if rng.random() < p:
        suly = rng.randint(1, 50)
        elek.append((u, v, suly))
  return elek

p = 0.2
meretek = [(i+1)*50 for i in range(5)]

for n in meretek:
  elek = grafot_general(n, p)
  m = len(elek)
  sorok = [f"{n} {m}"]
  for u, v, suly in elek:
    sorok.append(f"{u} {v} {suly}")
  sorok.append(f"0")
  BEMENET("\n".join(sorok))
