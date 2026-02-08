def general(n):
  return list(range(1, n + 1))

sizes = [10, 100, 1000, 10000, 1000000]
INPUTS = ["\n".join(map(str, general(n))) + "\n" for n in sizes]