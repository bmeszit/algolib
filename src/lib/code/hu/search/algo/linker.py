def linker(T, s):
  n = len(T)
  for i in range(n):
    if T[i] == s:
      return i
  return -1

T = list(map(int, input().split()))
s = int(input())
print(linker(T, s))