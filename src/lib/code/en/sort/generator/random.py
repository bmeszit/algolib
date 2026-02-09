import random
rng = random.Random(42)

def generate(n):
  return [rng.randint(1, 10**6) for _ in range(n)]

sizes = [(i+1) * 100 for i in range(9)]
INPUTS = [" ".join(map(str, generate(n))) for n in sizes]