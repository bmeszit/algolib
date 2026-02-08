def linear_search(arr, low, high, x):
  for i in range(low, high + 1):
    if arr[i] == x:
      return i
  return -1