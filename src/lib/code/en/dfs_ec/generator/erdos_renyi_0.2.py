import random
rng = random.Random(42)

# Erdős-Rényi generator
def generate_graph(n, p):
  edges = []
  for u in range(n):
    for v in range(n):
      if u==v:
        continue
      if rng.random() < p:
        edges.append((u, v))
  return(edges)

p = 0.2
sizes = [(i+1)*100 for i in range(5)]

for n in sizes:
  edges = generate_graph(n, p)
  m = len(edges)
  lines = [f"{n} {m}"]
  for u, v in edges:
    lines.append(f"{u} {v}")
  lines.append(f"0")
  INPUT("\n".join(lines))
