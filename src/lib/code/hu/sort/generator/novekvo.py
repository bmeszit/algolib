# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]

for n in meretek:
  # Generáljuk az 1..n számokat:
  szamok = list(range(1, n+1))
  BEMENET(" ".join(map(str, szamok)))
