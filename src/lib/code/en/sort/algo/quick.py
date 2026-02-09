def partition(arr, start, end):
  pivot_value = arr[start]
  left = start + 1
  right = end
  
  while left <= right:
    # Search from left for element greater than pivot
    while left <= right and arr[left] < pivot_value:
      left += 1
    
    # Search from right for element smaller than pivot
    while left <= right and arr[right] >= pivot_value:
      right -= 1
    
    # If we found a pair to swap, swap them
    if left < right:
      arr[left], arr[right] = arr[right], arr[left]
  
  # Swap pivot to the right pointer position (its final position)
  arr[start], arr[right] = arr[right], arr[start]
  return right

def sort_inplace(arr, start, end):
  if not start < end:
    return
  
  pivot_position = partition(arr, start, end)
  sort_inplace(arr, start, pivot_position - 1)
  sort_inplace(arr, pivot_position + 1, end)

def sort(arr):
  n = len(arr)
  sort_inplace(arr, 0, n - 1)
  return arr

A = list(map(int, input().split()))
print(sort(A))