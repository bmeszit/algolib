import random
rng = random.Random(42)

def general(n):
  return list(range(1, n+1))

meretek = [(i+1) * 100 for i in range(20)]
INPUTS = [" ".join(map(str, general(n))) for n in meretek]
