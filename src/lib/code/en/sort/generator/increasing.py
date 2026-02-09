def generate(n):
  return list(range(1, n+1))

sizes = [(i+1) * 100 for i in range(9)]
INPUTS = [" ".join(map(str, generate(n))) for n in sizes]