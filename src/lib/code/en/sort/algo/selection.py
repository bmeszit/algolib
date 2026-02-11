def selection_sort(A):
  n = len(A)
  for j in range(0, n-1):
    min_value = A[j]
    min_place = j
    for i in range(j+1, n):
      if A[i] < min_value:
        min_value = A[i]
        min_place = i
    A[j], A[min_place] = A[min_place], A[j]
  return A

A = list(map(int, input().split()))
MEASURE_START()
result = selection_sort(A.copy())
MEASURE_STOP()
print(result)