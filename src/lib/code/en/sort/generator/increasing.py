def general(n):
  return list(range(1, n + 1))

sizes = [10, 100, 200]
INPUTS = [" ".join(map(str, general(n))) + "\n" for n in sizes]