def binker(T, s):
  n = len(T)
  eleje = 0
  vege = n-1
  
  while eleje <= vege:
    kozepso = (eleje + vege) // 2
    if T[kozepso] == s:
      return kozepso
    elif T[kozepso] > s:
      vege = kozepso-1
    else:
      eleje = kozepso+1
  
  return -1

T = list(map(int, input().split()))
s = int(input())
MERES_KEZD()
eredmeny = binker(T, s)
MERES_VEG()
print(eredmeny)