# Generáljuk az n..1 számokat:
def general(n):
  return list(range(n, 0, -1))

# 100, 200, ..., 900 számból álló tesztesetek:
meretek = [(i+1) * 100 for i in range(9)]
BEMENETEK([" ".join(map(str, general(n))) for n in meretek])