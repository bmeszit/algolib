import random
rng = random.Random(42)

# Generate n numbers between 1 and 1000000:
def generate(n):
  return [rng.randint(1, 10**6) for _ in range(n)]

# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]
INPUTS([" ".join(map(str, generate(n))) for n in sizes])