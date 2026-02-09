import random
rng = random.Random(42)

# Generate the numbers 1..n:
def generate(n):
  return list(range(1, n+1))

# The number we are searching for is randomized:
def searched(n):
  return rng.randint(1, n)

# Test cases with 10000, 20000, ..., 20000 numbers:
meretek = [(i+1) * 10000 for i in range(20)]
INPUTS = [" ".join(map(str, generate(n))) + "\n" + str(searched(n)) for n in meretek]