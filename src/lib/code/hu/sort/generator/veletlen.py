import random

def general(n, seed = 42):
  rng = random.Random(seed)
  return [rng.randint(1, 10**6) for _ in range(n)]

meretek = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900]
INPUTS = [" ".join(map(str, general(n, n))) + "\n" for n in meretek]
