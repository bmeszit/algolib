def binsrc_pos(A, value, start, end):
  while start < end:
    middle = (start + end) // 2
    if A[middle] < value:
      start = middle+1
    else:
      end = middle
  return start

def insertion_sort_binsrc(A):
  n = len(A)
  for j in range(1, n):
    pos = binsrc_pos(A, A[j], 0, j)
    i = j
    while i > pos:
      A[i-1], A[i] = A[i], A[i-1]
      i = i-1
  return A

A = list(map(int, input().split()))
MEASURE_START()
result = insertion_sort_binsrc(A.copy())
MEASURE_STOP()
print(result)
