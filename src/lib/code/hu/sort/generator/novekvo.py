# Generáljuk az 1..n számokat:
def general(n):
  return list(range(1, n+1))

# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]
BEMENETEK([" ".join(map(str, general(n))) for n in meretek])