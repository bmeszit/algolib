import random
rng = random.Random(42)

# Test cases with 10000, 20000, ..., 20000 numbers:
sizes = [(i+1) * 10000 for i in range(20)]
for n in sizes:
  # Generate the numbers 1..n:
  numbers = list(range(1, n+1))
  # The number we are searching for is randomized:
  searched = rng.randint(1, n)
  INPUT(" ".join(map(str, numbers)) + "\n" + str(searched))
