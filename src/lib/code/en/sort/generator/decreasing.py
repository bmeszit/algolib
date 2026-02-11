# Generate the numbers n..1:
def generate(n):
  return list(range(n, 0, -1))

# Test cases with 100, 200, ..., 900 numbers:
sizes = [(i+1) * 100 for i in range(9)]
INPUTS([" ".join(map(str, generate(n))) for n in sizes])