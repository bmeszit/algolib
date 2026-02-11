def partition(A, start, end):
  pivot_value = A[start]
  left = start + 1
  right = end
  
  while left <= right:
    # Search from left for element greater than pivot
    while left <= right and A[left] < pivot_value:
      left += 1
    
    # Search from right for element smaller than pivot
    while left <= right and A[right] >= pivot_value:
      right -= 1
    
    # If we found a pair to swap, swap them
    if left < right:
      A[left], A[right] = A[right], A[left]
  
  # Swap pivot to the right pointer position (its final position)
  A[start], A[right] = A[right], A[start]
  return right

def quick_sort(A, start, end):
  if not start < end:
    return
  
  pivot_position = partition(A, start, end)
  quick_sort(A, start, pivot_position-1)
  quick_sort(A, pivot_position+1, end)
  return A

A = list(map(int, input().split()))
n = len(A)
MEASURE_START()
result = quick_sort(A.copy(), 0, n-1)
MEASURE_STOP()
print(result)