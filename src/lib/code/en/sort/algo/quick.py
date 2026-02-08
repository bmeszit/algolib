def partition(A, begin, end):
  pivot_value = A[end]
  pivot_place = end
  i = begin
  for j in range(begin, end):
    if A[j] < pivot_value:
      A[i], A[j] = A[j], A[i]
      i = i+1
  A[i], A[pivot_place] = A[pivot_place], A[i]
  return i

def inplace_sort(A, begin, end):
  if not begin<end:
    return
  
  pivot_place = partition(A, begin, end)
  inplace_sort(A, begin, pivot_place-1)
  inplace_sort(A, pivot_place+1, end)

def sort(A):
  n = len(A)
  inplace_sort(A, 0, n-1)
  return A

A = list(map(int, input().split()))
print(sort(A))
