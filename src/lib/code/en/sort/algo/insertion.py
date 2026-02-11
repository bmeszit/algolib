def sort(A):
  n = len(A)
  for j in range(1, n):
    i = j
    while A[i-1] > A[i] and i > 0:
      A[i-1], A[i] = A[i], A[i-1]
      i = i-1
  return A

A = list(map(int, input().split()))
MEASURE_START()
result = sort(A)
MEASURE_STOP()
print(result)