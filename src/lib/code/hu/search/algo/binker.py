def binker(T, eleje, vege, x):
  if eleje <= vege:
    kozepe = (eleje + vege) // 2
    if T[kozepe] == x:
      return kozepe + 1
    elif x < T[kozepe]:
      return binker(T, eleje, kozepe-1, x)
    else:  # T[kozepe] < x
      return binker(T, kozepe+1, vege, x)
  else:
    return -1

T = list(map(int, input().split()))
x = int(input())
n = len(T)
print(binker(T, 0, n-1, x))