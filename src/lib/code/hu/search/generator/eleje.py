def general(n):
  return list(range(1, n + 1))

def keresett(n):
  return 1

sizes = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900]
INPUTS = [
  " ".join(map(str, general(n))) + "\n" +
  str(keresett(n)) + "\n"
  for n in sizes
]
