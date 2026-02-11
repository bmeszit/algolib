# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]

for n in meretek:
  # Generáljuk az n..1 számokat:
  szamok = list(range(n, 0, -1))
  BEMENET(" ".join(map(str, szamok)))
