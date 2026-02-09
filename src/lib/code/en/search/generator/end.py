def general(n):
  return list(range(1, n + 1))

def searched(n):
  return n

sizes = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900]
INPUTS = [
  " ".join(map(str, general(n))) + "\n" +
  str(searched(n)) + "\n"
  for n in sizes
]
