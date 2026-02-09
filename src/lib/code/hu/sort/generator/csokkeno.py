def general(n):
  return list(range(n, 0, -1))

meretek = [(i+1) * 100 for i in range(9)]
INPUTS = [" ".join(map(str, general(n))) for n in meretek]