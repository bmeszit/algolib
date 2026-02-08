def binker(T, eleje, vege, x):
  if eleje <= vege:
    kozepe = (eleje+vege) // 2
    if T[kozepe] == x:
      return kozepe+1
    elif T[kozepe] < x:
      return binker(T, eleje, kozepe-1, x)
    else: # T[kozepe] > x
      return binker(T, kozepe+1, vege, x)
  else:
    return -1

T = list(map(int, input().split()))
x = int(input())
print(binker(T, 0, len(T)-1, x))
