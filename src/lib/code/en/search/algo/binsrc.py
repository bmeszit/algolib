def binsrc(T, begin, end, x):
  if begin <= end:
    mid = (begin + end) // 2
    if T[mid] == x:
      return mid + 1
    elif x < T[mid]:
      return binsrc(T, begin, mid-1, x)
    else:  # T[mid] < x
      return binsrc(T, mid+1, end, x)
  else:
    return -1

T = list(map(int, input().split()))
n = len(T)
for i in range(n):
  print(binsrc(T, 0, n-1, T[i]))
