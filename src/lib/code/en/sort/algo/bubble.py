def sort(A):
  n = len(A)
  for j in range(n-1, 0, -1):
    for i in range(0, j):
      if A[i] > A[i+1]:
        A[i], A[i+1] = A[i+1], A[i]
  return A

A = list(map(int, input().split()))
MEASURE_START()
result = sort(A)
MEASURE_STOP()
print(result)
