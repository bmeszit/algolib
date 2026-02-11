import random
rng = random.Random(42)

# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]

for n in sizes:
  # Generate n numbers between 1 and 1000000:
  numbers = [rng.randint(1, 10**6) for _ in range(n)]
  INPUT(" ".join(map(str, numbers)))
