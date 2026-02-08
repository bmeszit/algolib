import random

def general(n):
  return list(range(1, n + 1))

def keresett(n, rng):
  return rng.randint(1, n)

sizes = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900]
INPUTS = []
for n in sizes:
  rng = random.Random(n)
  INPUTS.append(
    " ".join(map(str, general(n))) + "\n" +
    str(keresett(n, rng)) + "\n"
  )
