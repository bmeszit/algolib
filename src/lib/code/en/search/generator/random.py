import random

def general(n):
  return list(range(1, n + 1))

def searched(n, rng):
  return rng.randint(1, n)

sizes = [(i+1) * 10000 for i in range(30)]
INPUTS = []
for n in sizes:
  rng = random.Random(n)
  INPUTS.append(
    " ".join(map(str, general(n))) + "\n" +
    str(searched(n, rng)) + "\n"
  )
