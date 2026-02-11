# Generate the numbers 1..n:
def generate(n):
  return list(range(1, n+1))

# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]
INPUTS([" ".join(map(str, generate(n))) for n in sizes])