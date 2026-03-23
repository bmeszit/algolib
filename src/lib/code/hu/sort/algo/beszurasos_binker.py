def binker_hely(T, ertek, eleje, vege):
  while eleje < vege:
    kozepso = (eleje + vege) // 2
    if T[kozepso] < ertek:
      eleje = kozepso+1
    else:
      vege = kozepso
  return eleje

def beszurasos_rendezes_binker(T):
  n = len(T)
  for j in range(1, n):
    hely = binker_hely(T, T[j], 0, j)
    i = j
    while i > hely:
      T[i-1], T[i] = T[i], T[i-1]
      i = i-1
  return T

T = list(map(int, input().split()))
MERES_KEZD()
eredmeny = beszurasos_rendezes_binker(T.copy())
MERES_VEG()
print(eredmeny)
