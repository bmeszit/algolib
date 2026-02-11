# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]

for n in sizes:
  # Generate the numbers n to 1:
  numbers = list(range(n, 0, -1))
  INPUT(" ".join(map(str, numbers)))
