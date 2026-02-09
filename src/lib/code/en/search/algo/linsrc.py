def linsrc(T, x):
  n = len(T)
  for i in range(n):
    if T[i] == x:
      return i+1
  return -1

T = list(map(int, input().split()))
n = len(T)
for i in range(n):
  print(linsrc(T, T[i]))