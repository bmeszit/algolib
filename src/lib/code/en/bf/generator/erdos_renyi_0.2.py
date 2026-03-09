import random
rng = random.Random(42)

# Erdős-Rényi directed graph generator (positive weights)
def generate_graph(n, p):
  edges = []
  for u in range(n):
    for v in range(n):
      if u != v and rng.random() < p:
        weight = rng.randint(1, 50)
        edges.append((u, v, weight))
  return edges

p = 0.2
sizes = [(i+1)*100 for i in range(5)]

for n in sizes:
  edges = generate_graph(n, p)
  m = len(edges)
  lines = [f"{n} {m}"]
  for u, v, weight in edges:
    lines.append(f"{u} {v} {weight}")
  lines.append(f"0")
  INPUT("\n".join(lines))
