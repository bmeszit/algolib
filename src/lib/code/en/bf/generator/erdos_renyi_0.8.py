import random
rng = random.Random(42)

# Erdős-Rényi directed graph generator.
# Uses a random permutation: edges going in the right direction can be negative,
# edges going against it are always positive, so no negative cycles.
def generate_graph(n, p):
  perm = list(range(n))
  rng.shuffle(perm)
  pos = [0] * n
  for i, v in enumerate(perm): pos[v] = i
  edges = []
  for u in range(n):
    for v in range(n):
      if u != v and rng.random() < p:
        if pos[u] < pos[v]:
          weight = rng.randint(-20, 50)
        else:
          weight = rng.randint(1, 50)
        edges.append((u, v, weight))
  return edges

p = 0.8
sizes = [(i+1)*100 for i in range(5)]

for n in sizes:
  edges = generate_graph(n, p)
  m = len(edges)
  lines = [f"{n} {m}"]
  for u, v, weight in edges:
    lines.append(f"{u} {v} {weight}")
  lines.append(f"0")
  INPUT("\n".join(lines))
