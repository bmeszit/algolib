import random
rng = random.Random(42)

def generate(n):
  return list(range(1, n+1))

sizes = [(i+1) * 100 for i in range(20)]
INPUTS = [" ".join(map(str, generate(n))) for n in sizes]