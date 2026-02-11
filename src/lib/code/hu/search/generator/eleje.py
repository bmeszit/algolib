import random
rng = random.Random(42)

# 10000, 20000, ..., 20000 számból álló tesztesetek:
meretek = [(i+1) * 10000 for i in range(20)]

for n in meretek:
  # Generáljuk az 1..n számokat:
  szamok = list(range(1, n+1))
  # A keresett szám a legelső:
  keresett = 1
  BEMENET(" ".join(map(str, szamok)) + "\n" + str(keresett))
