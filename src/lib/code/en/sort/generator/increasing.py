# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]

for n in sizes:
  # Generate the numbers 1 to n:
  numbers = list(range(1, n+1))
  INPUT(" ".join(map(str, numbers)))
