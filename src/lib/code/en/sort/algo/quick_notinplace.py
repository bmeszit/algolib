def partition(A, start, end):
  n = end-start+1
  auxarray = [None]*n
  
  pivot_value = A[start]
  
  left = 0
  right = n-1
  for i in range(start+1, end+1):
    if A[i]<pivot_value:
      auxarray[left] = A[i]
      left += 1
    else:
      auxarray[right] = A[i]
      right -= 1
  auxarray[left] = pivot_value
  
  for i in range(n):
    A[start+i] = auxarray[i]
  pivot_location = start+left
  
  return pivot_location

def quick_sort(A, start, end):
  if not start<end:
    return A
  
  pivot_location = partition(A, start, end)
  quick_sort(A, start, pivot_location-1)
  quick_sort(A, pivot_location+1, end)
  return A

A = list(map(int, input().split()))
n = len(T)
MEASURE_START()
result = quick_sort(A.copy(), 0, n-1)
MEASURE_STOP()
print(result)