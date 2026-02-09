def general(n):
  return list(range(1, n + 1))

def searched(n):
  return n

sizes = [(i+1) * 10000 for i in range(30)]
INPUTS = [
  " ".join(map(str, general(n))) + "\n" +
  str(searched(n)) + "\n"
  for n in sizes
]
