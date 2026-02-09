import random
rng = random.Random(42)

def general(n):
  return [rng.randint(1, 10**6) for _ in range(n)]

meretek = [(i+1) * 100 for i in range(9)]
INPUTS = [" ".join(map(str, general(n))) for n in meretek]