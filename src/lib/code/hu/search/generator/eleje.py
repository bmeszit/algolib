def general(n):
  return list(range(1, n + 1))

def keresett(n):
  return 1

meretek = [(i+1) * 10000 for i in range(30)]
INPUTS = [
  " ".join(map(str, general(n))) + "\n" +
  str(keresett(n)) + "\n"
  for n in meretek
]
