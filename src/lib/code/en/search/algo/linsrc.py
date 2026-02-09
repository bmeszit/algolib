def linsrc(A, s):
  n = len(A)
  for i in range(n):
    if A[i] == s:
      return i
  return -1

A = list(map(int, input().split()))
s = int(input())
print(linsrc(A, s))