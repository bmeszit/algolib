import random
rng = random.Random(42)

# Generáljuk az 1..n számokat:
def general(n):
  return list(range(1, n+1))

# A keresett szám véletlen:
def keresett(n):
  return rng.randint(1, n)

# 10000, 20000, ..., 20000 számból álló tesztesetek:
meretek = [(i+1) * 10000 for i in range(20)]
BEMENETEK([" ".join(map(str, general(n))) + "\n" + str(keresett(n)) for n in meretek])