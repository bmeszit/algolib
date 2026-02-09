import random
rng = random.Random(42)

# Generálunk n darab véletlen számot 1 és 1000000 között:
def general(n):
  return [rng.randint(1, 10**6) for _ in range(n)]

# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]
INPUTS = [" ".join(map(str, general(n))) for n in meretek]