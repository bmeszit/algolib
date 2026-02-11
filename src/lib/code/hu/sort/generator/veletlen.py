import random
rng = random.Random(42)

# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]

for n in meretek:
  # Generálunk n darab véletlen számot 1 és 1000000 között:
  szamok = [rng.randint(1, 10**6) for _ in range(n)]
  BEMENET(" ".join(map(str, szamok)))
