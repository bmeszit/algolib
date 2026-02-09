def linsrc(T, x):
  n = len(T)
  for i in range(n):
    if T[i] == x:
      return i+1
  return -1

T = list(map(int, input().split()))
x = int(input())
print(linsrc(T, x))