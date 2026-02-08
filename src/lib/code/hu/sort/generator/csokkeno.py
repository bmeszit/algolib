def general(n):
  return list(range(n, 0, -1))

sizes = [10, 100, 200, 300, 400, 500, 600, 700, 800, 900]
INPUTS = [" ".join(map(str, general(n))) + "\n" for n in sizes]
