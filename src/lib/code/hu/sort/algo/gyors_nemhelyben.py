def particional(T, eleje, vege):
  n = vege-eleje+1
  segedtomb = [None]*n
  
  pivot_ertek = T[eleje]
  
  bal = 0
  jobb = n-1
  for i in range(eleje+1, vege+1):
    if T[i]<pivot_ertek:
      segedtomb[bal] = T[i]
      bal += 1
    else:
      segedtomb[jobb] = T[i]
      jobb -= 1

  segedtomb[bal] = pivot_ertek
  
  for i in range(n):
    T[eleje+i] = segedtomb[i]
  pivot_hely = eleje+bal
  
  return pivot_hely

def gyors_rendezes(T, eleje, vege):
  if not eleje<vege:
    return T
  
  pivot_hely = particional(T, eleje, vege)
  gyors_rendezes(T, eleje, pivot_hely-1)
  gyors_rendezes(T, pivot_hely+1, vege)
  return T

T = list(map(int, input().split()))
n = len(T)
MERES_KEZD()
eredmeny = gyors_rendezes(T.copy(), 0, n-1)
MERES_VEG()
print(eredmeny)