import random
rng = random.Random(42)

# Erdős-Rényi directed graph generator with potential-based weights.
# Each vertex gets a random potential phi(v). Edge weight = phi(u) - phi(v) + extra,
# where extra >= 0. Any cycle's total weight = sum of extras >= 0, so no negative cycles,
# but individual edges can be negative when phi(v) > phi(u) + extra.
def generate_graph(n, p):
  phi = [rng.randint(-20, 20) for _ in range(n)]
  edges = []
  for u in range(n):
    for v in range(n):
      if u != v and rng.random() < p:
        extra = rng.randint(0, 30)
        weight = phi[u] - phi[v] + extra
        edges.append((u, v, weight))
  return edges

p = 0.8
sizes = [(i+1)*50 for i in range(5)]

for n in sizes:
  edges = generate_graph(n, p)
  m = len(edges)
  lines = [f"{n} {m}"]
  for u, v, weight in edges:
    lines.append(f"{u} {v} {weight}")
  lines.append(f"0")
  INPUT("\n".join(lines))
