def binsrc(A, s):
  n = len(A)
  start = 0
  end = n-1
  
  while start <= end:
    middle = (start + end) // 2
    if A[middle] == s:
      return middle
    elif A[middle] > s:
      end = middle-1
    else:
      start = middle+1
  
  return -1

A = list(map(int, input().split()))
s = int(input())
MEASURE_START()
result = binsrc(A.copy(), s)
MEASURE_STOP()
print(result)